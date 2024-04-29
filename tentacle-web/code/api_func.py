from user import User
from node import Node
from path import Path, path_node_association as PathNodeAssociation
import bcrypt
import re
from werkzeug.datastructures import FileStorage
from flask import send_file
import os
from sqlalchemy.orm import Session
from sqlalchemy import or_


def login_user_func(username: str, password: str, session: Session):
    """login user"""
    u = session.query(User).filter(User.username == username).first()

    if not u:
        return {"message": "user not found"}, 404

    if not bcrypt.checkpw(password.encode("utf-8"), u.password):
        return {"message": "invalid password"}, 401

    return {"message": "user logged in", 
            "username": u.username,
            "bio": u.bio,
            "email": u.email,
            "following": u.following,
            "followers": u.followers}, 200


def create_user_func(
    username: str, password: str, email: str, bio: str, session: Session
):
    """create user"""
    # perform email regex check
    if not re.match(r"^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$", email):
        return {"message": "invalid email"}, 400

    # check for existing username
    if session.query(User).filter(User.username == username).first():
        return {"message": "username already exists"}, 409

    # check for existing email
    if session.query(User).filter(User.email == email).first():
        return {"message": "email already exists"}, 409

    # create user
    User(session, username, password, email, bio)
    return {"message": "user created"}, 201


def change_user_bio_func(username: str, bio: str, session: Session):
    """change user bio"""
    u = session.query(User).filter(User.username == username).first()

    if not u:
        return {"message": "user not found"}, 404

    u.update_bio(session, bio)
    return {"message": "user bio updated", "bio": bio}, 200

def change_user_username_func(old_username: str, new_username: str, session: Session):
    """change user username"""
    u = session.query(User).filter(User.username == old_username).first()

    if not u:
        return {"message": "user not found"}, 404

    u.update_username(session, new_username)
    return {"message": "username updated", "username": new_username}, 200


def follow_user_func(username: str, followed_username: str, session: Session):
    """follow user"""
    u = session.query(User).filter(User.username == username).first()
    if not u:
        return {"message": "user not found"}, 404

    f = session.query(User).filter(User.username == followed_username).first()
    if not f:
        return {"message": "followed user not found"}, 404

    u.follow(session, f)
    return {"message": "user followed"}, 200


def unfollow_user_func(username: str, unfollowed_username: str, session: Session):
    # get user
    u = session.query(User).filter(User.username == username).first()
    if not u:
        return {"message": "user not found"}, 404

    # get user to be unfollowed
    f = session.query(User).filter(User.username == unfollowed_username).first()
    if not f:
        return {"message": "unfollowed user not found"}, 404

    try:
        u.unfollow(session, f)
    except:
        return {"message": "user is not being followed"}, 400

    # return user
    return {"message": "user unfollowed"}, 200


def get_follows_func(username: str, session: Session):
    """get follows"""
    u = session.query(User).filter(User.username == username).first()
    if not u:
        return {"message": "user not found"}, 404

    return {
        "message": "user following and followed",
        "following": u.get_following(session),
        "followed": u.get_followers(session),
    }, 200


def get_user_func(username: str, session: Session):
    """get user"""
    u = session.query(User).filter(User.username == username).first()
    if not u:
        return {"message": "user not found"}, 404

    nodes = session.query(Node).filter(Node.user_id == username).all()

    return {
        "message": "user info",
        "username": u.username,
        "bio": u.bio,
        "email": u.email,
        "following": u.following,
        "followers": u.followers,

        "nodes": [n.get_info() for n in nodes]
    }, 200

######################################################
######## FRIEND AND FOLLOW STUFF NOT USED YET ########
######################################################
def add_friend_func(username: str, friend_username: str, session: Session):
    """add friend"""
    u = session.query(User).filter(User.username == username).first()
    if not u:
        return {"message": "user not found"}, 404

    f = session.query(User).filter(User.username == friend_username).first()
    if not f:
        return {"message": "friend user not found"}, 404

    # already friends
    if friend_username in u.get_friends(session):
        return {"message": "user is already a friend"}, 400

    # check for existing friend request sent
    if friend_username in u.get_friend_requests_sent(session):
        return {"message": "friend request already sent"}, 400

    # check for other user already having asked them
    if friend_username in u.get_friend_requests(session):
        u.accept_friend_request(session, f)
        return {"message": "friend request accepted"}, 200

    u.send_friend_request(session, f)
    return {"message": "friend request sent"}, 200


def accept_friend_func(username: str, friend_username: str, session: Session):
    """accept friend"""
    u = session.query(User).filter(User.username == username).first()
    if not u:
        return {"message": "user not found"}, 404

    f = session.query(User).filter(User.username == friend_username).first()
    if not f:
        return {"message": "friend user not found"}, 404

    try:
        u.accept_friend_request(session, f)
    except:
        return {"message": "no friend request from this user"}, 400

    return {"message": "friend request accepted"}, 200


def reject_friend_func(username: str, friend_username: str, session: Session):
    """reject friend"""
    u = session.query(User).filter(User.username == username).first()
    if not u:
        return {"message": "user not found"}, 404

    f = session.query(User).filter(User.username == friend_username).first()
    if not f:
        return {"message": "friend user not found"}, 404

    try:
        u.reject_friend_request(session, f)
    except:
        return {"message": "no friend request from this user"}, 400

    return {"message": "friend request rejected"}, 200


def remove_friend_func(username: str, friend_username: str, session: Session):
    """remove friend"""
    u = session.query(User).filter(User.username == username).first()
    if not u:
        return {"message": "user not found"}, 404

    f = session.query(User).filter(User.username == friend_username).first()
    if not f:
        return {"message": "friend user not found"}, 404

    try:
        u.remove_friend(session, f)
    except:
        return {"message": "user is not a friend"}, 400

    return {"message": "friend removed"}, 200


def get_friends_func(username: str, session: Session):
    """get friends"""
    u = session.query(User).filter(User.username == username).first()
    if not u:
        return {"message": "user not found"}, 404

    return {
        "message": "user friends",
        "friends": u.get_friends(session),
        "requests": u.get_friend_requests(session),
        "sent requests": u.get_friend_requests_sent(session),
    }, 200
######################################################
######## FRIEND AND FOLLOW STUFF NOT USED YET ########
######################################################

def create_node_func(
    username: str,
    title: str,
    description: str,
    file_buf: FileStorage,
    is_initial: bool,
    is_final: bool,
    session: Session,
):
    """create node"""
    u = session.query(User).filter(User.username == username).first()
    if not u:
        return {"message": "user not found"}, 404

    # create node
    try:
        n = Node(session, u, title, description, file_buf, is_initial, is_final)
    except Exception:
        return {"message": "node creation failed. try again."}, 400

    return {"message": "node created", "node_id": n.id}, 201

def get_node_func(node_id: str, session: Session):
    """get node"""
    n = session.query(Node).filter(Node.id == node_id).first()
    if not n:
        return {"message": "node not found"}, 404

    return {
        "message": "node info",
        "user_id": n.user_id,
        "playcount": n.playcount,
        "num_ratings": n.num_ratings,
        "rating": n.rating,
        "description": n.description,
        "ts": n.ts,
        "title": n.title,
    }, 200


def link_nodes_func(
    username: str,
    origin_id: str,
    destination_id: str,
    description: str,
    session: Session,
):
    """link nodes"""
    u = session.query(User).filter(User.username == username).first()
    if not u:
        return {"message": "user not found"}, 404

    o = session.query(Node).filter(Node.id == origin_id).first()
    if not o:
        return {"message": "origin node not found"}, 404

    d = session.query(Node).filter(Node.id == destination_id).first()
    if not d:
        return {"message": "destination node not found"}, 404

    if u.username not in [o.user_id, d.user_id]:
        return {"message": "user does not own any of the nodes"}, 401

    try:
        o.link(d, description, session)
    except Exception as e:
        return {"message": str(e)}, 400

    return {"message": "nodes linked"}, 200


def get_next_links_func(node_id: str, session: Session):
    """get next links' id"""
    n = session.query(Node).filter(Node.id == node_id).first()
    if not n:
        return {"message": "node not found"}, 404

    return {
        "message": "next links",
        "next_links": [
            {"description": link.description, "destination_id": link.destination_id}
            for link in n.get_next_links(session)
        ],
    }, 200


def get_previous_links_func(node_id: str, session: Session):
    """get previous links' id"""
    n = session.query(Node).filter(Node.id == node_id).first()
    if not n:
        return {"message": "node not found"}, 404

    return {
        "message": "previous links",
        "previous_links": [
            {"description": link.description, "origin_id": link.origin_id}
            for link in n.get_previous_links(session)
        ],
    }, 200


def update_playcount_func(node_id: str, session: Session):
    """update playcount"""
    n = session.query(Node).filter(Node.id == node_id).first()
    if not n:
        return {"message": "node not found"}, 404

    n.update_playcount(session)
    return {"message": "playcount updated", "playcount": n.get_playcount()}, 200


def update_rating_func(node_id: str, rating: float, session: Session):
    """update rating"""
    n = session.query(Node).filter(Node.id == node_id).first()
    if not n:
        return {"message": "node not found"}, 404

    try:
        n.update_rating(rating, session)
    except Exception as e:
        return {"message": str(e)}, 400
    return {"message": "rating updated", "rating": n.get_rating()}, 200


def update_node_description_func(
    username: str, node_id: str, description: str, session: Session
):
    """update description"""
    n = session.query(Node).filter(Node.id == node_id).first()
    if not n:
        return {"message": "node not found"}, 404

    if n.user_id != username:
        return {"message": "user does not own this node"}, 401

    n.update_description(description, session)
    return {"message": "description updated", "description": n.description}, 200


def update_node_title_func(username: str, node_id: str, title: str, session: Session):
    """update title"""
    n = session.query(Node).filter(Node.id == node_id).first()
    if not n:
        return {"message": "node not found"}, 404

    if n.user_id != username:
        return {"message": "user does not own this node"}, 401

    n.update_title(title, session)
    return {"message": "title updated"}, 200


def update_node_level_func(
    username: str, node_id: str, level: FileStorage, session: Session
):
    """update level"""
    n = session.query(Node).filter(Node.id == node_id).first()
    if not n:
        return {"message": "node not found"}, 404

    if n.user_id != username:
        return {"message": "user does not own this node"}, 401

    n.update_level(level)
    return {"message": "level updated"}, 200


def get_level_func(node_id: str, session: Session):
    """get level"""
    n = session.query(Node).filter(Node.id == node_id).first()
    if not n:
        return {"message": "node not found"}, 404

    # return a file which is in n.get_file_path()
    path = n.get_file_path()
    if not os.path.exists(path):
        return {"message": "level not found"}, 404

    content = "" 
    with open(path) as f:
        content = f.read()

    return {"message": "level", "level": content, "node_id": node_id}, 200


def create_path_func(username: str, title: str, description: str, session: Session):
    """create path"""
    u = session.query(User).filter(User.username == username).first()
    if not u:
        return {"message": "user not found"}, 404

    p = Path(session, u, title, description)
    return {"message": "path created", "path_id": p.id}, 201


def add_to_path_func(
    username: str, path_id: str, node_id: str, position: int, session: Session
):
    """add to path"""
    u = session.query(User).filter(User.username == username).first()
    if not u:
        return {"message": "user not found"}, 404

    p = session.query(Path).filter(Path.id == path_id).first()
    if not p:
        return {"message": "path not found"}, 404

    if p.user_id != username:
        return {"message": "user does not own this path"}, 401

    n = session.query(Node).filter(Node.id == node_id).first()
    if not n:
        return {"message": "node not found"}, 404

    try:
        p.add_node(n, position, session)
    except Exception as e:
        return {"message": str(e)}, 400

    return {"message": "node added to path"}, 200


def get_path_func(path_id: str, session: Session):
    """get path"""
    p = session.query(Path).filter(Path.id == path_id).first()
    if not p:
        return {"message": "path not found"}, 404

    node_seq = p.get_node_sequence(session)

    return {
        "message": "path info",
        "path": path_info(p, session),
    }, 200


def create_path_from_nodes_func(
    username: str,
    title: str,
    description: str,
    node_ids: list,
    positions: list,
    session: Session,
):
    """create path from nodes"""
    if len(node_ids) != len(positions):
        return {"message": "node_ids and positions must be the same length"}, 400

    u = session.query(User).filter(User.username == username).first()
    if not u:
        return {"message": "user not found"}, 404

    p = Path(session, u, title, description)
    for node_id, i in zip(node_ids, positions):
        n = session.query(Node).filter(Node.id == node_id).first()
        if not n:
            p.delete(session)
            return {"message": "node not found"}, 404

        try:
            pos = int(i)
        except ValueError:
            p.delete(session)
            return {"message": "position is not a number"}, 400

        try:
            p.add_node(n, pos, session)
        except Exception as e:
            p.delete(session)
            return {
                "message": f"path not created. try again. node with id {node_id} in position {pos} had the following problem: {str(e)}"
            }, 400

    return {"message": "path created", "path_id": p.id}, 201


def update_path_playcount_func(path_id: str, session: Session):
    """update path playcount"""
    p = session.query(Path).filter(Path.id == path_id).first()
    if not p:
        return {"message": "path not found"}, 404

    p.update_playcount(session)
    return {"message": "path playcount updated", "playcount": p.playcount}, 200


def update_path_rating_func(path_id: str, rating: float, session: Session):
    """update path rating"""
    p = session.query(Path).filter(Path.id == path_id).first()
    if not p:
        return {"message": "path not found"}, 404

    try:
        p.update_rating(rating, session)
    except Exception as e:
        return {"message": str(e)}, 400
    return {"message": "path rating updated", "rating": p.get_rating()}, 200


def update_path_title_func(username: str, path_id: str, title: str, session: Session):
    """update path title"""
    p = session.query(Path).filter(Path.id == path_id).first()
    if not p:
        return {"message": "path not found"}, 404

    if p.user_id != username:
        return {"message": "user does not own this path"}, 401

    p.update_title(title, session)
    return {"message": "path title updated"}, 200


def update_path_description_func(
    username: str, path_id: str, description: str, session: Session
):
    """update path description"""
    p = session.query(Path).filter(Path.id == path_id).first()
    if not p:
        return {"message": "path not found"}, 404

    if p.user_id != username:
        return {"message": "user does not own this path"}, 401

    p.update_description(description, session)
    return {"message": "path description updated"}, 200


def get_user_paths_func(username: str, session: Session):
    u = session.query(User).filter(User.username == username).first()
    if not u:
        return {"message": "user not found"}, 404

    # get all paths for user
    paths = session.query(Path).filter(Path.user_id == username).all()

    return {
        "message": "user paths",
        "paths": [path_info(p, session) for p in paths],
    }, 200

def get_node_paths_func(node_id: str, session: Session):
    n = session.query(Node).filter(Node.id == node_id).first()
    if not n:
        return {"message": "node not found"}, 404

    # get all paths for node
    associations = (
        session.query(PathNodeAssociation)
        .filter(PathNodeAssociation.c.node_id == node_id)
        .all()
    )

    s = set([a.path_id for a in associations])

    return {
        "message": "node paths",
        "paths": [
            path_info(p, session)
            for p in session.query(Path).filter(Path.id.in_(s)).all()
        ],
    }, 200

def query_users_func(query: str, s: Session):
    # query for users that have name like the query, case insensitive
    users = s.query(User).filter(User.username.ilike(f"%{query}%")).limit(20).all()

    return {
        "message": "users found",
        "users": [u.get_info() for u in users],
    }, 200

def query_nodes_func(query: str, s: Session):
    # query for nodes that have title like the query, case insensitive
    nodes = s.query(Node).filter(
        or_(
            Node.title.ilike(f"%{query}%"),
            Node.user_id.ilike(f"%{query}%")
        )
    ).order_by(Node.playcount.desc()).limit(20).all()

    return {
        "message": "nodes found",
        "nodes": [n.get_info() for n in nodes],
    }, 200

def query_paths_func(query: str, s: Session):
    # query for paths that have title like the query, case insensitive
    paths = s.query(Path).filter(
        or_(
            Path.title.ilike(f"%{query}%"),
            Path.user_id.ilike(f"%{query}%")
        )
    ).order_by(Path.playcount.desc()).limit(20).all()

    return {
        "message": "paths found",
        "paths": [path_info(p, s) for p in paths],
    }, 200

def get_popular_paths_func(s: Session):
    # get 20 most popular paths
    paths = s.query(Path).order_by(Path.playcount.desc()).limit(20).all()

    return {
        "message": "popular paths",
        "paths": [path_info(p, s) for p in paths],
    }, 200

def get_popular_nodes_func(s: Session):
    # get 20 most popular nodes
    nodes = s.query(Node).order_by(Node.playcount.desc()).limit(20).all()

    return {
        "message": "popular nodes",
        "nodes": [n.get_info() for n in nodes],
    }, 200

def path_info(p: Path, session: Session):
    node_seq, positions = p.get_node_sequence(session)

    return {
        "path_id": p.id,
        "user_id": p.user_id,
        "title": p.title,
        "description": p.description,
        "num_ratings": p.num_ratings,
        "rating": p.rating,
        "playcount": p.playcount,
        "node_sequence": [{"node": n.get_info(), "position": pos} for n, pos in zip(node_seq, positions)],
    }
