from sqlalchemy import Column, String, ForeignKey, Integer, or_
from sqlalchemy.orm import Session, relationship
from db_manager import Base
from uuid import uuid4

class User(Base):
    __tablename__ = 'users'
    id = Column(String, primary_key=True, default=lambda: str(uuid4()), unique=True)
    username = Column(String)
    password = Column(String)
    email = Column(String)
    bio = Column(String)

    def __init__(self, session: Session, username: str, password: str, email: str, bio: str=""):
        self.username = username
        self.password = password
        self.email = email
        self.bio = bio
        self._save(session)

    def _save(self, session: Session):
        session.add(self)
        session.commit()

    def __repr__(self):
        return f"User({self.id}, {self.username}, {self.email}, {self.bio})"
    
    def get_friends(self, session: Session):
        ''' returns list of friends of the user '''
        return session.query(Friendship).filter(or_(Friendship.user_one_id == self.id, Friendship.user_two_id == self.id)).filter(Friendship.status == 1).all()

    def get_friend_requests(self, session: Session):
        ''' returns list of friend requests made to the user '''
        return session.query(Friendship).filter(Friendship.user_two_id == self.id).filter(Friendship.status == 0).all()
    
    def get_friend_requests_sent(self, session: Session):
        ''' returns list of friend requests made by the user '''
        return session.query(Friendship).filter(Friendship.user_one_id == self.id).filter(Friendship.status == 0).all()
    
    def accept_friend_request(self, session: Session, friend: 'User'):
        ''' accepts friend request from friend '''
        f = session.query(Friendship).filter(Friendship.user_one_id == friend.id).filter(Friendship.user_two_id == self.id).first()
        f.accept(session)

    def reject_friend_request(self, session: Session, friend: 'User'):
        ''' rejects friend request from friend '''
        f = session.query(Friendship).filter(Friendship.user_one_id == friend.id).filter(Friendship.user_two_id == self.id).first()
        f.reject(session)

    def send_friend_request(self, session: Session, friend: 'User'):
        ''' sends friend request to friend '''
        Friendship(session, self, friend)
        # maybe send something here, like an email or a notification

    def remove_friend(self, session: Session, friend: 'User'):
        ''' removes friend '''
        f = session.query(Friendship).filter(Friendship.user_one_id == self.id).filter(Friendship.user_two_id == friend.id).first()
        f.reject(session)
        
class Friendship(Base):
    __tablename__ = 'friendships'
    id = Column(String, primary_key=True, default=lambda: str(uuid4()), unique=True)
    user_one_id = Column(String, ForeignKey('users.id'))
    user_two_id = Column(String, ForeignKey('users.id'))
    status = Column(Integer)

    user_one = relationship('User', foreign_keys=[user_one_id])
    user_two = relationship('User', foreign_keys=[user_two_id])

    def __init__(self, session: Session, user_one: User, user_two: User):
        self.user_one = user_one
        self.user_one_id = user_one.id
        
        self.user_two = user_two
        self.user_two_id = user_two.id

        self.status = 0 # pending
        self._save(session)

    def accept(self, session: Session):
        self.status = 1 # accepted
        self._save(session)

    def reject(self, session: Session):
        session.delete(self)
        session.commit()

    def _save(self, session: Session):
        session.add(self)
        session.commit()

    def __repr__(self):
        return f"Friendship({self.id}, {self.user_one.id}, {self.user_two.id})"