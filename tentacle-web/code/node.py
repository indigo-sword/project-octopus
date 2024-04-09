from user import User
from uuid import uuid4
import os
from werkzeug.datastructures import FileStorage

from db_manager import Base
from sqlalchemy import (
    Column,
    Integer,
    String,
    Double,
    ForeignKey,
    update,
    or_,
    DateTime,
    and_,
    Boolean,
)
from sqlalchemy.orm import relationship, Session
from datetime import datetime


class NodeLink(Base):
    __tablename__ = "node_links"
    id = Column(
        String, primary_key=True, default=lambda: str(uuid4()), unique=True
    )  # id of the link
    origin_id = Column(Integer, ForeignKey("nodes.id"))  # id of the origin node
    destination_id = Column(
        Integer, ForeignKey("nodes.id")
    )  # id of the destination node
    description = Column(String)
    ts = Column(String, default=datetime.now().strftime('%Y-%m-%d'))

    origin = relationship("Node", foreign_keys=[origin_id])
    destination = relationship("Node", foreign_keys=[destination_id])

    def __init__(
        self, session: Session, origin: "Node", destination: "Node", description: str
    ):
        self.origin_id = origin.id
        self.destination_id = destination.id
        self.description = description

        self.save(session)

    def save(self, session: Session):
        session.add(self)
        session.commit()

    def __repr__(self):
        return f"NodeLink({self.origin_id}, {self.destination_id}, {self.description}, {self.ts})"


class Node(Base):
    __tablename__ = "nodes"
    id = Column(String, primary_key=True, default=lambda: str(uuid4()), unique=True)
    user_id = Column(Integer, ForeignKey("users.username"))
    title = Column(String)
    playcount = Column(Integer)
    num_ratings = Column(Integer)
    rating = Column(Double)
    description = Column(String)
    is_initial = Column(Boolean, default=False)
    is_final = Column(Boolean, default=False)
    ts = Column(DateTime, default=datetime.utcnow)
    user = relationship("User")

    def __init__(
        self,
        session: Session,
        user: User,
        title: str,
        description: str,
        lvl_buf: FileStorage,
        is_initial: bool = False,
        is_final: bool = False,
    ):
        # attributes that will change over time
        self.user_id = user.username
        self.title = title
        self.playcount = 0
        self.num_ratings = 0
        self.rating = 0
        self.description = description

        self.is_initial = is_initial
        self.is_final = is_final

        self.save(session)
        self._write_file(lvl_buf)

    def update_level(self, lvl_buf: FileStorage):
        # clear the content inside get_file_path()
        with open(self.get_file_path(), "w") as f:
            f.truncate(0)

        self._write_file(lvl_buf)

    def _write_file(self, lvl_buf: FileStorage):
        lvl_buf.save(self.get_file_path())

    def get_info(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "playcount": self.playcount,
            "num_ratings": self.num_ratings,
            "rating": self.get_rating(),
            "description": self.description,
            "is_initial": self.is_initial,
            "is_final": self.is_final,
            "ts": self.ts,
        }

    def get_file_path(self):
        # get project root
        root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        # go to /levels/self.id.level
        return root + "/levels/" + self.id + ".level"

    def __repr__(self):
        return f"Node({self.id}, {self.user_id}, {self.playcount}, {self.num_ratings}, {self.rating}, {self.description}, {self.ts})"

    def save(self, session: Session):
        session.add(self)  # add node to session
        session.commit()

    def link(self, node: "Node", description: str, session: Session):
        """link self to a next node"""
        if node == self:
            raise Exception("cannot link node to itself")

        if node.is_initial:
            raise Exception("cannot link to initial node")

        if self.is_final:
            raise Exception("cannot link from final node")

        # check if destination already has a link to self
        result = (
            session.query(NodeLink)
            .filter(
                or_(
                    and_(
                        NodeLink.destination_id == self.id,
                        NodeLink.origin_id == node.id,
                    ),
                    and_(
                        NodeLink.destination_id == node.id,
                        NodeLink.origin_id == self.id,
                    ),
                )
            )
            .all()
        )

        if result:
            raise Exception("nodes are already linked.")

        link = NodeLink(session, origin=self, destination=node, description=description)

    def get_next_links(self, session: Session):
        """get next links"""
        return session.query(NodeLink).filter(NodeLink.origin_id == self.id).all()

    def get_previous_links(self, session: Session):
        """get previous links"""
        return session.query(NodeLink).filter(NodeLink.destination_id == self.id).all()

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

    def update_description(self, description: str, session: Session):
        result = session.execute(
            update(Node)
            .where(Node.id == self.id)
            .values(description=description)
            .returning(Node.description)
        )

        self.description = result.scalar()

        session.commit()

    def update_title(self, title: str, session: Session):
        result = session.execute(
            update(Node)
            .where(Node.id == self.id)
            .values(title=title)
            .returning(Node.title)
        )

        self.title = result.scalar()

        session.commit()

    def update_rating(self, rating: float, session: Session):
        if rating < 0 or rating > 10:
            raise Exception("rating must be between 0 and 10")

        result = session.execute(
            update(Node)
            .where(Node.id == self.id)
            .values(
                rating=(Node.rating * Node.num_ratings + rating)
                / (Node.num_ratings + 1),
                num_ratings=Node.num_ratings + 1,
            )
            .returning(Node.rating, Node.num_ratings)
        )

        self.rating, self.num_ratings = result.fetchone()

        session.commit()

    def get_rating(self):
        return round(self.rating, 2)
