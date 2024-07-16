from sqlmodel import SQLModel, create_engine, Session
import urllib.parse
import logging
import os
from core.config import settings
from models import Video, Frame

DATABASE_URL = settings.SQLALCHEMY_DATABASE_URI

engine = create_engine(DATABASE_URL, echo=True)

# Khởi tạo cơ sở dữ liệu
def init_db() -> None:
    try:
        SQLModel.metadata.create_all(engine)
        logging.info("Database tables created successfully")
    except Exception as e:
        logging.error(f"Error creating database tables: {e}")

def load_data_from_folders(frames_folder: str, videos_folder: str):
    test = f"load"
    logging.info(test)
    with Session(engine) as session:
        # Load video data
        for video_name in os.listdir(frames_folder):
            video_path = os.path.join(videos_folder, f"{video_name}.mp4")
            if os.path.isfile(video_path):
                test = f"video path: {video_path}"
                logging.info(test)
                # Create Video record
                video = Video(path=video_path)
                session.add(video)
                session.commit()
                session.refresh(video)

                # Load frame data for this video
                video_frames_folder = os.path.join(frames_folder, video_name)
                if os.path.isdir(video_frames_folder):
                    for frame_file in os.listdir(video_frames_folder):
                        frame_path = os.path.join(video_frames_folder, f"{frame_file}")
                        frame_number = int(os.path.splitext(frame_file)[0])  # Get frame_number from filename
                        objects_path = ""  # Set this value according to your requirements

                        # Create Frame record
                        frame = Frame(
                            path=frame_path,
                            frame_number=frame_number,
                            objects_path=objects_path,
                            video_id=video.id
                        )
                        session.add(frame)

        session.commit()
