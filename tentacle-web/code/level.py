from sqlalchemy import Column, Integer
from db_manager import Base

class Level(Base):
    __tablename__ = 'levels'
    id = Column(Integer, primary_key=True)
    level = Column(Integer)
