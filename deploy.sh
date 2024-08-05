#!/bin/bash

# Cấu hình các biến
SERVER_USER="username"
SERVER_IP="server_ip"
REMOTE_PROJECT_PATH="/AIC_PROJECT/"
SSH_KEY_PATH="C:\Users\tranv/.ssh/id_rsa"
GIT_REPO_URL="https://github.com/trandiepp2105/AIC-2024.git"
GIT_BRANCH="main"  # Thay đổi theo nhánh bạn muốn

# Kiểm tra các tham số đầu vào
if [ -z "$SERVER_USER" ] || [ -z "$SERVER_IP" ]; then
  echo "Vui lòng cấu hình SERVER_USER và SERVER_IP trong script này."
  exit 1
fi

# Bước 2: Kết nối vào server và thực hiện các lệnh deploy
echo "Kết nối vào server và thực hiện các lệnh deploy..."
ssh -i $SSH_KEY_PATH $SERVER_USER@$SERVER_IP << EOF

  # Cài môi trường python trên má chủ ubuntu
  echo "Cài đặt môi trường python"
  sudo apt-get update
  sudo apt-get install -y python3 python3-pip

  # Cập nhật hệ thống và cài đặt Docker
  echo "Cập nhật hệ thống và cài đặt Docker..."
  sudo apt-get update
  sudo apt-get upgrade -y 
  sudo apt-get install -y apt-transport-https ca-certificates curl gnupg-agent software-properties-common
  curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
  sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu \$(lsb_release -cs) stable"
  sudo apt-get update
  sudo apt-get install -y docker-ce docker-ce-cli containerd.io

  # Cài đặt Docker Compose
  echo "Cài đặt Docker Compose..."
  sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-\$(uname -s)-\$(uname -m)" -o /usr/local/bin/docker-compose
  sudo chmod +x /usr/local/bin/docker-compose

  # Cấu hình tường lửa
  echo "Cấu hình tường lửa..."
  sudo ufw allow OpenSSH
  sudo ufw allow 80/tcp
  sudo ufw allow 8000/tcp
  sudo ufw allow 443/tcp
  sudo ufw --force enable

  # Điều hướng đến thư mục dự án
  cd $REMOTE_PROJECT_PATH

  # Xóa thư mục dự án hiện tại và clone lại từ GitHub
  echo "Xóa thư mục dự án hiện tại và clone lại từ GitHub..."
  sudo rm -rf $REMOTE_PROJECT_PATH
  git clone -b $GIT_BRANCH $GIT_REPO_URL $REMOTE_PROJECT_PATH

  # Di chuyển đến thư mục dự án
  cd /AIC-2024/Download_video
  pip3 install -r requirements.txt
  python3 download.py

  # Khởi động các container Docker
  cd ../ai
  echo "Khởi động các container Docker..."
  docker-compose up -d
  echo "Quá trình deploy hoàn tất!"
EOF
