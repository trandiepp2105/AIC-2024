from scripts.models import *
import os
import json
import numpy as np
import torch

device = 'cuda' if torch.cuda.is_available() else 'cpu'
embedding_model = VieEmbedding_Singleton(device=device)

def embedding_batch(data, batch_size):
    embeddings = []
    texts = []
    keys = []
    for key, value in data.items():
        texts.append(value)
        keys.append(key)
        if len(texts) == batch_size:
            embeddings.extend(embedding_model.get_embeddings(texts))
            texts = []
    if len(texts) > 0:
        embeddings.extend(embedding_model.get_embeddings(texts))
    return keys, embeddings


def embedding_ocr_folder(ocr_folder, output_folder, batch_size=32):
    for file in os.listdir(ocr_folder):
        if file.endswith('.json'):
            video_name = file.split('.')[0]
            embedding_folder = os.path.join(output_folder, video_name)
            os.makedirs(embedding_folder, exist_ok=True)
            with open(os.path.join(ocr_folder, file), 'r') as f:
                data = json.load(f)

                keys, embeddings = embedding_batch(data, batch_size)

                for key, embedding in zip(keys, embeddings):
                    embedding_file = os.path.join(embedding_folder, key + '.npy')
                    np.save(embedding_file, embedding)

            print(f"Extracted embeddings of {video_name}")
                    
