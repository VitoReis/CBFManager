from pymongo import MongoClient
from config import MONGO_URI, DB_NAME


def get_db():
    client = MongoClient(MONGO_URI)
    return client[DB_NAME]
