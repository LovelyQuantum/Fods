#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File    :   reader.py
@Time    :   2020/03/14
@Author  :   Yuhao Jin
@Contact :   jin1349595233@gmail.com
"""
from pymemcache.client.base import Client
import subprocess as sp
from pymemcache import serde
from time import sleep
import logging
import cv2
import numpy as np

image_register_A = Client(
    ("image_register_A", 12002),
    serializer=serde.python_memcache_serializer,
    deserializer=serde.python_memcache_deserializer,
)


def reader(device):
    # FIXME password are not safe now
    device["url"] = ["rtsp://ws_rtsp_server/test"]
    command = [
        "ffmpeg",
        "-i",
        device["url"],
        "-f",
        "image2pipe",
        "-pix_fmt",
        "rgb24",
        "-vcodec",
        "rawvideo",
        "-",
    ]
    pipe = sp.Popen(command, stdout=sp.PIPE)
    while True:
        raw_image = pipe.stdout.read(1280 * 720 * 3)
        image = np.fromstring(raw_image, dtype="uint8")
        try:
            image = image.reshape((1280, 720, 3))
        except ValueError:
            logging.warning(f"live string from {device['url']} broken!")
            sleep(5)
            pipe = sp.Popen(command, stdout=sp.PIPE)
        pipe.stdout.flush()
        image = cv2.resize(image, (640, 360))
        image_register_A.set(device["id"], image)
