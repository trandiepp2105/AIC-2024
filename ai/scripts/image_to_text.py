import os
from scripts.utils import wfile
import json
from scripts.models import BlipSingleton
from PIL import Image
import cv2

def devide_batch(data, batch_size):
    batchs = []
    batch = []
    for i in range(len(data)):
        frame_num = int(data[i].split('/')[-1].split('.')[0])
        batch.append((frame_num, data[i]))
        if len(batch) == batch_size:
            batchs.append(batch)
            batch = []
    if len(batch) > 0:
        batchs.append(batch)
    return batchs

def extract_batchs(batchs, extract_model):
    images = [Image.fromarray(cv2.imread(batch[1])) for batch in batchs]
    embeddings = extract_model.generate(images)
    res = [(batchs[i][0], embeddings[i]) for i in range(len(batchs))]
    return res

def extract_description(keyframes_foldder, description_folder, extract_model, batch_size=32):
    video_name = keyframes_foldder.split('/')[-1]
    description_file = os.path.join(description_folder, video_name + '.json')

    frames = wfile(keyframes_foldder, endswith='.jpg')

    batchs = devide_batch(frames, batch_size)
    descriptions = {}
    for batch in batchs:
        res = extract_batchs(batch, extract_model)
        for r in res:
            descriptions[r[0]] = r[1]

    with open(description_file, 'w') as f:
        json.dump(descriptions, f, indent=4)

    print(f"Extracted description of {video_name}")

def extract_description_folder(all_keyframes_folder, description_folder, extract_agrs, batch_size=32):
    extract_model = BlipSingleton(*extract_agrs)
    
    for folder in os.listdir(all_keyframes_folder):
        keyframes_foldder = os.path.join(all_keyframes_folder, folder)
        extract_description(keyframes_foldder, description_folder, extract_model, batch_size=batch_size)





    