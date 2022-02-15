from helper import query
from lib import mongo


class SaveData:
    def __init__(self):
        self.db = mongo.connect()

    def save(self, data):
        query.insert_data(self.db, "contentTweet", data)
