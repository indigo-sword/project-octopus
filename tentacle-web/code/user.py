from sqlalchemy import Column, String
from db_manager import Base
from uuid import uuid4

class User(Base):
    __tablename__ = 'users'
    id = Column(String, primary_key=True, default=str(uuid4()), unique=True)
    username = Column(String)
    password = Column(String)
    email = Column(String)

    def __init__(self, username: str, password: str, email: str):
        self.username = username
        self.password = password
        self.email = email