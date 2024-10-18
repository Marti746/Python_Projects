#Flask is a A simple framework for building complex web applications.
# install flask open a terminal and type pip install flask
from flask import Flask, request, jsonify

app = Flask(__name__)

# create a root (an endpoint to go to)
# @app.route("/") # using the / means we use the default root but anything that comes after is the location in dircetory
# def home():
#     return "Home"

# path peramater (a dynamic value you can pass in the path of a url)
@app.route("/get-user/<user_id>")
def get_user(user_id):
    user_data = {
        "user_id": user_id,
        "name": "John Doe",
        "email": "john.doe@example.com"
    }

    # Query Parameter which is include after the path
    # ex: "get_user/123?extra=hello world"
    extra = request.args.get("extra")
    if extra:
        user_data["extra"] = extra
    
    return jsonify(user_data), 200

@app.route("/create-user", methods=["POST"])
def create_user():
    #if request.method == "POST"
    data = request.get_json()

    return jsonify(data), 201

# Most common methods are GET, POST, PUT, and DELETE
# get(request data from a specific resource), post (create a resource), put (update a resource)
# delete (delete a resource)

if __name__ == "__main__":
    app.run(debug=True)

# how to test api you can use postman (https://www.postman.com/)