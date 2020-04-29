import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey, PickleType

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


engine = create_engine("postgresql://quantum:429526000@yuhao_postgresql/mydb")
session = sessionmaker(bind=engine)
my_session = session()
camera = my_session.query(Device).get(1)
