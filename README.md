# AIC-2024

sed -i 's/\r$//' entrypoint.sh

# Cấu hình SSH server

# đăng nhập vào server

ssh $SERVER_USER@$SERVER_IP

# nhập mật khẩu

# cập nhật cái gói

sudo apt-get update

sudo apt upgrade

# khởi động lại server

sudo reboot

# đợi 1-2p

# đăng nhập lại server

# mở file cấu hình

sudo nano /etc/ssh/sshd_config

# mở xác thực bằng public key

PubkeyAuthentication yes

# Thiết lập quyền thực thi

chmod +x deploy.sh

# sửa lại các ký tự đặc biệt

sed -i 's/\r$//' deploy.sh

# run deploy.sh
