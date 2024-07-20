from app.models import Frame
from app.crud import read_frames
from app.api.deps import get_session
from sqlmodel import Session, select
from app.core.database import engine
with Session(engine) as session:
    statement = select(Frame)
    results = session.exec(statement).all()
    print("rel: ")
    print(results[0])