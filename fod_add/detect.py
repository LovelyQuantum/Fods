import numpy as np
import cv2
from utils import (
    predictor,
    save_img,
    LoadImages,
    load_mask_points,
    circle_fusion,
    save_demo,
)

# 参数设置
erodeIterations = 1
dilateIterations = 1
AreaRange = [2000, 30000]  # acceptable area intervals
PIPELINE_NUM = 4
THRESHOLD = 5

# 候选框融合后在周围加大的像素数目
add_pixel = 50


def GMM_FrameDifferencing():
    image_loader = LoadImages()
    height, width, channel = image_loader.get_size()
    source_points = [load_mask_points(i, width, height) for i in range(PIPELINE_NUM)]
    e_element = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (4, 4))
    d_element = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (4, 5))
    fgbg = [
        cv2.createBackgroundSubtractorMOG2(varThreshold=10) for i in range(PIPELINE_NUM)
    ]
    hull = [cv2.convexHull(np.array(source_points[i])) for i in range(PIPELINE_NUM)]
    source_mask = [
        np.zeros((height, width, channel), dtype=np.uint8) for i in range(PIPELINE_NUM)
    ]
    source_mask = [
        cv2.fillConvexPoly(source_mask[i], hull[i], (255, 255, 255))
        for i in range(PIPELINE_NUM)
    ]
    source_mask = [
        cv2.threshold(source_mask[i], 0, 255, cv2.THRESH_BINARY)[1]
        for i in range(PIPELINE_NUM)
    ]
    frame = image_loader.get_frame(1)
    source_frame = [
        cv2.bitwise_and(source_mask[i], frame.copy()) for i in range(PIPELINE_NUM)
    ]
    old_fgmask = [fgbg[i].apply(source_frame[i]) for i in range(PIPELINE_NUM)]
    for pipeline, source_frame in image_loader:
        pipeline -= 1
        frame = cv2.bitwise_and(source_mask[pipeline], source_frame.copy())
        fgmask = fgbg[pipeline].apply(frame)  # 模型输出二值化mask
        mask = cv2.absdiff(fgmask, old_fgmask[pipeline])
        old_fgmask[pipeline] = fgmask
        mask = cv2.erode(mask, e_element, iterations=erodeIterations)  # 腐蚀
        mask = cv2.dilate(mask, d_element, iterations=dilateIterations)  # 膨胀
        contours, hierarchy = cv2.findContours(
            mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        points = []
        mids = []
        areas = []
        for cnt in contours:
            Area = cv2.contourArea(cnt)  # 计算轮廓面积
            if AreaRange[0] < Area < AreaRange[1]:
                # 将原始框信息放入列表
                points.append(cnt)
                x, y, w, h = cv2.boundingRect(cnt)
                mids.append([x + w / 2, y + h / 2])
                areas.append(w * h)
        # 循环融合，不再有合并动作即退出
        circle_fusion(points, mids, areas)
        # 画出融合后矩形框
        candidate_box = []
        base_frame = source_frame.copy()
        for i, cnt in enumerate(points):
            x, y, w, h = cv2.boundingRect(cnt)
            if x + w + add_pixel < width and y + h + add_pixel < height:
                x -= add_pixel
                y -= add_pixel
                w += add_pixel * 2
                h += add_pixel * 2
            stone = base_frame[y:y + h, x:x + w]
            candidate_box.append([x, y, w, h])
            stone_rgb = cv2.cvtColor(stone, cv2.COLOR_BGR2RGB)
            other_score, stone_score = predictor(stone_rgb)
            save_demo(stone, other_score)
            if other_score > THRESHOLD:
                cv2.rectangle(source_frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                save_img(pipeline, source_frame)


if __name__ == "__main__":
    GMM_FrameDifferencing()
