import tensorflow as tf
from pymemcache.client.base import Client
from pymemcache import serde
from yolov3_tf2.models import YoloV3
from yolov3_tf2.utils import draw_outputs
from time import time, sleep
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from utils.models import FodRecord, DeviceLocation
from pathlib import Path
from datetime import datetime
import cv2


def transform_image(image, size):
    image = tf.expand_dims(image, 0)
    image = tf.image.resize(image, (size, size))
    image = image / 255
    return image


def detector(device):
    engine = create_engine("postgresql://quantum:429526000@postgres/yqdb")
    Session = sessionmaker(bind=engine)
    session = Session()

    status_register = Client(
        ("status_register", 12001),
        serializer=serde.python_memcache_serializer,
        deserializer=serde.python_memcache_deserializer,
    )

    image_register_A = Client(
        ("image_register_A", 12002),
        serializer=serde.python_memcache_serializer,
        deserializer=serde.python_memcache_deserializer,
    )

    image_register_B = Client(
        ("image_register_B", 12003),
        serializer=serde.python_memcache_serializer,
        deserializer=serde.python_memcache_deserializer,
    )
    status_register.set(f"{device['id']}_time", time())
    physical_devices = tf.config.list_physical_devices("GPU")
    tf.config.set_logical_device_configuration(
        physical_devices[device["dnn_cfg"]["gpu_id"]],
        [tf.config.LogicalDeviceConfiguration(memory_limit=2560)],
    )
    logical_devices = tf.config.list_logical_devices("GPU")

    with tf.device(logical_devices[0].name):
        yolo = YoloV3(classes=len(device["dnn_cfg"]["classes"].split()))
        yolo.load_weights(device["dnn_cfg"]["weight"])
        class_names = device["dnn_cfg"]["classes"].split()

        while True:
            img = image_register_A.get(device["id"])
            img_in = transform_image(img, 416)
            boxes, scores, classes, nums = yolo.predict(img_in)
            img, flag = draw_outputs(img, (boxes, scores, classes, nums), class_names)
            if flag:
                # FIXME add center criterion
                if time() - status_register.get(f"{device['id']}_time") > 1:
                    status_register.set(f"{device['id']}_time", time())
                    timestamp = datetime.now()
                    dir_path = Path("/yolo/photos").joinpath(
                        timestamp.strftime("%Y"), timestamp.strftime("%B")
                    )
                    dir_path.mkdir(parents=True, exist_ok=True)
                    file_path = dir_path.joinpath(
                        timestamp.strftime(r"%Y%m%d%H%M%S%f") + ".jpg"
                    )
                    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
                    cv2.imwrite(str(file_path), img)

                    fod_record = FodRecord(
                        device_id=device["id"],
                        status=flag,
                        storage_path=str(file_path),
                        location=session.query(DeviceLocation)
                        .filter_by(device_id=device["id"])
                        .first()
                        .location,
                    )
                    session.add(fod_record)
                    session.commit()
            image_register_B.set(device["id"], img)


def transfer(device):
    image_register_A = Client(
        ("image_register_A", 12002),
        serializer=serde.python_memcache_serializer,
        deserializer=serde.python_memcache_deserializer,
    )

    image_register_B = Client(
        ("image_register_B", 12003),
        serializer=serde.python_memcache_serializer,
        deserializer=serde.python_memcache_deserializer,
    )
    while True:
        start_time = time()
        image_register_B.set(device["id"], image_register_A.get(device["id"]))
        sleep(0.04 - ((time() - start_time) % 0.04))
