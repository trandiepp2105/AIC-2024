from app.core.database import load_data_from_folders
from app.core.config import settings
import logging
import os

load_data_from_folders(videos_csv=f"{settings.videos_csv}")