#!/bin/bash

# Cấu hình các biến
SERVER_USER="root"
SERVER_IP="103.20.97.114"
REMOTE_PROJECT_PATH="/AIC_PROJECT/"
SSH_KEY_PATH="$HOME/.ssh/id_rsa"
SSH_PUB_KEY_PATH="$SSH_KEY_PATH.pub"
EMAIL_SSH_KEY="hokhanhduy324@gmail.com"
GIT_REPO_URL="https://github.com/trandiepp2105/AIC-2024.git"
GIT_BRANCH="main"  # Thay đổi theo nhánh bạn muốn

# Kiểm tra các tham số đầu vào
if [ -z "$SERVER_USER" ] || [ -z "$SERVER_IP" ]; then
  echo "Vui lòng cấu hình SERVER_USER và SERVER_IP trong script này."
  exit 1
fi

# Kiểm tra nếu SSH key đã tồn tại
if [ -f "$SSH_KEY_PATH" ]; then
  echo "SSH key đã tồn tại tại $SSH_KEY_PATH"
else
  # Tạo SSH key
  echo "Tạo SSH key..."
  ssh-keygen -t rsa -b 4096 -C "$EMAIL_SSH_KEY" -f "$SSH_KEY_PATH" -N ""
fi


# Sao chép SSH public key lên server
echo "Sao chép SSH public key lên server..."
ssh-copy-id -i "$SSH_PUB_KEY_PATH" $SERVER_USER@$SERVER_IP

# Kết nối vào server và thực hiện các lệnh deploy
echo "Kết nối vào server và thực hiện các lệnh deploy..."
ssh $SERVER_USER@$SERVER_IP -i $SSH_KEY_PATH << EOF
  # Cập nhật hệ thống và cài đặt Docker

  echo "Cập nhật hệ thống và cài đặt Docker..."
  sudo apt-get update

  sudo apt-get install -y apt-transport-https ca-certificates curl gnupg-agent software-properties-common
  curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
  sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu \$(lsb_release -cs) stable"
  sudo apt-get update
  sudo apt-get install -y docker-ce docker-ce-cli containerd.io

  # Cài đặt Docker Compose
  echo "Cài đặt Docker Compose..."
  sudo curl -L "https://github.com/docker/compose/releases/download/$(curl -s https://api.github.com/repos/docker/compose/releases/latest | grep -Po '\"tag_name\": \"\K.*?(?=\")')/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
  sudo chmod +x /usr/local/bin/docker-compose

  # # cài đặt nvidia container toolkit
  # sudo apt-get update

  curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey |sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg \
  && curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list \
  && sudo apt-get update

  # # Install the NVIDIA Container Toolkit packages:
  # sudo apt-get install -y nvidia-container-toolkit

  # Configure the container runtime by using the nvidia-ctk command:
  sudo nvidia-ctk runtime configure --runtime=docker

  # Restart the Docker daemon:
  sudo systemctl restart docker

  # Cấu hình tường lửa
  echo "Cấu hình tường lửa..."
  sudo ufw allow OpenSSH
  sudo ufw allow 80/tcp
  sudo ufw allow 8000/tcp
  sudo ufw allow 443/tcp
  sudo ufw --force enable

  # Xóa thư mục dự án hiện tại và clone lại từ GitHub
  echo "Xóa thư mục dự án hiện tại và clone lại từ GitHub..."
  sudo rm -rf $REMOTE_PROJECT_PATH
  git clone -b $GIT_BRANCH $GIT_REPO_URL $REMOTE_PROJECT_PATH

  # Di chuyển đến thư mục dự án
  cd $REMOTE_PROJECT_PATH
  cd AIC-2024
  cd Download_video
  pip3 install -r requirements.txt
  python3 download.py

  # Khởi động các container Docker
  cd ..
  cd ai
  echo "Khởi động các container Docker..."
  docker-compose up
  echo "Quá trình deploy hoàn tất!"
EOF