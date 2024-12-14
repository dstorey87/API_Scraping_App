# Use the CUDA 11.8 base image compatible with PyTorch
FROM nvidia/cuda:11.8.0-devel-ubuntu22.04

# Set the working directory
WORKDIR /app

# Install Python3 and pip3
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

# Install PyTorch and related packages compatible with CUDA 11.8
RUN pip3 install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu118

# Copy your application's requirements file
COPY requirements.txt .

# Install additional Python packages
RUN pip3 install -r requirements.txt

# Copy your application source code
COPY . .

# Set the default command to run your application
CMD ["python3", "your_app_entry_point.py"]
