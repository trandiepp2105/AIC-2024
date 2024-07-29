from scripts.utils import *
from scripts.extract_frame import *
from configs import *
import json
from scripts.embedding_model import CLIP_Embedding, CLIPSingleton
# from scripts.faiss_search import Faiss_Index
from tqdm import tqdm
import os, shutil
from object_detection import generate_output_json

def extract_from_videos(video_folder, keyframe_folder, frame_folder, embedding_folder, object_folder, threshold=1e-3, width=1024, height=1024):
    print("Loading CLIP model...")
    embedding = CLIPSingleton()
    print("Model loaded.")
    # Create frame folder
    if not os.path.exists(frame_folder):
        os.makedirs(frame_folder)
    else:
        shutil.rmtree(frame_folder)
        os.makedirs(frame_folder)
    # Create keyframe folder
    if not os.path.exists(keyframe_folder):
        os.makedirs(keyframe_folder)
    else:
        shutil.rmtree(keyframe_folder)
        os.makedirs(keyframe_folder)
    # Create embedding folder
    if not os.path.exists(embedding_folder):
        os.makedirs(embedding_folder)
    else:
        shutil.rmtree(embedding_folder)
        os.makedirs(embedding_folder)

    # Extract keyframes
    print("Extracting keyframes...")
    extract_keyframes(video_folder, keyframe_folder, embedding_folder, embedding, threshold=threshold, width=width, height=height)

    print("Extracting frames...")
    extract_from_keyframes(video_folder, keyframe_folder, frame_folder, width=width, height=height)

    print("Generating output JSON Object Detection...")
    generate_output_json(frame_folder, object_folder, models='yolov8m.pt', batch_size=64)
    print("Done.")

if __name__ == "__main__":
    extract_from_videos(VIDEO_FOLDER, KEYFRAME_FOLDER, FRAME_FOLDER, EMBEDDING_FOLDER, OBJECTS_FOLDER, THRESHOLD_SIMILARITY, FRAME_WIDTH, FRAME_HEIGHT)