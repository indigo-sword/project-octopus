from sqlalchemy import Column, String
from sqlalchemy.orm import Session
from db_manager import Base
from uuid import uuid4

class User(Base):
    __tablename__ = 'users'
    id = Column(String, primary_key=True, default=lambda: str(uuid4()), unique=True)
    username = Column(String)
    password = Column(String)
    email = Column(String)

    def __init__(self, username: str, password: str, email: str):
        self.username = username
        self.password = password
        self.email = email

    def save(self, session: Session):
        session.add(self)
        session.commit()