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
    def to_dict(self):
        return {
            "id": self.id,
            "path": self.path,
            "frame_number": self.frame_number,
            "objects_path": self.objects_path,
            "video_id": self.video_id
            # các cột khác
        }
