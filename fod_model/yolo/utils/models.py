from sqlalchemy.ext.declarative import declarative_base
import nvidia_smi
import tensorflow as tf
from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
import cv2


Base = declarative_base()


class Device(Base):
    __tablename__ = "device"
    id = Column(Integer, primary_key=True)
    name = Column(String, default="摄像头")
    ip = Column(String(30), default="0.0.0.0")
    username = Column(String, default="admin")
    password = Column(String, default="12345")
    client = Column(Integer, default=0)
    mode = Column(String, default="none")
    gpu = Column(Integer, default=-1)
    start_point = Column(String, default="432 0")
    nor_lim = Column(Integer, default=10000)
    ext_lim = Column(Integer, default=40000)
    borderline = Column(String, default="None")
    images = relationship("Image", back_populates="device")
    network_id = Column(Integer, ForeignKey("network.id"))
    network = relationship("Network")

    def to_json(self):
        to_dict = self.__dict__
        if "_sa_instance_state" in to_dict:
            del to_dict["_sa_instance_state"]
        return to_dict


class Image(Base):
    __tablename__ = "image"
    id = Column(Integer, primary_key=True)
    level = Column(String)
    storage_path = Column(String)
    timestamp = Column(DateTime, index=True)
    tags = Column(String, default="")
    areas = Column(String, default="")
    device_id = Column(Integer, ForeignKey("device.id"))
    device = relationship("Device", back_populates="images")


class Network(Base):
    __tablename__ = "network"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    usage = Column(String)
    loss = Column(Float)
    timestamp = Column(DateTime, index=True)
    classes = Column(String)
    storage_path = Column(String)


def get_gpu_mem(gpu_num):
    nvidia_smi.nvmlInit()
    handle = nvidia_smi.nvmlDeviceGetHandleByIndex(int(gpu_num))
    info = nvidia_smi.nvmlDeviceGetMemoryInfo(handle)
    nvidia_smi.nvmlShutdown()
    return int(f"{(info.free / 2 ** 30):.2f}")


def transform_image(camera, image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = tf.expand_dims(image, 0)
    image = tf.image.resize_with_pad(image, (416, 416))
    # FIXME don't use numbers
    image = image / 255
    return image
