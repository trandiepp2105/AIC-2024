import numpy as np
import pickle
import os
from scripts.utils import wfile
import shutil
from collections import deque
import numpy as np
import pandas as pd
from multiprocessing import Pool
import json

def video_data(video, list_keyframes, description_folder, embeddings_folder, objects_folder, ocr_embeddings_folder, caption_path):
    # videoDT = [[], [], [], [], [], []]
    # for keyframe in list_keyframes:
    #     keyframe_embedding = np.load(os.path.join(embeddings_folder, keyframe + '.npy'))
    #     keyframe_objects = np.load(os.path.join(objects_folder, keyframe + '.npy'))
    #     keyframe_ocr = np.random.rand(768).astype(np.float32)
    #     description_embedding = np.load(os.path.join(description_folder, keyframe + '.npy'))
    #     videoDT[0].append(video)
    #     videoDT[1].append(keyframe)
    #     videoDT[2].append(keyframe_embedding)
    #     videoDT[3].append(keyframe_objects)
    #     videoDT[4].append(keyframe_ocr)
    #     videoDT[5].append(description_embedding)
    with open(caption_path, 'r', encoding='utf-8') as json_file:
        captions = json.load(json_file)
    videoDT = [
        [video] * len(list_keyframes),
        list_keyframes,
        [np.load(os.path.join(embeddings_folder, keyframe + '.npy')).astype(np.float32) for keyframe in list_keyframes],
        [np.load(os.path.join(objects_folder, keyframe + '.npy')).astype(np.float32) for keyframe in list_keyframes],
        [np.random.rand(768).astype(np.float32) for keyframe in list_keyframes],
        [np.load(os.path.join(description_folder, keyframe + '.npy')).astype(np.float32) for keyframe in list_keyframes],
        [captions[keyframe] for keyframe in list_keyframes]
    ]
    return videoDT

def video_data_nextframe(video, list_keyframes, description_folder, embeddings_folder, objects_folder, ocr_embeddings_folder, caption_path, max_frames):
    videoDT = [[], [], [], [], [], [], [], []]
    with open(caption_path, 'r', encoding='utf-8') as json_file:
        captions = json.load(json_file)
    q = deque(maxlen=max_frames)
    for keyframe in list_keyframes:
        keyframe_name = os.path.basename(keyframe).split('.')[0]
        keyframe_embedding = np.load(os.path.join(embeddings_folder, keyframe_name + '.npy')).astype(np.float32)
        keyframe_objects = np.load(os.path.join(objects_folder, keyframe_name + '.npy')).astype(np.float32)
        keyframe_ocr = np.random.rand(768).astype(np.float32)
        description_embedding = np.load(os.path.join(description_folder, keyframe_name + '.npy')).astype(np.float32)
        caption = captions[keyframe_name]
        for i in range(len(q)):
            videoDT[0].append(q[i][0])
            videoDT[1].append(q[i][1])
            videoDT[2].append(q[i][2])
            videoDT[3].append(q[i][3])
            videoDT[4].append(q[i][4])
            videoDT[5].append(keyframe_embedding)
            videoDT[6].append(q[i][5])
            videoDT[7].append(caption)

        q.append([video, keyframe_name, keyframe_embedding, keyframe_objects, keyframe_ocr, description_embedding])
    return videoDT

def create_df(video_name, csv_path, description_folder, embeddings_folder, objects_folder, ocr_embeddings_folder, database_folder, caption_folder, bath_size=5000):
    print(f"Creating database for {video_name}")
    df = pd.read_csv(csv_path)
    list_keyframes = df['frame_number'].apply(lambda x: str(int(x))).tolist()
    description_f = os.path.join(description_folder, video_name)
    embeddings_f = os.path.join(embeddings_folder, video_name)
    objects_f = os.path.join(objects_folder, video_name)
    ocr_embeddings_f = os.path.join(ocr_embeddings_folder, video_name)
    caption_path = os.path.join(caption_folder, video_name + '.json')
    videoDT = video_data(video_name, list_keyframes, description_f, embeddings_f, objects_f, ocr_embeddings_f, caption_path)
    # with open(os.path.join(database_folder, video_name + '.pkl'), 'wb') as f:
    #     pickle.dump(videoDT, f)
    # print(f"Created database for {video_name}")
    for i in range(0, len(list_keyframes), bath_size):
        with open(os.path.join(database_folder, video_name + f'_{i}.pkl'), 'wb') as f:
            pickle.dump([x[i:i+bath_size] for x in videoDT], f)
        print(f"Created database for {video_name} - {i}")
    print(f"Created database for {video_name}")

def create_database_data(csv_folder, description_folder, embeddings_folder, objects_folder, ocr_embeddings_folder, database_folder, caption_folder, num_processes=8, bath_size=3500):
    if not os.path.exists(database_folder):
        os.makedirs(database_folder)
    else:   
        shutil.rmtree(database_folder)
        os.makedirs(database_folder)

    list_agrs = []

    list_csv = wfile(csv_folder, 'csv')
    for video in list_csv:
        video_name = os.path.basename(video).split('.')[0]
        csv_path = os.path.join(csv_folder, video)
        list_agrs.append((video_name, csv_path, description_folder, embeddings_folder, objects_folder, ocr_embeddings_folder, database_folder, caption_folder, bath_size))

    with Pool(num_processes) as p:
        p.starmap(create_df, list_agrs)

def create_df_nextframe(video_name, csv_path, description_folder, embeddings_folder, objects_folder, ocr_embeddings_folder, database_folder, caption_folder, max_frames, bath_size=5000):
    print(f"Creating database nextframe for {video_name}")
    df = pd.read_csv(csv_path)
    list_keyframes = df['frame_number'].apply(lambda x: str(int(x))).tolist()
    description_f = os.path.join(description_folder, video_name)
    embeddings_f = os.path.join(embeddings_folder, video_name)
    objects_f = os.path.join(objects_folder, video_name)
    ocr_embeddings_f = os.path.join(ocr_embeddings_folder, video_name)
    caption_path = os.path.join(caption_folder, video_name + '.json')
    videoDT = video_data_nextframe(video_name, list_keyframes, description_f, embeddings_f, objects_f, ocr_embeddings_f, caption_path, max_frames)
    # with open(os.path.join(database_folder, video_name + '.pkl'), 'wb') as f:
    #     pickle.dump(videoDT, f)
    # print(f"Created database nextframe for {video_name}")
    for i in range(0, len(videoDT[0]), bath_size):
        with open(os.path.join(database_folder, video_name + f'_{i}.pkl'), 'wb') as f:
            pickle.dump([x[i:i+bath_size] for x in videoDT], f)
        print(f"Created database nextframe for {video_name} - {i}")
    print(f"Created database nextframe for {video_name}")


def create_database_data_nextframe(csv_folder, description_folder, embeddings_folder, objects_folder, ocr_embeddings_folder, database_folder, caption_folder, max_frames, num_processes=8, bath_size=3500):
    if not os.path.exists(database_folder):
        os.makedirs(database_folder)
    else:   
        shutil.rmtree(database_folder)
        os.makedirs(database_folder)

    list_agrs = []

    list_csv = wfile(csv_folder, 'csv')
    for video in list_csv:
        video_name = os.path.basename(video).split('.')[0]
        csv_path = os.path.join(csv_folder, video)
        list_agrs.append((video_name, csv_path, description_folder, embeddings_folder, objects_folder, ocr_embeddings_folder, database_folder, caption_folder, max_frames, bath_size))

    with Pool(num_processes) as p:
        p.starmap(create_df_nextframe, list_agrs)