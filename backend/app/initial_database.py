from app.core.database import load_data_from_folders
from app.core.config import settings
import logging
import os

# # Đường dẫn tới thư mục videos và frames trong container
# videos_path = r"C:\AIC-2024-DATA\videos"
# frames_path = r"C:\AIC-2024-DATA\frames"
# logging.error("error")
# # Liệt kê các tệp trong thư mục videos
# video_files = os.listdir(frames_path)
# logging.error("Video files:", video_files)


load_data_from_folders(frames_folder=f"{settings.FRAMES_VOLUME_DIR}", videos_folder=f"{settings.VIDEOS_VOLUME_DIR}")