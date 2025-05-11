import json
import re
import os

def is_valid_entry(value):
    # Kiểm tra xem mục có phải là None, rỗng, chỉ chứa khoảng trắng hay không
    if value is None or value.strip() == "":
        return False
    
    # Biểu thức chính quy để kiểm tra định dạng thời gian
    time_pattern = re.compile(
        r'^(?:\d{0,2}.?\d{0,2}.?\d{0,2}\s*([gGiIlLaăâáấấàầAĂÂÁẮẤÀẦyY]{1,4})?\s*.?)$'
    )
    
    if time_pattern.match(value.strip()):
        return False
    
    return True


# print(is_valid_entry("00153:04 giây ")) 
if __name__ == "__main__":
    ocr_json_folder = os.getenv('CONTAINER_OCR_JSON_DATA_FOLDER')
    for filename in os.listdir(ocr_json_folder):
        if filename.endswith('.json'):
            video_name = filename[:-5]  # Lấy tên video từ tên file (bỏ đuôi .json)
            file_path = os.path.join(ocr_json_folder, filename)
            
            # Đọc dữ liệu từ file JSON
            with open(file_path, 'r', encoding='utf-8') as json_file:
                data = json.load(json_file)
            
            # Lọc các mục hợp lệ
            filtered_data = {key: value for key, value in data.items() if is_valid_entry(value)}
            
            # Ghi đè lên file JSON cũ với dữ liệu đã lọc
            with open(file_path, 'w', encoding='utf-8') as json_file:
                json.dump(filtered_data, json_file, ensure_ascii=False, indent=4)

            print(f"Đã lọc dữ liệu và ghi đè lên '{filename}'.")
