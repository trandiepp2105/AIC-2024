# Sử dụng hình ảnh Node.js để xây dựng ứng dụng
FROM node:20 AS build

# Thiết lập thư mục làm việc
WORKDIR /frontend

# Sao chép package.json và package-lock.json
COPY package*.json ./

# Cài đặt các phụ thuộc
RUN npm install

# Sao chép toàn bộ mã nguồn vào thư mục làm việc
COPY . .

# Xây dựng ứng dụng
RUN npm run build

# Sử dụng hình ảnh Nginx để phục vụ ứng dụng
FROM nginx:alpine

# Sao chép các tệp đã xây dựng từ bước trước sang thư mục phục vụ của Nginx
COPY --from=build /frontend/build /usr/share/nginx/html

# Sao chép cấu hình Nginx tùy chỉnh (tùy chọn)
COPY nginx.conf /etc/nginx/nginx.conf

# Mở cổng 80 để truy cập ứng dụng
EXPOSE 80

# Khởi động Nginx
CMD ["nginx", "-g", "daemon off;"]