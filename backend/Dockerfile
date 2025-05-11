# syntax = docker/dockerfile:1.4

# FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9-slim AS builder
FROM pytorch/pytorch:2.4.0-cuda11.8-cudnn9-runtime

WORKDIR /backend

# Cài đặt mysql-client
RUN apt-get update && apt-get install -y default-mysql-client
# Cài đặt curl
RUN apt-get update && apt-get install -y curl
RUN pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

COPY requirements.txt ./
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt

COPY ./ ./

ENV PYTHONPATH=/backend

COPY entrypoint.sh /entrypoint.sh

# Đảm bảo script có quyền thực thi
RUN chmod +x /entrypoint.sh

# Xóa ký tự \r trong file entrypoint.sh
RUN sed -i 's/\r$//' /entrypoint.sh

# Thiết lập script entrypoint để chạy khi container khởi động
ENTRYPOINT ["/entrypoint.sh"]


