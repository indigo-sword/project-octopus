from db_manager import db_session
from user import User
from node import Node
import bcrypt
import re
from werkzeug.datastructures import FileStorage

def create_user_func(username: str, password: str, email: str, bio: str):
    ''' create user '''
    # perform email regex check
    if not re.match(r'^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$', email):
        return {"message": "Invalid email"}, 400
    
    # check for existing username
    if db_session.query(User).filter(User.username == username).first():
        return {"message": "Username already exists"}, 409
    
    # check for existing email
    if db_session.query(User).filter(User.email == email).first():
        return {"message": "Email already exists"}, 409
    
    # hash the password
    password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # create user
    User(db_session, username, password, email, bio)

    return {"message": "User created"}, 201

def change_user_bio_func(username: str, bio: str):
    ''' change user bio '''
    u = db_session.query(User).filter(User.username == username).first()
    if not u: return {"message": "User not found"}, 404
    
    u.update_bio(db_session, bio)
    return {"message": "User bio updated", "bio": bio}, 200

def follow_user_func(username: str, followed_username: str):
    ''' follow user '''
    u = db_session.query(User).filter(User.username == username).first()
    if not u: return {"message": "User not found"}, 404
    
    f = db_session.query(User).filter(User.username == followed_username).first()
    if not f: return {"message": "Followed user not found"}, 404
    
    u.follow(db_session, f)
    return {"message": "User followed"}, 200

def unfollow_user_func(username: str, unfollowed_username: str):
    # get user
    u = db_session.query(User).filter(User.username == username).first()
    if not u: return {"message": "User not found"}, 404
    
    # get user to be unfollowed
    f = db_session.query(User).filter(User.username == unfollowed_username).first()
    if not f: return {"message": "Unfollowed user not found"}, 404

    try: u.unfollow(db_session, f)
    except: return {"message": "User is not being followed"}, 400

    # return user
    return {"message": "User unfollowed"}, 200

def get_follows_func(username: str):
    ''' get follows '''
    u = db_session.query(User).filter(User.username == username).first()
    if not u: return {"message": "User not found"}, 404
    
    return {"message": "user following and followed", "following": u.get_following(db_session), "followed": u.get_followers(db_session)}, 200

def get_user_func(username: str):
    ''' get user '''
    u = db_session.query(User).filter(User.username == username).first()
    if not u: return {"message": "User not found"}, 404
    
    return {"message": "user info", "username": u.username, "bio": u.bio, "email": u.email, "following": u.following, "followers": u.followers}, 200

def add_friend_func(username: str, friend_username: str):
    ''' add friend '''
    u = db_session.query(User).filter(User.username == username).first()
    if not u: return {"message": "User not found"}, 404
    
    f = db_session.query(User).filter(User.username == friend_username).first()
    if not f: return {"message": "Friend user not found"}, 404

    # already friends
    if friend_username in u.get_friends(db_session):
        return {"message": "User is already a friend"}, 400
    
    # check for existing friend request sent
    if friend_username in u.get_friend_requests_sent(db_session):
        return {"message": "Friend request already sent"}, 400

    # check for other user already having asked them
    if friend_username in u.get_friend_requests(db_session):
        u.accept_friend_request(db_session, f)
        return {"message": "Friend request accepted"}, 200
    
    u.send_friend_request(db_session, f)
    return {"message": "Friend request sent"}, 200

def accept_friend_func(username: str, friend_username: str):
    ''' accept friend '''
    u = db_session.query(User).filter(User.username == username).first()
    if not u: return {"message": "User not found"}, 404
    
    f = db_session.query(User).filter(User.username == friend_username).first()
    if not f: return {"message": "Friend user not found"}, 404
    
    try: u.accept_friend_request(db_session, f)
    except: return {"message": "No friend request from this user"}, 400

    return {"message": "Friend request accepted"}, 200

def reject_friend_func(username: str, friend_username: str):
    ''' reject friend '''
    u = db_session.query(User).filter(User.username == username).first()
    if not u: return {"message": "User not found"}, 404
    
    f = db_session.query(User).filter(User.username == friend_username).first()
    if not f: return {"message": "Friend user not found"}, 404
    
    try: u.reject_friend_request(db_session, f)
    except: return {"message": "No friend request from this user"}, 400

    return {"message": "Friend request rejected"}, 200

def remove_friend_func(username: str, friend_username: str):
    ''' remove friend '''
    u = db_session.query(User).filter(User.username == username).first()
    if not u: return {"message": "User not found"}, 404
    
    f = db_session.query(User).filter(User.username == friend_username).first()
    if not f: return {"message": "Friend user not found"}, 404
    
    try: u.remove_friend(db_session, f)
    except: return {"message": "User is not a friend"}, 400

    return {"message": "Friend removed"}, 200

def get_friends_func(username: str):
    ''' get friends '''
    u = db_session.query(User).filter(User.username == username).first()
    if not u: return {"message": "User not found"}, 404
    
    return {"message": "user friends", "friends": u.get_friends(db_session), "requests": u.get_friend_requests(db_session), "sent requests": u.get_friend_requests_sent(db_session)}, 200

def create_node_func(username: str, description: str, file_buf: FileStorage):
    ''' create node '''
    u = db_session.query(User).filter(User.username == username).first()
    if not u: return {"message": "User not found"}, 404

    # create node
    n = Node(db_session, u, description, file_buf)

    return {"message": "Node created", "node_id": n.id}, 201
    