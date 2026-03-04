from pymongo import MongoClient
from config import settings


class DbClient:

    def __init__(self):
        self.client = MongoClient(settings.db_url)
        self.db = self.client["freeapi"]

    def get_all_users(self):
        return list(self.db.users.find({}))
