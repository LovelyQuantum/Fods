#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File    :   sender.py
@Time    :   2020/03/14
@Author  :   Yuhao Jin
@Contact :   jin1349595233@gmail.com
"""
from pymemcache.client.base import Client
from pymemcache import serde
import subprocess as sp

image_register_B = Client(
    ("image_register_B", 12003),
    serializer=serde.python_memcache_serializer,
    deserializer=serde.python_memcache_deserializer,
)


def sender(device):
    command = [
        "ffmpeg",
        "-re",
        "-r",
        "10",
        "-f",
        "rawvideo",
        "-vcodec",
        "rawvideo",
        "-s",
        "640x360",
        "-pix_fmt",
        "rgb24",
        "-i",
        "-",
        "-an",
        "-vcodec",
        "h264",
        "-f",
        "flv",
        f"rtmp://nginx/show/device{device['id']}",
    ]

    pipe = sp.Popen(command, stdin=sp.PIPE)
    while True:
        img = image_register_B.get(device["id"])
        pipe.stdin.write(img.tostring())
