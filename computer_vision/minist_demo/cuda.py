import torch

print("CUDA是否可用:", torch.cuda.is_available())
if torch.cuda.is_available():
    print("CUDA设备数量:", torch.cuda.device_count())
    print("当前CUDA设备索引:", torch.cuda.current_device())
    print("当前CUDA设备名称:", torch.cuda.get_device_name(torch.cuda.current_device()))
    print("CUDA版本:", torch.version.cuda)
    print("cuDNN版本:", torch.backends.cudnn.version())
else:
    print("未检测到CUDA设备")