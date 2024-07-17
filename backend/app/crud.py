from typing import List, Any
from sqlmodel import Session, select
from models import FrameBase, Frame
from api.deps import SessionDep


def create_frame(session: Session, frame_create: FrameBase):
    frame = Frame.model_validate(frame_create)
    session.add(frame)
    session.commit()
    session.refresh(frame)
    return frame

def get_frame(session: Session, frame_id: int) -> Any:
    """
    Retrieve frames by a list of frame_ids.
    """
    statement = select(Frame).where(Frame.id == frame_id)
    results = session.exec(statement).first()
    return results

def get_frames( session: Session, frame_ids: List[int]) -> Any:
    """
    Retrieve frames by a list of frame_ids.
    """
    statement = select(Frame).where(Frame.id.in_(frame_ids))
    results = session.exec(statement).all()
    return results

def get_all_frames(session: Session) -> Any:
    """
    Retrieve all frames.
    """
    statement = select(Frame)
    results = session.exec(statement).all()
    return results

# rel = get_all_frames(SessionDep())
# print(rel)