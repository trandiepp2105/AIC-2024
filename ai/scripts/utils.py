from PIL import Image
from torchvision import transforms
# import faiss
from tqdm import tqdm
import numpy as np
import os
import pandas as pd
import pickle

def wfile(root, endswith='.mp4'):
    paths = []
    for dirpath, dirnames, filenames in os.walk(root):
        for filename in filenames:
            if filename.endswith(endswith):
                paths.append(os.path.join(dirpath, filename))
    sorted(paths)
    return paths

def img_preprocess(img_path, transform=transforms.Compose([transforms.Resize((1024, 1024))]), expand_dims=False):
    img = Image.open(img_path)
    img = transform(img)
    if expand_dims:
        img = img.unsqueeze(0)
    return img