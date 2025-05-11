import os
import urllib.parse
import redis
# import secrets
# from typing import Annotated, Any, Literal
# from pydantic import computed_field
# from pydantic_settings import BaseSettings
import logging
class Settings:
    MYSQL_USER = os.getenv('MYSQL_USER')
    MYSQL_ROOT_PASSWORD = os.getenv('MYSQL_ROOT_PASSWORD')
    HOST = os.getenv('MYSQL_HOST')
    CLOUD_HOST_DATA = os.getenv('CLOUD_HOST_DATA')
    MYSQL_PORT = os.getenv('MYSQL_PORT')
    MYSQL_DATABASE = os.getenv('MYSQL_DATABASE')
    PORT = os.getenv('PORT')
    # FRAMES_VOLUME_DIR = os.getenv('FRAMES_VOLUME_DIR')
    VIDEOS_VOLUME_DIR = os.getenv('VIDEOS_VOLUME_DIR')
    # CSV_FRAMES_PATH = os.getenv('CSV_FRAMES')
    CSV_VIDEOS_PATH = os.getenv('CSV_VIDEOS')

    REDIS_PORT: int = 6379  
    REDIS_DB: int = 0               # Cơ sở dữ liệu Redis
    REDIS_PASSWORD: str = ''        # Mật khẩu Redis nếu cần
    @property
    def REDIS_HOST(self) -> str:
        return 'redis'
    @property
    def server_host(self) -> str:
        return f"http://{self.HOST}:{self.PORT}"
    
    @property
    def cloud_host(self) -> str:
        return f"http://{self.CLOUD_HOST_DATA}:{self.PORT}"
    
    @property
    def BACKEND_CORS_ORIGINS(self) -> list[str]:
        if self.HOST:
            return [f"http://{self.HOST}", f"http://{self.HOST}/home"]
        return []
    
    @property
    def MYSQL_PASSWORD_ENCODE(self) -> str:
        return urllib.parse.quote(self.MYSQL_ROOT_PASSWORD.encode("utf-8"))
    
    @property
    def SQLALCHEMY_DATABASE_URI(self):
        return f"mysql+pymysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD_ENCODE}@{self.HOST}:{self.MYSQL_PORT}/{self.MYSQL_DATABASE}?connect_timeout=60"
    
    @property
    def videos_csv(self):
        return self.CSV_VIDEOS_PATH

settings = Settings()

# Kết nối đến Redis server
redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    password=settings.REDIS_PASSWORD
)

