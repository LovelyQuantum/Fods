import cv2
from time import time, sleep
from datetime import datetime, timezone, timedelta
from pymemcache.client.base import Client
from pymemcache import serde
from pathlib import Path


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

fod_image_register_B = Client(
    ("fod_image_register_B", 12005),
    serializer=serde.python_memcache_serializer,
    deserializer=serde.python_memcache_deserializer,
)


# 参数设置

erodeIterations = 1
dilateIterations = 1
AreaRange = [2000, 30000]  # acceptable area intervals
xyRatio = 5


def send_img(pipeline, img):
    fod_image_register_B.set(f"fod_pipeline_{pipeline}", img)


def save_img(pipeline, img, status):
    if time() - status_register.get(f"fod_pipeline_{pipeline}_time") > 1:
        status_register.set(f"fod_pipeline_{pipeline}_time", time())
        timestamp = datetime.utcnow().astimezone(timezone(timedelta(hours=8)))
        dir_path = Path("/yolov5/photos").joinpath(
            timestamp.strftime("%Y"), timestamp.strftime("%B")
        )
        dir_path.mkdir(parents=True, exist_ok=True)
        file_path = dir_path.joinpath(timestamp.strftime(r"%Y%m%d%H%M%S%f") + ".jpg")
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        cv2.imwrite(str(file_path), img)


class LoadImages:  # for inference
    def __init__(self, img_size=640):
        self.img_size = img_size
        temp_img = cv2.imread("demo/loading.png")
        for i in range(1, 5):
            status_register.set(f"fod_pipeline_{i}_time", time())
            fod_image_register_A.set(f"fod_pipeline_{i}", temp_img)

    def __iter__(self):
        self.pipeline = 1
        return self

    def __next__(self):
        img0 = fod_image_register_A.get(f"fod_pipeline_{self.pipeline}")
        return self.pipeline, img0


def judgeType(cnt, area):
    xMin = 999999
    xMax = 0
    yMin = 999999
    yMax = 0
    for c in cnt:
        if xMin > c[0][0]:
            xMin = c[0][0]
        if xMax < c[0][0]:
            xMax = c[0][0]
        if yMin > c[0][1]:
            yMin = c[0][1]
        if yMax < c[0][1]:
            yMax = c[0][1]
    xx = xMax - xMin
    yy = yMax - yMin
    if area < 0.1 * xx * yy:
        return "wood"
    else:
        if xx > xyRatio * yy or yy > xyRatio * xx:
            return "wood"
        else:
            return "stone"


def GMM_FrameDifferencing():
    sleep(5)
    dataset = LoadImages()
    fgbg = cv2.createBackgroundSubtractorMOG2(varThreshold=10)  # 混合高斯背景建模算法
    flag = 1
    for pipeline, frame in dataset:
        sleep(0.05)

        fgmask = fgbg.apply(frame)  # 模型输出二值化mask
        # 初始化前2帧
        if flag == 1:
            two_frame = frame
            two_fgmask = fgmask
            flag -= 1
            continue

        two_frame = frame
        one_fgmask, two_fgmask = two_fgmask, fgmask

        mask = cv2.absdiff(one_fgmask, two_fgmask)
        # mask = cv2.bitwise_and(mask,two_fgmask)

        # element = cv2.getStructuringElement(cv2.MORPH_CROSS, (5, 10))  # 形态学去噪
        e_element = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (4, 4))
        d_element = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (4, 5))
        # mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, element)  # 开运算去噪
        mask = cv2.erode(mask, e_element, iterations=erodeIterations)  # 腐蚀
        mask = cv2.dilate(mask, d_element, iterations=dilateIterations)  # 膨胀

        contours, hierarchy = cv2.findContours(
            mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )  # 寻找前景

        show_frame = two_frame.copy()
        show_fgmask = fgmask.copy()

        status = ""
        for cnt in contours:
            Area = cv2.contourArea(cnt)  # 计算轮廓面积
            if Area < AreaRange[0] or Area > AreaRange[1]:  # 过滤面积小于 or 大于的形状
                continue
            status = "预警"

            thisType = judgeType(cnt, Area)
            hull = cv2.convexHull(cnt)
            show_frame = cv2.polylines(show_frame, [hull], True, (255, 0, 255), 4)
            show_fgmask = cv2.polylines(show_fgmask, [hull], True, (255, 0, 255), 4)

            show_tag = thisType

            cv2.putText(
                show_frame,
                show_tag,
                (cnt[0][0][0], cnt[0][0][1]),
                cv2.FONT_HERSHEY_COMPLEX,
                2,
                (255, 0, 255),
                2,
            )
        if status == "预警":
            save_img(pipeline, show_frame, status)
        send_img(pipeline, show_frame)


if __name__ == "__main__":
    GMM_FrameDifferencing()
