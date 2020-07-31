FROM registry.cn-hangzhou.aliyuncs.com/hina/node:12.16.3 as build-stage
WORKDIR /web
COPY package*.json ./
RUN cnpm install
COPY ./ .
RUN npm run build

FROM nginx as production-stage
RUN mkdir /web
COPY --from=build-stage /web/dist /web
COPY nginx.conf /etc/nginx/nginx.conf