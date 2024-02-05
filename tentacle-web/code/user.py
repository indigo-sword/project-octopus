from sqlalchemy import Column, String, ForeignKey, Integer, or_, DateTime, update
from sqlalchemy.orm import Session, relationship
from db_manager import Base
from uuid import uuid4
from datetime import datetime

class User(Base):
    __tablename__ = 'users'
    username = Column(String, unique=True, primary_key=True, index=True)
    password = Column(String)
    email = Column(String, unique=True)
    bio = Column(String)
    ts = Column(DateTime, default=datetime.utcnow)
    following = Column(Integer)
    followers = Column(Integer)

    def __init__(self, session: Session, username: str, password: str, email: str, bio: str=""):
        self.username = username
        self.password = password
        self.email = email
        self.bio = bio
        self.following = 0
        self.followers = 0
        self._save(session)

    def _save(self, session: Session):
        session.add(self)
        session.commit()

    def __repr__(self):
        return f"User({self.id}, {self.username}, {self.email}, {self.bio}, {self.ts})"
    
    def update_bio(self, session: Session, bio: str):
        ''' update bio '''
        self.bio = bio
        self._save(session)

    def add_follower(self, session: Session):
        ''' update followers '''
        result = session.execute(
            update(User)
            .where(User.username == self.username)
            .values(followers=User.followers + 1)
            .returning(User.followers)
        )

        self.followers = result.scalar()
        self._save(session)

    def remove_follower(self, session: Session):
        ''' update followers '''
        result = session.execute(
            update(User)
            .where(User.username == self.username)
            .values(followers=User.followers - 1)
            .returning(User.followers)
        )

        self.followers = result.scalar()
        self._save(session)

    def add_following(self, session: Session):
        ''' update following '''
        self.following += 1
        self._save(session)

    def remove_following(self, session: Session):
        ''' update following '''
        self.following -= 1
        self._save(session)

    def follow(self, session: Session, user: 'User'):
        ''' follow user '''
        Follow(session, self, user)
        user.add_follower(session)
        self.add_following(session)

    def unfollow(self, session: Session, user: 'User'):
        # check for existing follow
        f = session.query(Follow).filter(Follow.follower == self.username).filter(Follow.followed == user.username).first()
        if not f: raise Exception("User is not being followed")

        f.unfollow(session)
        user.remove_follower(session)
        self.remove_following(session)

    def get_following(self, session: Session):
        ''' returns list of users being followed by the user '''
        return [follow.followed for follow in session.query(Follow).filter(Follow.follower == self.username).all()]
    
    def get_followers(self, session: Session):
        ''' returns list of users following the user '''
        return [follow.follower for follow in session.query(Follow).filter(Follow.followed == self.username).all()]
    
    def get_friends(self, session: Session):
        ''' returns list of friends of the user '''
        return [friendship.friend_one if friendship.friend_one != self.username else friendship.friend_two for friendship in session.query(Friendship).filter(or_(Friendship.friend_one == self.username, Friendship.friend_two == self.username)).filter(Friendship.status == 1).all()]

    def get_friend_requests(self, session: Session):
        ''' returns list of friend requests made to the user '''
        return [friendship.friend_one for friendship in session.query(Friendship).filter(Friendship.friend_two == self.username).filter(Friendship.status == 0).all()]
    
    def get_friend_requests_sent(self, session: Session):
        ''' returns list of friend requests made by the user '''
        return [friendship.friend_two for friendship in session.query(Friendship).filter(Friendship.friend_one == self.username).filter(Friendship.status == 0).all()]
    
    def accept_friend_request(self, session: Session, friend: 'User'):
        ''' accepts friend request from friend '''
        f = session.query(Friendship).filter(Friendship.friend_one == friend.username).filter(Friendship.friend_two == self.username).first()
        if not f: raise Exception("No friend request from this user")
        f.accept(session)

    def reject_friend_request(self, session: Session, friend: 'User'):
        ''' rejects friend request from friend '''
        f = session.query(Friendship).filter(Friendship.friend_one == friend.username).filter(Friendship.friend_two == self.username).first()
        if not f: raise Exception("No friend request from this user")
        f.reject(session)

    def send_friend_request(self, session: Session, friend: 'User'):
        ''' sends friend request to friend '''
        Friendship(session, self, friend)
        # maybe send something here, like an email or a notification

    def remove_friend(self, session: Session, friend: 'User'):
        ''' removes friend '''
        f = session.query(Friendship).filter(Friendship.friend_one == self.username).filter(Friendship.friend_two == friend.username).first()
        if not f: raise Exception("User is not a friend")
        f.reject(session)
        
class Friendship(Base):
    __tablename__ = 'friendships'
    id = Column(String, primary_key=True, default=lambda: str(uuid4()), unique=True)
    friend_one = Column(String, ForeignKey('users.username'))
    friend_two = Column(String, ForeignKey('users.username'))
    status = Column(Integer)
    ts = Column(DateTime, default=datetime.utcnow)

    user_one = relationship('User', foreign_keys=[friend_one])
    user_two = relationship('User', foreign_keys=[friend_two])

    def __init__(self, session: Session, user_one: User, user_two: User):
        self.friend_one = user_one.username
        self.friend_two = user_two.username

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
        return f"Friendship({self.id}, {self.friend_one}, {self.friend_two}, {self.status})"
    
class Follow(Base):
    __tablename__ = 'follows'
    id = Column(String, primary_key=True, default=lambda: str(uuid4()), unique=True)
    follower = Column(String, ForeignKey('users.username'))
    followed = Column(String, ForeignKey('users.username'))

    follower_user = relationship('User', foreign_keys=[follower])
    followed_user = relationship('User', foreign_keys=[followed])

    def __init__(self, session: Session, follower: User, followed: User):
        self.follower = follower.username
        self.followed = followed.username
        self._save(session)

    def _save(self, session: Session):
        session.add(self)
        session.commit()

    def unfollow(self, session: Session):
        session.delete(self)
        session.commit()

    def __repr__(self):
        return f"Follow({self.id}, {self.follower}, {self.followed})"

    
