FROM registry.cn-hangzhou.aliyuncs.com/hina/python:3.7
COPY . /server
WORKDIR /server
RUN apt-get update \
    && apt-get install -y python-psycopg2 libpq-dev \
    && pip config set global.index-url http://mirrors.aliyun.com/pypi/simple \
    && pip config set install.trusted-host mirrors.aliyun.com \
    && pip install -U pip \
    && pip install -r requirements.txt
