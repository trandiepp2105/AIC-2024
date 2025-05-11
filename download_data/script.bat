@echo off
REM Cài đặt các gói từ requirements.txt
pip install -r requirements.txt

REM Chạy tệp Python
python download_data.py

REM Giữ cửa sổ Command Prompt mở sau khi thực thi
pause