import torch
import os
from ai_workers.code_custodian import CodeCustodianAI

def verify_setup():
    print(f"PyTorch version: {torch.__version__}")
    print(f"CUDA available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"CUDA device: {torch.cuda.get_device_name()}")
    
    custodian = CodeCustodianAI()
    test_code = "def test(): pass"
    result = custodian.analyze_and_fix_code(test_code)
    print(f"AI Analysis result: {result}")

if __name__ == "__main__":
    verify_setup()