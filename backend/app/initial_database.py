from app.core.database import load_data_from_folders
from app.core.config import settings
import logging
import os

load_data_from_folders(frames_folder=f"{settings.FRAMES_VOLUME_DIR}", videos_folder=f"{settings.VIDEOS_VOLUME_DIR}")