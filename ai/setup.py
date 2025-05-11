from scripts.utils import *
from scripts.extract_frame import *
from configs import *
from OCR.OCR import *
from scripts.image_to_text import *
from scripts.models import *
from scripts.description_embedding import *

import os, shutil
from object_detection import generate_output_json
from timeit import default_timer as timer
from scripts.create_database_data import *
from scripts.image_to_text import *
import logging

def keyframe_and_embedding(frames_folder, video_folder, keyframe_folder, embedding_folder, csv_folder, threshold=1e-3, width=1024, height=1024, batch_size=32, num_processes=8):
    print("Loading CLIP model...")
    model_name = MODELS_CLIP_NAME
    pretrained = PRETRAINED_CLIP
    tokenizers = TOKENIZER_CLIP
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    embedding = (model_name, pretrained, tokenizers, device)
    print("Model loaded.")
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

    if not os.path.exists(csv_folder):
        os.makedirs(csv_folder)
    else:
        shutil.rmtree(csv_folder)
        os.makedirs(csv_folder)

    if not os.path.exists(frames_folder):
        os.makedirs(frames_folder)
    else:
        shutil.rmtree(frames_folder)
        os.makedirs(frames_folder)

    # Extract keyframes
    # print("Extracting keyframes...")
    # extract_keyframes(video_folder, keyframe_folder, embedding_folder, embedding, threshold=threshold, width=width, height=height, batch_size=256)

    # print("Extracting frames...")
    # multiprocessing_extract_from_keyframes(video_folder, keyframe_folder, frame_folder, width=width, height=height, num_processes=8)
    
    print("Extracting video...")
    extract_video(frames_folder, video_folder, keyframe_folder, embedding_folder, embedding, csv_folder, threshold=threshold, width=width, height=height, batch_size=batch_size, num_processes=num_processes)
    print("Done.")

def object_detection(frame_folder, object_folder, models = 'yolov8m.pt', batch_size = 64, model_dir='data/models_yolo'):
    if not os.path.exists(object_folder):
        os.makedirs(object_folder)
    else:
        shutil.rmtree(object_folder)
        os.makedirs(object_folder)

    print("Generating output JSON Object Detection...")
    generate_output_json(frame_folder, object_folder, model_path=models, batch_size=batch_size, model_dir=model_dir)
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

def extract_ocr_embedding(ocr_folder, ocr_embedding_folder, batch_size=128):
    if not os.path.exists(ocr_embedding_folder):
        os.makedirs(ocr_embedding_folder)
    else:
        shutil.rmtree(ocr_embedding_folder)
        os.makedirs(ocr_embedding_folder)

    print("Extracting OCR embeddings...")
    from scripts.text_embedding import embedding_ocr_folder
    embedding_ocr_folder(ocr_folder, ocr_embedding_folder, batch_size=128)
    print("Done.")

def description_embedding(keyframe_folder, description_folder, embedding_folder, description_model, embedding_model, description_batch_size=32, embedding_batch_size=32):
    if not os.path.exists(embedding_folder):
        os.makedirs(embedding_folder)
    else:
        shutil.rmtree(embedding_folder)
        os.makedirs(embedding_folder)

    if not os.path.exists(description_folder):
        os.makedirs(description_folder)
    else:
        shutil.rmtree(description_folder)
        os.makedirs(description_folder)

    print("Extracting description...")
    extract_description_folder(keyframe_folder, description_folder, description_model, batch_size=description_batch_size)
    print("Done.")

    print("Embedding description...")
    embedding_description_folder(description_folder, embedding_folder, embedding_model, batch_size=embedding_batch_size)
    print("Done.")


if __name__ == "__main__":
    s = timer()
    model_folder = MODELS_VOLUME_DIR

    if not os.path.exists(model_folder):
        os.makedirs(model_folder)

    videos_folder = VIDEOS_VOLUME_DIR
    keyframe_folder = KEYFRAME_VOLUME_DIR
    embedding_folder = EMBEDDING_VOLUME_DIR
    threshold_keyframe = THRESHOLD_SIMILARITY
    csv_folder = KF_CSV_VOLUME_DIR
    frames_folder = FRAMES_VOLUME_DIR

    batch_extract = BATCH_CLIP_SIZE

    width = FRAME_WIDTH
    height = FRAME_HEIGHT
    start = timer()

    num_process = KEYFRAME_PROCESS
    # keyframe_and_embedding(frames_folder, videos_folder, keyframe_folder, embedding_folder, csv_folder, threshold=threshold_keyframe, width=width, height=height, batch_size=batch_extract, num_processes=num_process)
    print("Time to extract keyframes and embeddings: ", timer()-start)

    description_name = DE_MODEL
    description_pretrained = DE_PROCESSOR
    embedding_name = MODELS_CLIP_NAME
    embedding_pretrained = PRETRAINED_CLIP
    tokenizer_name = TOKENIZER_CLIP
    description_folder = DE_VOLIME_DIR
    de_embedding_folder = DE_EMBEDDING_VOLUME_DIR
    description_batch = DE_BATCH_SIZE
    de_embedding_batch = DE_EMBEDDING_BATCH_SIZE
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    start = timer()
    # description_embedding(keyframe_folder, description_folder, de_embedding_folder, (description_name, description_pretrained, device), (embedding_name, embedding_pretrained, tokenizer_name, device), description_batch_size=description_batch, embedding_batch_size=de_embedding_batch)
    print("Time to extract description and embeddings: ", timer()-start)

    object_folder = OBJECTS_VOLUME_DIR
    batch_object = BATCH_SIZE_YOLO
    yolo_root = MODEL_YOLO_ROOT
    yolo_model = MODEL_YOLOV8
    start = timer()
    # object_detection(keyframe_folder, object_folder, models=yolo_model, batch_size=batch_object, model_dir=yolo_root)
    print("Time to extract objects: ", timer()-start)

    ocr_folder = OCR_VOLUME_DIR
    threshold_ocr = THRESHOLD_SCORE
    start = timer()
    # extract_text(keyframe_folder, ocr_folder, threshold_score=threshold_ocr)
    print("Time to extract OCR: ", timer()-start)

    ocr_embedding_folder = OCR_EMBEDDING_VOLUME_DIR
    start = timer()
    ocr_embedding_batch = OCR_EMBEDDING_BATCH
    # extract_ocr_embedding(ocr_folder, ocr_embedding_folder, batch_size=ocr_embedding_batch)
    print("Time to extract OCR embeddings: ", timer()-start)

    print("Total time: ", timer()-s)

    database_folder = DATABASE_VOLUME_DIR
    num_process_db = NUM_PROCESSES_DB
    start = timer()
    create_database_data(csv_folder, de_embedding_folder, EMBEDDING_V2, object_folder, ocr_embedding_folder, database_folder)
    print("Time to create database: ", timer()-start)

    database_folder = DATABASE_NEXTFRAME_VOLUME_DIR
    max_frames = MAX_NEXTFRAME
    num_processes_nextframe = NUM_PROCESSES_NEXTFRAME
    start = timer()
    create_database_data_nextframe(csv_folder, de_embedding_folder, EMBEDDING_V2, object_folder, ocr_embedding_folder, database_folder, max_frames=max_frames)
    print("Time to create database nextframe: ", timer()-start)

    print("Total time: ", timer()-s)
    print("Done.")
