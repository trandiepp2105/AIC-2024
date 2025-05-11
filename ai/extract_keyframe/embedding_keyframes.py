from clip_model import CLIPSingleton
from PIL import Image
from multiprocessing import Process
import os
import numpy as np
import pandas as pd
from configs import *
from timeit import default_timer as timer

def embedding_batch(list_frames, embedding_model):
    images = [Image.open(frame) for _, frame in list_frames]
    embeddings = embedding_model.get_images_embedding(images).detach().cpu().numpy()
    list_embedding = [(list_frames[i][0], embeddings[i]) for i in range(len(list_frames))]
    return list_embedding

def save_embedding(list_embedding, output_folder):
    for frame_number, embedding in list_embedding:
        embedding_path = os.path.join(output_folder, f'{frame_number}.npy')
        np.save(embedding_path, embedding)

def similarity(embedding1, embedding2):
    return np.dot(embedding1, embedding2) / (np.linalg.norm(embedding1) * np.linalg.norm(embedding2))

def get_keyframes(list_embedding, embedding_folder, csv_folder, video_name, threshold=0.9):
    list_keyframes = {
        'frame_number': []
    }

    v_pred = None
    keyframes_embedding = []
    for frame_number, embedding in list_embedding:
        if v_pred is None:
            v_pred = embedding
            list_keyframes['frame_number'].append(frame_number)
            keyframes_embedding.append(frame_number, embedding)
        else:
            sim = similarity(v_pred, embedding)
            if sim < threshold:
                v_pred = embedding
                list_keyframes['frame_number'].append(frame_number)
                keyframes_embedding.append(frame_number, embedding)

    df = pd.DataFrame(list_keyframes)
    df.to_csv(os.path.join(csv_folder, f'{video_name}.csv'), index=False)
    Process(target=save_embedding, args=(keyframes_embedding, embedding_folder)).start()
    print(f'Keyframes {video_name} done')
    

def embedding_frame(list_frames, embedding_folder, csv_folder, embedding_model, video_name, batch_size=32):
    output_folder = os.path.join(embedding_folder, video_name)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    list_embedding = []

    for i in range(0, len(list_frames), batch_size):
        batch = list_frames[i:i+batch_size]
        embeddings = embedding_batch(batch, embedding_model)
        print(f'Embedding {i} done')
        list_embedding.extend(embeddings)

    Process(target=get_keyframes, args=(list_embedding, output_folder, csv_folder, video_name)).start()

    print(f'Emedding {video_name} done')

# def get_list_keyframes(csv_path, keyframes_folder, video_name):
#     df = pd.read_csv(csv_path)
#     key_frames = df['frame_number'].values.tolist()

#     keyframes_f = os.path.join(keyframes_folder, video_name)

#     list_keyframes = []
#     for key_frame in key_frames:
#         key_frame_path = os.path.join(keyframes_f, f'{key_frame}.jpg')
#         list_keyframes.append((key_frame, key_frame_path))

#     return list_keyframes

def get_list_frames(frames_folder, video_name):
    frames_folder = os.path.join(frames_folder, video_name)
    list_frames = [(f.split('.')[0], os.path.join(frames_folder, f)) for f in os.listdir(frames_folder) if f.endswith('.jpg')]
    return list_frames

def create_embedding_and_csv(frames_folder, embedding_folder, csv_folder, embedding_model, video_name, batch_size):
    list_frames = get_list_frames(frames_folder, video_name)
    embedding_frame(list_frames, embedding_folder, csv_folder, embedding_model, video_name, batch_size)

# def extract_embedding(csv_path, video_name, keyframes_folder, embedding_folder, embedding_model, batch_size):
#     list_keyframes = get_list_keyframes(csv_path, keyframes_folder, video_name)
#     embedding_frame(list_keyframes, embedding_folder, embedding_model, video_name, batch_size)

# def wfile(folder, ext):
#     return [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith(ext)]

# def embedding_keyframes(csv_folder, keyframes_folder, embedding_folder, embedding_model, embedding_batch_size=32):
#     embedding_model = CLIPSingleton(*embedding_model)
#     videos = wfile(csv_folder, '.csv')

#     for video in videos:
#         start = timer()
#         video_name = os.path.basename(video).split('.')[0]
#         csv_path = os.path.join(csv_folder, f'{video_name}.csv')
#         extract_embedding(csv_path, video_name, keyframes_folder, embedding_folder, embedding_model, embedding_batch_size)

#         print(f'{video_name} done in {timer() - start}')

def frames_to_keyframes(frames_folder, csv_folder, embedding_folder, embedding_model, batch_size):
    embedding_model = CLIPSingleton(*embedding_model)
    videos = [os.path.join(frames_folder, f) for f in os.listdir(frames_folder) if os.path.isdir(os.path.join(frames_folder, f))]

    for video in videos:
        start = timer()
        video_name = os.path.basename(video)
        create_embedding_and_csv(frames_folder, embedding_folder, csv_folder, embedding_model, video_name, batch_size)

        print(f'{video_name} done in {timer() - start}')

if __name__ == '__main__':

    model_folder = '/data/models'

    if not os.path.exists(model_folder):
        os.makedirs(model_folder)

    embedding_model = EMBEDDING_NAME
    embedding_pretrained = EMBEDDING_PRETRAINED
    embedding_token = EMBEDDING_TOKEN
    device = 'cuda'
    embedding_batch_size = EMBEDDING_BATCH_SIZE

    csv_folder = CSV_FOLDER
    keyframes_folder = KEYFRAMES_FOLDER
    embedding_folder = EMBEDDING_FOLDER_V2

    if not os.path.exists(embedding_folder):
        os.makedirs(embedding_folder)

    embedding_keyframes(csv_folder, keyframes_folder, embedding_folder, (embedding_model, embedding_pretrained, device, embedding_token))