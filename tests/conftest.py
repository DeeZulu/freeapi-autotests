
from time import time

from pytest import fixture

from client.user_client import UserClient
from config import settings
from models.Users.user_register_request import UserRegisterRequest


@fixture(scope="session")
def user_client():
    """Клиент для запросов, требующих авторизацию"""
    client = UserClient()
    user = {"password": settings.service_password, "username": settings.service_username}
    client.auth(user)
    return client

@fixture(scope="class")
def test_user():
    """Cоздание тестового пользователя"""
    current_time = int(time())
    return UserRegisterRequest(
        email=f"{current_time}@gmail.com",
        password=settings.password,
        role="ADMIN",
        username=f"{settings.username}_{current_time}")
