from node import Node
from uuid import uuid4

from db_manager import Base
from sqlalchemy import Column, Integer, String, Double, ForeignKey, update, Table, DateTime
from sqlalchemy.orm import relationship, Session
from user import User
from datetime import datetime

class Path(Base):
    __tablename__ = 'paths'
    id = Column(String, primary_key=True, default=lambda: str(uuid4()), unique=True)
    user_id = Column(Integer, ForeignKey('users.username'))
    description = Column(String)
    ts = Column(DateTime, default=datetime.utcnow)

    playcount = Column(Integer)
    num_ratings = Column(Integer)
    rating = Column(Double)

    user = relationship('User')

    def __init__(self, session: Session, user: User, description: str=""):
        self.user = user
        self.description = description
        self.position = 0

        self.playcount = 0
        self.num_ratings = 0
        self.rating = 0

        self.save(session)

    def save(self, session: Session):
        session.add(self)
        session.commit()

    def add_node(self, node: Node, session: Session):
        # check for node in path
        q = session.query(path_node_association).filter(path_node_association.c.node_id == node.id).filter(path_node_association.c.path_id == self.id).first()
        if q is not None:
            raise Exception("Node already in path")
        
        session.execute(
            path_node_association.insert()
            .values(path_id=self.id, node_id=node.id, position=self.position)
        )

        self.position += 1

        session.commit()

    def get_node_sequence(self, session: Session):
        return session.query(path_node_association).filter(path_node_association.c.path_id == self.id).order_by(path_node_association.c.position).all()
    
    def __repr__(self):
        return f"Path({self.id}, {self.user_id}, {self.description}, {self.ts})"
    
    def update_playcount(self, session: Session):
        result = session.execute(
            update(Path)
            .where(Path.id == self.id)
            .values(playcount=Path.playcount + 1)
            .returning(Path.playcount)
        )
        
        self.playcount = result.scalar()
            
        session.commit()

    def get_playcount(self):
        return self.playcount
    
    def update_rating(self, rating: int, session: Session):
        if rating < 0 or rating > 10:
            raise Exception("Rating must be between 0 and 10")
        
        result = session.execute(
            update(Path)
            .where(Path.id == self.id)
            .values(rating=(Path.rating * Path.num_ratings + rating) / (Path.num_ratings + 1), num_ratings=Path.num_ratings + 1)
            .returning(Path.rating, Path.num_ratings)
        )

        self.rating, self.num_ratings = result.fetchone()
            
        session.commit()

    def get_rating(self):
        return round(self.rating, 2)
    
path_node_association = Table(
    'path_node_association',
    Base.metadata,
    Column('path_id', String, ForeignKey('paths.id')),
    Column('node_id', String, ForeignKey('nodes.id')),
    Column('position', Integer)                         
)
