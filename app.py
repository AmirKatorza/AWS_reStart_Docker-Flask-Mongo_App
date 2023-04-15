import requests
from flask import Flask, Response, request
import json
from TMDB_Downloader import TMDBDownloader
from MongoDBAPI import MongoAPI
from mongo_tmdb_logic import mongo_tmdb

app = Flask(__name__)

mdb_client = MongoAPI("movies", "posters")
TMDBDownloader_client = TMDBDownloader()


@app.route('/')
def index():
    return '<h1>Hello!</h1>'


@app.route('/search', methods=['GET'])
def search_movie():
    try:
        movie_name = request.form["movie_name"]
        logic_result = mongo_tmdb(mdb_client, TMDBDownloader_client, movie_name)
        return Response(
            response=json.dumps(logic_result),
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


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001)
    # url = 'http://localhost:5001/search'
    # moviename = "Avatar"
    # requests.post(url, moviename)

