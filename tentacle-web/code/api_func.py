from db_manager import db_session
from user import User
from node import Node
import bcrypt
import re
from werkzeug.datastructures import FileStorage

def login_user_func(username: str, password: str):
    ''' login user '''
    u = db_session.query(User).filter(User.username == username).first()
    if not u: return "user not found", 404
    
    if bcrypt.checkpw(password.encode('utf-8'), u.password):
        return "user logged in", 200
    
    else:
        return "invalid password", 401

def create_user_func(username: str, password: str, email: str, bio: str):
    ''' create user '''
    # perform email regex check
    if not re.match(r'^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$', email):
        return {"message": "invalid email"}, 400
    
    # check for existing username
    if db_session.query(User).filter(User.username == username).first():
        return {"message": "username already exists"}, 409
    
    # check for existing email
    if db_session.query(User).filter(User.email == email).first():
        return {"message": "email already exists"}, 409

    # create user
    User(db_session, username, password, email, bio)

    return {"message": "user created"}, 201

def change_user_bio_func(username: str, bio: str):
    ''' change user bio '''
    u = db_session.query(User).filter(User.username == username).first()
    if not u: return {"message": "user not found"}, 404
    
    u.update_bio(db_session, bio)
    return {"message": "user bio updated", "bio": bio}, 200

def follow_user_func(username: str, followed_username: str):
    ''' follow user '''
    u = db_session.query(User).filter(User.username == username).first()
    if not u: return {"message": "user not found"}, 404
    
    f = db_session.query(User).filter(User.username == followed_username).first()
    if not f: return {"message": "followed user not found"}, 404
    
    u.follow(db_session, f)
    return {"message": "user followed"}, 200

def unfollow_user_func(username: str, unfollowed_username: str):
    # get user
    u = db_session.query(User).filter(User.username == username).first()
    if not u: return {"message": "user not found"}, 404
    
    # get user to be unfollowed
    f = db_session.query(User).filter(User.username == unfollowed_username).first()
    if not f: return {"message": "unfollowed user not found"}, 404

    try: u.unfollow(db_session, f)
    except: return {"message": "user is not being followed"}, 400

    # return user
    return {"message": "user unfollowed"}, 200

def get_follows_func(username: str):
    ''' get follows '''
    u = db_session.query(User).filter(User.username == username).first()
    if not u: return {"message": "user not found"}, 404
    
    return {"message": "user following and followed", "following": u.get_following(db_session), "followed": u.get_followers(db_session)}, 200

def get_user_func(username: str):
    ''' get user '''
    u = db_session.query(User).filter(User.username == username).first()
    if not u: return {"message": "user not found"}, 404
    
    return {"message": "user info", "username": u.username, "bio": u.bio, "email": u.email, "following": u.following, "followers": u.followers}, 200

def add_friend_func(username: str, friend_username: str):
    ''' add friend '''
    u = db_session.query(User).filter(User.username == username).first()
    if not u: return {"message": "user not found"}, 404
    
    f = db_session.query(User).filter(User.username == friend_username).first()
    if not f: return {"message": "friend user not found"}, 404

    # already friends
    if friend_username in u.get_friends(db_session):
        return {"message": "user is already a friend"}, 400
    
    # check for existing friend request sent
    if friend_username in u.get_friend_requests_sent(db_session):
        return {"message": "friend request already sent"}, 400

    # check for other user already having asked them
    if friend_username in u.get_friend_requests(db_session):
        u.accept_friend_request(db_session, f)
        return {"message": "friend request accepted"}, 200
    
    u.send_friend_request(db_session, f)
    return {"message": "friend request sent"}, 200

def accept_friend_func(username: str, friend_username: str):
    ''' accept friend '''
    u = db_session.query(User).filter(User.username == username).first()
    if not u: return {"message": "user not found"}, 404
    
    f = db_session.query(User).filter(User.username == friend_username).first()
    if not f: return {"message": "friend user not found"}, 404
    
    try: u.accept_friend_request(db_session, f)
    except: return {"message": "no friend request from this user"}, 400

    return {"message": "friend request accepted"}, 200

def reject_friend_func(username: str, friend_username: str):
    ''' reject friend '''
    u = db_session.query(User).filter(User.username == username).first()
    if not u: return {"message": "user not found"}, 404
    
    f = db_session.query(User).filter(User.username == friend_username).first()
    if not f: return {"message": "friend user not found"}, 404
    
    try: u.reject_friend_request(db_session, f)
    except: return {"message": "no friend request from this user"}, 400

    return {"message": "friend request rejected"}, 200

def remove_friend_func(username: str, friend_username: str):
    ''' remove friend '''
    u = db_session.query(User).filter(User.username == username).first()
    if not u: return {"message": "user not found"}, 404
    
    f = db_session.query(User).filter(User.username == friend_username).first()
    if not f: return {"message": "friend user not found"}, 404
    
    try: u.remove_friend(db_session, f)
    except: return {"message": "user is not a friend"}, 400

    return {"message": "friend removed"}, 200

def get_friends_func(username: str):
    ''' get friends '''
    u = db_session.query(User).filter(User.username == username).first()
    if not u: return {"message": "user not found"}, 404
    
    return {"message": "user friends", "friends": u.get_friends(db_session), "requests": u.get_friend_requests(db_session), "sent requests": u.get_friend_requests_sent(db_session)}, 200

def create_node_func(username: str, description: str, file_buf: FileStorage, is_initial: bool = False):
    ''' create node '''
    u = db_session.query(User).filter(User.username == username).first()
    if not u: return {"message": "user not found"}, 404

    # create node
    n = Node(db_session, u, description, file_buf, is_initial)

    return {"message": "node created", "node_id": n.id}, 201

def get_node_func(node_id: str):
    ''' get node '''
    n = db_session.query(Node).filter(Node.id == node_id).first()
    if not n: return {"message": "node not found"}, 404
    
    return {"message": "node info", "user_id": n.user_id, "playcount": n.playcount, "num_ratings": n.num_ratings, "rating": n.rating, "description": n.description, "ts": n.ts}, 200

def link_nodes_func(username: str, origin_id: str, destination_id: str, description: str):
    ''' link nodes '''
    u = db_session.query(User).filter(User.username == username).first()
    if not u: return {"message": "user not found"}, 404

    o = db_session.query(Node).filter(Node.id == origin_id).first()
    if not o: return {"message": "origin node not found"}, 404

    d = db_session.query(Node).filter(Node.id == destination_id).first()
    if not d: return {"message": "destination node not found"}, 404

    if u.username not in [o.user_id, d.user_id]: return {"message": "user does not own any of the nodes"}, 401

    try: o.link(d, description, db_session)
    except Exception as e: return {"message": str(e)}, 400

    return {"message": "nodes linked"}, 200

def get_next_links_func(node_id: str):
    ''' get next links' id'''
    n = db_session.query(Node).filter(Node.id == node_id).first()
    if not n: return {"message": "node not found"}, 404

    return {"message": "next links", "next_links": [{"description": link.description, "destination_id": link.destination_id} for link in n.get_next_links(db_session)]}, 200

def get_previous_links_func(node_id: str):
    ''' get previous links' id'''
    n = db_session.query(Node).filter(Node.id == node_id).first()
    if not n: return {"message": "node not found"}, 404

    return {"message": "previous links", "previous_links": [{"description": link.description, "origin_id": link.origin_id} for link in n.get_previous_links(db_session)]}, 200

def update_playcount_func(node_id: str):
    ''' update playcount '''
    n = db_session.query(Node).filter(Node.id == node_id).first()
    if not n: return {"message": "node not found"}, 404

    n.update_playcount(db_session)
    return {"message": "playcount updated", "playcount": n.get_playcount()}, 200

def update_rating_func(node_id: str, rating: float):
    ''' update rating '''
    n = db_session.query(Node).filter(Node.id == node_id).first()
    if not n: return {"message": "node not found"}, 404

    try:
        n.update_rating(rating, db_session)
    except Exception as e:
        return {"message": str(e)}, 400
    return {"message": "rating updated", "rating": n.get_rating()}, 200

def update_node_description_func(username: str, node_id: str, description: str):
    ''' update description '''
    n = db_session.query(Node).filter(Node.id == node_id).first()
    if not n: return {"message": "node not found"}, 404

    if n.user_id != username: return {"message": "user does not own this node"}, 401

    n.update_description(description, db_session)
    return {"message": "description updated", "description": n.description}, 200