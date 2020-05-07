#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File    :   yolo.py
@Time    :   2020/03/14
@Author  :   Yuhao Jin
@Contact :   jin1349595233@gmail.com
"""
from time import sleep
from utils.reader import reader
from utils.sender import sender
from utils.processor import detector, transfer
from multiprocessing import Process
from sqlalchemy import create_engine
from utils.models import FodCfg, Device, DnnModel, VirtualGpu
from sqlalchemy.orm import sessionmaker
from pymemcache.client.base import Client
from pymemcache import serde


engine = create_engine("postgresql://quantum:429526000@postgres/yqdb")
Session = sessionmaker(bind=engine)
session = Session()
status_register = Client(
    ("status_register", 12001),
    serializer=serde.python_memcache_serializer,
    deserializer=serde.python_memcache_deserializer,
)

devices = []
for index, device in enumerate(session.query(Device).order_by(Device.id)):
    devices.append(
        {
            "id": f"{device.id}",
            "url": f"rtsp://{device.username}:{device.password}"
            f"@{device.ip}:554/Streaming/Channels/1",
        }
    )
    if session.query(FodCfg).filter_by(device_id=device.id).scalar():
        devices[index]["dnn_cfg"] = {
            "weight": session.query(DnnModel).filter_by(id=1).first().weight,
            "classes": session.query(DnnModel).filter_by(id=1).first().classes,
            "gpu_id": session.query(VirtualGpu)
            .filter_by(
                id=session.query(FodCfg)
                .filter_by(device_id=device.id)
                .first()
                .virtual_gpu_id
            )
            .first()
            .gpu_id,
        }

read_procs = [Process(target=reader, args=(device,)) for device in devices]
send_procs = [Process(target=sender, args=(device,)) for device in devices]
procs = {
    device["id"]: Process(
        target=detector if device.get("dnn_cfg") else transfer, args=(device,),
    )
    for device in devices
}

for read_proc in read_procs:
    read_proc.start()
    sleep(15)

for device in devices:
    status_register.set(device["id"], "running")
    procs[device["id"]].start()
    sleep(15)

for send_proc in send_procs:
    send_proc.start()
    sleep(15)

while True:
    sleep(1)
    for device in devices:
        if status_register.get(device["id"]) == "changed":
            procs[device["id"]].terminate()
            status_register.set(device["id"], "running")
            sleep(20)
            if session.query(FodCfg).filter_by(device_id=int(device["id"])).scalar():
                device["dnn_cfg"] = {
                    "weight": session.query(DnnModel).filter_by(id=1).first().weight,
                    "classes": session.query(DnnModel).filter_by(id=1).first().classes,
                    "gpu_id": session.query(VirtualGpu)
                    .filter_by(
                        id=session.query(FodCfg)
                        .filter_by(device_id=int(device["id"]))
                        .first()
                        .virtual_gpu_id
                    )
                    .first()
                    .gpu_id,
                }
            else:
                device.pop("dnn_cfg", None)

            procs[device["id"]] = Process(
                target=detector if device.get("dnn_cfg") else transfer, args=(device,),
            )
            procs[device["id"]].start()
