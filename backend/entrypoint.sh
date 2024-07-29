#!/bin/sh

# Đường dẫn đến file đánh dấu
MIGRATION_FLAG="/backend/app/migrations/.migration_flag"

echo "Running backend"

# Kiểm tra xem file đánh dấu đã tồn tại hay chưa
if [ ! -f "$MIGRATION_FLAG" ]; then
  # Nếu không tồn tại, chạy các lệnh ban đầu
  echo "Running initial migrations and database setup..."
  sleep 30

  # Chạy các lệnh Alembic để tạo và áp dụng migration
  alembic revision --autogenerate -m 'initial migration'
  alembic upgrade head

  # Chạy script để khởi tạo dữ liệu ban đầu cho database
  python ./app/initial_database.py

  # Tạo file đánh dấu để ghi nhớ lần chạy đầu tiên
  touch "$MIGRATION_FLAG"

  sleep 15
fi

echo "Running AI script"

# Chạy script liên quan đến AI
python ./ai/database/database.py

echo "Starting FastAPI server"

# Chạy FastAPI
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
