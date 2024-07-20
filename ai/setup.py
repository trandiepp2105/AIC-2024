from scripts.utils import *
from scripts.extract_frame import *
from configs import *
import json
from scripts.embedding_model import CLIP_Embedding, CLIPSingelton
# from scripts.faiss_search import Faiss_Index
from tqdm import tqdm

if __name__ == '__main__':
    embedding = CLIPSingelton()
    video_folder = VIDEO_FOLDER
    frame_folder = FRAME_FOLDER
    keyframe_folder = KEYFRAME_FOLDER
    embedding_folder = EMBEDDING_FOLDER
    # Create frame folder
    if not os.path.exists(frame_folder):
        os.makedirs(frame_folder)
    # Create keyframe folder
    if not os.path.exists(keyframe_folder):
        os.makedirs(keyframe_folder)
    # Create embedding folder
    if not os.path.exists(embedding_folder):
        os.makedirs(embedding_folder)

    # Extract keyframes
    print("Extracting keyframes...")
    extract_keyframes(video_folder, keyframe_folder, embedding_folder, embedding, threshold=1.5e-2, width=1024, height=1024)

    print("Extracting frames...")
    extract_from_keyframes(video_folder, keyframe_folder, frame_folder, width=1024, height=1024)