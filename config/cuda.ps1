# Set working directory
$rootDir = "C:\API_Scraping_App"

Write-Output "Setting up CUDA and PyTorch environment..."

# Configure CUDA environment variables
$Env:CUDA_VISIBLE_DEVICES = "0"
$Env:CUDA_DEVICE_ORDER = "PCI_BUS_ID"
$Env:PYTORCH_CUDA_ALLOC_CONF = "max_split_size_mb:512"

# Create Dockerfile for CUDA support
$dockerfileContent = @"
FROM nvidia/cuda:11.8.0-devel-ubuntu22.04

WORKDIR /app

RUN apt-get update && \
    apt-get install -y python3.11 python3-pip && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .

CMD ["python3", "verify_setup.py"]
"@

$dockerfilePath = Join-Path -Path $rootDir -ChildPath "Dockerfile"
$dockerfileContent | Out-File -FilePath $dockerfilePath -Encoding utf8

Write-Output "Created Dockerfile with CUDA 11.8 support"

# Create verification script
$verifySetupContent = @"
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
"@

$verifyPath = Join-Path -Path $rootDir -ChildPath "verify_setup.py"
$verifySetupContent | Out-File -FilePath $verifyPath -Encoding utf8

Write-Output "Created verification script"
Write-Output "CUDA setup complete! You can now build the Docker image or run verify_setup.py directly"