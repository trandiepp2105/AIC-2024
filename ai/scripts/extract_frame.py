from scripts.utils import *
import os
import cv2
import numpy as np
import pickle
from tqdm import tqdm

def similar_cosine(v1, v2):
    return np.dot(v1, v2)

def save_keyframes_and_embedding(video_path, keyframe_folder, embedding_folder, embedding_model, threshold=1e-3, width=1024, height=1024, batch_size=256): 
    video_name = os.path.basename(video_path).split('.')[0]
    video_name = video_name.replace(' ', '_')
    keyframe_out_dir = keyframe_folder
    if not os.path.exists(keyframe_out_dir):
        os.makedirs(keyframe_out_dir)
    embedding_out_dir = os.path.join(embedding_folder, video_name)
    if not os.path.exists(embedding_out_dir):
        os.makedirs(embedding_out_dir)
    cap = cv2.VideoCapture(video_path)
    keyframes = []
    d_prev = None
    batchs = []
    ids = []
    total_frame = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            if len(batchs) > 0:
                v = embedding_model.get_images_embedding(batchs).detach().cpu().numpy().astype(np.float32)
                for i in range(len(v)):
                    if similar_cosine(v[i], d_prev) > threshold:
                        d_prev = v[i]
                        embedding_path = os.path.join(embedding_out_dir, f'{ids[i]}')
                        np.save(embedding_path, v[i])
                        keyframes.append(ids[i])
                batchs = []
                ids = []
            break
        if total_frame % 7 != 0:
            total_frame += 1
            continue
        frame = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)).resize((width, height))
        # v = embedding_model.get_image_embedding(frame).detach().cpu().numpy()
        if d_prev is None:
            v = embedding_model.get_image_embedding(frame).detach().cpu().numpy().astype(np.float32)
            d_prev = v
            embedding_path = os.path.join(embedding_out_dir, f'{total_frame}')
            np.save(embedding_path, v)
            keyframes.append(total_frame)   
        else:
            batchs.append(frame)
            ids.append(total_frame)
            if len(batchs) == batch_size:
                v = embedding_model.get_images_embedding(batchs).detach().cpu().numpy().astype(np.float32)
                for i in range(len(v)):
                    if similar_cosine(v[i], d_prev) < 0.9:
                        d_prev = v[i]
                        embedding_path = os.path.join(embedding_out_dir, f'{ids[i]}')
                        np.save(embedding_path, v[i])
                        keyframes.append(ids[i])
                batchs = []
                ids = []
        total_frame += 1
    keyframes_path = os.path.join(keyframe_out_dir, f'{video_name}.pickle')
    with open(keyframes_path, 'wb') as f:
        pickle.dump(keyframes, f)
    cap.release()

def extract_keyframes(videos_folder, keyframe_folder, embedding_folder, embedding_model, threshold=1e-3, width=1024, height=1024):
    videos = wfile(videos_folder, '.mp4')
    for video in tqdm(videos):
        save_keyframes_and_embedding(video, keyframe_folder, embedding_folder, embedding_model, threshold, width, height)

def extract_videoframes(videos_path, keyframe_folder, frame_folder, width=1024, height=1024):
    video_name = os.path.basename(videos_path).split('.')[0]
    video_name = video_name.replace(' ', '_')
    frame_out_dir = os.path.join(frame_folder, video_name)
    if not os.path.exists(frame_out_dir):
        os.makedirs(frame_out_dir)
    cap = cv2.VideoCapture(videos_path)
    frame_cout = 0
    with open(os.path.join(keyframe_folder, f'{video_name}.pickle'), 'rb') as f:
        keyframes = pickle.load(f)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if frame_cout not in keyframes:
            frame_cout += 1
            continue
        frame = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)).resize((width, height))
        frame_path = os.path.join(frame_out_dir, f'{frame_cout}.jpg')
        frame.save(frame_path)
        frame_cout += 1

def extract_from_keyframes(video_folder, keyframe_folder, frame_folder, width=1024, height=1024):
    videos = wfile(video_folder, '.mp4')
    for video in tqdm(videos):
        extract_videoframes(video, keyframe_folder, frame_folder, width, height)