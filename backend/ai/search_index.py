from ai.scripts.milvus_seach import MilvusSingleton, MilvusSearch
from ai.scripts.embedding_model import CLIPSingleton, CLIP_Embedding
from ai.configs import *

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
    description_embedding = embedding_model.get_text_embedding(search_input['text']['value']).cpu().numpy()
    objects_vector = {int(k):v for k,v in search_input['objects']['value'].items()}
    image_embedding = embedding_model.get_image_embedding(search_input['similar_image']['value']).cpu().numpy()
    objects_vector[100] = 1.0
    vectors = {
        'description_vector': [description_embedding],
        'objects': [objects_vector],
        'time': None,
        'similar_image_vector': [image_embedding],
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
        'description_vector': search_input['text']['priority']/total_priority,
        'objects': search_input['objects']['priority']/total_priority,
        'time': search_input['time']['priority']/total_priority,
        'similar_image_vector': search_input['similar_image']['priority']/total_priority,
        'ocr_embedding': search_input['ocr']['priority']/total_priority,
        'audio_embedding': search_input['audio']['priority']/total_priority
    }
    res = search.search_hybrid(vectors, fields, priorities, top_k)
    return res
