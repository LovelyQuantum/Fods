import cv2
import nvidia_smi
import tensorflow as tf


def get_gpu_mem(gpu_num):
    nvidia_smi.nvmlInit()
    handle = nvidia_smi.nvmlDeviceGetHandleByIndex(int(gpu_num))
    info = nvidia_smi.nvmlDeviceGetMemoryInfo(handle)
    nvidia_smi.nvmlShutdown()
    return int(f"{(info.free / 2 ** 30):.2f}")


def transform_image(camera, image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = tf.expand_dims(image, 0)
    image = tf.image.resize_with_pad(image, (416, 416))
    # FIXME don't use numbers
    image = image / 255
    return image