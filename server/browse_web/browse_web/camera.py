import cv2
import numpy as np
from time import sleep


class VideoCamera:
    def __init__(self, number):
        self.video = cv2.VideoCapture('../videos/%d.mp4' % number)

    def __del__(self):
        self.video.release()

    def detection(self, flag, mode):
        success, img = self.video.read()
        sleep(0.035)
        # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # img = np.asarray(img, np.float32)
        if flag == True:
            img = cv2.pyrDown(img)
            ret, thresh = cv2.threshold(cv2.cvtColor(img.copy(), cv2.COLOR_BGR2GRAY), 170, 255, cv2.THRESH_BINARY)
            contours, hier = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            for c in contours:
                x, y, w, h = cv2.boundingRect(c)
                if w * h > 5000:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        if mode == 1:
            img = cv2.resize(img, tuple([960, 540]))
        else:
            img = cv2.resize(img, tuple([400, 225]))
        ret, jpeg = cv2.imencode('.jpg', img)
        return jpeg.tobytes()


def gen(camera, flag, mode):
    while True:
        frame = camera.detection(flag, mode)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpg\r\n\r\n' + frame + b'\r\n\r\n')
