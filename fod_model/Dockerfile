FROM tensorflow/tensorflow:2.1.0-gpu-py3
COPY ./yolo /yolo
COPY ./sources.list /etc/apt/sources.list
WORKDIR /yolo
RUN apt-get update \
    && pip config set global.index-url http://mirrors.aliyun.com/pypi/simple \
    && pip config set install.trusted-host mirrors.aliyun.com \
    && apt-get install -y python-psycopg2 libpq-dev libsm6 libxext6 libxrender-dev \
    && pip install -U pip \
    && pip install -r requirements.txt \
