from flask import Flask, request
from db_manager import db_session

app = Flask(__name__)
app.config["SECRET_KEY"] = "projectOctopusCertainlyIsNotThatSecret"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # return a JSON
        print(request.form)
        return {"message": "Welcome to the Tentacle API (this is a post request)"}
    
    # return a JSON
    return {"message": "Welcome to the Tentacle API"}

@app.route("/create_user", methods=["POST"])
def create_user():
    print(request.form)
    # return a JSON
    return {"message": "User created"}, 201

@app.route("/change_user_bio", methods=["POST"])
def change_user_bio():
    print(request.form)

if __name__ == "__main__":
    app.run(host='localhost', port=7809)
