from pymongo import MongoClient
import gridfs
import logging as log
import os
import TMDB_Downloader


class MongoAPI:
    def __init__(self, db_name, collection, ip="localhost", port=27017):
        self.client = MongoClient(host=ip,
                                  port=port,
                                  serverSelectionTimeoutMS=10
                                  )
        self.collection = collection
        self.db = self.client[db_name]
        self.fs = gridfs.GridFS(self.db, collection)

    def write_image(self, file_name, movie_name, imdb_id, byte_arr):
        log.info('Writing Data')
        fs_id = self.fs.put(byte_arr, movie_name=movie_name, imdb_id=imdb_id, filename=file_name)
        output = {'_id': fs_id, 'Status': 'Successfully Inserted'}
        return output

    def read_image(self, movie_name):
        f_id = self.db[self.collection + ".files"].find_one({"movie_name": movie_name}, {"_id": 1})
        if f_id is not None:
            byte_arr = self.fs.get(f_id['_id']).read()
            path = "./posters_images/"
            is_exist = os.path.exists(path)
            if not is_exist:
                os.mkdir("./posters_images/")
            with open(path + movie_name + ".jpeg", 'wb') as w:
                w.write(byte_arr)
        return f_id

    def get_file_id_by_name(self, movie_name):
        return self.db[self.collection + ".files"].find_one({"movie_name": movie_name}, {"_id": 1})

    def del_image(self, movie_name):
        log.info('Deleting Data')
        f_id = self.get_file_id_by_name(movie_name)
        self.fs.delete(f_id)
        output = {'Status': 'Successfully Deleted' if f_id else "Nothing was Deleted."}
        return output

    def update_image_file_meta_data(self, movie_name, key_to_update, val_to_update):
        f_id = self.get_file_id_by_name(movie_name)
        mycol = self.db[self.collection + ".files"]
        myquery = {"_id": f_id}
        new_values = {"$set": {key_to_update: val_to_update}}
        db_update_response = mycol.update_one(myquery, new_values)
        output = {'Status': 'Successfully Updated' if db_update_response.modified_count > 0 else "Nothing was updated."}
        return output


if __name__ == '__main__':
    mdb = MongoAPI("movies", "posters")
    # download_agent = TMDB_Downloader.TMDBDownloader()
    moviename = "Batman"
    # movieid, file_name, byte_arr = download_agent.download_poster(moviename)
    # mdb.write_image(file_name, moviename, movieid, byte_arr)
    r = mdb.read_image(moviename)
    print(r)
