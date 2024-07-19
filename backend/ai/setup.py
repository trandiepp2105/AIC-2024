from scripts.utils import *
from scripts.extract_frame import *
from configs import *
import json
from scripts.embedding_model import CLIPSingleton
from scripts.faiss_search import Faiss_Index
from tqdm import tqdm

if __name__ == '__main__':
    embedding = CLIPSingleton()
    video_folder = VIDEO_FOLDER
    output_dir = FRAME_FOLDER

    videos = wfile(video_folder, '.mp4')

    print('Extracting frames from videos')
    for video in tqdm(videos):
        extract_frame(video, output_dir, embedding_model=embedding, threshold=THRESHOLD_SIMILARITY)

    dic = dictionary_frame(output_dir)

    print('Creating index')
    index = Faiss_Index(INDEX, embedding, id2img=dic)
    index.save_index()
    print('Index created')

    print('Saving dictionary')
    with open(DIC_PATH, 'w') as f:
        json.dump(dic, f)
