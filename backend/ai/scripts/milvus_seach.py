from pymilvus import connections, Collection, AnnSearchRequest, WeightedRanker
import json

class MilvusSearch:
    def __init__(self, host='milvus-standalone', port='19530', collection_name='search_collection'):
        self.client = connections.connect('default', host=host, port=port)
        self.collection = Collection(collection_name)

    def search(self, vectors, top_k=100):
        param = {
            "metric_type": "IP",
            "params": {"nprobe": 92}
        }

        output_fields = ['idx']

        self.collection.load()
        
        response = self.collection.search(data=vectors, anns_field='embedding', param=param, limit=top_k, output_fields=output_fields)

        res = []
        for e in response[0]:
            res.append(e.entity.get('idx'))
            
        return res
    
    def search_hybrid(self, vectors, fields, priorities, top_k=100):
        features = ['description_vector', 'objects', 'time', 'similar_image_vector', 'ocr_embedding', 'audio_embedding']
        p = []
        reqs = []
        if vectors['description_vector'] is not None:
            p.append(priorities['description_vector'])
            param = {
                'data' : vectors['description_vector'],
                'anns_field' : fields['description_vector'],
                'param' : {
                    'metric_type' : 'IP',
                    'params' : {'nprobe': 92}
                },
                'limit' : top_k
            }
            reqs.append(AnnSearchRequest(**param))

        if vectors['objects'] is not None:
            p.append(priorities['objects'])
            param = {
                'data' : vectors['objects'],
                'anns_field' : fields['objects'],
                'param' : {
                    'metric_type' : 'L2',
                    'params' : {'nprobe': 92}
                },
                'limit' : top_k
            }
            reqs.append(AnnSearchRequest(**param))

        if vectors['time'] is not None:
            p.append(priorities['time'])
            param = {
                'data' : vectors['time'],
                'anns_field' : fields['time'],
                'param' : {
                    'metric_type' : 'L2',
                    'params' : {'nprobe': 92}
                },
                'limit' : top_k
            }
            reqs.append(AnnSearchRequest(**param))

        if vectors['similar_image_vector'] is not None:
            p.append(priorities['similar_image_vector'])
            param = {
                'data' : vectors['similar_image_vector'],
                'anns_field' : fields['similar_image_vector'],
                'param' : {
                    'metric_type' : 'IP',
                    'params' : {'nprobe': 92}
                },
                'limit' : top_k
            }
            reqs.append(AnnSearchRequest(**param))

        if vectors['ocr_embedding'] is not None:
            p.append(priorities['ocr_embedding'])
            param = {
                'data' : vectors['ocr_embedding'],
                'anns_field' : fields['ocr_embedding'],
                'param' : {
                    'metric_type' : 'IP',
                    'params' : {'nprobe': 92}
                },
                'limit' : top_k
            }
            reqs.append(AnnSearchRequest(**param))

        if vectors['audio_embedding'] is not None:
            p.append(priorities['audio_embedding'])
            param = {
                'data' : vectors['audio_embedding'],
                'anns_field' : fields['audio_embedding'],
                'param' : {
                    'metric_type' : 'IP',
                    'params' : {'nprobe': 92}
                },
                'limit' : top_k
            }
            reqs.append(AnnSearchRequest(**param))

        rerank = WeightedRanker(*p)
        self.collection.load()
        response = self.collection.hybrid_search(
            reqs,
            rerank,
            limit=top_k,
            output_fields=['idx']
        )

        print(response[0].distances)

        resuit = []
        for res in response[0]:
            resuit.append(res.entity.get('idx'))

        return resuit

class MilvusSingleton:
    _instance = None

    def __new__(cls, host='milvus-standalone', port='19530', collection_name='search_collection'):
        if cls._instance is None:
            cls._instance = MilvusSearch(host, port, collection_name)
        return cls._instance