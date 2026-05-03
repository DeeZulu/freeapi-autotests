from bson import ObjectId
from pymongo import MongoClient
from pymongo.results import DeleteResult

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

    def delete_user(self, username: str) -> DeleteResult:
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

    def get_category(self, category_id: str):
        """
        Получение категории по ID
        :return Категория продуктов
        """
        return self.db.categories.find_one({"_id": category_id})

    def delete_category(self, category_id: str) -> DeleteResult:
        """
        Удаление пользователя
        :param category_id: ID категории продуктов
        """
        return self.db.users.delete_one({"_id": category_id})

    def get_product(self, product_id: str) -> str:
        """
        Получение продукта по ID
        :param product_id: ID продукта
        :return: Запись с продуктом
        """
        return self.db.products.find_one({"_id": ObjectId(product_id)})

    def delete_product(self, product_id: str) -> DeleteResult:
        """
        Удаление продукта по ID
        :param product_id: ID продукта
        :return: Результат удаления продукта
        """
        return self.db.products.delete_one({"_id": ObjectId(product_id)})
