from pymilvus import connections, Collection, AnnSearchRequest, WeightedRanker, FieldSchema, CollectionSchema, DataType, utility
import json
from time import sleep

class MilvusSearch:
    def __init__(self, host='milvus-standalone', port='19530', collection_name='search_collection', collection_name2='search_collection2'):
        self.client = connections.connect('default', host=host, port=port)
        self.collection = Collection(collection_name)

    def create_collection2(self):
        index_params = {
            "metric_type": "IP",
            "index_type": "IVF_FLAT",
            "params": {"nlist": 1024}
        }

        object_detection_index_params = {
            "metric_type": "L2",
            "index_type": "IVF_FLAT",
            "params": {"nlist": 1024}
        }

        ocr_embedding_index_params = {
            "metric_type": "IP",
            "index_type": "IVF_FLAT",
            "params": {"nlist": 1024}
        }

        fields2 = [
            FieldSchema(name="idx", dtype=DataType.INT64, is_primary=True),
            FieldSchema(name="frame_embedding", dtype=DataType.FLOAT_VECTOR, dim=768),
            FieldSchema(name="object_detection", dtype=DataType.FLOAT_VECTOR, dim=80),
            FieldSchema(name="ocr_embedding", dtype=DataType.FLOAT_VECTOR, dim=768),
            FieldSchema(name="before_frame_embedding", dtype=DataType.FLOAT_VECTOR, dim=768),
        ]

        schema2 = CollectionSchema(fields=fields2)
        collection2 = Collection("seacolletion2", schema=schema2)

        collection2.create_index(field_name="frame_embedding", index_params=index_params)
        collection2.create_index(field_name="object_detection", index_params=object_detection_index_params)
        collection2.create_index(field_name="ocr_embedding", index_params=ocr_embedding_index_params)
        collection2.create_index(field_name="before_frame_embedding", index_params=index_params)

        return collection2

    def search(self, vectors, fields, priorities, top_k=100, search1_limit=500):
        features = ['description_vector', 'objects', 'time', 'similar_image_vector', 'ocr_embedding', 'audio_embedding']
        search_params = {
            'description_vector': {
                'data' : vectors['description_vector'],
                'anns_field' : fields['description_vector'],
                'param' : {
                    'metric_type' : 'IP',
                    'params' : {'nprobe': 92}
                },
            },
            'objects': {
                'data' : vectors['objects'],
                'anns_field' : fields['objects'],
                'param' : {
                    'metric_type' : 'L2',
                    'params' : {'nprobe': 92}
                },
            },
            'time': {
                'data' : vectors['time'],
                'anns_field' : fields['time'],
                'param' : {
                    'metric_type' : 'L2',
                    'params' : {'nprobe': 92}
                },
            },
            'similar_image_vector': {
                'data' : vectors['similar_image_vector'],
                'anns_field' : fields['similar_image_vector'],
                'param' : {
                    'metric_type' : 'IP',
                    'params' : {'nprobe': 92}
                },
            },
            'ocr_embedding': {
                'data' : vectors['ocr_embedding'],
                'anns_field' : fields['ocr_embedding'],
                'param' : {
                    'metric_type' : 'IP',
                    'params' : {'nprobe': 92}
                },
            },
            'audio_embedding': {
                'data' : vectors['audio_embedding'],
                'anns_field' : fields['audio_embedding'],
                'param' : {
                    'metric_type' : 'IP',
                    'params' : {'nprobe': 92}
                },
            },
            'next_frame_embedding': {
                'data' : vectors['next_frame_embedding'],
                'anns_field' : fields['next_frame_embedding'],
                'param' : {
                    'metric_type' : 'IP',
                    'params' : {'nprobe': 92}
                },
            }
        }
        fisrt_search = None
        max_priority = 0
        for feature in features:
            if priorities[feature] > max_priority and vectors[feature] is not None:
                max_priority = priorities[feature]
                fisrt_search = feature

        self.collection.load()
        print('search1')
        response = self.collection.search(**search_params[fisrt_search], limit=search1_limit, output_fields=['idx', 'video_id', 'frame_id', 'frame_embedding'])
        print('search1 done')
        search_2_data = []
        for res in response[0]:
            data = self.collection.query(
                expr = f'video_id == {res.entity.get("video_id")} && frame_id < {res.entity.get("frame_id") + 100} && frame_id > {res.entity.get("frame_id")}',
                output_fields=['idx', 'frame_embedding', 'object_detection', 'ocr_embedding']
            )
            insert_data = [{**d, 'before_frame_embedding': res.entity.get('frame_embedding')} for d in data]

            search_2_data.extend(insert_data)

        self.collection.release()
        print('search2')
        
        print('create collection2')
        self.collection2 = self.create_collection2()
        print('load collection2')
        print(search_2_data)
        print(self.collection2)
        self.collection2.load()
        self.collection2.insert(search_2_data)  
        self.collection2.load()
        sleep(5)
        search_params2 = {
            'description_vector': {
                'data' : vectors['description_vector'],
                'anns_field' : 'before_frame_embedding',
                'param' : {
                    'metric_type' : 'IP',
                    'params' : {'nprobe': 92}
                },
                'limit' : top_k
            },
            'objects': {
                'data' : vectors['objects'],
                'anns_field' : fields['objects'],
                'param' : {
                    'metric_type' : 'L2',
                    'params' : {'nprobe': 92}
                },
                'limit' : top_k
            },
            'time': {
                'data' : vectors['time'],
                'anns_field' : fields['time'],
                'param' : {
                    'metric_type' : 'L2',
                    'params' : {'nprobe': 92}
                },
                'limit' : top_k
            },
            'similar_image_vector': {
                'data' : vectors['similar_image_vector'],
                'anns_field' : fields['similar_image_vector'],
                'param' : {
                    'metric_type' : 'IP',
                    'params' : {'nprobe': 92}
                },
                'limit' : top_k
            },
            'ocr_embedding': {
                'data' : vectors['ocr_embedding'],
                'anns_field' : fields['ocr_embedding'],
                'param' : {
                    'metric_type' : 'IP',
                    'params' : {'nprobe': 92}
                },
                'limit' : top_k
            },
            'audio_embedding': {
                'data' : vectors['audio_embedding'],
                'anns_field' : fields['audio_embedding'],
                'param' : {
                    'metric_type' : 'IP',
                    'params' : {'nprobe': 92}
                },
                'limit' : top_k
            },
            'next_frame_embedding': {
                'data' : vectors['next_frame_embedding'],
                'anns_field' : fields['next_frame_embedding'],
                'param' : {
                    'metric_type' : 'IP',
                    'params' : {'nprobe': 92}
                },
                'limit' : top_k
            }
        }
        p = []
        reqs = []

        for feature in features:
            if vectors[feature] is not None:
                p.append(priorities[feature])
                reqs.append(AnnSearchRequest(**search_params2[feature]))

        p = [i/sum(p) for i in p]
        rerank = WeightedRanker(*p)
        self.collection2.load()

        response = self.collection2.hybrid_search(
            reqs,
            rerank,
            limit=top_k,
            output_fields=['idx']
        )

        self.collection2.drop()

        resuit = []
        for res in response[0]:
            resuit.append(res.entity.get('idx'))

        return resuit


    def search_hybrid(self, vectors, fields, priorities, top_k=100):
        features = ['description_vector', 'objects', 'time', 'similar_image_vector', 'ocr_embedding', 'audio_embedding']
        search_params = {
            'description_vector': {
                'data' : vectors['description_vector'],
                'anns_field' : fields['description_vector'],
                'param' : {
                    'metric_type' : 'IP',
                    'params' : {'nprobe': 92}
                },
                'limit' : top_k
            },
            'objects': {
                'data' : vectors['objects'],
                'anns_field' : fields['objects'],
                'param' : {
                    'metric_type' : 'L2',
                    'params' : {'nprobe': 92}
                },
                'limit' : top_k
            },
            'time': {
                'data' : vectors['time'],
                'anns_field' : fields['time'],
                'param' : {
                    'metric_type' : 'L2',
                    'params' : {'nprobe': 92}
                },
                'limit' : top_k
            },
            'similar_image_vector': {
                'data' : vectors['similar_image_vector'],
                'anns_field' : fields['similar_image_vector'],
                'param' : {
                    'metric_type' : 'IP',
                    'params' : {'nprobe': 92}
                },
                'limit' : top_k
            },
            'ocr_embedding': {
                'data' : vectors['ocr_embedding'],
                'anns_field' : fields['ocr_embedding'],
                'param' : {
                    'metric_type' : 'IP',
                    'params' : {'nprobe': 92}
                },
                'limit' : top_k
            },
            'audio_embedding': {
                'data' : vectors['audio_embedding'],
                'anns_field' : fields['audio_embedding'],
                'param' : {
                    'metric_type' : 'IP',
                    'params' : {'nprobe': 92}
                },
                'limit' : top_k
            },
            'next_frame_embedding': {
                'data' : vectors['next_frame_embedding'],
                'anns_field' : fields['next_frame_embedding'],
                'param' : {
                    'metric_type' : 'IP',
                    'params' : {'nprobe': 92}
                },
                'limit' : top_k
            }
        }
        
        p = []
        reqs = []

        for feature in features:
            if vectors[feature] is not None:
                p.append(priorities[feature])
                reqs.append(AnnSearchRequest(**search_params[feature]))

        p = [i/sum(p) for i in p]
        rerank = WeightedRanker(*p)
        self.collection.load()
        response = self.collection.hybrid_search(
            reqs,
            rerank,
            limit=top_k,
            output_fields=['idx']
        )

        resuit = []
        for res in response[0]:
            resuit.append(res.entity.get('idx'))

        return resuit

    # def search_hybrid(self, vectors, fields, priorities, top_k=100):
    #     features = ['description_vector', 'objects', 'time', 'similar_image_vector', 'ocr_embedding', 'audio_embedding']
    #     print(priorities)
    #     p = []
    #     reqs = []
    #     if vectors['description_vector'] is not None:
    #         p.append(priorities['description_vector'])
    #         param = {
    #             'data' : vectors['description_vector'],
    #             'anns_field' : fields['description_vector'],
    #             'param' : {
    #                 'metric_type' : 'IP',
    #                 'params' : {'nprobe': 92}
    #             },
    #             'limit' : top_k
    #         }
    #         reqs.append(AnnSearchRequest(**param))

    #     if vectors['objects'] is not None:
    #         p.append(priorities['objects'])
    #         param = {
    #             'data' : vectors['objects'],
    #             'anns_field' : fields['objects'],
    #             'param' : {
    #                 'metric_type' : 'L2',
    #                 'params' : {'nprobe': 92}
    #             },
    #             'limit' : top_k
    #         }
    #         reqs.append(AnnSearchRequest(**param))

    #     if vectors['time'] is not None:
    #         p.append(priorities['time'])
    #         param = {
    #             'data' : vectors['time'],
    #             'anns_field' : fields['time'],
    #             'param' : {
    #                 'metric_type' : 'L2',
    #                 'params' : {'nprobe': 92}
    #             },
    #             'limit' : top_k
    #         }
    #         reqs.append(AnnSearchRequest(**param))

    #     if vectors['similar_image_vector'] is not None:
    #         p.append(priorities['similar_image_vector'])
    #         param = {
    #             'data' : vectors['similar_image_vector'],
    #             'anns_field' : fields['similar_image_vector'],
    #             'param' : {
    #                 'metric_type' : 'IP',
    #                 'params' : {'nprobe': 92}
    #             },
    #             'limit' : top_k
    #         }
    #         reqs.append(AnnSearchRequest(**param))

    #     if vectors['ocr_embedding'] is not None:
    #         p.append(priorities['ocr_embedding'])
    #         param = {
    #             'data' : vectors['ocr_embedding'],
    #             'anns_field' : fields['ocr_embedding'],
    #             'param' : {
    #                 'metric_type' : 'IP',
    #                 'params' : {'nprobe': 92}
    #             },
    #             'limit' : top_k
    #         }
    #         reqs.append(AnnSearchRequest(**param))

    #     if vectors['audio_embedding'] is not None:
    #         p.append(priorities['audio_embedding'])
    #         param = {
    #             'data' : vectors['audio_embedding'],
    #             'anns_field' : fields['audio_embedding'],
    #             'param' : {
    #                 'metric_type' : 'IP',
    #                 'params' : {'nprobe': 92}
    #             },
    #             'limit' : top_k
    #         }
    #         reqs.append(AnnSearchRequest(**param))
    #     p = [i/sum(p) for i in p]
    #     print(p)
    #     rerank = WeightedRanker(*p)
    #     self.collection.load()
    #     response = self.collection.hybrid_search(
    #         reqs,
    #         rerank,
    #         limit=top_k,
    #         output_fields=['idx']
    #     )

    #     print(response[0].distances)

    #     resuit = []
    #     for res in response[0]:
    #         resuit.append(res.entity.get('idx'))

    #     return resuit

class MilvusSingleton:
    _instance = None

    def __new__(cls, host='milvus-standalone', port='19530', collection_name='search_collection'):
        if cls._instance is None:
            cls._instance = MilvusSearch(host, port, collection_name)
        return cls._instance