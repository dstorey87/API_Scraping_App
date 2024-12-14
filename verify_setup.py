import sys
import torch
import os

def verify_setup():
    print(f"Python version: {sys.version}")
    print(f"PyTorch version: {torch.__version__}")
    print(f"CUDA available: {torch.cuda.is_available()}")
    
    if torch.cuda.is_available():
        print(f"CUDA device: {torch.cuda.get_device_name()}")
    else:
        print("Running in CPU-only mode")

if __name__ == "__main__":
    verify_setup()
