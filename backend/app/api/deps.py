from core.database import engine
from fastapi import Depends, HTTPException, status
from sqlmodel import Session
from typing import Annotated


def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]