from elastic_search.elastic.elasticsearch_schema import ParseqSearch
import os

# Sử dụng class OCRSearch
def load_data_into_elastic():
    # Thiết lập kết nối và tạo chỉ mục nếu chưa tồn tại
    elastic_json_dir = os.path.join(os.getenv('ROOT_DIR'), "elastic-json")
    ocr_json_folder = os.path.join(elastic_json_dir, "parseq-ocr-json-data")
    parseq_search = ParseqSearch(hosts=['http://elasticsearch:9200'])
    parseq_search.setup()
    parseq_search.load_data_from_json_files(ocr_json_folder)

if __name__ == "__main__":
    load_data_into_elastic()