from pymemcache.client.base import Client
from pymemcache import serde
from time import time, sleep


image_register_A = Client(
    ("image_register_A", 12002),
    serializer=serde.python_memcache_serializer,
    deserializer=serde.python_memcache_deserializer,
)

image_register_B = Client(
    ("image_register_B", 12003),
    serializer=serde.python_memcache_serializer,
    deserializer=serde.python_memcache_deserializer,
)

fod_image_register_A = Client(
    ("fod_image_register_A", 12004),
    serializer=serde.python_memcache_serializer,
    deserializer=serde.python_memcache_deserializer,
)

fod_image_register_B = Client(
    ("fod_image_register_B", 12005),
    serializer=serde.python_memcache_serializer,
    deserializer=serde.python_memcache_deserializer,
)


def transfer(device):
    while True:
        start_time = time()
        image_register_B.set(device["id"], image_register_A.get(device["id"]))
        sleep(0.04 - ((time() - start_time) % 0.04))


def fod_transfer(device):
    while True:
        start_time = time()
        fod_image_register_A.set(
            f"fod_pipeline_{device['virtual_gpu_id']}",
            image_register_A.get(device["id"]),
        )
        image_register_B.set(
            device["id"],
            fod_image_register_B.get(f"fod_pipeline_{device['virtual_gpu_id']}"),
        )
        sleep(0.04 - ((time() - start_time) % 0.04))
