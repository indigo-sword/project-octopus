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