from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from datetime import datetime


Base = declarative_base()


# init when init system update when submit device settings
class Device(Base):
    __tablename__ = "device"
    id = Column(Integer, primary_key=True)
    name = Column(String, default="摄像头")
    ip = Column(String, default="0.0.0.0")
    type = Column(String, default="camera")
    username = Column(String, default="admin")
    password = Column(String, default="12345")


# Foreign object detection
# filled when submit device settings
class FodCfg(Base):
    __tablename__ = "fodCfg"
    id = Column(Integer, primary_key=True)
    device_id = Column(Integer)
    n_warning_threshold = Column(Integer, default=10000)
    ex_warning_threshold = Column(Integer, default=40000)


class FodRecord(Base):
    __tablename__ = "fodRecord"
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.now, index=True)
    device_id = Column(Integer)
    dnn_model_id = Column(Integer, default=1)
    status = Column(String)
    storage_path = Column(String)
    tags = Column(String, default="")
    areas = Column(String, default="")


# Belt deviation detection
# filled when submit device settings
class BddCfg(Base):
    __tablename__ = "bddCfg"
    id = Column(Integer, primary_key=True)
    device_id = Column(Integer)
    offset_distance = Column(Integer)


# filled when init system
class ModeCategory(Base):
    __tablename__ = "modeCategory"
    id = Column(Integer, primary_key=True)
    name = Column(String)


# filled when submit device settings
# all dnn models include fod, bdd and others
class DnnModel(Base):
    __tablename__ = "dnnModel"
    id = Column(Integer, primary_key=True)
    category = Column(String)
    classes = Column(String)  # use whitespace to split class names
    weight = Column(String)


# filled when init system
class Location(Base):
    __tablename__ = "location"
    id = Column(Integer, primary_key=True)
    location_name = Column(Integer)


# filled when init system
class VirtualGpu(Base):
    __tablename__ = "virtualGpu"
    id = Column(Integer, primary_key=True)
    used = Column(Boolean)


# filled when submit device settings
class DeviceLocation(Base):
    __tablename__ = "deviceLocation"
    id = Column(Integer, primary_key=True)
    device_id = Column(Integer)
    location_id = Column(Integer)


# system status(running training or erroring...)
class SystemStatus(Base):
    __tablename__ = "systemStatus"
    id = Column(Integer, primary_key=True)
    status = Column(String, default="running")
