FROM registry.cn-hangzhou.aliyuncs.com/hina/python:3.7
COPY . /server
WORKDIR /server
RUN apt-get update \
    && apt-get install -y python-psycopg2 libpq-dev \
    && pip install -U pip -i https://pypi.tuna.tsinghua.edu.cn/simple \
    && pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
