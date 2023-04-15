def mongo_tmdb(mongo_client, tmdb_client, movie_name):
    search_mongo_result = mongo_client.read_image(movie_name)
    if search_mongo_result is None:
        imdb_id, file_name, byte_arr = tmdb_client.download_poster(movie_name)
        if (imdb_id != 0) and (file_name is not None) and (byte_arr != 0):
            write_results = mongo_client.write_image(file_name, movie_name, imdb_id, byte_arr)
            new_search_mongo = mongo_client.read_image(movie_name)
            new_search_mongo['Status'] = "Added to DB"
            new_search_mongo['file_name'] = movie_name + ".jpeg"
            return new_search_mongo
        else:
            output = {'_id': None, 'Status': "Not Exists", 'file_name': None}
            return output
    search_mongo_result["Status"] = "Found in DB"
    search_mongo_result['file_name'] = movie_name + ".jpeg"
    return search_mongo_result

