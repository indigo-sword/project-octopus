from flask import Flask, request, session
from api_func import *
from functools import wraps

app = Flask(__name__)
app.config["SECRET_KEY"] = "projectOctopusCertainlyIsNotThatSecret"
app.secret_key = "projectOctopusCertainlyIsNotThatSecret"

########### User API ###########
def login_required(func):
    @wraps(func)
    @attribute_required("username")
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return {"message": "user not logged in"}, 401
        
        if request.form["username"] != session["username"]:
            return {"message": "wrong user for request"}, 401
        
        return func(*args, **kwargs)
    return decorated_function

def attribute_required(attribute):
    def decorator(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            if attribute not in request.form:
                return {"message": f"no {attribute} parameter"}, 404
            return func(*args, **kwargs)
        return decorated_function
    return decorator

@app.route("/login", methods=["POST"])
@attribute_required("username")
@attribute_required("password")
def login():
    msg, code = login_user_func(request.form["username"], request.form["password"])
    if code == 200:
        session["username"] = request.form["username"]
        session["logged_in"] = True

    return {"message": msg}, code

@app.route('/logout', methods=["POST"])
@login_required
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    return {"message": "logged out"}, 200

@app.route("/create_user", methods=["POST"])
@attribute_required("username")
@attribute_required("password")
@attribute_required("email")
def create_user():    
    bio = "" if not("bio" in request.form) else request.form["bio"]
    return create_user_func(request.form["username"], request.form["password"], request.form["email"], bio)

@app.route("/get_user", methods=["GET"])
@attribute_required("username")
def get_user():    
    return get_user_func(request.form["username"])

@app.route("/change_user_bio", methods=["POST"])
@login_required
@attribute_required("bio")
def change_user_bio():    
    return change_user_bio_func(request.form["username"], request.form["bio"])

@app.route("/follow_user", methods=["POST"])
@login_required
@attribute_required("followed_username")
def follow_user():
    return follow_user_func(request.form["username"], request.form["followed_username"])

@app.route("/unfollow_user", methods=["POST"])
@login_required
@attribute_required("unfollowed_username")
def unfollow_user():
    return unfollow_user_func(request.form["username"], request.form["unfollowed_username"])

@app.route("/get_follows", methods=["GET"])
@attribute_required("username")
def get_follows():     
    return get_follows_func(request.form["username"])

@app.route("/add_friend", methods=["POST"])
@login_required
@attribute_required("friend_username")
def add_friend():    
    return add_friend_func(request.form["username"], request.form["friend_username"])

@app.route("/accept_friend", methods=["POST"])
@login_required
@attribute_required("friend_username")
def accept_friend():
    return accept_friend_func(request.form["username"], request.form["friend_username"])

@app.route("/reject_friend", methods=["POST"])
@login_required
@attribute_required("friend_username")
def reject_friend():    
    return reject_friend_func(request.form["username"], request.form["friend_username"])

@app.route("/remove_friend", methods=["POST"])
@login_required
@attribute_required("friend_username")
def remove_friend():    
    return remove_friend_func(request.form["username"], request.form["friend_username"])

@app.route("/get_friends", methods=["GET"])
@attribute_required("username")
def get_friends():   
    return get_friends_func(request.form["username"])

########### Node API ###########
@app.route("/create_node", methods=["POST"])
@login_required
@attribute_required("description")
def create_node():    
    # needs to have also sent a file
    if "file" not in request.files:
        return {"message": "no file parameter"}, 404
    
    file_buf = request.files["file"]
    file_buf.seek(0, 2)

    if not file_buf or file_buf.tell() == 0:
        return {"message": "no file data"}, 404
    
    file_buf.seek(0)
    
    is_initial = False if not("is_initial" in request.form) else request.form["is_initial"] == "true"
    is_final = False if not("is_final" in request.form) else request.form["is_final"] == "true"
    return create_node_func(request.form["username"], request.form["description"], file_buf, is_initial, is_final)

@app.route("/get_node", methods=["GET"])
@attribute_required("node_id")
def get_node():    
    return get_node_func(request.form["node_id"])

@app.route("/link_nodes", methods=["POST"])
@login_required
@attribute_required("origin_id")
@attribute_required("destination_id")
@attribute_required("description")
def link_nodes():    
    return link_nodes_func(request.form["username"], request.form["origin_id"], request.form["destination_id"], request.form["description"])

@app.route("/get_next_links", methods=["GET"])
@attribute_required("node_id")
def get_next_links():    
    return get_next_links_func(request.form["node_id"])

@app.route("/get_previous_links", methods=["GET"])
@attribute_required("node_id")
def get_previous_links():    
    return get_previous_links_func(request.form["node_id"])

@app.route("/update_playcount", methods=["POST"])
@attribute_required("node_id")
def update_playcount():    
    return update_playcount_func(request.form["node_id"])

@app.route("/update_rating", methods=["POST"])
@login_required
@attribute_required("node_id")
@attribute_required("rating")
def update_rating():
    # check if rating is a number
    try:
        rating = float(request.form["rating"])
    except ValueError:
        return {"message": "rating is not a number"}, 404
        
    return update_rating_func(request.form["node_id"], rating)

@app.route("/update_node_description", methods=["POST"])
@login_required
@attribute_required("node_id")
@attribute_required("description")
def update_node_description():    
    return update_node_description_func(request.form["username"], request.form["node_id"], request.form["description"])

########### Path API ###########

if __name__ == "__main__":
    app.run(host='localhost', port=7809)
