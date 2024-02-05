from flask import Flask, request
from api_func_user import *

app = Flask(__name__)
app.config["SECRET_KEY"] = "projectOctopusCertainlyIsNotThatSecret"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        return {"message": "Welcome to the Tentacle API (this is a post request)"}
    
    return {"message": "Welcome to the Tentacle API"}

@app.route("/create_user", methods=["POST"])
def create_user():
    if not("username" in request.form):
        return {"message": "no username parameter"}, 404
    
    if not("password" in request.form):
        return {"message": "no password parameter"}, 404
    
    if not("email" in request.form):
        return {"message": "no email parameter"}, 404
    
    return create_user_func(request.form["username"], request.form["password"], request.form["email"])

@app.route("/change_user_bio", methods=["POST"])
def change_user_bio():
    if not("username" in request.form):
        return {"message": "no username parameter"}, 404
    
    if not("bio" in request.form):
        return {"message": "no bio parameter"}, 404
    
    return change_user_bio_func(request.form["username"], request.form["bio"])

@app.route("/follow_user", methods=["POST"])
def follow_user():
    # check for existing username
    if not("username" in request.form):
        return {"message": "no username parameter"}, 404
    
    # check for existing followed username
    if not("followed_username" in request.form):
        return {"message": "no followed_username parameter"}, 404
    
    return follow_user_func(request.form["username"], request.form["followed_username"])

@app.route("/unfollow_user", methods=["POST"])
def unfollow_user():
    # check for existing username
    if not("username" in request.form):
        return {"message": "no username parameter"}, 404
    
    # check for existing unfollowed username
    if not("unfollowed_username" in request.form):
        return {"message": "no unfollowed_username parameter"}, 404
    
    return unfollow_user_func(request.form["username"], request.form["unfollowed_username"])

@app.route("/get_follows", methods=["GET"])
def get_follows():
    # check for existing username
    if not("username" in request.form):
        return {"message": "no username parameter"}, 404
     
    return get_follows_func(request.form["username"])

@app.route("/add_friend", methods=["POST"])
def add_friend():
    # check for existing username
    if not("username" in request.form):
        return {"message": "no username parameter"}, 404
    
    # check for existing friend username
    if not("friend_username" in request.form):
        return {"message": "no friend_username parameter"}, 404
    
    return add_friend_func(request.form["username"], request.form["friend_username"])

@app.route("/accept_friend", methods=["POST"])
def accept_friend():
    # check for existing username
    if not("username" in request.form):
        return {"message": "no username parameter"}, 404
    
    # check for existing friend username
    if not("friend_username" in request.form):
        return {"message": "no friend_username parameter"}, 404
    
    return accept_friend_func(request.form["username"], request.form["friend_username"])

@app.route("/reject_friend", methods=["POST"])
def reject_friend():
    # check for existing username
    if not("username" in request.form):
        return {"message": "no username parameter"}, 404
    
    # check for existing friend username
    if not("friend_username" in request.form):
        return {"message": "no friend_username parameter"}, 404
    
    return reject_friend_func(request.form["username"], request.form["friend_username"])

@app.route("/remove_friend", methods=["POST"])
def remove_friend():
    # check for existing username
    if not("username" in request.form):
        return {"message": "no username parameter"}, 404
    
    # check for existing friend username
    if not("friend_username" in request.form):
        return {"message": "no friend_username parameter"}, 404
    
    return remove_friend_func(request.form["username"], request.form["friend_username"])

@app.route("/get_friends", methods=["GET"])
def get_friends():
    # check for existing username
    if not("username" in request.form):
        return {"message": "no username parameter"}, 404
    
    return get_friends_func(request.form["username"])

if __name__ == "__main__":
    app.run(host='localhost', port=7809)
