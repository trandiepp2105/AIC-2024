from ai.scripts.milvus_seach import MilvusSingleton
from ai.scripts.embedding_model import CLIPSingleton, CLIP4CLIPSingleton
from ai.configs import *
from ai.scripts.utils import class2Id
import numpy as np
from PIL import Image
from io import BytesIO
import base64
import logging
from ai.configs import *
import torch
   
logging.info('Load search index')
device = 'cuda' if torch.cuda.is_available() else 'cpu'
# clip4clip_model = CLIP4CLIPSingleton(device = device)
logging.info('Load clip4clip model done')
# embedding_model = CLIPSingleton(model_name='ViT-L-14-quickgelu', pretrained='dfn2b', device='cuda')
embedding_model = CLIPSingleton(model_name=MODELS_CLIP_NAME, pretrained=PRETRAINED_CLIP, device=device, tokenizers=TOKENIZER_CLIP)
logging.info('Load embedding model done')
search = MilvusSingleton(collection_name='vector_db')
logging.info('Load search done')

def search_index(search_input, top_k=500):
    for k,v in search_input.items():
        if v['value'] is None:
            search_input[k]['priority'] = 0
    description_embedding = embedding_model.get_text_embedding(search_input['raw_text']['value']).cpu().numpy().astype(np.float32) if search_input['raw_text']['value'] else None
    objects_vector = [0 for i in range(80)]
    if search_input['objects']['value']:
        for obj in search_input['objects']['value']:    
            objects_vector[class2Id[obj['class_name']]] = obj['quantity']
    else:
        objects_vector = None
    image_embedding = None
    if search_input['image']['value']:
        image_data = base64.b64decode(search_input['image']['value'].split(",")[1])
        image = Image.open(BytesIO(image_data))
        image_embedding = embedding_model.get_image_embedding(image).cpu().numpy().astype(np.float32)
    ocr_embedding = None
    if search_input['ocr']['value']:
        ocr_embedding = vie_embedding.get_embedding(search_input['ocr']['value'])
    next_frame_embedding = None
    if search_input['next_frame_query']['value']:
        next_frame_embedding = embedding_model.get_text_embedding(search_input['next_frame_query']['value']).cpu().numpy().astype(np.float32)
    audio = None
    if search_input['speech']['value']:
        audio = search_input['speech']['value']

    vectors = {
        'description_vector': [description_embedding] if description_embedding is not None else None,
        'similar_image_vector': [image_embedding] if image_embedding is not None else None,
        'next_frame_vector': [next_frame_embedding] if next_frame_embedding is not None else None
    }
    filterz = {
        'objects': objects_vector if objects_vector is not None else None,
        'time': None,
        'ocr_embedding': None,
        'audio_embedding': audio if audio is not None else None
    }
    priorities = {
        'description_vector': search_input['raw_text']['priority'],
        'similar_image_vector': search_input['image']['priority'],
        'next_frame_vector': search_input['next_frame_query']['priority']
    }
    res = search.search_milvus(vectors, priorities, filterz, top_k)
    print(res)
    return res

# def search_tem(search_input, top_k=500):
#     list_query = search_input['raw_text']['value']
#     list_field = ['frame_embedding', 'description_embedding', 'clip4clip']

#     all_query = []

#     for query in list_query:
#         clip_embedding = embedding_model.get_text_embedding(query).cpu().numpy().astype(np.float32)
#         clip4clip_embedding = clip4clip_model.embedding_text(query).astype(np.float32)

#         q = [
#             {
#                 'vector': [clip_embedding],
#                 'field': 'description_embedding',
#             },
#             {
#                 'vector': [clip4clip_embedding],
#                 'field': 'clip4clip',
#             },
#             {
#                 'vector': [clip_embedding],
#                 'field': 'frame_embedding',
#             }
#         ]

#         all_query.append(q)

#     res = search.new_search(all_query, top_k=top_k, properties=(0.1,0.1,0.8))
#     print(res)
#     return res

def search_tem(search_input, top_k=500, ocr = None, speech = None):
    list_query = search_input['raw_text']['value']
    list_field = ['frame_embedding', 'description_embedding', 'clip4clip']

    result = []

    num_feature = len(list_query)
    feature_idx = 0
    if ocr is not None or speech is not None:
        num_feature += 1
        feature_idx = 1

    if ocr is not None:
        result.extend([[ocr[i] if idx == 0 else 0 for idx in range(num_feature)] for i in range(num_feature)])

    if speech is not None:
        result.extend([[speech[i] if idx == 0 else 0 for idx in range(num_feature)] for i in range(num_feature)])

    add_result = []
    if ocr is not None and speech is not None:
        result.sort(lambda x: (x[0][0], x[0][1]))
        for i in range(len(result)):
            if i == 0 or result[i][0] != result[i-1][0] or result[i][1] != result [i-1][1]:
                add_result.append(result[i])
            else:
                add_result[-1][1][0] += result[i][1][0]
    else:
        add_result = result
    
    

    embeddings_query = []

    for query in list_query:
        clip_embedding = embedding_model.get_text_embedding(query).cpu().numpy().astype(np.float32)
        # # clip4clip_embedding = clip4clip_model.embedding_text(query).astype(np.float32)

        # q = {
        #         'vector': [clip_embedding],
        #         'field': 'description_embedding',
        #     }
        embeddings_query.append(clip_embedding)

    res = search.new_search(embeddings_query, top_k=top_k)
    print(res)
    return res