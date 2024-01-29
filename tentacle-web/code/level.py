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

# 1) save level file in tentacle-web/levels with level id as name
# 2) create level object in db
# 3) retrieve from db and send to client