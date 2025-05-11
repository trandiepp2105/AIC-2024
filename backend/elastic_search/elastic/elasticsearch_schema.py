from elasticsearch_dsl import Document, Text, Integer, Keyword, connections, Float
from elasticsearch.exceptions import NotFoundError
from elasticsearch.helpers import bulk
from elasticsearch_dsl import Q
import os
import json


class ElasticBase(Document):

    def __init__(self, **kwargs):  # Thay đổi ở đây
        super().__init__(**kwargs)  # Truyền tất cả các tham số vào hàm khởi tạo của lớp cha
        self.hosts = kwargs.get('hosts', None)  # Lấy hosts từ kwargs
        self.connection = None
        self.connect()  # Kết nối khi tạo đối tượng
    
    def setup(self):
        self.create_index_if_not_exists()  # Tạo chỉ mục nếu chưa có

    def connect(self):
        print("hosts: ", self.hosts)
        self.connection = connections.create_connection(hosts=self.hosts)
        if self.connection.ping():
            print("Kết nối thành công!")
        else:
            print("Kết nối thất bại!")

    def create_index_if_not_exists(self):
        if not self.connection.indices.exists(index=self.Index.name):
            print(f"Tạo chỉ mục '{self.Index.name}'...")
        else:
            print(f"Chỉ mục '{self.Index.name}' đã tồn tại.")

    def clear_index(self):
        try:
            self.connection.indices.delete(index=self.Index.name)
            print(f"Đã xóa chỉ mục '{self.Index.name}'.")
            self.create_index_if_not_exists()  # Tạo lại chỉ mục sau khi xóa
        except Exception as e:
            print(f"Lỗi khi xóa chỉ mục '{self.Index.name}': {str(e)}")

    def load_data_in_batches(self, data, batch_size=500):
        self.create_index_if_not_exists()
        es = self.connection

        for i in range(0, len(data), batch_size):
            batch_data = data[i:i + batch_size]
            actions = [
                {
                    "_index": self.Index.name,
                    "_source": item
                }
                for item in batch_data
            ]

            success, failed = bulk(es, actions)
            print(f"Batch từ {i} tới {i + batch_size}: {success} documents đã được thêm vào, {failed} thất bại.")

    def load_data_from_json_files(self, folder_path, text_field_name, batch_size=500):
        """
        Đọc dữ liệu từ tất cả các file JSON trong thư mục và thêm vào Elasticsearch.
        :param folder_path: Đường dẫn đến thư mục chứa các file JSON.
        :param text_field_name: Tên của trường chứa văn bản (ví dụ: 'ocr_text', 'caption').
        :param batch_size: Kích thước batch khi thêm vào Elasticsearch.
        """
        print("CLEAR DATA IN ELASTICSEARCH!")
        self.clear_index()
        print("START LOADING ELASTICSEARCH DATA!")

        for filename in os.listdir(folder_path):
            if filename.endswith('.json'):
                video_name = filename[:-5]  # Lấy tên video từ tên file (bỏ đuôi .json)
                file_path = os.path.join(folder_path, filename)
                
                with open(file_path, 'r', encoding='utf-8') as json_file:
                    data = json.load(json_file)
                    records = []

                    for frame_number, v in data.items():
                        text_content = v['text']
                        fps = v['fps']
                        second = frame_number/fps
                        if text_content and text_content.strip():
                            records.append({
                                text_field_name: text_content,
                                'frame_number': int(frame_number),
                                'video_name': video_name,
                                'second': second
                            })
                            
                            if len(records) >= batch_size:
                                self.load_data_in_batches(records, batch_size)
                                records = []

                    if records:
                        self.load_data_in_batches(records, batch_size)

    def convert_to_lowercase(self, field_name, batch_size=1000):
        """
        Duyệt qua toàn bộ index và chuyển các trường về dạng chữ thường.
        
        :param field_name: Tên trường cần chuyển đổi về dạng chữ thường (ví dụ: 'ocr_text', 'caption', ...)
        :param batch_size: Kích thước batch khi xử lý.
        """
        print(f"Chuyển tất cả văn bản trong trường '{field_name}' của chỉ mục '{self.Index.name}' về dạng chữ thường...")
        es = self.connection
        scroll = es.search(index=self.Index.name, scroll='2m', body={"query": {"match_all": {}}}, size=batch_size)
        scroll_id = scroll['_scroll_id']
        hits = scroll['hits']['hits']

        while len(hits) > 0:
            actions = [
                {
                    "_op_type": "update",
                    "_index": self.Index.name,
                    "_id": hit['_id'],
                    "doc": {
                        field_name: hit['_source'][field_name].lower() if field_name in hit['_source'] else ""
                    }
                }
                for hit in hits
            ]
            
            success, failed = bulk(es, actions)
            print(f"Đã cập nhật {success} documents thành công, {failed} thất bại.")
            
            scroll = es.scroll(scroll_id=scroll_id, scroll='2m')
            scroll_id = scroll['_scroll_id']
            hits = scroll['hits']['hits']
        
        print(f"Hoàn tất chuyển đổi các tài liệu về chữ thường trong chỉ mục '{self.Index.name}'.")

    def search_field(self, query, top_k=30):
        """
        Tìm kiếm trong chỉ mục với từ khóa được cung cấp.
        Sử dụng tên chỉ mục làm tên trường để tìm kiếm.

        :param query: Chuỗi truy vấn để tìm kiếm.
        :param top_k: Số lượng kết quả muốn trả về (mặc định là 30).
        :return: Danh sách kết quả tìm kiếm dưới dạng tuple (frame_number, video_name).
        """
        field_name = self.Index.name  # Lấy tên trường tìm kiếm từ tên chỉ mục

        # Tạo các truy vấn
        match_phrase_query = Q("match_phrase", **{field_name: query})  # Tìm kiếm cụm từ chính xác
        match_query = Q("match", **{
            field_name: {
                "query": query,
                "operator": "AND"  # Yêu cầu tất cả các từ trong query phải xuất hiện
            }
        })
        fuzzy_query = Q("match", **{
            field_name: {
                "query": query,
                "fuzziness": "AUTO"  # Cho phép tìm kiếm mờ để khắc phục lỗi chính tả
            }
        })

        # Kết hợp các truy vấn với nhau, ưu tiên match_phrase trước
        bool_query = Q("bool", should=[match_phrase_query, match_query, fuzzy_query])

        # Thực hiện tìm kiếm
        # search_instance = self.search().query(bool_query).extra(size=top_k)
        search_instance = self.connection.search(index=self.Index.name, body={
        "query": bool_query.to_dict(),
        "size": top_k
    })
        # search_result = search_instance.execute()

        # # Chuyển đổi kết quả thành danh sách các tuple
        # results = [(hit.video_name, hit.frame_number) for hit in search_result]
        results = [(hit['_source']['video_name'], hit['_source']['frame_number'], hit['_source']['second']) for hit in search_instance['hits']['hits']]

        return results
    
class ParseqSearch(ElasticBase):
    # Định nghĩa các trường trong chỉ mục
    parseq = Text(analyzer='standard')  # Dữ liệu dạng văn bản, được phân tích để tìm kiếm
    frame_number = Integer()              # Dữ liệu dạng số nguyên
    video_name = Keyword()                # Dữ liệu dạng keyword, không phân tích
    second = Float()
    
    class Index:
        name = 'parseq'  # Tên chỉ mục

    def load_data_from_json_files(self, folder_path, batch_size=500):
        super().load_data_from_json_files(folder_path, self.Index.name, batch_size)


    def search_with_priority(self, query, top_k=100):
        """
        Tìm kiếm tài liệu với ưu tiên:
        1. Chứa cụm từ chính xác như trong query.
        2. Chứa từ nhưng không có khoảng trắng (nếu có nhiều từ trong query).
        3. Chứa các từ trong query theo đúng thứ tự.
        4. Chứa các từ trong query nhưng không cần đúng thứ tự.
        
        :param query: Chuỗi truy vấn, ví dụ: "nhiệt đới".
        :param top_k: Số lượng kết quả muốn trả về (mặc định là 30).
        :return: Danh sách kết quả tìm kiếm dưới dạng (video_name, frame_number, _score).
        """
        field_name = self.Index.name

        # Điều kiện ưu tiên 1: Cụm từ chính xác
        match_phrase_query = Q("match_phrase", **{field_name: query})

        # Điều kiện ưu tiên 2: Không có khoảng trắng (nếu query có nhiều từ)
        if " " in query:
            query_no_space = query.replace(" ", "")
            match_exact_no_space = Q("match", **{field_name: query_no_space})
        else:
            match_exact_no_space = Q("match", **{field_name: query})

        # Điều kiện ưu tiên 3: Các từ trong query, đúng thứ tự
        match_ordered = Q("match_phrase", **{field_name: query})

        # Điều kiện ưu tiên 4: Các từ trong query nhưng không cần đúng thứ tự
        match_unordered = Q("match", **{
            field_name: {
                "query": query,
                "operator": "AND"
            }
        })

        # Kết hợp các truy vấn với độ ưu tiên giảm dần
        bool_query = Q("bool", should=[
            match_phrase_query,   # Điều kiện 1
            match_exact_no_space, # Điều kiện 2
            match_ordered,        # Điều kiện 3
            match_unordered       # Điều kiện 4
        ])

        # Thực hiện tìm kiếm với truy vấn trên
        search_instance = self.connection.search(index=self.Index.name, body={
            "query": bool_query.to_dict(),
            "size": top_k
        })

        # Trích xuất kết quả gồm video_name, frame_number và _score
        results = [
            (hit['_source']['video_name'], hit['_source']['frame_number'], hit['_score'])
            for hit in search_instance['hits']['hits']
        ]

        return results
    # @classmethod
    # def search_ocr(cls, query, top_k=30):
    #     """
    #     Tìm kiếm trong chỉ mục với từ khóa được cung cấp.
    #     Nếu có kết quả chính xác, sẽ có rank cao hơn so với các kết quả khác.
        
    #     :param query: Chuỗi truy vấn để tìm kiếm
    #     :param top_k: Số lượng kết quả muốn trả về (mặc định là 30)
    #     :return: Danh sách kết quả tìm kiếm dưới dạng tuple (frame_number, video_name)
    #     """
    #     # Tạo các truy vấn
    #     match_phrase_query = Q("match_phrase", ocr_text=query)  # Tìm kiếm cụm từ chính xác
    #     match_query = Q("match", ocr_text=query)  # Tìm kiếm từ khóa
    #     fuzzy_query = Q("fuzzy", ocr_text={"value": query, "fuzziness": "AUTO"})  # Tìm kiếm fuzzy
        
    #     # Kết hợp các truy vấn với nhau, ưu tiên match_phrase trước
    #     bool_query = Q("bool", should=[match_phrase_query, match_query, fuzzy_query])
        
    #     # Thực hiện tìm kiếm
    #     search_instance = cls.search().query(bool_query).extra(size=top_k)
    #     search_result = search_instance.execute()
        
    #     # Chuyển đổi kết quả thành danh sách các tuple
    #     results = [(hit.video_name, hit.frame_number) for hit in search_result]
        
    #     return results

class VietOCRSearch(ElasticBase):
    # Định nghĩa các trường trong chỉ mục
    vietocr = Text(analyzer='standard')  # Dữ liệu dạng văn bản, được phân tích để tìm kiếm
    frame_number = Integer()              # Dữ liệu dạng số nguyên
    video_name = Keyword()                # Dữ liệu dạng keyword, không phân tích
    
    class Index:
        name = 'vietocr'  # Tên chỉ mục

    def load_data_from_json_files(self, folder_path, batch_size=500):
        super().load_data_from_json_files(folder_path, self.Index.name, batch_size)

class CaptionSearch(ElasticBase):
    # Định nghĩa các trường trong chỉ mục
    caption = Text(analyzer='standard')  # Dữ liệu dạng văn bản, được phân tích để tìm kiếm
    frame_number = Integer()              # Dữ liệu dạng số nguyên
    video_name = Keyword()                # Dữ liệu dạng keyword, không phân tích
    
    class Index:
        name = 'caption'  # Tên chỉ mục
    def load_data_from_json_files(self, folder_path, batch_size=500):
        super().load_data_from_json_files(folder_path, self.Index.name, batch_size)