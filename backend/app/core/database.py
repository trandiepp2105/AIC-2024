from sqlmodel import SQLModel, create_engine, Session
import os
import json
import logging
from app.core.config import settings, redis_client
from app.models import Video
import pandas as pd
from timeit import default_timer as timer

DATABASE_URL = settings.SQLALCHEMY_DATABASE_URI
engine = create_engine(DATABASE_URL, echo=True)

def insert_in_batches(session, data, batch_size=100000):
    for i in range(0, len(data), batch_size):
        batch = data[i:i+batch_size]
        session.bulk_save_objects(batch)
    session.commit()

def cache_data(videos_to_add, frames_to_add):
    pipe = redis_client.pipeline()  # Create a pipeline for batch operations

    for video in videos_to_add:
        key = f"video:{video.id}"
        pipe.set(key, json.dumps(video.to_dict()))
        pipe.persist(key)

    for frame in frames_to_add:

        key = f"frame:{frame.video_name}-{frame.frame_number}"
        pipe.set(key, json.dumps(frame.to_dict()))
        pipe.persist(key)

    pipe.execute()  # Execute all batch operations at once


def load_data_from_folders(videos_csv: str):
    print("STARTING INSERT DATA TO SQL!")
    
    video_url_base = f"{settings.cloud_host}/stream/videos"
    
    videos_to_add = []

    # Đọc dữ liệu từ CSV và thu thập thông tin video
    videos_df = pd.read_csv(videos_csv)
    list_videos = videos_df[['video_name', 'fps']].to_dict(orient='records')

    # Tạo danh sách các đối tượng Video với fps
    videos_to_add = [
        Video(
            path=f"{video_url_base}/{video['video_name']}.mp4", 
            video_name=video['video_name'],
            fps=video['fps']
        ) for video in list_videos
    ]
    
    # Thêm video vào database
    with Session(engine) as session:
        try:
            # Insert video vào MySQL
            start = timer()
            insert_in_batches(session=session, data=videos_to_add)
            print("Time to insert videos_to_add: ", timer() - start)
        finally:
            session.close()