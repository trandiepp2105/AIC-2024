from elastic_search.elastic.elasticsearch_schema import CaptionSearch
import os

# Sử dụng class OCRSearch
def load_data_into_elastic():
    # Thiết lập kết nối và tạo chỉ mục nếu chưa tồn tại
    elastic_json_dir = os.path.join(os.getenv('ROOT_DIR'), "elastic-json")
    caption_json_folder = os.path.join(elastic_json_dir, "captions")
    caption_search = CaptionSearch(hosts=['http://elasticsearch:9200'])
    caption_search.setup()
    
    # CaptionSearch.setup(hosts=['http://elasticsearch:9200'])
    caption_search.load_data_from_json_files(caption_json_folder)

if __name__ == "__main__":
    load_data_into_elastic()