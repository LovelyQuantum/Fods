FROM tensorflow/tensorflow:2.1.0-gpu-py3
RUN mkdir /code
COPY . code/
WORKDIR code/yolo
RUN apt-get update \
    && apt-get install -y python-psycopg2 libpq-dev libsm6 libxext6 libxrender-dev ffmpeg \
    && pip install -U pip -i https://pypi.tuna.tsinghua.edu.cn/simple \
    && pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# FROM registry.cn-hangzhou.aliyuncs.com/hina/yolo:v0.9
# # RUN mkdir /code
# COPY . code/
# WORKDIR code/yolo
# # RUN apt-get update \
# #     && apt-get install -y python-psycopg2 libpq-dev libsm6 libxext6 libxrender-dev ffmpeg \
# #     && pip install -U pip -i https://pypi.tuna.tsinghua.edu.cn/simple \
# #     && pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple