import pymongo
import os
from dotenv import load_dotenv

load_dotenv()


def connect():
    client = pymongo.MongoClient(os.environ.get('MONGO_HOST'))
    return getattr(client, os.environ.get('MONGO_DB'))


def connect_client():
    client = pymongo.MongoClient(os.environ.get('MONGO_HOST'))
    return getattr(client, os.environ.get('MONGO_DB')), client
