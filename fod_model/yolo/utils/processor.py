#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File    :   processor.py
@Time    :   2020/03/14
@Author  :   Yuhao Jin
@Contact :   jin1349595233@gmail.com
"""
# add additional function
from pymemcache.client.base import Client
from pymemcache import serde
import tensorflow as tf
from yolov3_tf2.models import YoloV3
from yolov3_tf2.utils import draw_outputs
from utils.models import get_gpu_mem, transform_image
from time import time, sleep

# FIXME limit detector number in flask
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


physical_devices = tf.config.list_physical_devices("GPU")
if len(physical_devices) > 0:
    for i in range(len(physical_devices)):
        # tf.config.experimental.set_memory_growth(physical_devices[i], True)
        tf.config.set_logical_device_configuration(
            physical_devices[i],
            [
                tf.config.LogicalDeviceConfiguration(memory_limit=3072),
                tf.config.LogicalDeviceConfiguration(memory_limit=3072),
                tf.config.LogicalDeviceConfiguration(memory_limit=3072),
            ],
        )


def detector(camera):
    for i in range(len(physical_devices)):
        if get_gpu_mem(i) > 4 or (i == 0 and get_gpu_mem(i) > 6):
            camera["gpu_num"] = i
        else:
            error_info = status_register.get("error_resgiter")
            error_info += "GPU_OUT_OF_USE,"
            status_register.set("error_resgiter", error_info)
            return

    with tf.device(f"/physical_device:GPU:{camera['gpu_num']}"):
        yolo = YoloV3(classes=FLAGS.num_classes)
        yolo.load_weights(FLAGS.weights)
        class_names = [c.strip() for c in open(FLAGS.classes).readlines()]

        while True:
            img_in = image_register_A.get(camera["id"])
            img_in = transform_image(img_in, 416)
            boxes, scores, classes, nums = yolo.predict(img_in)
            img = draw_outputs(img, (boxes, scores, classes, nums), class_names)


def transfer(camera):
    while True:
        start_time = time()
        image_register_B.set(camera["id"], image_register_A.get(camera["id"]))
        sleep(0.04 - ((time() - start_time) % 0.04))


config = {
    "transfer": transfer,
    "detector": transfer,
}
