from scripts.utils import *
from scripts.models import *
import os
import cv2
import numpy as np
import pickle
from tqdm import tqdm
from multiprocessing import Pool, Process, Semaphore, Queue
from PIL import Image
from time import sleep
import shutil
import pandas as pd

def similar_cosine(v1, v2):
    return np.dot(v1, v2)

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
        list_args.append((video, frame_folder, width, height))
    with Pool(num_processes) as p:
        p.starmap(extract_frame, list_args)

def save_keyframes_and_embedding(video_path, keyframe_folder, embedding_folder, embedding_model, threshold=1e-3, width=1024, height=1024, batch_size=32): 
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
                    if similar_cosine(v[i], d_prev) < threshold:
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
                    if similar_cosine(v[i], d_prev) < threshold:
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
    print(f'{video_name} done')
    cap.release()

def extract_keyframes(videos_folder, keyframe_folder, embedding_folder, embedding_model, threshold=1e-3, width=1024, height=1024, batch_size=32):
    videos = wfile(videos_folder, '.mp4')
    for video in tqdm(videos):
        save_keyframes_and_embedding(video, keyframe_folder, embedding_folder, embedding_model, threshold, width, height, batch_size)

def multiprocessing_extract_keyframes(videos_folder, keyframe_folder, embedding_folder, embedding_model, threshold=1e-3, width=1024, height=1024):
    videos = wfile(videos_folder, '.mp4')
    list_args = []
    for video in videos:
        list_args.append((video, keyframe_folder, embedding_folder, embedding_model, threshold, width, height))
    with Pool(2) as p:
        p.starmap(save_keyframes_and_embedding, list_args)

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
    cap.release()
    print(f'{video_name} done')

def extract_from_keyframes(video_folder, keyframe_folder, frame_folder, width=1024, height=1024):
    videos = wfile(video_folder, '.mp4')
    for video in tqdm(videos):
        extract_videoframes(video, keyframe_folder, frame_folder, width, height)

def multiprocessing_extract_from_keyframes(video_folder, keyframe_folder, frame_folder, width=1024, height=1024, num_processes=8):
    videos = wfile(video_folder, '.mp4')
    list_args = []
    for video in videos:
        list_args.append((video, keyframe_folder, frame_folder, width, height))
    with Pool(num_processes) as p:
        p.starmap(extract_videoframes, list_args)


def save_image(image, path):
    image.save(path)

def extract_video_frame(video_path, temp_folder='./temp_folder', width=1024, height=1024):
    video_name = os.path.basename(video_path).split('.')[0]
    video_name = video_name.replace(' ', '_')
    frame_out_dir = os.path.join(temp_folder, video_name)
    if not os.path.exists(frame_out_dir):
        os.makedirs(frame_out_dir)
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_cout = 0
    list_frame = []
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if frame_cout % 7 != 0:
            frame_cout += 1
            continue
        frame = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)).resize((width, height))
        frame_path = os.path.join(frame_out_dir, f'{frame_cout}.jpg')
        save_image(frame, frame_path)
        list_frame.append((frame_cout, frame_path))
        frame_cout += 1
    cap.release()
    print(f'Step 1 {video_name} done')
    return video_name, list_frame, fps

def embedding_from_batch(batch, embedding_model):
    list_image = [Image.open(frame_path) for _,frame_path in batch]
    embeddings = embedding_model.get_images_embedding(list_image).detach().cpu().numpy().astype(np.float32)
    return [(frame[0], embeddings[i]) for i, frame in enumerate(batch)]

def save_list_embedding(list_embedding, embeddings_folder, video_name):
    outdir = os.path.join(embeddings_folder, video_name)
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    else:
        shutil.rmtree(outdir)
        os.makedirs(outdir)
    for frame in list_embedding:
        embedding_path = os.path.join(outdir, f'{frame[0]}.npy')
        np.save(embedding_path, frame[1])

def extract_key_frame(list_frame, embeddings_folder, video_name, embedding_model, batch_size=32):
    list_embedding = []
    for i in range(0, len(list_frame), batch_size):
        batchs = list_frame[i:i+batch_size]
        v = embedding_from_batch(batchs, embedding_model)
        list_embedding.extend(v)
    Process(target=save_list_embedding, args=(list_embedding, embeddings_folder, video_name)).start()
    print(f'Step 2 {video_name} done')

def move_keyframes(keyframes_folder, embedding_folder, csv_folder, video_name, list_frame, queue, fps, threshold=0.9):
    outdir = os.path.join(keyframes_folder, video_name)
    keyframes = {
        'frame_number': [],
        'fps': []
    }
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    v_prev = None
    for frame in list_frame:
        frame_number, frame_path = frame
        frame_embedding = np.load(os.path.join(embedding_folder, video_name, f'{frame_number}.npy'))
        if v_prev is None or similar_cosine(v_prev, frame_embedding) < threshold:
            shutil.copy(frame_path, os.path.join(outdir, f'{frame_number}.jpg'))
            keyframes['frame_number'].append(frame_number)
            keyframes['fps'].append(fps)
            v_prev = frame_embedding

    csv_path = os.path.join(csv_folder, f'{video_name}.csv')
    df = pd.DataFrame(keyframes)
    df.to_csv(csv_path, index=False)
    
    queue.put(video_name)

    print(f'{queue.qsize()} {video_name} done')

    print(f'Step 3 {video_name} done')

def process_task(videos_path, semaphore, temp_folder, queue, width=1024, height=1024):
    with semaphore:
        print(f'Processing {videos_path}')
        video_name, list_frame, fps = extract_video_frame(videos_path, temp_folder, width, height)
        queue.put((video_name, list_frame, fps))

def process_task2(embedding_model, threshold, batch_size, frames_folder, embeddings_folder, csv_folder, queue, num_videos, queue_count):
    num_video_done = 0
    embedding_model = CLIPSingleton(model_name=embedding_model[0], pretrained=embedding_model[1], device=embedding_model[3], tokenizers=embedding_model[2])
    while True:
        item = queue.get()
        if item is not None:
            video_name, list_frame, fps = item
            list_keyframes = extract_key_frame(list_frame, embeddings_folder, video_name, embedding_model, batch_size)
            Process(target=move_keyframes, args=(frames_folder, embeddings_folder, csv_folder, video_name, list_frame, queue_count, fps, threshold)).start()
            num_video_done += 1
        if num_video_done == num_videos:
            break
        sleep(1)


def extract_video(all_frames_folder, videos_folder, frames_folder, embeddings_folder, embedding_model, csv_folder, threshold=1e-3, width=1024, height=1024, batch_size=32, num_processes=8):
    list_video = wfile(videos_folder, '.mp4')
    semaphore = Semaphore(num_processes)
    queue = Queue()
    queue_count = Queue()
    queue.put(None)
    q = []
    for video in list_video:
        q.append(Process(target=process_task, args=(video, semaphore, all_frames_folder, queue, width, height)))
    for p in q:
        p.start()

    process_task2(embedding_model, threshold, batch_size, frames_folder, embeddings_folder, csv_folder, queue, len(list_video), queue_count)

    while queue_count.qsize() < len(list_video):
        sleep(5)