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
    output_dir = FRAME_FOLDER

    video2frame(video_folder, output_dir)