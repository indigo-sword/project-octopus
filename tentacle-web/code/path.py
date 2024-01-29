from node import Node
from uuid import uuid4

from db_manager import Base
from sqlalchemy import Column, Integer, String, Double, ForeignKey, update, Table
from sqlalchemy.orm import relationship, Session

class Path(Base):
    __tablename__ = 'paths'
    id = Column(String, primary_key=True, default=str(uuid4()), unique=True)
    description = Column(String)

    def __init__(self, description: str=""):
        self.description = description
        self.position = 0

    def save(self, session: Session):
        session.add(self)
        session.commit()

    def add_node(self, node: Node, session: Session):
        node.save(session)

        # check for node in path
        if session.query(path_node_association).filter(path_node_association.c.node_id == node.id).first() is not None:
            raise Exception("Node already in path")
        
        session.execute(
            path_node_association.insert()
            .values(path_id=self.id, node_id=node.id, position=self.position)
        )

        session.commit()

        self.position += 1

    def get_node_sequence(self, session: Session):
        return session.query(path_node_association).filter(path_node_association.c.path_id == self.id).order_by(path_node_association.c.position).all()
    
path_node_association = Table(
    'path_node_association',
    Base.metadata,
    Column('path_id', String, ForeignKey('paths.id')),
    Column('node_id', String, ForeignKey('nodes.id')),
    Column('position', Integer)                         
)
