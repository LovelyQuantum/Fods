from flask import Flask, render_template, Response
import cv2
from pymemcache.client.base import Client
from pymemcache import serde


image_register = Client(
    ("yolo_test_use_memcache", 12009),
    serializer=serde.python_memcache_serializer,
    deserializer=serde.python_memcache_deserializer,
)


def get_frame():
    image = image_register.get("image")
    image = cv2.resize(image, (1280, 720))

    _, thresh = cv2.threshold(
        cv2.cvtColor(image.copy(), cv2.COLOR_BGR2GRAY), 170, 255, cv2.THRESH_BINARY
    )
    contours, hier = cv2.findContours(
        thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    for c in contours:
        # find bounding box coordinates
        x, y, w, h = cv2.boundingRect(c)
        if w * h > 2500:
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # 因为opencv读取的图片并非jpeg格式，因此要用motion JPEG模式需要先将图片转码成jpg格式图片
    ret, jpeg = cv2.imencode(".jpg", image)
    return jpeg.tobytes()


# app = Flask(__name__, template_folder="D:/code/newTest/Pycode/异物检测/网页版视频传输")
app = Flask(__name__)

@app.route("/")  # 主页
def index():
    return render_template("index.html")


def gen():
    while True:
        frame = get_frame()
        yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n\r\n")


@app.route("/video_feed")
def video_feed():
    return Response(
        gen(), mimetype="multipart/x-mixed-replace; boundary=frame"
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False)
