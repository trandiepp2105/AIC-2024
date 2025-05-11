from sqlmodel import SQLModel, create_engine, Session
import os
import json
import logging
from app.core.config import settings, redis_client
from app.models import Video, Frame
import pandas as pd
from timeit import default_timer as timer

DATABASE_URL = settings.SQLALCHEMY_DATABASE_URI
engine = create_engine(DATABASE_URL, echo=True)

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


def load_data():
    with Session(engine) as session:
        try:
            print("STARTING INSERT DATA TO SQL!")
            start = timer()
            videos_to_cache = session.query(Video).all()
            print("Time to query data: ", timer()-start)
            start = timer()
            frames_to_cache = session.query(Frame).all()
            print("Time to query data: ", timer()-start)
            # Cache data
            start = timer()
            cache_data(videos_to_cache, frames_to_cache)
            print("Time to cache data: ", timer()-start)
        finally:
            session.close()


if __name__ == "__main__":
    load_data()
