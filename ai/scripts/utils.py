from PIL import Image
from torchvision import transforms
# import faiss
from tqdm import tqdm
import numpy as np
import os
import pandas as pd
import pickle

def wfile(root, endswith='.mp4'):
    paths = []
    for dirpath, dirnames, filenames in os.walk(root):
        for filename in filenames:
            if filename.endswith(endswith):
                paths.append(os.path.join(dirpath, filename))
    sorted(paths)
    return paths

def img_preprocess(img_path, transform=transforms.Compose([transforms.Resize((1024, 1024))]), expand_dims=False):
    img = Image.open(img_path)
    img = transform(img)
    if expand_dims:
        img = img.unsqueeze(0)
    return img

# def path2Embedding(img_path, embedding_model):
#     img = img_preprocess(img_path)
#     img_embedding = embedding_model.get_image_embedding(img).detach().numpy()
#     return img_embedding

# def create_index_frame(id2img, embedding_model, embedding_dim=768, _index = faiss.IndexFlatIP):
#     frame_index = _index(embedding_dim)

#     for img_id, img_path in tqdm(id2img.items()):
#         try:
#             img = img_preprocess(img_path)
#             img_embedding = embedding_model.get_image_embedding(img).detach().cpu().numpy()
#             img_embedding = img_embedding / np.linalg.norm(img_embedding) # Normalize
#             frame_index.add(img_embedding)
#         except Exception as e:
#             print(f"Error processing image {img_path}: {e}")
#     return frame_index

# def dictionary_frame(path_to_frames):
#     id2img = {}
#     paths = wfile(path_to_frames, '.jpg')
#     for id, path in enumerate(paths):
#         id2img[id] = path

#     return id2img

# def csv_frames(path_to_frames, path_to_csv):
#     data = []

#     idx = 0

#     for video_name in os.listdir(path_to_frames):
#         video_frames_folder = os.path.join(path_to_frames, video_name)
#         if os.path.isdir(video_frames_folder):
#             paths = wfile(video_frames_folder, '.jpg')
#             for path in paths:
#                 frame_number = int(os.path.splitext(os.path.basename(path))[0])
#                 objects_path = ""
#                 data.append({
#                     'path': path,
#                     'frame_number': frame_number,
#                     'video_id': video_name,
#                     'objects_path': objects_path,
#                     'id': idx
#                 })
#                 idx += 1

#     df = pd.DataFrame(data, columns=['path', 'frame_number', 'video_id', 'objects_path', 'id'])
#     df.to_csv(path_to_csv, index=False)
#     return df

# def embedding_frame(path_to_csv, embedding_model, pickle_path):
#     df = pd.read_csv(path_to_csv)
#     embeddings = []

#     for i, row in tqdm(df.iterrows()):
#         img = img_preprocess(row['path'])
#         img_embedding = embedding_model.get_image_embedding(img).detach().cpu().numpy()
#         img_embedding = img_embedding / np.linalg.norm(img_embedding) # Normalize
#         embeddings.append({'id': row['id'], 'embedding': img_embedding.tolist()})

#     with open(pickle_path, 'wb') as f:
#         pickle.dump(embeddings, f)

#     return embeddings