from scripts.utils import wfile
import numpy as np
from scripts.models import *
import json
import os

def devide_batch(data, batch_size):
    batchs = []
    batch = []
    for i in range(len(data)):
        frame_num = int(data[i][0])
        batch.append((frame_num, data[i][1]))
        if len(batch) == batch_size:
            batchs.append(batch)
            batch = []
    if len(batch) > 0:
        batchs.append(batch)
    return batchs

def embedding_batch(batchs, extract_model):
    images = [b[1] for b in batchs]
    embeddings = extract_model.get_texts_embedding(images).cpu().numpy()    
    res = [(batchs[i][0], embeddings[i]) for i in range(len(batchs))]
    return res

def embedding_description(description_path, embedding_folder, embedding_model, batch_size=32):
    with open(description_path, 'r') as f:
        description = json.load(f)
    list_text = [(key, value) for key, value in description.items()]
    
    batchs = devide_batch(list_text, batch_size)
    for batch in batchs:
        res = embedding_batch(batch, embedding_model)
        for r in res:
            embedding_path = os.path.join(embedding_folder, str(r[0]) + '.npy')
            np.save(embedding_path, r[1].astype(np.float32))


def embedding_description_folder(all_keyframes_folder, description_folder, extract_agrs, batch_size=32):
    print(extract_agrs)
    embedding_model = CLIPSingleton(*extract_agrs)

    list_description = wfile(all_keyframes_folder, endswith='.json')

    for description_path in list_description:
        video_name = description_path.split('/')[-1].split('.')[0]
        embedding_folder = os.path.join(description_folder, video_name)
        if not os.path.exists(embedding_folder):
            os.makedirs(embedding_folder)
        embedding_description(description_path, embedding_folder, embedding_model, batch_size=batch_size)
        print(f"Embedding {video_name} done")
