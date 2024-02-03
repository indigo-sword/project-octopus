from db_manager import db_session
from user import User
import bcrypt

def create_user_func(username, password, email):
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

    return {"message": "user created", "user_id": u.id}, 201