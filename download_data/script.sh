#!/bin/bash

# Bước 1: Cài đặt các gói từ requirements.txt
echo "Installing Python packages from requirements.txt..."
pip install -r requirements.txt

# Kiểm tra xem việc cài đặt có thành công hay không
if [ $? -ne 0 ]; then
    echo "Failed to install packages. Exiting."
    exit 1
fi

# Bước 2: Chạy file Python
echo "Running the Python script..."
python download_data.py

# Kiểm tra xem việc chạy script có thành công hay không
if [ $? -ne 0 ]; then
    echo "Python script failed to run. Exiting."
    exit 1
fi

echo "Script executed successfully."
