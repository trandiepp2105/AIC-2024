FROM pytorch/pytorch:2.1.0-cuda12.1-cudnn8-runtime


# RUN apt-get update && apt-get install -y git ninja-build libglib2.0-0 libsm6 libxrender-dev libxext6 libgl1-mesa-glx \
#     && apt-get clean \
#     && rm -rf /var/lib/apt/listsconda install pytorch==2.1.0 torchvision==0.16.0 torchaudio==2.1.0 -c pytorch/*

WORKDIR /ai

COPY requirements.txt ./
COPY ./ ./

RUN pip install -U openmim
RUN mim install mmengine

ENV FORCE_CUDA="1"

RUN pip install --upgrade pip setuptools wheel
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt

RUN pip install --no-cache-dir -e .
RUN pip install -r OCR/requirements/albu.txt

ENV PYTHONPATH=/ai

COPY entrypoint.sh /entrypoint.sh

# Đảm bảo script có quyền thực thi
RUN chmod +x /entrypoint.sh

# Xóa ký tự \r trong file entrypoint.sh
RUN sed -i 's/\r$//' /entrypoint.sh

# Thiết lập script entrypoint để chạy khi container khởi động
ENTRYPOINT ["/entrypoint.sh"]