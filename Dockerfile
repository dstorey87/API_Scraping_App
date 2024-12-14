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
