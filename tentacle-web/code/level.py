from sqlalchemy import Column, Integer, String
from db_manager import Base
from uuid import uuid4

from sqlalchemy.orm import Session

class Level(Base):
    __tablename__ = 'levels'
    id = Column(String, primary_key=True, default=lambda: str(uuid4()), unique=True)
    level = Column(Integer)

    def __init__(self, session: Session, level: int=0):
        self.level = level
        self._save(session)

    def _save(self, session: Session):
        session.add(self)
        session.commit()

    # create / link level func needed
