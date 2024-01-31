from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db_manager import Base
from uuid import uuid4
import os
from user import User

from sqlalchemy.orm import Session

class Level(Base):
    __tablename__ = 'levels'
    id = Column(String, primary_key=True, default=lambda: str(uuid4()), unique=True)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship('User')

    def __init__(self, session: Session, user: User, lvl_buf: bytes=b''):
        ''' lvl_buf is the level file '''
        self.user = user
        self._save(session)
        self._write_file(lvl_buf)

    def _write_file(self, lvl_buf: bytes):
        # create level file based on some variable passed here (will do tests later w/ api)
        f = open(self.get_file_path(), 'wb')
        f.write(lvl_buf)

    def _save(self, session: Session):
        session.add(self)
        session.commit()

    def get_file_path(self):
        # get project root
        root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        # go to /levels/self.id.level
        return root + "/levels/" + self.id + ".level"
    
    def __repr__(self):
        return f"Level({self.id}, {self.user_id})"
    
