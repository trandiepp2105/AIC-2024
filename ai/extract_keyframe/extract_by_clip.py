from clip_model import CLIPSingleton
import os
from PIL import Image
from configs import *
from multiprocessing import Process, Pool
import numpy as np
import pandas as pd
import torch
import shutil

def wfile(root, endswith='.mp4'):
    paths = []
    for dirpath, dirnames, filenames in os.walk(root):
        for filename in filenames:
            if filename.endswith(endswith):
                paths.append(os.path.join(dirpath, filename))
    sorted(paths)
    return paths

def embedding_batch(list_images, embedding_model):
    images = [Image.open(image) for _, image in list_images]
    embeddings = embedding_model.get_images_embedding(images).detach().cpu().numpy()
    list_embedding = [(list_images[i][0], embeddings[i]) for i in range(len(list_images))]
    return list_embedding

def get_list_frames(frame_folder):
    frames = wfile(frame_folder, '.jpg')

    list_frames = []
    for frame in frames:
        frame_number = int(os.path.basename(frame).split('.')[0])
        list_frames.append((frame_number, frame))

    list_frames = sorted(list_frames, key=lambda x: x[0])

    return list_frames

def save_embedding(list_embedding, output_folder):
    for frame_number, embedding in list_embedding:
        embedding_path = os.path.join(output_folder, f'{frame_number}.npy')
        np.save(embedding_path, embedding)

def embedding_frame(list_frames, embedding_folder, embedding_model, video_name, batch_size=32):
    output_folder = os.path.join(embedding_folder, video_name)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    list_embedding = []

    for i in range(0, len(list_frames), batch_size):
        batch = list_frames[i:i+batch_size]
        embeddings = embedding_batch(batch, embedding_model)
        list_embedding.extend(embeddings)

    Process(target=save_embedding, args=(list_embedding, output_folder)).start()

    print(f'Emedding {video_name} done')

def similarity(embedding1, embedding2):
    return np.dot(embedding1, embedding2)

def move_keyframes(csv_folder, embedding_folder, video_name, list_frame, threshold=0.9):
    keyframes = {
        'frame_number': []
    }
    v_prev = None
    for frame in list_frame:
        frame_number, frame_path = frame
        frame_embedding = np.load(os.path.join(embedding_folder, video_name, f'{frame_number}.npy'))
        if v_prev is None or similarity(v_prev, frame_embedding) < threshold:
            keyframes['frame_number'].append(frame_number)
            v_prev = frame_embedding

    csv_path = os.path.join(csv_folder, f'{video_name}.csv')
    df = pd.DataFrame(keyframes)
    df.to_csv(csv_path, index=False)

    print(f'{video_name} done')

def extract_keyframes_csv(frame_folder, video_name, embedding_folder, csv_folder, threshold=0.9):
    print(f'Processing {video_name}')
    frame_folder = os.path.join(frame_folder, video_name)
    list_frames = get_list_frames(frame_folder)
    move_keyframes(csv_folder, embedding_folder, video_name, list_frames, threshold)

def extract_keyframes(frame_folder, embedding_folder, csv_folder, embedding_model, threshold=0.9, batch_size=32):
    clip_model = CLIPSingleton(*embedding_model)
    count = 0
    for video_name in os.listdir(frame_folder):
        print(f'Processing {video_name}')
        list_frames = get_list_frames(os.path.join(frame_folder, video_name))
        embedding_frame(list_frames, embedding_folder, clip_model, video_name, batch_size=batch_size)
        # Process(target=move_keyframes, args=(csv_folder, embedding_folder, video_name, list_frames, threshold)).start()
        count += 1
        print(f'{count} {video_name} done')

def run_copy_keyframes(csv_path, keyframes_folder, frames_folder):
    video_name = os.path.basename(csv_path).split('.')[0]
    print(f'Processing {video_name}')
    df = pd.read_csv(csv_path)
    keyframes = df['frame_number'].tolist()
    keyframes_folder_path = os.path.join(keyframes_folder, video_name)
    frames_folder_path = os.path.join(frames_folder, video_name)
    if not os.path.exists(keyframes_folder_path):
        os.makedirs(keyframes_folder_path)
    for keyframe in keyframes:
        frame_path = os.path.join(frames_folder_path, f'{keyframe}.jpg')
        keyframe_path = os.path.join(keyframes_folder_path, f'{keyframe}.jpg')
        shutil.copy(frame_path, keyframe_path)
    print(f'{video_name} done')


def copy_keyframes(csv_folder, keyframes_folder, frames_folder):
    list_csv = wfile(csv_folder, '.csv')

    list_agrs = []
    for video in list_csv:
        list_agrs.append((video, keyframes_folder, frames_folder))

    num_processes = 8

    with Pool(num_processes) as p:
        p.starmap(run_copy_keyframes, list_agrs)

if __name__ == '__main__':
    frames_folder = FRAMES_FOLDER
    embedding_folder = EMBEDDING_FOLDER
    keyframes_folder = KEYFRAMES_FOLDER
    csv_folder = CSV_FOLDER

    if not os.path.exists(embedding_folder):
        os.makedirs(embedding_folder)

    if not os.path.exists(csv_folder):
        os.makedirs(csv_folder)

    if not os.path.exists(keyframes_folder):
        os.makedirs(keyframes_folder)

    # device = 'cuda' if torch.cuda.is_available() else 'cpu'
    # model_clip = (MODEL_CLIP_NAME, PRETRAINED_CLIP, device, TOKENIZER_CLIP)
    threshold = THRESHOLD_SIMILARITY
    # batch_size = BATCH_CLIP_SIZE

    # extract_keyframes(frames_folder, embedding_folder, csv_folder, model_clip, threshold, batch_size)

    # print("Done.")

    # videos = os.listdir(frames_folder)

    # list_agrs = []
    # for video in videos:
    #     list_agrs.append((frames_folder, video, embedding_folder, csv_folder, threshold))

    # num_processes = 8

    # with Pool(num_processes) as p:
    #     p.starmap(extract_keyframes_csv, list_agrs)

    copy_keyframes(csv_folder, KEYFRAMES_FOLDER, frames_folder)

    print("Done.")
    
    
    