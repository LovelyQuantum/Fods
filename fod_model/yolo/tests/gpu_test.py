import nvidia_smi

nvidia_smi.nvmlInit()

handle = nvidia_smi.nvmlDeviceGetHandleByIndex(0)
# card id 0 hardcoded here, there is also a call to get all available card ids, so we could iterate

info = nvidia_smi.nvmlDeviceGetMemoryInfo(handle)

print(type(f"{(info.total / 2 ** 30):.2f}"))
print("Free memory:", info.free / 2 ** 30)
print("Used memory:", info.used / 2 ** 30)
print(type(f"I'm{123}"))
nvidia_smi.nvmlShutdown()
