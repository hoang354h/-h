import torch
import psutil
import GPUtil

class ModelManager:
    def clear_cache(self):
        torch.cuda.empty_cache()
        memory = psutil.virtual_memory()
        gpus = GPUtil.getGPUs()
        print(f"RAM: {memory.percent}% | GPU: {gpus[0].load*100 if gpus else 0}%")
