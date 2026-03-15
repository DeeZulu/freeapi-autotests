from time import time

from pytest import fixture

from client.db_client import DbClient
from client.user_client import UserClient
from config import settings
from models.Users.user_register_request import UserRegisterRequest


@fixture(scope="function")
def user_client():
    """Клиент для запросов /users"""
    client = UserClient()
    yield client
    client.session.close()


@fixture(scope="function")
def db_client():
    """Клиент для работы с базой данных"""
    client = DbClient()
    yield client
    client.client.close()


@fixture(scope="function")
def fresh_user():
    """Не зарегистрированный пользователь"""
    current_time = int(time())
    user = UserRegisterRequest(
        email=f"{current_time}@gmail.com",
        password=settings.password,
        role="ADMIN",
        username=f"{settings.username}_{current_time}")
    yield user
    mongo_client = DbClient()
    mongo_client.delete_user(user.username)

@fixture(scope="session")
def auth_client():
    """Клиент для запросов, требующих авторизацию"""
    client = UserClient()
    username, password = settings.service_username, settings.service_password
    user = {"password": password, "username": username}
    response = client.auth(user)
    if response.status_code == 404:
        service_user = UserRegisterRequest(
            email=settings.service_email,
            password=settings.service_password,
            role="ADMIN",
            username=settings.service_username
        )
        response = client.register(service_user)
        assert response.status_code == 200, "Не удалось зарегистрировать технического пользователя"
        client.auth(user)
    return client


@fixture(scope="class")
def registered_user():
    """Зарегистрированный пользователь"""
    current_time = int(time())
    client = UserClient()
    user = UserRegisterRequest(
        email=f"{current_time}@gmail.com",
        password=settings.password,
        role="ADMIN",
        username=f"{settings.username}_{current_time}")
    response = client.register(user)
    assert response.status_code == 200, "Не удалось зарегистрировать технического пользователя"
    yield user
    mongo_client = DbClient()
    mongo_client.delete_user(user.username)


@fixture(scope="function")
def logged_in_user_client(registered_user):
    """
    Клиент с авторизованным пользователем
    :param registered_user свежий зарегистрированный пользователь
    :return Клиент с авторизованным пользователем
    """
    client = UserClient()
    client.auth({"password": registered_user.password,
                 "username": registered_user.username})
    return client
