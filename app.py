import requests
from flask import Flask, Response, request
import json
import bson.json_util as json_util
from TMDB_Downloader import TMDBDownloader
from MongoDBAPI import MongoAPI
from mongo_tmdb_logic import mongo_tmdb

app = Flask(__name__)

mdb_client = MongoAPI("movies", "posters")
TMDBDownloader_client = TMDBDownloader()


@app.route('/')
def index():
    return '''
        <form method="GET" action="/search_movie enctype="multipart/form-data">
            <input type="text" name="movie_name">
            <input type="submit">
        </form>
    '''


@app.route('/search', methods=['GET'])
def search_movie():
    try:
        movie_name = request.form["movie_name"]
        logic_result = mongo_tmdb(mdb_client, TMDBDownloader_client, movie_name)
        return Response(
            response=json_util.dumps(logic_result),
            status=200,
            mimetype="application/json"
        )
    except Exception as ex:
        print(ex)
        return Response(
            response=json_util.dumps({"message": "cannot read users"}),
            status=500,
            mimetype="application/json"
        )


# @app.route('/file/<filename>')
# def file(filename):
#     return mongo.send_file(filename)
#
# @app.route('/movie/<movie_name>')
# def movie(movie_name):
#     user = mongo.db.users.find_one_or_404({'username': username})
#     return f'''
#     <h1>{username}</h1>
#     <img src="{url_for('file', filename=user['profile_image_name'])}">
# '''


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001)
    # url = 'http://localhost:5001/search'
    # moviename = "Avatar"
    # requests.post(url, moviename)
