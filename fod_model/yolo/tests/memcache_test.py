from pymemcache.client.base import Client
from pymemcache import serde
import logging
from time import sleep, time
import cv2


client = Client(
    ("status_register", 12001),
    serializer=serde.python_memcache_serializer,
    deserializer=serde.python_memcache_deserializer,
)
def test_fun():
    client.set(1, "error")
    if  not client.get(1):
        print("not found")
    else:
        print(client.get(1))
# img = cv2.imread(result)

# while True:
#     t2 = time()
#     result = client.get("some_key")
#     t3 = time()
#     logging.warning("Get Time: {:.4f}s".format(t3 - t2))
#     sleep(1)
if __name__ == "__main__":
    test_fun()