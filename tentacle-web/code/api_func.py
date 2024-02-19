from db_manager import Session
from user import User
from node import Node
from path import Path, path_node_association as PathNodeAssociation
import bcrypt
import re
from werkzeug.datastructures import FileStorage
from flask import send_file
import os


def login_user_func(username: str, password: str):
    """login user"""
    session = Session()
    u = session.query(User).filter(User.username == username).first()
    Session.remove()

    if not u:
        return "user not found", 404

    if bcrypt.checkpw(password.encode("utf-8"), u.password):
        return "user logged in", 200

    else:
        return "invalid password", 401


def create_user_func(username: str, password: str, email: str, bio: str):
    """create user"""
    # perform email regex check
    if not re.match(r"^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$", email):
        return {"message": "invalid email"}, 400

    # check for existing username
    if Session.query(User).filter(User.username == username).first():
        return {"message": "username already exists"}, 409

    # check for existing email
    if Session.query(User).filter(User.email == email).first():
        return {"message": "email already exists"}, 409

    # create user
    User(Session, username, password, email, bio)

    return {"message": "user created"}, 201


def change_user_bio_func(username: str, bio: str):
    """change user bio"""
    u = Session.query(User).filter(User.username == username).first()
    if not u:
        return {"message": "user not found"}, 404

    u.update_bio(Session, bio)
    return {"message": "user bio updated", "bio": bio}, 200


def follow_user_func(username: str, followed_username: str):
    """follow user"""
    u = Session.query(User).filter(User.username == username).first()
    if not u:
        return {"message": "user not found"}, 404

    f = Session.query(User).filter(User.username == followed_username).first()
    if not f:
        return {"message": "followed user not found"}, 404

    u.follow(Session, f)
    return {"message": "user followed"}, 200


def unfollow_user_func(username: str, unfollowed_username: str):
    # get user
    u = Session.query(User).filter(User.username == username).first()
    if not u:
        return {"message": "user not found"}, 404

    # get user to be unfollowed
    f = Session.query(User).filter(User.username == unfollowed_username).first()
    if not f:
        return {"message": "unfollowed user not found"}, 404

    try:
        u.unfollow(Session, f)
    except:
        return {"message": "user is not being followed"}, 400

    # return user
    return {"message": "user unfollowed"}, 200


def get_follows_func(username: str):
    """get follows"""
    u = Session.query(User).filter(User.username == username).first()
    if not u:
        return {"message": "user not found"}, 404

    return {
        "message": "user following and followed",
        "following": u.get_following(Session),
        "followed": u.get_followers(Session),
    }, 200


def get_user_func(username: str):
    """get user"""
    u = Session.query(User).filter(User.username == username).first()
    if not u:
        return {"message": "user not found"}, 404

    return {
        "message": "user info",
        "username": u.username,
        "bio": u.bio,
        "email": u.email,
        "following": u.following,
        "followers": u.followers,
    }, 200


def add_friend_func(username: str, friend_username: str):
    """add friend"""
    u = Session.query(User).filter(User.username == username).first()
    if not u:
        return {"message": "user not found"}, 404

    f = Session.query(User).filter(User.username == friend_username).first()
    if not f:
        return {"message": "friend user not found"}, 404

    # already friends
    if friend_username in u.get_friends(Session):
        return {"message": "user is already a friend"}, 400

    # check for existing friend request sent
    if friend_username in u.get_friend_requests_sent(Session):
        return {"message": "friend request already sent"}, 400

    # check for other user already having asked them
    if friend_username in u.get_friend_requests(Session):
        u.accept_friend_request(Session, f)
        return {"message": "friend request accepted"}, 200

    u.send_friend_request(Session, f)
    return {"message": "friend request sent"}, 200


def accept_friend_func(username: str, friend_username: str):
    """accept friend"""
    u = Session.query(User).filter(User.username == username).first()
    if not u:
        return {"message": "user not found"}, 404

    f = Session.query(User).filter(User.username == friend_username).first()
    if not f:
        return {"message": "friend user not found"}, 404

    try:
        u.accept_friend_request(Session, f)
    except:
        return {"message": "no friend request from this user"}, 400

    return {"message": "friend request accepted"}, 200


def reject_friend_func(username: str, friend_username: str):
    """reject friend"""
    u = Session.query(User).filter(User.username == username).first()
    if not u:
        return {"message": "user not found"}, 404

    f = Session.query(User).filter(User.username == friend_username).first()
    if not f:
        return {"message": "friend user not found"}, 404

    try:
        u.reject_friend_request(Session, f)
    except:
        return {"message": "no friend request from this user"}, 400

    return {"message": "friend request rejected"}, 200


def remove_friend_func(username: str, friend_username: str):
    """remove friend"""
    u = Session.query(User).filter(User.username == username).first()
    if not u:
        return {"message": "user not found"}, 404

    f = Session.query(User).filter(User.username == friend_username).first()
    if not f:
        return {"message": "friend user not found"}, 404

    try:
        u.remove_friend(Session, f)
    except:
        return {"message": "user is not a friend"}, 400

    return {"message": "friend removed"}, 200


def get_friends_func(username: str):
    """get friends"""
    u = Session.query(User).filter(User.username == username).first()
    if not u:
        return {"message": "user not found"}, 404

    return {
        "message": "user friends",
        "friends": u.get_friends(Session),
        "requests": u.get_friend_requests(Session),
        "sent requests": u.get_friend_requests_sent(Session),
    }, 200


def create_node_func(
    username: str,
    title: str,
    description: str,
    file_buf: FileStorage,
    is_initial: bool = False,
    is_final: bool = False,
):
    """create node"""
    u = Session.query(User).filter(User.username == username).first()
    if not u:
        return {"message": "user not found"}, 404

    # create node
    try:
        n = Node(Session, u, title, description, file_buf, is_initial, is_final)
    except Exception:
        return {"message": "node creation failed. try again."}, 400

    return {"message": "node created", "node_id": n.id}, 201


def get_node_func(node_id: str):
    """get node"""
    n = Session.query(Node).filter(Node.id == node_id).first()
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
    username: str, origin_id: str, destination_id: str, description: str
):
    """link nodes"""
    u = Session.query(User).filter(User.username == username).first()
    if not u:
        return {"message": "user not found"}, 404

    o = Session.query(Node).filter(Node.id == origin_id).first()
    if not o:
        return {"message": "origin node not found"}, 404

    d = Session.query(Node).filter(Node.id == destination_id).first()
    if not d:
        return {"message": "destination node not found"}, 404

    if u.username not in [o.user_id, d.user_id]:
        return {"message": "user does not own any of the nodes"}, 401

    try:
        o.link(d, description, Session)
    except Exception as e:
        return {"message": str(e)}, 400

    return {"message": "nodes linked"}, 200


def get_next_links_func(node_id: str):
    """get next links' id"""
    n = Session.query(Node).filter(Node.id == node_id).first()
    if not n:
        return {"message": "node not found"}, 404

    return {
        "message": "next links",
        "next_links": [
            {"description": link.description, "destination_id": link.destination_id}
            for link in n.get_next_links(Session)
        ],
    }, 200


def get_previous_links_func(node_id: str):
    """get previous links' id"""
    n = Session.query(Node).filter(Node.id == node_id).first()
    if not n:
        return {"message": "node not found"}, 404

    return {
        "message": "previous links",
        "previous_links": [
            {"description": link.description, "origin_id": link.origin_id}
            for link in n.get_previous_links(Session)
        ],
    }, 200


def update_playcount_func(node_id: str):
    """update playcount"""
    n = Session.query(Node).filter(Node.id == node_id).first()
    if not n:
        return {"message": "node not found"}, 404

    n.update_playcount(Session)
    return {"message": "playcount updated", "playcount": n.get_playcount()}, 200


def update_rating_func(node_id: str, rating: float):
    """update rating"""
    n = Session.query(Node).filter(Node.id == node_id).first()
    if not n:
        return {"message": "node not found"}, 404

    try:
        n.update_rating(rating, Session)
    except Exception as e:
        return {"message": str(e)}, 400
    return {"message": "rating updated", "rating": n.get_rating()}, 200


def update_node_description_func(username: str, node_id: str, description: str):
    """update description"""
    n = Session.query(Node).filter(Node.id == node_id).first()
    if not n:
        return {"message": "node not found"}, 404

    if n.user_id != username:
        return {"message": "user does not own this node"}, 401

    n.update_description(description, Session)
    return {"message": "description updated", "description": n.description}, 200


def update_node_title_func(username: str, node_id: str, title: str):
    """update title"""
    n = Session.query(Node).filter(Node.id == node_id).first()
    if not n:
        return {"message": "node not found"}, 404

    if n.user_id != username:
        return {"message": "user does not own this node"}, 401

    n.update_title(title, Session)
    return {"message": "title updated"}, 200


def update_node_level_func(username: str, node_id: str, level: FileStorage):
    """update level"""
    n = Session.query(Node).filter(Node.id == node_id).first()
    if not n:
        return {"message": "node not found"}, 404

    if n.user_id != username:
        return {"message": "user does not own this node"}, 401

    n.update_level(level)
    return {"message": "level updated"}, 200


def get_level_func(node_id: str):
    """get level"""
    n = Session.query(Node).filter(Node.id == node_id).first()
    if not n:
        return {"message": "node not found"}, 404

    # return a file which is in n.get_file_path()
    path = n.get_file_path()
    if not os.path.exists(path):
        return {"message": "level not found"}, 404

    return send_file(path, as_attachment=True)


def create_path_func(username: str, title: str, description: str):
    """create path"""
    u = Session.query(User).filter(User.username == username).first()
    if not u:
        return {"message": "user not found"}, 404

    p = Path(Session, u, title, description)
    return {"message": "path created", "path_id": p.id}, 201


def add_to_path_func(username: str, path_id: str, node_id: str, position: int):
    """add to path"""
    u = Session.query(User).filter(User.username == username).first()
    if not u:
        return {"message": "user not found"}, 404

    p = Session.query(Path).filter(Path.id == path_id).first()
    if not p:
        return {"message": "path not found"}, 404

    if p.user_id != username:
        return {"message": "user does not own this path"}, 401

    n = Session.query(Node).filter(Node.id == node_id).first()
    if not n:
        return {"message": "node not found"}, 404

    try:
        p.add_node(n, position, Session)
    except Exception as e:
        return {"message": str(e)}, 400

    return {"message": "node added to path"}, 200


def get_path_func(path_id: str):
    """get path"""
    p = Session.query(Path).filter(Path.id == path_id).first()
    if not p:
        return {"message": "path not found"}, 404

    node_seq = p.get_node_sequence(Session)

    return {
        "message": "path info",
        "path": path_info(p),
    }, 200


def create_path_from_nodes_func(
    username: str, title: str, description: str, node_ids: list, positions: list
):
    """create path from nodes"""
    if len(node_ids) != len(positions):
        return {"message": "node_ids and positions must be the same length"}, 400

    u = Session.query(User).filter(User.username == username).first()
    if not u:
        return {"message": "user not found"}, 404

    p = Path(Session, u, title, description)
    for node_id, i in zip(node_ids, positions):
        n = Session.query(Node).filter(Node.id == node_id).first()
        if not n:
            p.delete(Session)
            return {"message": "node not found"}, 404

        try:
            pos = int(i)
        except ValueError:
            p.delete(Session)
            return {"message": "position is not a number"}, 400

        try:
            p.add_node(n, pos, Session)
        except Exception as e:
            p.delete(Session)
            return {
                "message": f"path not created. try again. node with id {node_id} in position {pos} had the following problem: {str(e)}"
            }, 400

    return {"message": "path created", "path_id": p.id}, 201


def update_path_playcount_func(path_id: str):
    """update path playcount"""
    p = Session.query(Path).filter(Path.id == path_id).first()
    if not p:
        return {"message": "path not found"}, 404

    p.update_playcount(Session)
    return {"message": "path playcount updated", "playcount": p.playcount}, 200


def update_path_rating_func(path_id: str, rating: int):
    """update path rating"""
    p = Session.query(Path).filter(Path.id == path_id).first()
    if not p:
        return {"message": "path not found"}, 404

    try:
        p.update_rating(rating, Session)
    except Exception as e:
        return {"message": str(e)}, 400
    return {"message": "path rating updated", "rating": p.get_rating()}, 200


def update_path_title_func(username: str, path_id: str, title: str):
    """update path title"""
    p = Session.query(Path).filter(Path.id == path_id).first()
    if not p:
        return {"message": "path not found"}, 404

    if p.user_id != username:
        return {"message": "user does not own this path"}, 401

    p.update_title(title, Session)
    return {"message": "path title updated"}, 200


def update_path_description_func(username: str, path_id: str, description: str):
    """update path description"""
    p = Session.query(Path).filter(Path.id == path_id).first()
    if not p:
        return {"message": "path not found"}, 404

    if p.user_id != username:
        return {"message": "user does not own this path"}, 401

    p.update_description(description, Session)
    return {"message": "path description updated"}, 200


def get_user_paths_func(username: str):
    u = Session.query(User).filter(User.username == username).first()
    if not u:
        return {"message": "user not found"}, 404

    # get all paths for user
    paths = Session.query(Path).filter(Path.user_id == username).all()

    return {
        "message": "user paths",
        "paths": [path_info(p) for p in paths],
    }, 200


def get_node_paths_func(node_id: str):
    n = Session.query(Node).filter(Node.id == node_id).first()
    if not n:
        return {"message": "node not found"}, 404

    # get all paths for node
    associations = (
        Session.query(PathNodeAssociation)
        .filter(PathNodeAssociation.c.node_id == node_id)
        .all()
    )

    s = set([a.path_id for a in associations])

    return {
        "message": "node paths",
        "paths": [
            path_info(p) for p in Session.query(Path).filter(Path.id.in_(s)).all()
        ],
    }, 200


def path_info(p: Path):
    node_seq = p.get_node_sequence(Session)

    return {
        "path_id": p.id,
        "user_id": p.user_id,
        "title": p.title,
        "description": p.description,
        "num_ratings": p.num_ratings,
        "rating": p.rating,
        "playcount": p.playcount,
        "node_sequence": [n.node_id for n in node_seq],
        "positions": [n.position for n in node_seq],
    }
