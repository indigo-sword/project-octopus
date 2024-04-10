from node import Node
from uuid import uuid4

from db_manager import Base
from sqlalchemy import (
    Column,
    Integer,
    String,
    Double,
    ForeignKey,
    update,
    Table,
    DateTime,
)
from sqlalchemy.orm import relationship, Session
from user import User
from datetime import datetime


class Path(Base):
    __tablename__ = "paths"
    id = Column(String, primary_key=True, default=lambda: str(uuid4()), unique=True)
    user_id = Column(String, ForeignKey("users.username"))
    description = Column(String)
    ts = Column(DateTime, default=datetime.utcnow)

    playcount = Column(Integer)
    num_ratings = Column(Integer)
    rating = Column(Double)
    position = Column(Integer)
    title = Column(String)

    user = relationship("User")

    def __init__(self, session: Session, user: User, title: str, description: str):
        self.user = user
        self.title = title
        self.description = description
        self.position = 0

        self.playcount = 0
        self.num_ratings = 0
        self.rating = 0

        self.save(session)

    def save(self, session: Session):
        session.add(self)
        session.commit()

    def delete(self, session: Session):
        session.delete(self)
        # remove all mentions to path p in db
        session.execute(
            path_node_association.delete().where(
                path_node_association.c.path_id == self.id
            )
        )

        session.commit()

    def add_node(self, node: Node, position: int, session: Session):
        # check for valid position
        if position < 0:
            raise Exception("invalid position - negative")

        # check for path having any nodes already
        if position == 0:
            q = (
                session.query(path_node_association)
                .filter(path_node_association.c.path_id == self.id)
                .filter(path_node_association.c.position == 0)
                .first()
            )

            if q is not None:
                raise Exception(
                    "invalid position - path already has node in position zero"
                )

        if position > self.position + 1:
            raise Exception("invalid position - no way to link")

        # check for node in path
        q = (
            session.query(path_node_association)
            .filter(path_node_association.c.node_id == node.id)
            .filter(path_node_association.c.path_id == self.id)
            .first()
        )
        if q is not None:
            raise Exception("node already in path")

        # increase position in case we add a next node
        if position == self.position + 1:
            self.position += 1

        session.execute(
            path_node_association.insert().values(
                path_id=self.id, node_id=node.id, position=position
            )
        )

        session.commit()

    def get_node_sequence(self, session: Session):
        nodes_and_positions = (
            session.query(path_node_association)  
            .filter(path_node_association.c.path_id == self.id)     
            .order_by(path_node_association.c.position)            
            .all()
        )
        
        node_ids = [node_id for _, node_id, _ in nodes_and_positions]
        positions = [position for _, _, position in nodes_and_positions]
        
        nodes = (
            session.query(Node)
            .filter(Node.id.in_(node_ids))
            .order_by(
                # Order by the order of appearance in the node_ids list
                Node.id.in_(node_ids).desc()
            )
            .all()
        )

        return nodes, positions

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

    def update_rating(self, rating: float, session: Session):
        if rating < 0 or rating > 10:
            raise Exception("rating must be between 0 and 10")

        result = session.execute(
            update(Path)
            .where(Path.id == self.id)
            .values(
                rating=(Path.rating * Path.num_ratings + rating)
                / (Path.num_ratings + 1),
                num_ratings=Path.num_ratings + 1,
            )
            .returning(Path.rating, Path.num_ratings)
        )

        self.rating, self.num_ratings = result.fetchone()

        session.commit()

    def get_rating(self):
        return round(self.rating, 2)

    def update_title(self, title: str, session: Session):
        session.execute(
            update(Path)
            .where(Path.id == self.id)
            .values(title=title)
            .returning(Path.title)
        )

        self.title = title

        session.commit()

    def update_description(self, description: str, session: Session):
        session.execute(
            update(Path)
            .where(Path.id == self.id)
            .values(description=description)
            .returning(Path.description)
        )

        self.description = description

        session.commit()


path_node_association = Table(
    "path_node_association",
    Base.metadata,
    Column("path_id", String, ForeignKey("paths.id")),
    Column("node_id", String, ForeignKey("nodes.id")),
    Column("position", Integer),
)
