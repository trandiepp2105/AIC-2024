# Using image python 3.11
FROM python:3.11-slim

# Create working dir
WORKDIR /cloudserver

# copy requirements.txt to working dir
COPY requirements.txt .

# download package from requirements
RUN pip install --no-cache-dir -r requirements.txt

# copy all code to container
COPY . .

ENV PYTHONPATH=/cloudserver

COPY entrypoint.sh /entrypoint.sh

# Đảm bảo script có quyền thực thi
RUN chmod +x /entrypoint.sh

# Xóa ký tự \r trong file entrypoint.sh
RUN sed -i 's/\r$//' /entrypoint.sh

# Định nghĩa lệnh chạy container
ENTRYPOINT ["sh", "/entrypoint.sh"]