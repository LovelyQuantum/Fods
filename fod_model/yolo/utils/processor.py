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
from utils.methods import transform_image
from time import time, sleep


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
        tf.config.set_logical_device_configuration(
            physical_devices[i],
            [
                tf.config.LogicalDeviceConfiguration(memory_limit=3072),
                tf.config.LogicalDeviceConfiguration(memory_limit=3072),
                tf.config.LogicalDeviceConfiguration(memory_limit=3072),
            ],
        )
logical_devices = tf.config.list_logical_devices("GPU")


def detector(camera):
    with tf.device(logical_devices[camera["dnn_cfg"]["virtual_gpu_id"]].name):
        yolo = YoloV3(classes=len(camera["dnn_cfg"]["classes"].split()))
        yolo.load_weights(camera["dnn_cfg"]["weight"])
        class_names = camera["dnn_cfg"]["classes"].split()

        while True:
            img = image_register_A.get(camera["id"])
            img_in = transform_image(img, 416)
            boxes, scores, classes, nums = yolo.predict(img_in)
            img = draw_outputs(img, (boxes, scores, classes, nums), class_names)


def transfer(camera):
    while True:
        start_time = time()
        image_register_B.set(camera["id"], image_register_A.get(camera["id"]))
        sleep(0.04 - ((time() - start_time) % 0.04))


config = {
    "transfer": transfer,
    "detector": detector,
}
