FROM python:3.10

WORKDIR /ai

RUN pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

COPY requirements.txt ./

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt

COPY ./ ./

ENV PYTHONPATH=/ai

COPY entrypoint.sh /entrypoint.sh

# Đảm bảo script có quyền thực thi
RUN chmod +x /entrypoint.sh

# Xóa ký tự \r trong file entrypoint.sh
RUN sed -i 's/\r$//' /entrypoint.sh

# Thiết lập script entrypoint để chạy khi container khởi động
ENTRYPOINT ["/entrypoint.sh"]