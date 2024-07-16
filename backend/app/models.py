from sqlmodel import Field, SQLModel
from typing import Optional

class VideoBase(SQLModel):
    path: str

class Video(VideoBase, table=True):
    id: int = Field(default=None, primary_key=True)

class FrameBase(SQLModel):
    path: str
    frame_number: int 
    objects_path: str
    video_id: int = Field(default=None, foreign_key="video.id")


class Frame(FrameBase, table=True):
    id: int = Field(default=None, primary_key=True)
