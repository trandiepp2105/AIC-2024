from scripts.utils import *
import os
import cv2
import numpy as np
from scripts.embedding_model import CLIP_Embedding
import torch

def extract_frame(video_path, output_dir, embedding_model, threshold = 1e-3):
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
        frame = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
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

def similar_frame(frame1, frame2, frame3):
    return np.linalg.norm(frame1-frame3) / frame1.shape[1]
