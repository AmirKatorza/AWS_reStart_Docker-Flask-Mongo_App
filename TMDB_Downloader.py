from credentials import API_KEY_V3
import requests
import imdb


class TMDBDownloader:
    CONFIG_PATTERN = 'http://api.themoviedb.org/3/configuration?api_key={key}'
    IMG_PATTERN = "http://api.themoviedb.org/3/movie/{imdbid}/images?api_key={key}"

    def __init__(self):
        url = self.CONFIG_PATTERN.format(key=API_KEY_V3)
        result = requests.get(url)
        config = result.json()
        self.base_url = config["images"]["base_url"]
        self.poster_size = config["images"]["poster_sizes"][3]

    def _get_movies_ids(self, movie_name: str):
        ia = imdb.IMDb()
        items = ia.search_movie(movie_name)
        movies_dict = {}
        for movie in items:
            movie_id = movie.movieID  # Key
            movie_name = f"{movie}"  # Value
            movies_dict[movie_id] = movie_name
        return movies_dict

    def _get_poster_url(self, movie_id):
        result = requests.get(self.IMG_PATTERN.format(key=API_KEY_V3, imdbid=f"tt{movie_id}"))
        api_response = result.json()
        poster_path = api_response["posters"][0]["file_path"]
        return poster_path

    def download_poster(self, movie_name):
        movie_ids = self._get_movies_ids(movie_name)
        if movie_ids:
            for movie_id, movie_name in movie_ids.items():
                try:
                    poster_path = self._get_poster_url(movie_id)
                except Exception as e:
                    print(f"Could not find movie - {movie_name} - {movie_id}")
                else:
                    url = self.base_url + self.poster_size + poster_path
                    r = requests.get(url)
                    filetype = r.headers['content-type'].split('/')[-1]
                    filename = f"poster_{movie_id}.{filetype}"
                    return movie_id, filename, r.content
        return 0, None, 0


if __name__ == "__main__":
    download_agent = TMDBDownloader()
    moviename = "superman"
    # print(download_agent._get_movies_ids(moviename))
    movieid, file_name, byte_arr = download_agent.download_poster(moviename)
    print(movieid, file_name)
