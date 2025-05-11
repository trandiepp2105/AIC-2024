from configs import *
from scripts.utils import wfile
import cv2
import os
from multiprocessing import Pool
from PIL import Image

def extract_frame(video_path, frame_folder, width=1024, height=1024):
    video_name = os.path.basename(video_path).split('.')[0]
    print(f'Processing {video_name}')
    video_name = video_name.replace(' ', '_')
    frame_out_dir = os.path.join(frame_folder, video_name)
    if not os.path.exists(frame_out_dir):
        os.makedirs(frame_out_dir)
    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if frame_count % 7 != 0:
            frame_count += 1
            continue
        # frame = cv2.resize(frame, (width, height))
        # frame_out_path = os.path.join(frame_out_dir, f'{frame_count}.jpg')
        # cv2.imwrite(frame_out_path, frame)
        frame = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)).resize((width, height))
        frame_path = os.path.join(frame_out_dir, f'{frame_count}.jpg')
        frame.save(frame_path)
        frame_count += 1
    cap.release()
    print(f'{video_name} done')

def extract_all_frames(videos_folder, frame_folder, width=1024, height=1024, num_processes=8):
    videos = wfile(videos_folder, '.mp4')
    list_args = []
    for video in videos:
        video_path = os.path.join(videos_folder, video)
        list_args.append((video_path, frame_folder, width, height))
    with Pool(num_processes) as p:
        p.starmap(extract_frame, list_args)

if __name__ == '__main__':
    # Extract all frames from the video
    video_folder = r"C:\Users\hokha\OneDrive\Desktop\storage\videos"
    output_folder = r"C:\Users\hokha\OneDrive\Desktop\storage\frames"

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    extract_all_frames(video_folder, output_folder, FRAME_WIDTH, FRAME_HEIGHT, num_processes=4)
