import nvidia_smi
import tensorflow as tf


def get_gpu_mem(gpu_num):
    nvidia_smi.nvmlInit()
    handle = nvidia_smi.nvmlDeviceGetHandleByIndex(int(gpu_num))
    info = nvidia_smi.nvmlDeviceGetMemoryInfo(handle)
    nvidia_smi.nvmlShutdown()
    return int(f"{(info.free / 2 ** 30):.2f}")


def transform_image(image, size):
    image = tf.expand_dims(image, 0)
    image = tf.image.resize(image, (size, size))
    # FIXME don't use numbers
    image = image / 255
    return image
