import os
import urllib.parse
# import secrets
# from typing import Annotated, Any, Literal
# from pydantic import computed_field
# from pydantic_settings import BaseSettings
import logging
class Settings:
    MYSQL_USER = os.getenv('MYSQL_USER')
    MYSQL_ROOT_PASSWORD = os.getenv('MYSQL_ROOT_PASSWORD')
    HOST = os.getenv('HOST')
    MYSQL_PORT = os.getenv('MYSQL_PORT')
    MYSQL_DATABASE = os.getenv('MYSQL_DATABASE')
    PORT = os.getenv('PORT')
    FRAMES_VOLUME_DIR = os.getenv('FRAMES_VOLUME_DIR')
    VIDEOS_VOLUME_DIR = os.getenv('VIDEOS_VOLUME_DIR')
    @property
    def server_host(self) -> str:
        return f"http://{self.HOST}:{self.PORT}"
    
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

settings = Settings()
logging.error(f"ERROR: {settings.MYSQL_ROOT_PASSWORD}" )