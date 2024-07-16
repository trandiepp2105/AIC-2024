from sqlmodel import SQLModel, create_engine, Session
import urllib.parse
import logging
from core.config import settings

DATABASE_URL = settings.SQLALCHEMY_DATABASE_URI

engine = create_engine(DATABASE_URL, echo=True)

# Khởi tạo cơ sở dữ liệu
def init_db() -> None:
    try:
        SQLModel.metadata.create_all(engine)
        logging.info("Database tables created successfully")
    except Exception as e:
        logging.error(f"Error creating database tables: {e}")

