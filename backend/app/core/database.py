from sqlmodel import SQLModel, create_engine, Session
import logging
import os
from app.core.config import settings
from app.models import Video, Frame

DATABASE_URL = settings.SQLALCHEMY_DATABASE_URI

engine = create_engine(DATABASE_URL, echo=True)

# Khởi tạo cơ sở dữ liệu
# def init_db() -> None:
#     try:
#         SQLModel.metadata.create_all(engine)
#         logging.info("Database tables created successfully")
#     except Exception as e:
#         logging.error(f"Error creating database tables: {e}")

def load_data_from_folders(frames_folder: str, videos_folder: str):
    test = "load"
    logging.info(test)
    
    video_url_base = f"{settings.server_host}/videos"
    frame_url_base = f"{settings.server_host}/frames"
    
    with Session(engine) as session:
        # Load video data
        for video_name in os.listdir(frames_folder):
            video_file = f"{video_name}.mp4"
            video_path = os.path.join(videos_folder, video_file)
            if os.path.isfile(video_path):
                video_url = f"{video_url_base}/{video_file}"
                test = f"video URL: {video_url}"
                logging.info(test)
                
                # Create Video record
                video = Video(path=video_url)
                session.add(video)
                session.commit()
                session.refresh(video)

                # Load frame data for this video
                video_frames_folder = os.path.join(frames_folder, video_name)
                if os.path.isdir(video_frames_folder):
                    for frame_file in os.listdir(video_frames_folder):
                        frame_path = os.path.join(video_frames_folder, frame_file)
                        frame_number = int(os.path.splitext(frame_file)[0])  # Get frame_number from filename
                        frame_url = f"{frame_url_base}/{video_name}/{frame_file}"
                        objects_path = ""  # Set this value according to your requirements

                        # Create Frame record
                        frame = Frame(
                            path=frame_url,
                            frame_number=frame_number,
                            objects_path=objects_path,
                            video_id=video.id
                        )
                        session.add(frame)

        session.commit()

