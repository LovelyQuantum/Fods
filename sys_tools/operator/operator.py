from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import models
import os


engine = create_engine("postgresql://quantum:429526000@init_postgres/yqdb")
Session = sessionmaker(bind=engine)
session = Session()


def init_db():
    print("Initializing the database...")
    dnn_model = models.DnnModel(
        weight="./checkpoints/yolov3_train_15.tf", category="fod", classes="stone"
    )
    session.add(dnn_model)
    for i in range(10):
        device = models.Device()
        session.add(device)
    for _ in range(2):
        for index in range(3):
            v_gpu = models.VirtualGpu(used=False, gpu_id=index)
            session.add(v_gpu)
    session.commit()


if __name__ == "__main__":
    SYSTEM_CHECK = os.getenv("SYSTEM_CHECK", True)

    DB_DROP_ALL = os.getenv("DB_DROP_ALL", False)
    DB_CREATE_TABLES = os.getenv("DB_CREATE_TABLES", False)
    DB_INIT = os.getenv("DB_INIT", False)
    DB_MIGRATION = os.getenv("DB_MIGRATION", False)

    if SYSTEM_CHECK:
        print("System checking...")
    if DB_DROP_ALL:
        print("Droping tables...")
        session.drop_all()
    if DB_CREATE_TABLES:
        print("Create tables...")
        session.create_all()
    if DB_INIT:
        init_db()
    if DB_MIGRATION:
        pass
