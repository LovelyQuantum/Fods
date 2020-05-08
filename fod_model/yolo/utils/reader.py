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
    # FIXME change url
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
    no_signal_img = cv2.imread("no_signal.jpg")
    image_register_A.set(device["id"], no_signal_img)
    while True:
        raw_image = pipe.stdout.read(1280 * 720 * 3)
        image = np.fromstring(raw_image, dtype='uint8')
        try:
            image = image.reshape((720, 1280, 3))
        except ValueError:
            logging.warning(f"live string from {device['url']} broken!")
            image_register_A.set(device["id"], no_signal_img)
            sleep(5)
            pipe = sp.Popen(command, stdout=sp.PIPE)
        pipe.stdout.flush()
        image = cv2.resize(image, (640, 360))
        image_register_A.set(device["id"], image)
