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
    print(request.form)

if __name__ == "__main__":
    app.run(host='localhost', port=7809)
