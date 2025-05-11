import os
import json
from unidecode import unidecode

def lowercase_json_file(ocr_json_folder):
    for filename in os.listdir(ocr_json_folder):
        if filename.endswith('.json'):
            file_path = os.path.join(ocr_json_folder, filename)
            
            # Đọc dữ liệu từ file JSON
            with open(file_path, 'r', encoding='utf-8') as json_file:
                data = json.load(json_file)
            
            # Xóa dấu và chuyển thành chữ viết thường cho tất cả các giá trị trong dữ liệu JSON
            for key in data:
                # Xóa dấu và chuyển thành chữ viết thường
                data[key] = unidecode(data[key]).lower()
            
            # Lưu lại dữ liệu vào file JSON
            with open(file_path, 'w', encoding='utf-8') as json_file:
                json.dump(data, json_file, ensure_ascii=False, indent=4)

            print(f"Đã xóa dấu và chuyển thành chữ viết thường trong file: {filename}")

if __name__ == "__main__":
    ocr_json_folder = r"D:\ELASTIC-DATA\viet-ocr-json-data"  # Sử dụng 'r' để định nghĩa đường dẫn
    lowercase_json_file(ocr_json_folder)  
