from time import time, sleep
from pymemcache.client.base import Client
from pymemcache import serde
import cv2


client = Client(
    ("yuhao_memcache", 12000),
    serializer=serde.python_memcache_serializer,
    deserializer=serde.python_memcache_deserializer,
)
client2 = Client(
    ("yuhao_memcache_2", 12001),
    serializer=serde.python_memcache_serializer,
    deserializer=serde.python_memcache_deserializer,
)

img = cv2.imread("test.png")
img = cv2.resize(img, (1280, 720))
client.set("image", img)

while True:
    start_time=time()
    image = client.get("image")
    # print(time() - start_time)
    client2.set("image", image)
    sleep(0.04 - ((time() - start_time) % 0.04))
    print(time() - start_time)
