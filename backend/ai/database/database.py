from pathlib import Path
import sys
current_dir = Path(__file__).resolve().parent
app_dir = current_dir / '../app'
sys.path.append(str(app_dir))

from ai.configs import *
from pymilvus import connections, Collection, FieldSchema, CollectionSchema, DataType, utility
import pickle
import numpy as np
import os
import logging
import math

table = None

print("START ai database")

# try:
#     with Session(engine) as session:
#         statement = select(Frame)
#         table = session.exec(statement).all()
# except Exception as e:
#     print(f"Error: {e}")


connect = connections.connect("default", host="milvus-standalone", port="19530")

collection_name = "vector_db"

fields = [
    FieldSchema(name="idx", dtype=DataType.INT64, is_primary=True, auto_id=True),
    FieldSchema(name="video", dtype=DataType.VARCHAR, max_length=20),
    FieldSchema(name="frame", dtype=DataType.VARCHAR, max_length=20),
    FieldSchema(name="second", dtype=DataType.FLOAT),
    FieldSchema(name="frame_embedding", dtype=DataType.FLOAT_VECTOR, dim=CLIP_DIM),
    # FieldSchema(name="description_embedding", dtype=DataType.FLOAT_VECTOR, dim=CLIP_DIM),
    # FieldSchema(name="clip4clip", dtype=DataType.FLOAT_VECTOR, dim=CLIP4CLIP_DIM),
    FieldSchema(name="time", dtype=DataType.INT64),
    # FieldSchema(name="audio_embedding", dtype=DataType.VARCHAR, max_length=30000)
]

schema = CollectionSchema(fields=fields)

collection = Collection(collection_name, schema=schema)

nlist = math.ceil((NUM_ENTITIES**0.5)/4)

index_params = {
    "metric_type": "IP",
    "index_type": "IVF_FLAT",
    "params": {"nlist": nlist}
}

collection.create_index(field_name="frame_embedding", index_params=index_params)
# collection.create_index(field_name="description_embedding", index_params=index_params)
# collection.create_index(field_name="clip4clip", index_params=index_params)

def load_data(data_folder, collection):
    i = 0
    for root, dirs, files in os.walk(data_folder):
        for file in files:
            if file.endswith(".pkl"):
                with open(os.path.join(root, file), 'rb') as f:
                    data = pickle.load(f)
                    collection.insert(data)
                print(f"Inserting {file}")
    collection.load()
    collection.flush()

load_data(DATABASE_VOLUME_DIR, collection)
collection.release()

connections.disconnect("default")

print("END ai database")