#!/bin/sh

# Đường dẫn đến file đánh dấu
MIGRATION_FLAG="/backend/app/migrations/.migration_flag"

# Kiểm tra xem file đánh dấu đã tồn tại hay chưa
if [ ! -f "$MIGRATION_FLAG" ]; then
  # Nếu không tồn tại, chạy các lệnh ban đầu
  echo "Running initial migrations and database setup..."
  sleep 30
  alembic revision --autogenerate -m 'initial migration'
  alembic upgrade head
  python ./app/initial_database.py

  # Tạo file đánh dấu để ghi nhớ lần chạy đầu tiên
  touch "$MIGRATION_FLAG"
fi

# Chạy FastAPI
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
echo "run ai"
python ./ai/database/database.py