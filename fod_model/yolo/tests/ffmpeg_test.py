# import click

# @click.command()
# @click.option('--debug', 'de_bug')
# def output(de_bug):
#     print(de_bug)


# if __name__ == '__main__':
#     output()

import cv2
import sys
import logging
from time import time, sleep
import click
import subprocess as sp
import logging


@click.command()
@click.argument('input_url')
def img_read(input_url):
    # command = [ 'ffmpeg',
    #     '-re',
    #     '-f', 'rawvideo',
    #     '-vcodec','rawvideo',
    #     '-s', '1280x720', # size of one frame
    #     '-pix_fmt', 'rgb24',
    #     # '-r', '10',
    #     '-i', '-', # The imput comes from a pipe
    #     '-an', # Tells FFMPEG not to expect any audio
    #     '-rtsp_transport', 'tcp',
    #     '-vcodec', 'h264',
    #     '-f', 'rtsp', 'rtsp://localhost:45812/test']
    command = [ 'ffmpeg',
        '-re',
        '-r', '15',
        '-f', 'rawvideo',
        '-vcodec','rawvideo',
        '-s', '1280x720', # size of one frame
        '-pix_fmt', 'rgb24',
        '-i', '-', # The imput comes from a pipe
        # '-vstats_file', '/home/hina/output.txt',
        '-an', # Tells FFMPEG not to expect any audio
        '-vcodec', 'h264',
        '-f', 'flv',
        'rtmp://yuhao_nginx/stream/livestream']
    # command = ['ffmpge -re -f rawvideo -vcodec rawvideo -s 1280x720 -pix_fmt rgb24 -i - -an -vcodec libx264 -f flv rtmp://localhost/show/livestream']
    # pipe = sp.Popen(command, stdin=sp.PIPE, stderr=sp.PIPE)
    pipe = sp.Popen(command, stdin=sp.PIPE)
    cap = cv2.VideoCapture(input_url)
    # logging.info(pipe.stdout.read())
    while True:
        # logging.warning(pipe.stdout.read())
        start_time = time()
        _, img = cap.read()
        if img is None:
            logging.warning("Empty Frame")
            break
        img_in = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        pipe.stdin.write(img.tostring())
        end_time = time()
        sleep(0.1)
        # print(end_time - start_time)


if __name__ == '__main__':
    img_read()

# ffmpeg -re -i C:\Users\Administrator\Videos\test.mkv -rtsp_transport tcp -vcodec h264 -f rtsp rtsp://localhost/test
