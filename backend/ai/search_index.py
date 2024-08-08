from ai.scripts.milvus_seach import MilvusSearch
from ai.scripts.embedding_model import CLIPSingleton
from ai.configs import *
from ai.scripts.utils import class2Id
from ai.scripts.vietnamese_embedding import VieEmbedding_Singleton
import numpy as np
from PIL import Image
from io import BytesIO
import base64

print("RUN ai search_index")    
vie_embedding = VieEmbedding_Singleton()
print('Load vietnamese embedding model done')
embedding_model = CLIPSingleton(model_name='ViT-L-14-quickgelu', pretrained='dfn2b', device='cuda')
print('Load embedding model done')
search = MilvusSearch(collection_name='search_collection')
print('Load search done')

def image_search(image, top_k=500):
    embedding = embedding_model.get_image_embedding(image).cpu().numpy().tolist()
    res = search.search([embedding], top_k)
    return res   

def search_text(text, top_k=500):
    text_embedding = embedding_model.get_text_embedding(text).cpu().numpy().tolist()
    res = search.search([text_embedding], top_k)
    return res

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

    vectors = {
        'description_vector': [description_embedding] if description_embedding is not None else None,
        'objects': [objects_vector] if objects_vector is not None else None,
        'time': None,
        'similar_image_vector': [image_embedding] if image_embedding is not None else None,
        'ocr_embedding': [ocr_embedding] if ocr_embedding is not None else None,
        'audio_embedding': None,
        'next_frame_embedding': [next_frame_embedding] if next_frame_embedding is not None else None
    }
    fields = {
        'description_vector': 'frame_embedding',
        'objects': 'object_detection',
        'time': 'time_vector',
        'similar_image_vector': 'frame_embedding',
        'ocr_embedding': 'ocr_embedding',
        'audio_embedding': 'audio_embedding',
        'next_frame_embedding': 'frame_embedding'
    }
    priorities = {
        'description_vector': search_input['raw_text']['priority'],
        'objects': search_input['objects']['priority'],
        'time': search_input['time']['priority'],
        'similar_image_vector': search_input['image']['priority'],
        'ocr_embedding': search_input['ocr']['priority'],
        'audio_embedding': search_input['speech']['priority'],
        'next_frame_embedding': search_input['next_frame_query']['priority']
    }
    res = search.search(vectors, fields, priorities, top_k)
    return res
