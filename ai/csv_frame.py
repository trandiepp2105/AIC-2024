import os
import pandas as pd
from tqdm import tqdm

def csv_frames(frames_folder):
    csv = {
        'video_name': [],
        'frame_number': [],
    }
    for root, _, files in tqdm(os.walk(frames_folder)):
        for file in files:
            if file.endswith('.jpg'):
                video_name = os.path.basename(root)
                frame_number = int(os.path.splitext(file)[0])
                csv['video_name'].append(video_name)
                csv['frame_number'].append(frame_number)

    return pd.DataFrame(csv)

def csv_videos(videos_folder):
    csv = {
        'video_name': [],
    }
    for root, _, files in tqdm(os.walk(videos_folder)):
        for file in files:
            if file.endswith('.mp4'):
                video_name = os.path.splitext(file)[0]
                csv['video_name'].append(video_name)

    return pd.DataFrame(csv)

def load_data_from_folders(frames_folder, videos_folder, csv_videos_path, csv_frames_path):
    videos_df = csv_videos(videos_folder)
    frames_df = csv_frames(frames_folder)
    videos_df.to_csv(csv_videos_path, index=False)
    frames_df.to_csv(csv_frames_path, index=False)

    return csv_videos_path, csv_frames_path

if __name__ == '__main__':
    frames_folder = r"C:\Users\hokha\OneDrive\Desktop\storage\frames"
    videos_folder = r"C:\Users\hokha\OneDrive\Desktop\storage\videos"
    csv_videos_path = 'videos.csv'
    csv_frames_path = 'frames.csv'
    load_data_from_folders(frames_folder, videos_folder, csv_videos_path, csv_frames_path)
    print('Data saved to csv files')
