from time import time

from pytest import fixture

from client.db_client import DbClient
from client.ecommerce_client import EcommerceClient
from client.user_client import UserClient
from config import settings
from models.Users.user_login_response import UserLoginResponse
from models.Users.user_register_request import UserRegisterRequest
from utils.faker import FakeGenerator


@fixture(scope="function")
def user_client():
    """Клиент для запросов /users"""
    client = UserClient()
    yield client
    client.client.close()


@fixture(scope="function")
def ecommerce_client():
    """Клиент для запросов /ecommerce"""
    client = EcommerceClient()
    yield client
    client.client.close()

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
    response = client.auth(user, validate=False)
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
    elif response.status_code == 200:
        data = UserLoginResponse.model_validate(response.json())
        client.client.headers.update({"Authorization": f"Bearer {data.data.access_token}"})
    yield client
    client.client.close()


@fixture(scope="session")
def ecommerce_auth_client(auth_client):
    """Авторизованный Ecommerce клиент"""
    ecom_client = EcommerceClient()
    token = auth_client.client.headers.get("Authorization")
    if not token:
        raise AssertionError("Токен авторизации отсутствует")
    ecom_client.client.headers["Authorization"] = token
    yield ecom_client
    ecom_client.client.close()


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


@fixture(scope="function")
def clear_category(db_client, request):
    """
    Удаляет созданные категории после теста
    :param db_client: MongoDB клиент
    :param request: Специальный объект Pytest
    """
    request.node.ids_to_delete = []
    yield
    for cat_id in request.node.ids_to_delete:
        db_client.delete_category(cat_id)


@fixture(scope="function")
def create_category(ecommerce_auth_client):
    """Создаёт новую категорию продуктов"""
    new_category = {"name": FakeGenerator.get_ecommerce_category()}
    response = ecommerce_auth_client.create_category(new_category)
    category_id = response.json()["data"]["_id"]
    return category_id
