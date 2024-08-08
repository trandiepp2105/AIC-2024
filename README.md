# AIC-2024

# Cấu hình SSH server

# đăng nhập vào server

ssh $SERVER_USER@$SERVER_IP

# nhập mật khẩu

# cập nhật cái gói

sudo apt-get update

# đợi 1-2p

# đăng nhập lại server

# kiểm tra nvidia driver

nvidia-smi

# kiểm tra vidia-container

nvidia-container-cli --version

# mở file cấu hình

sudo nano /etc/ssh/sshd_config

# mở xác thực bằng public key

PubkeyAuthentication yes

# kiểm tra dòng này được mở comment chưa

AuthorizedKeysFile .ssh/authorized_keys

# Thiết lập quyền thực thi

chmod +x deploy.sh

# sửa lại các ký tự đặc biệt

sed -i 's/\r$//' deploy.sh

# run deploy.sh
