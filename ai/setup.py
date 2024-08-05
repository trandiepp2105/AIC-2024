from scripts.utils import *
from scripts.extract_frame import *
from configs import *
from OCR.OCR import *
from scripts.text_embedding import *
from scripts.embedding_model import CLIP_Embedding, CLIPSingleton
# from scripts.faiss_search import Faiss_Index
from tqdm import tqdm
import os, shutil
from object_detection import generate_output_json
import os


# def extract_from_videos(video_folder, keyframe_folder, frame_folder, embedding_folder, object_folder, threshold=0.9, width=1024, height=1024):
#     print("Loading CLIP model...")
#     embedding = CLIPSingleton(model_name='ViT-L-14-quickgelu', pretrained='dfn2b', device='cuda')
#     print("Model loaded.")
#     # Create frame folder
#     if not os.path.exists(frame_folder):
#         os.makedirs(frame_folder)
#     else:
#         shutil.rmtree(frame_folder)
#         os.makedirs(frame_folder)
#     # Create keyframe folder
#     if not os.path.exists(keyframe_folder):
#         os.makedirs(keyframe_folder)
#     else:
#         shutil.rmtree(keyframe_folder)
#         os.makedirs(keyframe_folder)
#     # Create embedding folder
#     if not os.path.exists(embedding_folder):
#         os.makedirs(embedding_folder)
#     else:
#         shutil.rmtree(embedding_folder)
#         os.makedirs(embedding_folder)

#     # Extract keyframes
#     print("Extracting keyframes...")
#     extract_keyframes(video_folder, keyframe_folder, embedding_folder, embedding, threshold=threshold, width=width, height=height, batch_size=256)

#     print("Extracting frames...")
#     multiprocessing_extract_from_keyframes(video_folder, keyframe_folder, frame_folder, width=width, height=height, num_processes=8)

#     print("Generating output JSON Object Detection...")
#     generate_output_json(frame_folder, object_folder, models='yolov8m.pt', batch_size=64)
#     print("Done.")

#     print("Extracting text...")
#     OCR_from_folder(frame_folder, output_dir=ocr_folder, threshold_score=threshold_score)
#     print("Done.")

#     print("Extracting text...")
#     OCR_from_folder(frame_folder, output_dir=ocr_folder, threshold_score=threshold_score)
#     print("Done.")

def keyframe_and_embedding(video_folder, keyframe_folder, embedding_folder, threshold=1e-3, width=1024, height=1024, batch_size=32):
    print("Loading CLIP model...")
    embedding = CLIPSingleton(model_name='ViT-L-14-quickgelu', pretrained='dfn2b', device='cuda')
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
    extract_keyframes(video_folder, keyframe_folder, embedding_folder, embedding, threshold=threshold, width=width, height=height, batch_size=256)

    print("Extracting frames...")
    multiprocessing_extract_from_keyframes(video_folder, keyframe_folder, frame_folder, width=width, height=height, num_processes=8)
    
def object_detection(frame_folder, object_folder, models = 'yolov8m.pt', batch_size = 64):
    if not os.path.exists(object_folder):
        os.makedirs(object_folder)
    else:
        shutil.rmtree(object_folder)
        os.makedirs(object_folder)

    print("Generating output JSON Object Detection...")
    generate_output_json(frame_folder, object_folder, models=models, batch_size=batch_size)
    print("Done.")

def extract_text(frame_folder, ocr_folder, threshold_score=0.59):
    if not os.path.exists(ocr_folder):
        os.makedirs(ocr_folder)
    else:
        shutil.rmtree(ocr_folder)
        os.makedirs(ocr_folder)


    print("Extracting text...")
    OCR_from_folder(frame_folder, output_dir=ocr_folder, threshold_score=threshold_score)
    print("Done.")

def extract_ocr_embedding(ocr_folder, ocr_embedding_folder):
    if not os.path.exists(ocr_embedding_folder):
        os.makedirs(ocr_embedding_folder)
    else:
        shutil.rmtree(ocr_embedding_folder)
        os.makedirs(ocr_embedding_folder)

    print("Extracting OCR embeddings...")
    embedding_foler(ocr_folder, ocr_embedding_folder, batch_size=128)
    print("Done.")


if __name__ == "__main__":
    root_dir = os.getenv("ROOT_DIR")

    model_folder = os.path.join(root_dir, "models")

    if not os.path.exists(model_folder):
        os.makedirs(model_folder)

    videos_folder = os.path.join(root_dir, "videos")
    keyframe_folder = os.path.join(root_dir, "keyframes")
    frame_folder = os.path.join(root_dir, "frames")
    embedding_folder = os.path.join(root_dir, "embeddings")
    threshold_keyframe = 0.9

    width = 640
    height = 480

    # keyframe_and_embedding(videos_folder, keyframe_folder, embedding_folder, threshold=threshold_keyframe, width=width, height=height, batch_size=256)

    object_folder = os.path.join(root_dir, "objects")
    # object_detection(frame_folder, object_folder, models='yolov8m.pt', batch_size=64)

    ocr_folder = os.path.join(root_dir, "ocrs")
    threshold_ocr = 0.59
    # extract_text(frame_folder, ocr_folder, threshold_score=threshold_ocr)

    ocr_embedding_folder = os.path.join(root_dir, "ocr_embeddings")
    extract_ocr_embedding(ocr_folder, ocr_embedding_folder)
