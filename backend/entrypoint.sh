#!/bin/sh


echo "Waiting for MySQL to be ready..."

# Kiểm tra trạng thái của MySQL, thử lại nếu thất bại
until mysqladmin ping -h "mysql" --silent; do
  echo "MySQL is unavailable - waiting..."
  sleep 5
done
echo "MySQL is ready!"

echo "Waiting for Elasticsearch to be ready..."
if ! command -v curl &> /dev/null
then
    echo "curl is not installed. Installing curl..."
    apt-get update && apt-get install -y curl
fi
echo "install curl successfully"
# Kiểm tra trạng thái của Elasticsearch, thử lại nếu thất bại
until curl -s http://elasticsearch:9200/_cluster/health | grep -q '"status":"green"\|"status":"yellow"'; do
  echo "Elasticsearch is unavailable - waiting..."
  sleep 5
done

echo "Elasticsearch is ready!"




echo "Running backend"

# Đường dẫn đến file đánh dấu
MIGRATION_FLAG="/backend/app/migrations/.migration_flag"
# Kiểm tra xem file đánh dấu đã tồn tại hay chưa
if [ ! -f "$MIGRATION_FLAG" ]; then
  # Nếu không tồn tại, chạy các lệnh ban đầu
  echo "Running initial migrations and database setup..."

  # Chạy các lệnh Alembic để tạo và áp dụng migration
  alembic revision --autogenerate -m 'initial migration'
  alembic upgrade head

  # Chạy script để khởi tạo dữ liệu ban đầu cho database
  python ./app/initial_database.py

  # Tạo file đánh dấu để ghi nhớ lần chạy đầu tiên
  touch "$MIGRATION_FLAG"

  echo "initial database done!"
fi

echo "Running AI script"

MILVUS_FLAG="/backend/ai/database/.milvus_flag"

if [ ! -f "$MILVUS_FLAG" ]; then
  echo "Running AI database setup..."
  # # Chạy script liên quan đến AI
  python -u ./ai/database/database.py 
  touch "$MILVUS_FLAG"
  echo "AI database done!"
fi

REDIS_FLAG="/backend/app/core/.redis_flag"

if [ ! -f "$REDIS_FLAG" ]; then
  echo "Running Redis database setup..."
  # # Chạy script liên quan đến AI
  python -u ./app/core/create_redis.py
  touch "$REDIS_FLAG"
  echo "Redis database done!"
fi

echo "Starting FastAPI server"

# Chạy FastAPI
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
