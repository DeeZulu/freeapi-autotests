import os
from pathlib import Path
from time import time

from pytest import fixture

from client.db_client import DbClient
from client.ecommerce_client import EcommerceClient
from client.user_client import UserClient
from config import settings
from models.Ecommerce.create_product_request import CreateProductRequest
from models.Users.user_login_response import UserLoginResponse
from models.Users.user_register_request import UserRegisterRequest
from utils.faker import FakeGenerator

BASE_DIR = Path(__file__).resolve().parent.parent

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
def new_category(ecommerce_auth_client):
    """Создаёт новую категорию продуктов"""
    new_category = {"name": FakeGenerator.get_ecommerce_category()}
    response = ecommerce_auth_client.create_category(new_category)
    return response.json()


@fixture(scope="function")
def new_product_with_cleanup(request, new_category, ecommerce_auth_client, db_client):
    """Подготовка продукта для запроса на создание и дальнейшее удаление"""
    product_ids = []
    category_id = new_category["data"]["_id"]
    category_name = new_category["data"]["name"]
    new_product = CreateProductRequest(
        category=category_id,
        description=FakeGenerator.get_product_description(category_name),
        main_image="images/samsung.png",
        name=FakeGenerator.get_product_name(category_name),
        price="1000",
        stock="5",
        sub_images=[]
    )

    def _create():
        image_path = BASE_DIR / "images" / "samsung.png"
        with open(image_path, "rb") as image:
            file = {
                "mainImage": (os.path.basename(image_path), image, "image/png")
            }
            response = ecommerce_auth_client.create_product(new_product, file)
            if response.status_code == 201:
                product_id = response.json()["data"]["_id"]
                product_ids.append(product_id)
            return response
    yield _create

    for p_id in product_ids:
        db_client.delete_product(p_id)
