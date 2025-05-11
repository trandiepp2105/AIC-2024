from preprocess.invalid_entry_parseq import remove_invalid_entry
from preprocess.lowercase import lowercase_json_file
from preprocess.remove_accent import remove_accent_in_json_file

if __name__ == "__main__":
    ocr_json_folder = r"D:\ELASTIC-DATA\parseq-ocr-json-data"  # Sử dụng 'r' để định nghĩa đường dẫn
    remove_accent_in_json_file(ocr_json_folder)
    lowercase_json_file(ocr_json_folder)
    remove_invalid_entry(ocr_json_folder)