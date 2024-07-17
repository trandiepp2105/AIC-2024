from fastapi import Query
from typing import List, Any, Optional
from sqlmodel import Session, select
from models import FrameBase, Frame
from sqlalchemy.sql import func

def create_frame(session: Session, frame_create: FrameBase):
    frame = Frame.model_validate(frame_create)
    session.add(frame)
    session.commit()
    session.refresh(frame)
    return frame

def read_frames(
    session: Session,
    limit: int = Query(10, ge=1, le=100),  # Giới hạn kết quả từ 1 đến 100
    offset: int = Query(0, ge=0)  # Bắt đầu từ 0
):
    """
    Retrieve frames with pagination support.
    """
    statement = select(Frame).limit(limit).offset(offset)
    results = session.exec(statement).all()
    return results

def get_frame(session: Session, frame_id: int) -> Any:
    """
    Retrieve frames by a list of frame_ids.
    """
    statement = select(Frame).where(Frame.id == frame_id)
    results = session.exec(statement).first()
    return results

def get_mul_frames( session: Session, frame_ids: List[int]) -> Any:
    """
    Retrieve frames by a list of frame_ids.
    """
    # statement = select(Frame).where(Frame.id.in_(frame_ids))
    # results = session.exec(statement).all()
    # return results
    resuilt = []
    for frame_id in frame_ids:
        statement = select(Frame).where(Frame.id == frame_id)
        result = session.exec(statement).first()
        resuilt.append(result)
    return resuilt
        

def count_frames(session: Session) -> int:
    """
    Count the total number of frames.
    """
    statement = select(func.count(Frame.id))
    result = session.execute(statement).scalar_one()  # Sử dụng scalar_one() để lấy giá trị đơn
    return result
