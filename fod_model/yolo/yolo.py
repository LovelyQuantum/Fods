#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File    :   yolo.py
@Time    :   2020/03/14
@Author  :   Yuhao Jin
@Contact :   jin1349595233@gmail.com
"""
import os
from time import sleep
from dotenv import load_dotenv
from utils.reader import reader
from utils.sender import sender
from utils.processor import config
from multiprocessing import Process
from sqlalchemy import create_engine
from utils.models import FodCfg, Device, DnnModel, VirtualGpu
from sqlalchemy.orm import sessionmaker
from pymemcache.client.base import Client
import tensorflow as tf


load_dotenv()
engine = create_engine(os.getenv("DB_URL"))
Session = sessionmaker(bind=engine)
session = Session()
status_resgiter = Client(("status_resgiter", 12001))
virtual_devices = tf.config.list_physical_devices("GPU") * 3
for virtual_device in virtual_devices:
    v_gpu = VirtualGpu(used=False)
    session.add(v_gpu)
session.commit()


if __name__ == "__main__":
    devices = []
    for index, device in enumerate(session.query(Device).order_by(Device.id)):
        devices.append(
            {
                "id": device.id,
                "url": f"rtsp://{device.username}:{device.password}"
                f"@{device.ip}:554/Streaming/Channels/1",
            }
        )
        if session.query(FodCfg).filter_by(device_id=device.id).scalar():
            devices[index]["dnn_cfg"] = {
                "weight": session.query(DnnModel).filter_by(id=1).first().weight,
                "classes": session.query(DnnModel).filter_by(id=1).first().classes,
                "virtual_gpu_id": session.query(DnnModel)
                .filter_by(id=1)
                .first()
                .virtual_gpu_id,
            }

    print(devices)
    read_procs = [Process(target=reader, args=(device,)) for device in devices]
    send_procs = [Process(target=sender, args=(device,)) for device in devices]
    procs = [
        Process(
            target=config["detector"] if device.get("dnn_cfg") else config["transfer"],
            args=(device,),
        )
        for device in devices
    ]

    for read_proc in read_procs:
        read_proc.start()
        sleep(15)

    for proc in procs:
        proc.start()
        sleep(15)

    for send_proc in send_procs:
        send_proc.start()
        sleep(15)

    while True:
        sleep(1)
