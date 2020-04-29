from pymemcache.client.base import Client
import logging
from time import sleep, time
import cv2


client = Client(("yuhao_memcache", 12000))
img = cv2.imread("test.png")
# try:
#     client.set("some_key", "some_value")
# except:
#     raise SystemError



while True:
    t1 = time()
    client.set("some_key", img)
    t2 = time()
    print(t2 - t1)
    sleep(0.1)

