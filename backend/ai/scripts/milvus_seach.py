from pymilvus import connections, Collection, DataType, FieldSchema, CollectionSchema, utility

class MilvusSearch:
    def __init__(self, host='127.0.0.1', port='19530', collection_name='search_collection'):
        self.client = connections.connect(host=host, port=port)
        self.collection = Collection(collection_name)

    def search(self, vectors, top_k=100):
        search_param = {
            "data": vectors,
            "anns_field": "vector_embedding",
            "param": {
                "metric_type": "IP",
                "params": {"nprobe": 10}
            },
            "limit": top_k
        }
        search_request = self.collection.search(**search_param)

        self.collection.load()

        res = self.collection.hybrid_search(search_request)

        return res
    
class MilvusSingleton:
    _instance = None

    def __new__(cls, host='127.0.0.1', port='19530', collection_name='search_collection'):
        if cls._instance is None:
            cls._instance = MilvusSearch(host, port, collection_name)
        return cls._instance