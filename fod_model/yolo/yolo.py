#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File    :   yolo.py
@Time    :   2020/03/14
@Author  :   Yuhao Jin
@Contact :   jin1349595233@gmail.com
"""
from time import sleep
from utils.methods import detector, transfer
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
for index, device_info in enumerate(session.query(Device).order_by(Device.id)):
    devices.append(
        {
            "id": f"{device_info.id}",
            "url": f"rtsp://{device_info.username}:{device_info.password}"
            f"@{device_info.ip}:554/Streaming/Channels/1",
        }
    )
    if session.query(FodCfg).filter_by(device_id=device_info.id).scalar():
        devices[index]["dnn_cfg"] = {
            "weight": session.query(DnnModel).filter_by(id=1).first().weight,
            "classes": session.query(DnnModel).filter_by(id=1).first().classes,
            "gpu_id": session.query(VirtualGpu)
            .filter_by(
                id=session.query(FodCfg)
                .filter_by(device_id=device_info.id)
                .first()
                .virtual_gpu_id
            )
            .first()
            .gpu_id,
        }

procs = {
    device["id"]: Process(
        target=detector if device.get("dnn_cfg") else transfer, args=(device,),
    )
    for device in devices
}

for device in devices:
    while status_register.get(f"{device['id']}_basic") != "running":
        sleep(1)
    procs[device["id"]].start()
    sleep(15)


while True:
    sleep(1)
    for device in devices:
        if status_register.get(f"{device['id']}_fod") == "changed":
            procs[device["id"]].terminate()
            status_register.set(f"{device['id']}_fod", "running")
            sleep(15)

            device_info = session.query(Device).filter_by(int(device["id"]))
            new_url = (
                f"rtsp://{device_info.username}:{device_info.password}"
                f"@{device_info.ip}:554/Streaming/Channels/1"
            )

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
