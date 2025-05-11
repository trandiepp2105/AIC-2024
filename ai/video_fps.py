import pandas as pd
import os
import cv2
from tqdm import tqdm
from time import sleep

def get_fps(video_path):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    cap.release()
    return fps

def wfile(file, end='.mp4'):
    list_files = []
    for root, dirs, files in os.walk(file):
        for file in files:
            if file.endswith(end):
                list_files.append(os.path.join(root, file))
    return list_files

def video_fps(video_folder, output_csv):
    list_files = wfile(video_folder)
    df = {
        'video_name': [],
        'fps': []
    }
    for file in tqdm(list_files):
        df['video_name'].append(os.path.basename(file).split('.')[0])
        df['fps'].append(get_fps(file))
    df = pd.DataFrame(df)
    df.to_csv(output_csv, index=False)

def fps_csv(df, video_name):
    return df[df['video_name'] == video_name]['fps'].values[0]

def video_and_frame(frames_folder, end='.jpg'):
    list_files = []
    for root, dirs, files in os.walk(frames_folder):
        for file in files:
            if file.endswith(end):
                list_files.append((os.path.basename(root), file.split('.')[0]))
    return list_files

def frame_second(frames_folder, video_fps_csv, output_folder):
    frames = video_and_frame(frames_folder)
    df1 = pd.read_csv(video_fps_csv)

    df = {
        'video_name': [],
        'frame_number': [],
        'second' : []
    }

    for frame in tqdm(frames):
        video_name, frame_name = frame
        video_fps = fps_csv(df1, video_name)
        frame_second = int(frame_name) / video_fps
        df['video_name'].append(video_name)
        df['frame_number'].append(frame_name)
        df['second'].append(frame_second)
    df = pd.DataFrame(df)
    df.to_csv(output_folder, index=False)

if __name__ == '__main__':
    video_folder = r'E:\videos'
    output_csv = r'E:\videos.csv'
    video_fps(video_folder, output_csv)

    # frames_folder = r'C:\Users\hokha\OneDrive\Desktop\storage\frames'
    # video_fps_csv = r'C:\Users\hokha\OneDrive\Desktop\storage\videos.csv'
    # output_folder = r'C:\Users\hokha\OneDrive\Desktop\storage\frames.csv'
    # frame_second(frames_folder, video_fps_csv, output_folder)
        
