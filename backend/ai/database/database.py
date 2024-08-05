from pathlib import Path
import sys
current_dir = Path(__file__).resolve().parent
app_dir = current_dir / '../app'
sys.path.append(str(app_dir))

from app.models import Frame, Video
from sqlmodel import Session, select
from app.core.database import engine

from ai.configs import *
from pymilvus import connections, Collection, FieldSchema, CollectionSchema, DataType, utility
import pickle
import numpy as np
import json

table = None

print("RUN ai database")

try:
    with Session(engine) as session:
        statement = select(Frame)
        table = session.exec(statement).all()
except Exception as e:
    print(f"Error: {e}")


connections.connect("default", host="milvus-standalone", port="19530")

collection_name = "search_collection"

if collection_name in utility.list_collections():
    try:
        collection = Collection(collection_name)
        collection.drop()
    except Exception as e:
        print(f"Error: {e}")

fields = [
    FieldSchema(name="idx", dtype=DataType.INT64, is_primary=True),
    FieldSchema(name="frame_embedding", dtype=DataType.FLOAT_VECTOR, dim=768),
    FieldSchema(name="object_detection", dtype=DataType.FLOAT_VECTOR, dim=80),
    FieldSchema(name="ocr_embedding", dtype=DataType.FLOAT_VECTOR, dim=768)
]

schema = CollectionSchema(fields=fields)

collection = Collection(collection_name, schema=schema)

index_params = {
    "metric_type": "IP",
    "index_type": "IVF_FLAT",
    "params": {"nlist": 1024}
}

object_detection_index_params = {
    "metric_type": "L2",
    "index_type": "IVF_FLAT",
    "params": {"nlist": 1024}
}

ocr_embedding_index_params = {
    "metric_type": "IP",
    "index_type": "IVF_FLAT",
    "params": {"nlist": 1024}
}

collection.create_index(field_name="frame_embedding", index_params=index_params)
collection.create_index(field_name="object_detection", index_params=object_detection_index_params)
collection.create_index(field_name="ocr_embedding", index_params=ocr_embedding_index_params)

def get_video_frame(path):
    paths = path.split('/')
    video_id = paths[-2]
    frame_id = paths[-1].split('.')[0]
    return video_id, frame_id

def get_embedding(video_id, frame_id):
    embedding_path = f"{EMBEDDING_FOLDER}/{video_id}/{frame_id}.npy"
    embedding = np.load(embedding_path)
    return embedding

def get_object_detection(video_id, frame_id):
    object_detection_path = f"{OBJECTS_FOLDER}/{video_id}/{frame_id}.npy"
    object_detection = np.load(object_detection_path)
    return object_detection

def get_ocr_embedding(video_id, frame_id):
    ocr_embedding_path = f"{OCR_EMBEDDING_FOLDER}/{video_id}/{frame_id}.npy"
    ocr_embedding = np.load(ocr_embedding_path)
    return ocr_embedding
    
entity = [[],[],[],[]]

count = 0
mut = 100

for row in table:
    video_id, frame_id = get_video_frame(row.path)
    embedding = get_embedding(video_id, frame_id)
    object_detection = get_object_detection(video_id, frame_id)
    ocr_embedding = get_ocr_embedding(video_id, frame_id)
    entity[0].append(int(row.id))
    entity[1].append(embedding)
    entity[2].append(object_detection)
    entity[3].append(ocr_embedding)

    count += 1
    if count % mut == 0:
        print(f"Inserting {mut} frames")
        collection.insert(entity)
        entity = [[],[],[],[]]

collection.insert(entity)

collection.load()

connections.disconnect("default")

print("END ai database")