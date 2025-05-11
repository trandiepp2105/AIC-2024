from elastic_search.elastic.elasticsearch_schema import VietOCRSearch
import os

# Sử dụng class OCRSearch
def load_data_into_elastic():
    # Thiết lập kết nối và tạo chỉ mục nếu chưa tồn tại
    elastic_json_dir = os.path.join(os.getenv('ROOT_DIR'), "elastic-json")
    ocr_json_folder = os.path.join(elastic_json_dir, "viet-ocr-json-data")
    vietocr_search = VietOCRSearch(hosts=['http://elasticsearch:9200'])
    vietocr_search.setup()
    vietocr_search.load_data_from_json_files(ocr_json_folder)

if __name__ == "__main__":
    load_data_into_elastic()