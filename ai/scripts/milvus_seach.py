from pymilvus import connections, Collection, DataType, FieldSchema, CollectionSchema, utility

class MilvusSearch:
    def __init__(self, host='localhost', port='19530', collection_name='embedding_collection'):
        self.client = connections.connect(host=host, port=port,time_out=100)
        try:
            self.collection = Collection(collection_name)
        except:
            search_schema = CollectionSchema([
                FieldSchema(name="id", dtype=DataType.INT64, is_primary=True),
                FieldSchema(name="path", dtype=DataType.STRING, description="path of the video"),
                FieldSchema(name="vector_embedding", dtype=DataType.FLOAT_VECTOR, dim=768, description="embedding vector")
            ], description="embedding collection")
            schema = CollectionSchema([search_schema])
            self.collection = Collection(name=collection_name, schema=schema)

            index_param = {"index_type": "IVF_FLAT", "metric_type": "IP", "params": {"nlist": 2048}}
            self.collection.create_index(field_name="vector_embedding", index_params=index_param)

    def insert(self, data):
        self.collection.insert(data)

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

    def __new__(cls, host='localhost', port='19530', collection_name='embedding_collection'):
        if cls._instance is None:
            cls._instance = MilvusSearch(host, port, collection_name)
        return cls._instance