FROM pytorch/pytorch
COPY . /yolov5
COPY ./sources.list /etc/apt/sources.list
RUN apt-get update \
    && apt-get install -y python-psycopg2 libpq-dev libsm6 libxext6 libxrender-dev gcc libglib2.0-0 \
    && pip config set global.index-url http://mirrors.aliyun.com/pypi/simple/ \
    && pip config set install.trusted-host mirrors.aliyun.com \
    && pip install -U pip \
    && pip install -U -r /yolov5/requirements.txt
WORKDIR /yolov5
