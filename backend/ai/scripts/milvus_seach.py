from pymilvus import connections, Collection, AnnSearchRequest, WeightedRanker, FieldSchema, CollectionSchema, DataType, utility
import json
from time import sleep

class MilvusSearch:
    def __init__(self, host='milvus-standalone', port='19530', collection_name='search_collection'):
        self.client = connections.connect('default', host=host, port=port)
        self.collection = Collection(collection_name)
        self.collection.load()
    
    def hybrid_milvus_nextframe(self, reqs, p, top_k=100):
        reqs = [AnnSearchRequest(**req) for req in reqs]
        rerank = WeightedRanker(*p)
        response = self.collection2.hybrid_search(
            reqs,
            rerank,
            limit=top_k,
            output_fields=['video', 'frame']
        )
        resuit = []
        for res in response[0]:
            enti = (res.entity.get('video'), res.entity.get('frame'))
            if enti not in resuit:
                resuit.append(enti)
        return resuit
    
    def hybrid_milvus(self, reqs, p, top_k=100):
        reqs = [AnnSearchRequest(**req) for req in reqs]
        rerank = WeightedRanker(*p)
        response = self.collection.hybrid_search(
            reqs,
            rerank,
            limit=top_k,
            output_fields=['video', 'frame']
        )
        resuit = []
        for res in response[0]:
            enti = (res.entity.get('video'), res.entity.get('frame'))
            if enti not in resuit:
                resuit.append(enti)
        return resuit
    
    def filter_objects(self, objects, rangez=2):
        list_objects = []

        for idx, obj in enumerate(objects):
            if obj != 0:
                list_objects.append(f'(object_detection[{idx}] >= {max(1, obj - rangez)} and object_detection[{idx}] <= {obj + rangez})')

        return ' and '.join(list_objects) if list_objects else ''
    
    def filter_time(self, time, rangez=2):
        return f'(time >= {time - rangez} and time <= {time + rangez})'
    
    def filter_audio(self, audio):
        return f'(audio_embedding like "%{audio}%")'

    def search_milvus(self, vectors, properties, filterz, top_k=100):
        features = ['description_vector', 'similar_image_vector', 'next_frame_vector']
        features_filter = ['objects', 'time', 'audio_embedding']
        search_params = {
            'description_vector': {
                'data' : vectors['description_vector'],
                'anns_field' : 'frame_embedding',
                'param' : {
                    'metric_type' : 'IP',
                    'params' : {'nprobe': 92}
                },
                'limit' : top_k
            },
            'similar_image_vector': {
                'data' : vectors['similar_image_vector'],
                'anns_field' : 'frame_embedding',
                'param' : {
                    'metric_type' : 'IP',
                    'params' : {'nprobe': 92}
                },
                'limit' : top_k
            },
            'next_frame_vector': {
                'data' : vectors['next_frame_vector'],
                'anns_field' : 'next_frame_embedding',
                'param' : {
                    'metric_type' : 'IP',
                    'params' : {'nprobe': 92}
                },
                'limit' : top_k
            }
        }

        list_reqs = []
        for feature in features:
            if vectors[feature] is not None:
                list_reqs.append(search_params[feature])

        if len(list_reqs) > 1:
            p = [properties[feature] for feature in features if vectors[feature] is not None]
            p = [i/sum(p) for i in p]
            if vectors['next_frame_vector'] is not None:
                return self.hybrid_milvus_nextframe(list_reqs, p, top_k)
            else:
                return self.hybrid_milvus(list_reqs, p, top_k)
        
        filter_query = []   
        for feature in features_filter:
            if filterz[feature] is not None:
                if feature == 'objects':
                    filter_query.append(self.filter_objects(filterz['objects']))
                elif feature == 'time':
                    filter_query.append(self.filter_time(filterz['time']))
                elif feature == 'audio_embedding':
                    filter_query.append(self.filter_audio(filterz['audio_embedding']))

        filter_query = ' and '.join(filter_query) if filter_query else ''

        if len(list_reqs) == 1:
            if filter_query:
                response = self.collection.search(
                    **list_reqs[0],
                    expr = filter_query,
                    output_fields=['video', 'frame']
                )

                resuit = []
                for res in response[0]:
                    enti = (res.entity.get('video'), res.entity.get('frame'))
                    if enti not in resuit:
                        resuit.append(enti)
                return resuit
            else:
                response = self.collection.search(
                    **list_reqs[0],
                    output_fields=['video', 'frame']
                )

                resuit = []
                for res in response[0]:
                    enti = (res.entity.get('video'), res.entity.get('frame'))
                    if enti not in resuit:
                        resuit.append(enti)
                return resuit
        else:
            response = self.collection.query(
                expr = filter_query,
                output_fields=['video', 'frame'],
                limit = top_k
            )

            resuit = []
            for res in response:
                enti = (res['video'], res['frame'])
                if enti not in resuit:
                    resuit.append(enti)
            return resuit
        
        return []
    
    def new_search(self, querys, num_features, feature_idx, top_k = 100, time_distance = 60, num_of_frames = 5000):
        search_param = {
                'data' : querys,
                'param' : {
                    'metric_type' : 'IP',
                    'params' : {'nprobe': 92}
                },
                'limit' : num_of_frames,
                'output_fields' : ['video', 'frame', 'second'],
                'anns_field' : 'frame_embedding'
            }

        full_resuit = []

        response = self.collection.search(
            **search_param,
        )

        for idx, resp in enumerate(response):
            result = []
            for res in resp:
                enti = (res.entity.get('video'), res.entity.get('frame'), res.entity.get('second'))
                if enti not in result:
                    result.append(enti)
            distances = resp.distances
            distances = [distances[i] / max(distances) for i in range(len(distances))]
            querys_distance = [[0 for _ in range(len(distances))] if i != feature_idx + idx else distances for i in range(num_features)]
            resuit = zip(result, list(zip(*querys_distance)))
            full_resuit.extend(resuit)

        # full_resuit = []
        # for idx in range(len(querys)):
        #     full_resuit = full_resuit + querys_results[idx]

        full_resuit.sort(key=lambda x: (x[0][0], x[0][1]))

        rerank_results = []
        for idx in range(len(full_resuit)):
            if idx == 0 or full_resuit[idx][0][0] != full_resuit[idx-1][0][0] or full_resuit[idx][0][2] - full_resuit[idx-1][0][2] > time_distance:
                rerank_results.append([])
            rerank_results[-1].append(full_resuit[idx])


        for idx in range(len(rerank_results)):
            rerank_results[idx].sort(lambda x: (-x[1][0]))

            for i in range(1, len(rerank_results[idx])):
                rerank_results[idx][i] = (rerank_results[idx][i][0], [max(rerank_results[idx][i][1][i], rerank_results[idx][i-1][1][k-1] + rerank_results[-1][-1][1][k] if k > 0 else rerank_results[-1][-1][1][k]) for k in range(num_features)])

        rerank_results.sort(key=lambda x: x[-1][1][-1], reverse=True)
        final_results = [[(result[idx][0][0], result[idx][0][1]) for idx in range(len(result)) if idx < 2 or sum(result[idx][1]) > sum(result[idx-1][1])] for result in rerank_results[:top_k]]

        return final_results
    
    def gen_filter(self, prev_results, time_distance):
        filter_query = []
        for result in prev_results:
            filter_query.append(f'(video == "{result[0][0]}" and second >= {result[0][2]}) and second <= {result[0][2] + time_distance})')
        return ' or '.join(filter_query) if filter_query else ''

    # def temporal_search(self, querys, top_k=100, time_distance=45, num_of_frames = 3000):
    #     total_results = []

    #     search_param = {
    #             'param' : {
    #                 'metric_type' : 'IP',
    #                 'params' : {'nprobe': 92}
    #             },
    #             'limit' : num_of_frames,
    #             'output_fields' : ['video', 'frame', 'second']
    #         }

    #     res1 = self.collection.search(
    #         **search_param,
    #         data=querys[0]['vector'],
    #     )

    #     prev_results = [[(res.entity.get('video'), res.entity.get('frame'), res.entity.get('second')), [res.distance if i == 0 else 0 for i in range(len(querys))] ] for res in res1[0]]
    #     total_results = total_results + prev_results

    #     for idx in range(1, len(querys)):
    #         filter_query = self.gen_filter(prev_results, time_distance)
    #         res2 = self.collection.search(
    #             **search_param,
    #             data=querys[idx]['vector'],
    #             expr=filter_query
    #         )

    #         prev_results = [[(res.entity.get('video'), res.entity.get('frame'), res.entity.get('second')), res.distance if i == 0 else 0 for i in range(len(querys))] for res in res2[0]]
    #         total_results = total_results + prev_results

    #     total_results.sort(key=lambda x: (x[0][0], x[0][1]))

    #     rerank_results = []
    #     for idx in range(len(total_results)):
    #         if idx == 0 or total_results[idx][0][0] != total_results[idx-1][0][0] or total_results[idx][0][2] - total_results[idx-1][0][2] > time_distance:
    #             rerank_results.append([])
    #         rerank_results[-1].append(total_results[idx])
    #         if len(rerank_results[-1]) > 1:
    #             rerank_results[-1][-1] = (rerank_results[-1][-1][0], [max(rerank_results[-1][-1][1][i], rerank_results[-1][-2][1][i]) for i in range(len(rerank_results[-1][-1][1]))])

    #     rerank_results.sort(key=lambda x: sum(x[-1][1]), reverse=True)

    #     final_results = [[(x[0][0], x[0][1]) for x in result] for result in rerank_results[:top_k]]

    #     return final_results
        
class MilvusSingleton:
    _instance = None

    def __new__(cls, host='milvus-standalone', port='19530', collection_name='search_collection'):
        if cls._instance is None:
            cls._instance = MilvusSearch(host, port, collection_name)
        return cls._instance