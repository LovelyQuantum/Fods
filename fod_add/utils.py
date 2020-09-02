import torch
import torch.nn as nn
from torchvision import models, transforms
import cv2
from time import sleep
from datetime import datetime, timezone, timedelta
import logging
import json
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import FodCfg, Device
from pymemcache.client.base import Client
from pymemcache import serde
from pathlib import Path
import numpy as np


engine = create_engine("postgresql://quantum:429526000@postgres/yqdb")
Session = sessionmaker(bind=engine)
session = Session()

transform = transforms.Compose(
    [
        transforms.ToPILImage(),
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
    ]
)


status_register = Client(
    ("status_register", 12001),
    serializer=serde.python_memcache_serializer,
    deserializer=serde.python_memcache_deserializer,
)


fod_image_register_A = Client(
    ("fod_image_register_A", 12004),
    serializer=serde.python_memcache_serializer,
    deserializer=serde.python_memcache_deserializer,
)


if not torch.cuda.is_available():
    raise RuntimeError("It seems like cuda:0 is not available, please check (o´ω`o)")

device = torch.device("cuda:0")
model_ft = models.wide_resnet50_2()
num_ftrs = model_ft.fc.in_features
model_ft.fc = nn.Linear(num_ftrs, 4)
# model_ft.load_state_dict(torch.load("./best.pt"))
model_ft.load_state_dict(torch.load("./wise_res_best.pt"))
model_ft.eval()
model_ft = model_ft.to(device)


def load_mask_points(pipeline, width, height):
    with open("source_points.json", mode="rb") as file:
        json_points = json.loads(file.read().decode("utf-8"))
    source_points = []
    if not session.query(FodCfg).filter_by(virtual_gpu_id=pipeline).scalar():
        for point in json_points[0]["points"]:
            source_points.append(
                [int(float(point["x"]) * width), int(float(point["y"]) * height)]
            )
        logging.warning(
            f"(*・ω・)ﾉ Device record of pipeline {pipeline} not found, load default"
        )
        return source_points
    device_id = (
        session.query(FodCfg).filter_by(virtual_gpu_id=pipeline).first().device_id
    )
    device_name = session.query(Device).filter_by(id=device_id).first().name
    for i in json_points:
        if i["cameraName"] == device_name:
            for point in i["points"]:
                source_points.append(
                    [int(float(point["x"]) * width), int(float(point["y"]) * height)]
                )
            return source_points
    raise FileNotFoundError(
        f"Mask points of {device_name} not found( ; ω ; ), please check"
    )


class LoadImages:  # for inference
    def __init__(self):
        temp_img = cv2.imread("background.png")
        for i in range(1, 5):
            fod_image_register_A.set(f"fod_pipeline_{i}", temp_img)

    def __iter__(self):
        self.pipeline = 0
        return self

    def __next__(self):
        self.pipeline = self.pipeline + 1 if self.pipeline < 4 else 1
        while True:
            img = fod_image_register_A.get(f"fod_pipeline_{self.pipeline}")
            if img is not None:
                break
            logging.error(
                f"Σ(O_O) get frame from pipeline {self.pipeline} fall, retry in 1s..."
            )
            sleep(1)
        return self.pipeline, img

    def get_size(self, pipeline=1):
        while True:
            img = fod_image_register_A.get(f"fod_pipeline_{pipeline}")
            if img is not None:
                break
            logging.error(
                f"Σ(O_O) get frame from pipeline {pipeline} fall, retry in 1s..."
            )
            sleep(1)
        iamge_size = img.shape
        return iamge_size

    def get_frame(self, pipeline):
        while True:
            img = fod_image_register_A.get(f"fod_pipeline_{pipeline}")
            if img is not None:
                break
            logging.error(
                f"Σ(O_O) get frame from pipeline {pipeline} fall, retry in 1s..."
            )
            sleep(1)
        return img

    def skip_frames(self, num):
        current_frame = self.cap.get(cv2.CAP_PROP_POS_FRAMES)
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, current_frame + num)

    def get_frame_num(self):
        return self.cap.get(cv2.CAP_PROP_POS_FRAMES)


def predictor(img):
    with torch.no_grad():
        img = transform(img)
        img = img.unsqueeze(0)
        img = img.to(device)
        output = model_ft(img)
        other_score = output[0][2].item()
        stone_score = output[0][3].item()
        return other_score, stone_score


def save_img(pipeline, img):
    timestamp = datetime.utcnow().astimezone(timezone(timedelta(hours=8)))
    dir_path = Path("/yolov5/others_photos").joinpath(
        timestamp.strftime("%Y"), timestamp.strftime("%B"), timestamp.strftime("%d"),
    )
    dir_path.mkdir(parents=True, exist_ok=True)
    file_path = dir_path.joinpath(timestamp.strftime(r"%Y%m%d%H%M%S%f") + ".jpg")
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    cv2.imwrite(str(file_path), img)

    # if not session.query(FodCfg).filter_by(virtual_gpu_id=pipeline).scalar():
    #     return
    # device_id = (
    #     session.query(FodCfg).filter_by(virtual_gpu_id=pipeline).first().device_id
    # )
    # fod_record = FodRecord(
    #     device_id=device_id,
    #     status="预警",
    #     tags="others",
    #     timestamp=timestamp,
    #     storage_path=str(file_path),
    #     location=session.query(DeviceLocation)
    #     .filter_by(device_id=device_id)
    #     .first()
    #     .location,
    # )
    # session.add(fod_record)
    # session.commit()
    sleep(1)


def circle_fusion(points, mids, areas, max_distance=50000, max_area=50000):
    while True:
        change = 0
        if len(points) == 1:
            x, y, w, h = cv2.boundingRect(points[0])
            break
        # 循环依次根据阈值判断是否融合
        for i, mid in enumerate(mids):
            one = i
            two = (one + 1) % len(mids)
            distance = (mids[one][0] - mids[two][0]) ** 2 + (
                mids[one][1] - mids[two][1]
            ) ** 2
            if (
                distance < max_distance
                and (areas[one] < max_area and areas[two] < max_area)
                and (areas[one] + areas[two]) < max_area
            ):
                # 融合后信息写入one处并删除two处信息
                points[one] = np.array(points[one].tolist() + points[two].tolist())
                x, y, w, h = cv2.boundingRect(points[one])
                areas[one] = w * h
                mids[one] = np.sum([mids[one], mids[two]], axis=0) / 2
                points.pop(two)
                mids.pop(two)
                areas.pop(two)
                change = 1
        if change == 0:
            break


def save_demo(img, score):
    timestamp = datetime.utcnow().astimezone(timezone(timedelta(hours=8)))
    dir_path = Path("/yolov5/demo_photos").joinpath(
        timestamp.strftime("%Y"), timestamp.strftime("%B"), timestamp.strftime("%d"),
    )
    dir_path.mkdir(parents=True, exist_ok=True)
    file_path = dir_path.joinpath(
        f"{timestamp.strftime(r'%H%M%S%f')}_other_score:{score:.3f}.jpg"
    )
    cv2.imwrite(str(file_path), img)
