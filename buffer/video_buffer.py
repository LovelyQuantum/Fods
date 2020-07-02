from utils.reader import reader
from utils.sender import sender
from utils.models import Device, FodCfg, DnnModel
from utils.transfer import transfer, fod_transfer
from time import sleep
from multiprocessing import Process
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from pymemcache.client.base import Client
from pymemcache import serde
import cv2


engine = create_engine("postgresql://quantum:429526000@postgres/yqdb")
Session = sessionmaker(bind=engine)
session = Session()

status_register = Client(
    ("status_register", 12001),
    serializer=serde.python_memcache_serializer,
    deserializer=serde.python_memcache_deserializer,
)

# image_register_A = Client(
#     ("image_register_A", 12002),
#     serializer=serde.python_memcache_serializer,
#     deserializer=serde.python_memcache_deserializer,
# )

image_register_B = Client(
    ("image_register_B", 12003),
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
            "virtual_gpu_id": session.query(FodCfg)
            .filter_by(device_id=device_info.id)
            .first()
            .virtual_gpu_id,
        }

loading_img = cv2.imread("img/loading.jpg")
loading_img = cv2.resize(loading_img, (640, 360))
for device in devices:
    image_register_B.set(device["id"], loading_img)


read_procs = {
    device["id"]: Process(target=reader, args=(device,),) for device in devices
}

transfer_procs = {
    device["id"]: Process(
        target=fod_transfer if device.get("dnn_cfg") else transfer, args=(device,),
    )
    for device in devices
}

send_procs = {
    device["id"]: Process(target=sender, args=(device,),) for device in devices
}

for device in devices:
    status_register.set(f"{device['id']}_basic", "running")
    read_procs[device["id"]].start()
    sleep(5)
    send_procs[device["id"]].start()
    sleep(5)

while True:
    sleep(1)
    for device in devices:
        if status_register.get(f"{device['id']}_basic") == "changed":
            device_info = session.query(Device).filter_by(int(device["id"]))
            if (
                device["url"] != f"rtsp://{device_info.username}:{device_info.password}"
                f"@{device_info.ip}:554/Streaming/Channels/1"
            ):
                status_register.set(f"{device['id']}_basic", "restarting")
                read_procs[device["id"]].terminate()
                device["url"] = (
                    f"rtsp://{device_info.username}:{device_info.password}"
                    f"@{device_info.ip}:554/Streaming/Channels/1"
                )
                read_procs[device["id"]] = Process(target=reader, args=(device,),)
                read_procs[device["id"]].start()
                status_register.set(f"{device['id']}_basic", "running")

        if status_register.get(f"{device['id']}_fod") == "changed":
            transfer_procs[device["id"]].terminate()
            device_info = session.query(Device).filter_by(id=int(device["id"])).first()
            device["url"] = (
                f"rtsp://{device_info.username}:{device_info.password}"
                f"@{device_info.ip}:554/Streaming/Channels/1"
            )

            if session.query(FodCfg).filter_by(device_id=int(device["id"])).scalar():
                device["dnn_cfg"] = {
                    "weight": session.query(DnnModel).filter_by(id=1).first().weight,
                    "classes": session.query(DnnModel).filter_by(id=1).first().classes,
                    "virtual_gpu_id": session.query(FodCfg)
                    .filter_by(device_id=device_info.id)
                    .first()
                    .virtual_gpu_id,
                }
            else:
                device.pop("dnn_cfg", None)
            transfer_procs[device["id"]] = Process(
                target=fod_transfer if device.get("dnn_cfg") else transfer,
                args=(device,),
            )
            transfer_procs[device["id"]].start()
            status_register.set(f"{device['id']}_fod", "running")
