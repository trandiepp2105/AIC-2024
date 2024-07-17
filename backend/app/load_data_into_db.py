from core.database import load_data_from_folders
from core.config import settings

load_data_from_folders(frames_folder=settings.FRAMES_PATH, videos_folder=settings.VIDEOS_PATH)