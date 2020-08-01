"""
@Author: Yuhao Jin
@Date: 2020-07-20 20:03:18
@LastEditTime: 2020-07-20 22:28:31
@Description: 
"""
import argparse
import torch.backends.cudnn as cudnn
from utils import google_utils
from utils.datasets import *
from utils.utils import *
from pymemcache.client.base import Client
from pymemcache import serde
import os
import logging
from datetime import datetime

status_register = Client(
    ("status_register", 12001),
    serializer=serde.python_memcache_serializer,
    deserializer=serde.python_memcache_deserializer,
)


def detect():
    init_cache()
    weights = "weights/yolov5l.pt"
    imgsz = 640
    conf_thres = 0.4
    iou_thres = 0.5

    # Initialize
    device = torch_utils.select_device("")
    half = device.type != "cpu"  # half precision only supported on CUDA

    # Load model
    google_utils.attempt_download(weights)
    model = torch.load(weights, map_location=device)["model"].float()  # load to FP32
    model.to(device).eval()
    if half:
        model.half()  # to FP16

    # Get names and colors
    names = model.module.names if hasattr(model, "module") else model.names
    colors = [[random.randint(0, 255) for _ in range(3)] for _ in range(len(names))]

    # Run inference
    t0 = time.time()
    img = torch.zeros((1, 3, imgsz, imgsz), device=device)  # init img
    _ = model(img.half() if half else img) if device.type != "cpu" else None  # run once

    dataset = LoadImages()
    counter = 0
    old_area, old_core_y = 1, 1
    nThresholds = [
        status_register.get(f"fod_pipeline_{i}_nThreshold") for i in range(1, 5)
    ]
    exThresholds = [
        status_register.get(f"fod_pipeline_{i}_exThreshold") for i in range(1, 5)
    ]
    for pipeline, img, im0 in dataset:
        ori_img = im0.copy()
        counter += 1
        if counter > 40:
            counter = 0
            nThresholds[pipeline - 1] = status_register.get(f"fod_pipeline_{pipeline}_nThreshold")
            exThresholds[pipeline - 1] = status_register.get(f"fod_pipeline_{pipeline}_exThreshold")
        img = torch.from_numpy(img).to(device)
        img = img.half() if half else img.float()  # uint8 to fp16/32
        img /= 255.0  # 0 - 255 to 0.0 - 1.0
        if img.ndimension() == 3:
            img = img.unsqueeze(0)

        # Inference
        t1 = torch_utils.time_synchronized()
        pred = model(img)[0]

        # Apply NMS
        pred = non_max_suppression(pred, conf_thres, iou_thres,)
        t2 = torch_utils.time_synchronized()

        # Process detections
        for i, det in enumerate(pred):  # detections per image
            s = ""
            s += "%gx%g " % img.shape[2:]  # print string
            gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]  #  normalization gain whwh
            if det is not None and len(det):
                # Rescale boxes from img_size to im0 size
                det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0.shape).round()

                # Print results
                for c in det[:, -1].unique():
                    n = (det[:, -1] == c).sum()  # detections per class
                    s += "%g %ss, " % (n, names[int(c)])  # add to string

                # Write results
                max_area = 0
                core_y = 0
                for *xyxy, conf, cls in det:
                    # Add bbox to image
                    label = "%s" % (names[int(cls)])
                    x1, y1, x2, y2 = (
                        int(xyxy[0]),
                        int(xyxy[1]),
                        int(xyxy[2]),
                        int(xyxy[3]),
                    )
                    if abs((y2 - y1) * (x2 - x1)) > max_area:
                        core_y = (y1 + y2) / 2
                        max_area = abs((y2 - y1) * (x2 - x1))
                    im0 = plot_one_box(
                        xyxy,
                        im0,
                        label=label,
                        line_thickness=3,
                    )
                if 0.9 < old_area / max_area < 1.1 or 0.9 < old_core_y / core_y < 1.1:
                    pass
                elif max_area > nThresholds[pipeline - 1]:
                    save_img(pipeline, im0, status="严重预警")
                    trigger_alarm(pipeline)
                    ori_img = im0
                elif nThresholds[pipeline - 1] < max_area < exThresholds[pipeline - 1]:
                    save_img(pipeline, im0, status="预警")
                    ori_img = im0
                old_area = max_area
                old_core_y = core_y
        send_img(pipeline, ori_img)


if __name__ == "__main__":
    with torch.no_grad():
        detect()
        # Update all models
        # for opt.weights in ['yolov5s.pt', 'yolov5m.pt', 'yolov5l.pt', 'yolov5x.pt', 'yolov3-spp.pt']:
        #    detect()
        #    create_pretrained(opt.weights, opt.weights)
