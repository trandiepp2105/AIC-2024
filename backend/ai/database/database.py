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

table = None

print("RUN ai database")
with Session(engine) as session:
    statement = select(Frame)
    table = session.exec(statement).all()

for i in table:
    print(i.id, i.path)

connections.connect("default", host="milvus-standalone", port="19530")

collection_name = "search_collection"

if collection_name in utility.list_collections():
    collection = Collection(collection_name)
    collection.drop()

collection = Collection(collection_name, schema=CollectionSchema([
    FieldSchema("id", DataType.INT64, is_primary=True),
    FieldSchema("embedding", DataType.FLOAT_VECTOR, dim=768)
]))

index_params = {
    "metric_type": "IP",
    "index_type": "IVF_FLAT",
    "params": {"nlist": 1024}
}

collection.create_index(field_name="embedding", index_params=index_params)

def get_video_frame(path):
    paths = path.split('/')
    video_id = paths[-2]
    frame_id = paths[-1].split('.')[0]
    return video_id, frame_id

def get_embedding(video_id, frame_id):
    embedding_path = f"{EMBEDDING_FOLDER}/{video_id}/{frame_id}.pickle"
    with open(embedding_path, 'rb') as f:
        return pickle.load(f)

for row in table:
    video_id, frame_id = get_video_frame(row.path)
    embedding = get_embedding(video_id, frame_id)
    collection.insert([{"id": row.id, "embedding": embedding}])

connections.close()
print("END ai database")