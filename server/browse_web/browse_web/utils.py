try:
    from urlparse import urlparse, urljoin
except ImportError:
    from urllib.parse import urlparse, urljoin

from flask import request, redirect, url_for, current_app
import cv2
from time import sleep
from pymemcache.client.base import Client
from pymemcache import serde
from PIL import Image, ImageFont, ImageDraw
import os
from time import time
import numpy as np
import pickle

# mc = Client(
#     ("yuhao_memcache", 12002),
#     serializer=serde.python_memcache_serializer,
#     deserializer=serde.python_memcache_deserializer,
# )

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ("http", "https") and ref_url.netloc == test_url.netloc


def redirect_back(default="blog.index", **kwargs):
    for target in request.args.get("next"), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return redirect(target)
    return redirect(url_for(default, **kwargs))


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in current_app.config["BLUELOG_ALLOWED_IMAGE_EXTENSIONS"]
    )


# def gen_frame(raw_group, mode):
#     pre_time = time()
#     if mode == 1:
#         while True:
#             sleep(0.001)
#             if time() - pre_time > 0.04:
#                 pre_time = time()
#                 frame = mc.get("camera%s_ori" % raw_group)
#                 yield (
#                     b"--frame\r\n"
#                     b"Content-Type: image/jpg\r\n\r\n" + frame + b"\r\n\r\n"
#                 )
#     else:
#         while True:
#             sleep(0.001)
#             if time() - pre_time > 0.04:
#                 pre_time = time()
#                 frame = mc.get("row%s" % raw_group)
#                 yield (
#                     b"--frame\r\n"
#                     b"Content-Type: image/jpg\r\n\r\n" + frame + b"\r\n\r\n"
#                 )


def generate_screen_shot(camera_id):
    frame = pickle.loads(mc.get("camera%s" % camera_id))
    frame = cv2.resize(frame, (1280, 720))
    basedir = os.path.abspath(os.path.dirname(__file__))
    cv2.imwrite("%s/static/img/screen_shot/camera%s.jpg" % (basedir, camera_id), frame)


def paint_target(image, class_name, c1, c2, show_path="none", save=True):
    cv2.rectangle(image, c1, c2, (37, 232, 209), 4)
    bbox_mess = "TONS"
    t_size = cv2.getTextSize(bbox_mess, 0, fontScale=1, thickness=30)[0]
    cv2.rectangle(
        image, c1, (c1[0] + t_size[0], c1[1] - t_size[1] - 3), (37, 232, 209), -1
    )  # filled
    pil_img = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    font = ImageFont.truetype("NotoSansCJK-Bold.ttc", 35)
    fill_color = (0, 0, 0)
    draw = ImageDraw.Draw(pil_img)
    # 调整文字输出位置
    c1 = list(c1)
    c1[0] += 15
    c1[1] -= 45
    draw.text(c1, class_name, font=font, fill=fill_color)
    image = cv2.cvtColor(np.asarray(pil_img), cv2.COLOR_RGB2BGR)
    if save:
        cv2.imwrite(show_path, image)
    else:
        return image


def resize_image(image):
    height = image.shape[0]
    width = image.shape[1]
    factor = max(height / 1080, width / 1920)
    print(factor, type(factor))
    image = cv2.resize(
        image, (int(width / (factor * 1.5)), int(height / (factor * 1.5)))
    )
    return image
