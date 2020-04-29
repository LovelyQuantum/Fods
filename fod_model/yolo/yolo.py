#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File    :   yolo.py
@Time    :   2020/03/14
@Author  :   Yuhao Jin
@Contact :   jin1349595233@gmail.com
"""
import tensorflow as tf
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from multiprocessing import Process
from pymemcache.client.base import Client
from utils.models import Device
from utils.processor import config
from utils.reader import reader
from utils.sender import sender
from time import sleep


# read class number from db?
# get weights(yolov3.tf) from db?
# get camera url from db
engine = create_engine("postgresql://quantum:429526000@postgres/mydb")
session = sessionmaker(bind=engine)
my_session = session()
status_resgiter = Client(("status_resgiter", 12001))


if __name__ == "__main__":
    cameras = [camera.to_json() for camera in my_session.query(Device).all()]
    for camera in cameras:
        camera["id"] = str(camera["id"])
    read_procs = [Process(target=reader, args=(camera,)) for camera in cameras]
    send_procs = [Process(target=sender, args=(camera,)) for camera in cameras]
    procs = [
        Process(target=config["detector"], args=(camera,))
        for camera in cameras
    ]

    for read_proc in read_procs:
        read_proc.start()
        sleep(10)

    for proc in procs:
        proc.start()
        sleep(10)

    for send_proc in send_procs:
        send_proc.start()
        sleep(10)
