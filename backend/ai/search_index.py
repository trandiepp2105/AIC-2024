from ai.scripts.milvus_seach import MilvusSearch
from ai.scripts.embedding_model import CLIPSingleton
from ai.configs import *
from ai.scripts.utils import class2Id
import numpy as np

embedding_model = CLIPSingleton()
search = MilvusSearch(collection_name='search_collection')

def image_search(image, top_k=500):
    embedding = embedding_model.get_image_embedding(image).cpu().numpy().tolist()
    res = search.search([embedding], top_k)
    return res   

def search_text(text, top_k=500):
    text_embedding = embedding_model.get_text_embedding(text).cpu().numpy().tolist()
    res = search.search([text_embedding], top_k)
    return res

def search_index(search_input, top_k=500):
    description_embedding = embedding_model.get_text_embedding(search_input['raw_text']['value']).cpu().numpy().astype(np.float32) if search_input['raw_text']['value'] else None
    objects_vector = {class2Id[obj['class_name']]: float(obj['quantity']) for obj in search_input['objects']['value']} if search_input['objects']['value'] else {}
    objects_vector[100] = 1.0
    image_embedding = embedding_model.get_image_embedding(search_input['image']['value']).cpu().numpy() if search_input['image']['value'] else None
    vectors = {
        'description_vector': [description_embedding] if description_embedding is not None else None,
        'objects': [objects_vector] if objects_vector is not None else None,
        'time': None,
        'similar_image_vector': None,
        'ocr_embedding': None,
        'audio_embedding': None,
    }
    fields = {
        'description_vector': 'frame_embedding',
        'objects': 'object_detection',
        'time': 'time_vector',
        'similar_image_vector': 'frame_embedding',
        'ocr_embedding': 'ocr_embedding',
        'audio_embedding': 'audio_embedding'
    }
    total_priority = sum([v['priority'] for k,v in search_input.items()])
    priorities = {
        'description_vector': search_input['raw_text']['priority']/total_priority if vectors['description_vector'] is not None else 0,
        'objects': search_input['objects']['priority']/total_priority if vectors['objects'] is not None else 0,
        'time': search_input['time']['priority']/total_priority if vectors['time'] is not None else 0,
        'similar_image_vector': search_input['image']['priority']/total_priority if vectors['similar_image_vector'] is not None else 0,
        # 'ocr_embedding': search_input['ocr']['priority']/total_priority if vectors['ocr_embedding'] is not None else 0,
        # 'audio_embedding': search_input['audio']['priority']/total_priority if vectors['audio_embedding'] is not None else 0,
    }
    res = search.search_hybrid(vectors, fields, priorities, top_k)
    return res
