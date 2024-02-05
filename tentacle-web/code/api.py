from flask import Flask, request
from db_manager import db_session
from api_func import *

app = Flask(__name__)
app.config["SECRET_KEY"] = "projectOctopusCertainlyIsNotThatSecret"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        return {"message": "Welcome to the Tentacle API (this is a post request)"}
    
    return {"message": "Welcome to the Tentacle API"}

@app.route("/create_user", methods=["POST"])
def create_user():
    return create_user_func(request.form["username"], request.form["password"], request.form["email"])

@app.route("/change_user_bio", methods=["POST"])
def change_user_bio():
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

@app.route("/get_follows", methods=["POST"])
def get_follows():
    # check for existing username
    if not("username" in request.form):
        return {"message": "no username parameter"}, 404
     
    return get_follows_func(request.form["username"])

if __name__ == "__main__":
    app.run(host='localhost', port=7809)
