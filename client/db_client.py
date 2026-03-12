from pymongo import MongoClient
from config import settings


class DbClient:

    def __init__(self):
        self.client = MongoClient(settings.db_url)
        self.db = self.client["freeapi"]

    def get_all_users(self) -> list:
        """
        Получение всех пользователей
        :return Список пользователей
        """
        return list(self.db.users.find({}))

    def delete_user(self, username: str):
        """
        Удаление пользователя
        :param username
        """
        return self.db.users.delete_one({"username": username})

    def get_user(self, username: str) -> dict:
        """
        Получение пользователя
        :param username Имя пользователя
        :return Пользователь
        """
        return self.db.users.find_one({"username": username})
