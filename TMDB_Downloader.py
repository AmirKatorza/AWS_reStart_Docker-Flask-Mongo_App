from credentials import *
import requests
import imdb
import pymongo
import gridfs


def mongo_conn():
    try:
        conn = pymongo.MongoClient(
            host="localhost",
            port=27017,
            serverSelectionTimeoutMS=10
        )
        conn.server_info()  # trigger exception if you cannot connect to db
        print("MongoDB connected", conn)
        return conn
        return conn.grid_file
    except Exception as e:
        print("Error in mongo connection: ", e)


def config_poster_download():
    CONFIG_PATTERN = 'http://api.themoviedb.org/3/configuration?api_key={key}'
    url = CONFIG_PATTERN.format(key=API_KEY_V3)
    result = requests.get(url)
    config = result.json()
    base_url = config["images"]["base_url"]
    poster_size = config["images"]["poster_sizes"][3]
    return base_url, poster_size


def get_imdb_id(movie_name: str) -> dict:
    ia = imdb.IMDb()
    items = ia.search_movie(movie_name)
    movie_dict = {}
    for movie in items:
        movie_id = movie.movieID  # Key
        movie_name = f"{movie}"   # Value
        movie_dict[movie_id] = movie_name
    return movie_dict


def get_posters_urls(movie_id):
    IMG_PATTERN = "http://api.themoviedb.org/3/movie/{imdbid}/images?api_key={key}"
    result = requests.get(IMG_PATTERN.format(key=API_KEY_V3, imdbid=f"tt{movie_id}"))
    api_response = result.json()
    # json_formatted_str = json.dumps(api_response, indent=2)
    # print(json_formatted_str)
    poster_path = api_response["posters"][0]["file_path"]
    return poster_path


def index_poster(movies_dict):
    db = mongo_conn().movies
    fs = gridfs.GridFS(db, "posters")
    base_url, size = config_poster_download()
    for movie_id, movie_name in movies_dict.items():
        try:
            poster_path = get_posters_urls(movie_id)
        except Exception as e:
            print(f"Could not find movie - {movie_name} - {movie_id}")
        else:
            url = base_url + size + poster_path
            r = requests.get(url)
            filetype = r.headers['content-type'].split('/')[-1]
            filename = f"poster_{movie_id}.{filetype}"
            fs.put(r.content, movie_name=movie_name, imdb_id=movie_id, filename=filename)


movie_search = input("Please enter movie name to search: ")
search_results = get_imdb_id(movie_search)
index_poster(search_results)

# movies_db = mongo_conn().movies
# query = movies_db.posters.files.find({'movie_name': {'$regex': 'Avatar'}})
# # for item in query:
# #     print(item)
# print(list(query))
# if len(list(query)) == 0:

