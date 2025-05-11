FROM pytorch/pytorch:2.1.0-cuda12.1-cudnn8-runtime

WORKDIR /extract_keyframe

COPY requirements.txt ./

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt

COPY ./ ./

ENV PYTHONPATH=/extract_keyframe

COPY entrypoint.sh /entrypoint.sh

# Đảm bảo script có quyền thực thi
RUN chmod +x /entrypoint.sh

# Xóa ký tự \r trong file entrypoint.sh
RUN sed -i 's/\r$//' /entrypoint.sh

# Thiết lập script entrypoint để chạy khi container khởi động
ENTRYPOINT ["/entrypoint.sh"]