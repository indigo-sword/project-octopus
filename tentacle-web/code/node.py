from level import Level
from user import User
from uuid import uuid4

from db_manager import Base
from sqlalchemy import Column, Integer, String, Double, ForeignKey, update, or_
from sqlalchemy.orm import relationship, Session

class NodeLink(Base):
    __tablename__ = 'node_links'
    id = Column(String, primary_key=True, default=lambda: str(uuid4()), unique=True) # id of the link
    origin_id = Column(Integer, ForeignKey('nodes.id'))                      # id of the origin node
    destination_id = Column(Integer, ForeignKey('nodes.id'))                 # id of the destination node
    description = Column(String)

    origin = relationship('Node', foreign_keys=[origin_id])
    destination = relationship('Node', foreign_keys=[destination_id])

    def __init__(self, origin, destination, description):
        self.origin_id = origin.id
        self.destination_id = destination.id
        self.description = description

class Node(Base):
    __tablename__ = 'nodes'
    id = Column(String, primary_key=True, default=lambda: str(uuid4()), unique=True)
    level_id = Column(Integer, ForeignKey('levels.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    playcount = Column(Integer)
    num_ratings = Column(Integer)
    rating = Column(Double)
    description = Column(String)

    level = relationship('Level')
    user = relationship('User')

    def __init__(self, session: Session, level: Level, user: User, description: str=""):
        self.level = level  
        self.user = user 

        # attributes that will change over time
        self.playcount = 0
        self.num_ratings = 0
        self.rating = 0                
        self.description = description

        self._save(session)

    def __repr__(self):
        return "<Node(id='%s', level='<%s, %s>', user='<%s, %s, %s, %s>', playcount='%s', num_ratings='%s', rating='%s', description='%s')>" % (
            self.id, self.level.id, self.level.level, self.user.id, self.user.username, self.user.password, self.user.email, self.playcount, self.num_ratings, self.rating, self.description)

    def _save(self, session: Session):
        session.add(self) # add node to session
        session.commit()

    def link(self, node: 'Node', description: str, session: Session):
        ''' link self to a next node '''
        if node == self:
            raise Exception("Cannot link node to itself")
        
        # check if destination already has a link to self
        result = session.query(NodeLink).filter(
            or_(
                (NodeLink.destination_id == self.id and NodeLink.origin_id == node.id),
                (NodeLink.destination_id == node.id and NodeLink.origin_id == self.id)
            )
        ).all()
        
        if result:
            raise Exception("Nodes are already linked.")
        
        link = NodeLink(origin=self, destination=node, description=description)
        session.add(link)  # add link to session
        session.commit()   # commit    

    def update_playcount(self, session: Session):
        result = session.execute(
            update(Node)
            .where(Node.id == self.id)
            .values(playcount=Node.playcount + 1)
            .returning(Node.playcount)
        )
        
        self.playcount = result.scalar()
        session.commit()

    def get_playcount(self):
        return self.playcount
    
    def update_rating(self, rating: int, session: Session):
        if rating < 0 or rating > 10:
            raise Exception("Rating must be between 0 and 10")
        
        result = session.execute(
            update(Node)
            .where(Node.id == self.id)
            .values(rating=(Node.rating * Node.num_ratings + rating) / (Node.num_ratings + 1), num_ratings=Node.num_ratings + 1)
            .returning(Node.rating, Node.num_ratings)
        )

        self.rating, self.num_ratings = result.fetchone()
        session.commit()

    def get_rating(self):
        return round(self.rating, 2)