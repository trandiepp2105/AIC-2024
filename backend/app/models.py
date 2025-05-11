from sqlmodel import Field, SQLModel
from typing import Optional
import json
from app.core.config import redis_client

class TeamPickedFrame(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    video_name: str
    frame_number: int
    priority: int
    query_index: int
    mode: str
    answer: Optional[str] = Field(default=None)

class Video(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    path: str
    video_name: str
    fps: float
    def to_dict(self):
        return {
            "id": self.id,
            "path": self.path,
            "video_name": self.video_name,
            "fps": self.fps
        }


# class FrameBase(SQLModel):
#     path: str
#     frame_number: int 
#     objects_path: str
#     video_name: str
#     video_id: int = Field(default=None, foreign_key="video.id")

# class Frame(FrameBase, table=True):
#     id: int = Field(default=None, primary_key=True)
#     duration: float = Field(default=None)  # Tính duration mặc định
    
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         # Tính toán duration từ frame_number
#         FPS = 25
#         if not self.duration:
#             self.duration = self.frame_number / FPS

#     def to_dict(self):
#         return {
#             "id": self.id,
#             "path": self.path,
#             "video_name": self.video_name,
#             "frame_number": self.frame_number,
#             "objects_path": self.objects_path,
#             "video_id": self.video_id,
#             "duration": self.duration,
#         }
