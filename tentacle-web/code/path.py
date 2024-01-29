from node import Node
from uuid import uuid4

from db_manager import Base
from sqlalchemy import Column, Integer, String, Double, ForeignKey, update, Table
from sqlalchemy.orm import relationship, Session

class Path:
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
        session.execute(
            path_node_association.insert()
            .values(path_id=self.id, node_id=node.id, position=self.position)
        )

        self.position += 1

path_node_association = Table(
    'path_node_association',
    Base.metadata,
    Column('path_id', String, ForeignKey('paths.id')),
    Column('node_id', String, ForeignKey('nodes.id')),
    Column('position', Integer)                         
)