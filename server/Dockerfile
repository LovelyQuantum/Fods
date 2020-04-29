FROM python
RUN mkdir /code
COPY . /code/
WORKDIR /code/browse_web
RUN apt-get update \
    && apt-get install -y python-psycopg2 libpq-dev \
    && pip install -U pip -i https://pypi.tuna.tsinghua.edu.cn/simple \
    && pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# FROM registry.cn-hangzhou.aliyuncs.com/hina/server:v1.0
# # RUN mkdir /code
# COPY . /code/
# WORKDIR /code/browse_web
# # RUN apt-get update \
# #     && apt-get install -y python-psycopg2 libpq-dev libsm6 libxext6 libxrender-dev ffmpeg \
# #     && pip install -U pip -i https://pypi.tuna.tsinghua.edu.cn/simple \
# #     && pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple