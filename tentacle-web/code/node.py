from level import Level
from user import User

# All of this code is not database-ready yet. 
# we need to create code to initiate empty guys.
# we need to create code to load, save, update and delete them to the database.

# OR: we could use an ORM like SQLAlchemy to do this for us, so the objects will be
# stored and we don't have to worry about it.
        ## ^^ i chose this option btw

from db_manager import Base, engine
from sqlalchemy import Column, Integer, String, ForeignKe, update
from sqlalchemy.orm import relationship, Session

class NodeLink(Base):
    __tablename__ = 'node_links'
    id = Column(Integer, primary_key=True)                                  # id of the link
    origin_id = Column(Integer, ForeignKey('nodes.id'))                     # id of the origin node
    destination_id = Column(Integer, ForeignKey('nodes.id'))                # id of the destination node
    description = Column(String)

    origin = relationship('Node', foreign_keys=[origin_id])
    destination = relationship('Node', foreign_keys=[destination_id])

    def __init__(self, origin, destination, description):
        self.origin_id = origin.id
        self.destination_id = destination.id
        self.description = description

class Node(Base):
    __tablename__ = 'nodes'
    id = Column(Integer, primary_key=True)
    level_id = Column(Integer, ForeignKey('levels.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    playcount = Column(Integer)
    total_rating = Column(Integer)
    ratings = Column(Integer)
    description = Column(String)

    level = relationship('Level')
    user = relationship('User')

    def __init__(self, level: Level, user: User, description: str=""):
        self.level = level  
        self.user = user 

        # attributes that will change over time
        self.playcount = 0
        self.total_rating = 0
        self.ratings = 0                
        self.description = description   

    def link(self, node: 'Node', description: str, session: Session):
        ''' link self to a next node '''
        if node == self:
            raise Exception("Cannot link node to itself")
        
        link = NodeLink(origin=self, destination=node, description=description)
        session.add(link)  # add link to session
        session.commit()   # commit    

    def update_playcount(self, session: Session):
        result = session.execute(
            # execute update, will do later
        )
        self.playcount += 1

    def get_rating(self):
        return round(self.total_rating / self.ratings, 1)
    
    def update_rating(self, rating: int):
        self.total_rating += rating
        self.ratings += 1