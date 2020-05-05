FROM tensorflow/tensorflow:2.1.0-gpu-py3
COPY ./yolo /yolo
COPY ./sources.list /etc/apt/sources.list
WORKDIR /yolo
RUN apt-get update \
    && apt-get install -y python-psycopg2 libpq-dev libsm6 libxext6 libxrender-dev ffmpeg \
    && pip install -U pip -i https://pypi.tuna.tsinghua.edu.cn/simple \
    && pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
