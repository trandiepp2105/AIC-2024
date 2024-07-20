from scripts.utils import *
import os
import cv2
import numpy as np
import pickle
from tqdm import tqdm

def extract_all_frames(video_path, output_dir, width=1024, height=1024):
    video_name = os.path.basename(video_path).split('.')[0]
    video_name = video_name.replace(' ', '_')
    out_dir = os.path.join(output_dir, video_name)
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if frame_count % 7 != 0:
            frame_count += 1
            continue
        frame = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)).resize((width, height))
        frame_path = os.path.join(out_dir, f'{frame_count}.jpg')
        frame.save(frame_path)
        frame_count += 1
    cap.release()

def similar_frame(frame1, frame2, frame3):
    return np.linalg.norm(frame1-frame3) / frame1.shape[0]

def extract_frame(video_path, output_dir, embedding_model, threshold = 1e-3, width=1024, height=1024):
    video_name = os.path.basename(video_path).split('.')[0]
    video_name = video_name.replace(' ', '_')
    out_dir = os.path.join(output_dir, video_name)
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    d_prev = None
    v_prev = None
    total_frame = 0
    idx = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if total_frame % 7 != 0:
            total_frame += 1
            continue
        idx += 1
        frame = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)).resize((width, height))
        v = embedding_model.get_image_embedding(frame).detach().cpu().numpy()
        if d_prev is None:
            # K[f'{idx}'] = v
            d_prev = v
            v_prev = v
            frame_path = os.path.join(out_dir, f'{total_frame}.jpg')
            frame.save(frame_path)
            frame_count += 1
        else:
            # print(similar_frame(v, v_prev, d_prev))
            # print(threshold)
            if similar_frame(v, v_prev, d_prev) > threshold:
                # K[f'{idx}'] = v
                d_prev = v
                frame_path = os.path.join(out_dir, f'{total_frame}.jpg')
                frame.save(frame_path)
                frame_count += 1
        
        v_prev = v
        total_frame += 1
    cap.release()

def save_keyframes_and_embedding(video_path, keyframe_folder, embedding_folder, embedding_model, threshold=1e-3, width=1024, height=1024):  
    video_name = os.path.basename(video_path).split('.')[0]
    video_name = video_name.replace(' ', '_')
    keyframe_out_dir = os.path.join(keyframe_folder, video_name)
    if not os.path.exists(keyframe_out_dir):
        os.makedirs(keyframe_out_dir)
    embedding_out_dir = os.path.join(embedding_folder, video_name)
    if not os.path.exists(embedding_out_dir):
        os.makedirs(embedding_out_dir)
    cap = cv2.VideoCapture(video_path)
    keyframes = []
    d_prev = None
    v_prev = None
    total_frame = 0
    idx = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if total_frame % 7 != 0:
            total_frame += 1
            continue
        idx += 1
        frame = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)).resize((width, height))
        v = embedding_model.get_image_embedding(frame).detach().cpu().numpy()
        if d_prev is None:
            d_prev = v
            v_prev = v
            embedding_path = os.path.join(embedding_out_dir, f'{total_frame}.pickle')
            with open(embedding_path, 'wb') as f:
                pickle.dump(v.tolist(), f)
            keyframes.append(total_frame)
        else:
            if similar_frame(v, v_prev, d_prev) > threshold:
                d_prev = v
                embedding_path = os.path.join(embedding_out_dir, f'{total_frame}.pickle')
                with open(embedding_path, 'wb') as f:
                    pickle.dump(v.tolist(), f)
                keyframes.append(total_frame)
        v_prev = v
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
    with open(os.path.join(keyframe_folder, f'{video_name}\\{video_name}.pickle'), 'rb') as f:
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