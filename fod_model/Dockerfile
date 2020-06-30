FROM pytorch/pytorch
COPY ./yolov5 /yolov5
COPY ./sources.list /etc/apt/sources.list
RUN mv /home/files/source/aliyun.list /etc/apt/sources.list \
    && apt-get update \
    && apt-get install -y libsm6 libxext6 libxrender-dev gcc
WORKDIR /yolov5
RUN pip config set global.index-url http://mirrors.aliyun.com/pypi/simple/ \
    && pip config set install.trusted-host mirrors.aliyun.com \
    && pip install -U pip \
    && pip install -U -r requirements.txt
