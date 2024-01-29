from sqlalchemy import Column, Integer, String
from db_manager import Base
from uuid import uuid4

class Level(Base):
    __tablename__ = 'levels'
    id = Column(String, primary_key=True, default=str(uuid4()), unique=True)
    level = Column(Integer)

    def __init__(self, level: int=0):
        self.level = level
