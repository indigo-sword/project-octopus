from node import Node
from uuid import uuid4

from db_manager import Base
from sqlalchemy import Column, Integer, String, Double, ForeignKey, update
from sqlalchemy.orm import relationship, Session

# paths WILL need to be stored in a DB.
class Path:
    __tablename__ = 'node_links'
    def __init__(self, description: str=""):
        self.node_id_sequence = []
        self.description = description

    def add_node(self, node: Node):
        self.node_id_sequence.append(node.id)