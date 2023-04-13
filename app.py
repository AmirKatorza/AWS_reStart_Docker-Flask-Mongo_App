from flask import Flask, redirect, url_for
from pymongo import MongoClient
from flask import Flask, Response, request
import pymongo
import json
from bson.objectid import ObjectId

app = Flask(__name__)

try:
    mongo = pymongo.MongoClient(
        host="localhost",
        port=27017,
        serverSelectionTimeoutMS=10
    )
    db = mongo.movie_posters
    mongo.server_info()  # trigger exception if you cannot connect to db
except:
    print("Error - Cannot connect to db")


#########################
@app.route("/posters", methods=["GET"])
def get_some_users():
    try:
        data = list(db.users.find())
        for user in data:
            user["_id"] = str(user["_id"])
        return Response(
            response=json.dumps(data),
            status=200,
            mimetype="application/json"
        )
    except Exception as ex:
        print(ex)
        return Response(
            response=json.dumps({"message": "cannot read users"}),
            status=500,
            mimetype="application/json"
        )


#########################
@app.route("/users", methods=["POST"])
def create_user():
    try:
        user = {"name": request.form["name"], "lastName": request.form["lastName"]}
        db_response = db.users.insert_one(user)
        print(db_response.inserted_id)
        # for attr in dir(db_response):
        #     print(attr)
        return Response(
            response=json.dumps(
                {"message": "user created",
                 "id": f"{db_response.inserted_id}"
                 }
            ),
            status=200,
            mimetype="application/json"
        )
    except Exception as ex:
        print(ex)


#########################
@app.route("/users/<imdb_id>", methods=["PATCH"])
def update_user(imdb_id):
    try:
        db_response = db.users.update_one(
            {"_id": ObjectId(imdb_id)},
            {"$set": {"name": request.form["name"]}}
        )
        # for attr in dir(db_response):
        #     print(f"******{attr}******")
        if db_response.modified_count == 1:
            return Response(
                response=json.dumps({"message": "user is updated"}),
                status=200,
                mimetype="application/json"
            )
        return Response(
            response=json.dumps({"message": "nothing to updated"}),
            status=200,
            mimetype="application/json"
        )
    except Exception as ex:
        print("*****************************")
        print(ex)
        print("*****************************")
        return Response(
            response=json.dumps({"message": "sorry cannot update"}),
            status=500,
            mimetype="application/json"
        )


#########################
@app.route("/users/<imdb_id>", methods=["DELETE"])
def delete_user(imdb_id):
    try:
        db_response = db.users.delete_one({"_id": ObjectId(imdb_id)})
        if db_response.deleted_count == 1:
            return Response(
                response=json.dumps({"message": "user deleted", "id": f"{imdb_id}"}),
                status=200,
                mimetype="application/json"
            )
        return Response(
            response=json.dumps({"message": "user not found", "id": f"{imdb_id}"}),
            status=200,
            mimetype="application/json"
        )
    except Exception as ex:
        print("*****************************")
        print(ex)
        print("*****************************")
        return Response(
            response=json.dumps({"message": "sorry cannot delete"}),
            status=500,
            mimetype="application/json"
        )


#########################

if __name__ == "__main__":
    app.run(port=80, debug=True)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
