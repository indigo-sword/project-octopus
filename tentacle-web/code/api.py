from flask import Flask, request, session
from api_func import *
from functools import wraps
from db_manager import Session

app = Flask(__name__)
app.config["SECRET_KEY"] = "projectOctopusCertainlyIsNotThatSecret"
app.secret_key = "projectOctopusCertainlyIsNotThatSecret"


########### User API ###########
def login_required(func):
    @wraps(func)
    @attribute_required("username")
    def decorated_function(*args, **kwargs):
        if "logged_in" not in session:
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
    s = Session()
    ret, code = login_user_func(request.form["username"], request.form["password"], s)

    if code == 200:
        session["username"] = request.form["username"]
        session["logged_in"] = True

    Session.remove()
    return ret, code


@app.route("/logout", methods=["POST"])
@login_required
def logout():
    session.pop("logged_in", None)
    session.pop("username", None)
    return {"message": "logged out"}, 200


@app.route("/create_user", methods=["POST"])
@attribute_required("username")
@attribute_required("password")
@attribute_required("email")
def create_user():
    bio = "" if not ("bio" in request.form) else request.form["bio"]
    s = Session()
    ret, code = create_user_func(
        request.form["username"],
        request.form["password"],
        request.form["email"],
        bio,
        s,
    )

    Session.remove()
    return ret, code


@app.route("/get_user", methods=["GET"])
@attribute_required("username")
def get_user():
    s = Session()
    ret, code = get_user_func(request.form["username"], s)

    Session.remove()
    return ret, code


@app.route("/change_user_bio", methods=["POST"])
@login_required
@attribute_required("bio")
def change_user_bio():
    s = Session()
    ret, code = change_user_bio_func(request.form["username"], request.form["bio"], s)

    Session.remove()
    return ret, code


@app.route("/follow_user", methods=["POST"])
@login_required
@attribute_required("followed_username")
def follow_user():
    s = Session()
    ret, code = follow_user_func(
        request.form["username"], request.form["followed_username"], s
    )

    Session.remove()
    return ret, code


@app.route("/unfollow_user", methods=["POST"])
@login_required
@attribute_required("unfollowed_username")
def unfollow_user():
    s = Session()
    ret, code = unfollow_user_func(
        request.form["username"], request.form["unfollowed_username"], s
    )
    Session.remove()
    return ret, code


@app.route("/get_follows", methods=["GET"])
@attribute_required("username")
def get_follows():
    s = Session()
    ret, code = get_follows_func(request.form["username"], s)
    Session.remove()
    return ret, code


@app.route("/add_friend", methods=["POST"])
@login_required
@attribute_required("friend_username")
def add_friend():
    s = Session()
    ret, code = add_friend_func(
        request.form["username"], request.form["friend_username"], s
    )
    Session.remove()
    return ret, code


@app.route("/accept_friend", methods=["POST"])
@login_required
@attribute_required("friend_username")
def accept_friend():
    s = Session()
    ret, code = accept_friend_func(
        request.form["username"], request.form["friend_username"], s
    )
    Session.remove()
    return ret, code


@app.route("/reject_friend", methods=["POST"])
@login_required
@attribute_required("friend_username")
def reject_friend():
    s = Session()
    ret, code = reject_friend_func(
        request.form["username"], request.form["friend_username"], s
    )
    Session.remove()
    return ret, code


@app.route("/remove_friend", methods=["POST"])
@login_required
@attribute_required("friend_username")
def remove_friend():
    s = Session()
    ret, code = remove_friend_func(
        request.form["username"], request.form["friend_username"], s
    )
    Session.remove()
    return ret, code


@app.route("/get_friends", methods=["GET"])
@attribute_required("username")
def get_friends():
    s = Session()
    ret, code = get_friends_func(request.form["username"], s)
    Session.remove()
    return ret, code


########### Node API ###########
@app.route("/create_node", methods=["POST"])
@login_required
@attribute_required("description")
@attribute_required("title")
def create_node():
    # needs to have also sent a file
    if "file" not in request.files:
        return {"message": "no file parameter"}, 404

    file_buf = request.files["file"]
    file_buf.seek(0, 2)

    if not file_buf or file_buf.tell() == 0:
        return {"message": "no file data"}, 404

    file_buf.seek(0)

    is_initial = (
        False
        if not ("is_initial" in request.form)
        else request.form["is_initial"] == "true"
    )
    is_final = (
        False
        if not ("is_final" in request.form)
        else request.form["is_final"] == "true"
    )

    s = Session()
    ret, code = create_node_func(
        request.form["username"],
        request.form["title"],
        request.form["description"],
        file_buf,
        is_initial,
        is_final,
        s,
    )
    Session.remove()
    return ret, code


@app.route("/get_level", methods=["GET"])
@attribute_required("node_id")
def get_level():
    s = Session()
    ret, code = get_level_func(request.form["node_id"], s)
    Session.remove()
    return ret, code


@app.route("/update_node_level", methods=["POST"])
@login_required
@attribute_required("node_id")
def update_node_level():
    # needs to have also sent a file
    if "file" not in request.files:
        return {"message": "no file parameter"}, 404

    file_buf = request.files["file"]
    file_buf.seek(0, 2)

    if not file_buf or file_buf.tell() == 0:
        return {"message": "no file data"}, 404

    file_buf.seek(0)

    s = Session()
    ret, code = update_node_level_func(
        request.form["username"], request.form["node_id"], file_buf, s
    )
    Session.remove()
    return ret, code


@app.route("/get_node", methods=["GET"])
@attribute_required("node_id")
def get_node():
    s = Session()
    ret, code = get_node_func(request.form["node_id"], s)
    Session.remove()
    return ret, code


@app.route("/link_nodes", methods=["POST"])
@login_required
@attribute_required("origin_id")
@attribute_required("destination_id")
@attribute_required("description")
def link_nodes():
    s = Session()
    ret, code = link_nodes_func(
        request.form["username"],
        request.form["origin_id"],
        request.form["destination_id"],
        request.form["description"],
        s,
    )
    Session.remove()
    return ret, code


@app.route("/get_next_links", methods=["GET"])
@attribute_required("node_id")
def get_next_links():
    s = Session()
    ret, code = get_next_links_func(request.form["node_id"], s)
    Session.remove()
    return ret, code


@app.route("/get_previous_links", methods=["GET"])
@attribute_required("node_id")
def get_previous_links():
    s = Session()
    ret, code = get_previous_links_func(request.form["node_id"], s)
    Session.remove()
    return ret, code


@app.route("/update_playcount", methods=["POST"])
@attribute_required("node_id")
def update_playcount():
    s = Session()
    ret, code = update_playcount_func(request.form["node_id"], s)
    Session.remove()
    return ret, code


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

    s = Session()
    ret, code = update_rating_func(request.form["node_id"], rating, s)
    Session.remove()
    return ret, code


@app.route("/update_node_description", methods=["POST"])
@login_required
@attribute_required("node_id")
@attribute_required("description")
def update_node_description():
    s = Session()
    ret, code = update_node_description_func(
        request.form["username"],
        request.form["node_id"],
        request.form["description"],
        s,
    )
    Session.remove()
    return ret, code


@app.route("/update_node_title", methods=["POST"])
@login_required
@attribute_required("node_id")
@attribute_required("title")
def update_node_title():
    s = Session()
    ret, code = update_node_title_func(
        request.form["username"], request.form["node_id"], request.form["title"], s
    )
    Session.remove()
    return ret, code


########### Path API ###########
@app.route("/create_path", methods=["POST"])
@login_required
@attribute_required("title")
@attribute_required("description")
def create_path():
    s = Session()
    ret, code = create_path_func(
        request.form["username"], request.form["title"], request.form["description"], s
    )
    Session.remove()
    return ret, code


@app.route("/add_to_path", methods=["POST"])
@login_required
@attribute_required("path_id")
@attribute_required("node_id")
@attribute_required("position")
def add_to_path():
    # parse int for position
    try:
        position = int(request.form["position"])
    except ValueError:
        return {"message": "position is not a number"}, 404

    s = Session()
    ret, code = add_to_path_func(
        request.form["username"],
        request.form["path_id"],
        request.form["node_id"],
        position,
        s,
    )
    Session.remove()
    return ret, code


@app.route("/get_path", methods=["GET"])
@attribute_required("path_id")
def get_path():
    s = Session()
    ret, code = get_path_func(request.form["path_id"], s)
    Session.remove()
    return ret, code


@app.route("/create_path_from_nodes", methods=["POST"])
@login_required
@attribute_required("title")
@attribute_required("description")
@attribute_required("node_ids")
@attribute_required("positions")
def create_path_from_nodes():
    node_ids = request.form.getlist("node_ids", type=str)
    positions = request.form.getlist("positions", type=int)

    s = Session()
    ret, code = create_path_from_nodes_func(
        request.form["username"],
        request.form["title"],
        request.form["description"],
        node_ids,
        positions,
        s,
    )
    Session.remove()
    return ret, code


@app.route("/update_path_playcount", methods=["POST"])
@attribute_required("path_id")
def update_path_playcount():
    s = Session()
    ret, code = update_path_playcount_func(request.form["path_id"], s)
    Session.remove()
    return ret, code


@app.route("/update_path_rating", methods=["POST"])
@login_required
@attribute_required("path_id")
@attribute_required("rating")
def update_path_rating():
    # check if rating is a number
    try:
        rating = int(request.form["rating"])
    except ValueError:
        return {"message": "rating is not an int"}, 404

    s = Session()
    ret, code = update_path_rating_func(request.form["path_id"], rating, s)
    Session.remove()
    return ret, code


@app.route("/update_path_title", methods=["POST"])
@login_required
@attribute_required("path_id")
@attribute_required("title")
def update_path_title():
    s = Session()
    ret, code = update_path_title_func(
        request.form["username"], request.form["path_id"], request.form["title"], s
    )
    Session.remove()
    return ret, code


@app.route("/update_path_description", methods=["POST"])
@login_required
@attribute_required("path_id")
@attribute_required("description")
def update_path_description():
    s = Session()
    ret, code = update_path_description_func(
        request.form["username"],
        request.form["path_id"],
        request.form["description"],
        s,
    )
    Session.remove()
    return ret, code


@app.route("/get_user_paths", methods=["GET"])
@attribute_required("username")
def get_user_paths():
    s = Session()
    ret, code = get_user_paths_func(request.form["username"], s)
    Session.remove()
    return ret, code


@app.route("/get_node_paths", methods=["GET"])
@attribute_required("node_id")
def get_node_paths():
    s = Session()
    ret, code = get_node_paths_func(request.form["node_id"], s)
    Session.remove()
    return ret, code


def custom_logger(environ, start_response):
    remote_address = environ.get("REMOTE_ADDR", "UNKNOWN")
    request_method = environ.get("REQUEST_METHOD", "UNKNOWN")
    path_info = environ.get("PATH_INFO", "UNKNOWN")
    query_string = environ.get("QUERY_STRING", "UNKNOWN")

    print(f"Request from: {remote_address}")
    print(f"Method: {request_method}")
    print(f"Path: {path_info}")

    return app(environ, start_response)


if __name__ == "__main__":
    from waitress import serve

    host = "0.0.0.0"
    port = 8080
    print(f"Running server on host {host} at port {port}")
    serve(custom_logger, host=host, port=port)
