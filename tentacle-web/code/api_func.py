from db_manager import db_session
from user import User
import bcrypt

def create_user_func(username: str, password: str, email: str):
    ''' create user '''
    # check for existing username
    if db_session.query(User).filter(User.username == username).first():
        return {"message": "Username already exists"}, 409
    
    # check for existing email
    if db_session.query(User).filter(User.email == email).first():
        return {"message": "Email already exists"}, 409
    
    # hash the password
    password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # create user
    u = User(db_session, username, password, email)

    return {"message": "User created", "user_id": u.id}, 201

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
    
    # unfollow
    u.unfollow(db_session, f)

    # return user
    return {"message": "User unfollowed"}, 200

def get_follows_func(username: str):
    ''' get follows '''
    u = db_session.query(User).filter(User.username == username).first()
    if not u: return {"message": "User not found"}, 404
    
    return {"message": "user following and followed", "following": u.get_following(db_session), "followed": u.get_followers(db_session)}, 200

