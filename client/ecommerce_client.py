from requests.models import Response

from client.base_client import BaseClient
from models.Ecommerce.create_category_response import CreateCategoryResponse
from models.Ecommerce.create_product_request import CreateProductRequest
from models.Ecommerce.create_product_response import CreateProductResponse
from models.Ecommerce.get_all_products_response import GetAllProductsResponse
from models.Ecommerce.get_profile_response import GetProfileResponse
from models.Ecommerce.update_profile_request import UpdateProfileRequest
from models.Ecommerce.update_profile_response import UpdateProfileResponse


class EcommerceClient(BaseClient):
    def __init__(self):
        super().__init__()
        self.path = "/ecommerce"

    def get_profile(self) -> Response | GetProfileResponse:
        """Получить информацию о зарегистрированном профиле"""
        endpoint = f"{self.path}/profile"
        response = self._request("GET", endpoint, refresh=True)
        return response

    def update_profile(self, body: UpdateProfileRequest) -> Response | UpdateProfileResponse:
        """Частичное обновление профиля"""
        endpoint = f"{self.path}/profile"
        response = self._request(
            "PATCH",
            endpoint,
            json=body.model_dump(by_alias=True, exclude_none=True),
            refresh=True
        )
        return response

    def get_all_products(self, page_number: int, products_limit: int) -> Response | GetAllProductsResponse:
        """
        Получение всех продуктов
        :param page_number Номер страницы с продуктами
        :param products_limit Количество продуктов
        """
        endpoint = f"{self.path}/products"
        response = self._request(
            "GET",
            endpoint,
            refresh=True,
            params={"page": page_number, "limit": products_limit}
        )
        return response

    def create_product(self, body: CreateProductRequest, file: dict) -> Response:
        """
        Создание продукта
        :param file Файл для главного изображения продукта
        :param body Тело запроса
        """
        endpoint = f"{self.path}/products"
        response = self._request(
            "POST",
            endpoint,
            refresh=True,
            data=body.model_dump(by_alias=True, exclude={"main_image"}),
            files=file
        )
        return response

    def delete_product(self, product_id: str):
        """Удаление продукта"""
        endpoint = f"{self.path}/products/{product_id}"
        response = self._request("DELETE", endpoint, refresh=True)
        return response

    def get_categories(self, page_number: int, products_limit: int) -> Response:
        """
        Получение категорий товаров
        :param page_number Номер страницы с продуктами
        :param products_limit Количество продуктов
        """
        endpoint = f"{self.path}/categories"
        response = self._request(
            "GET",
            endpoint,
            refresh=True,
            params={"page": page_number, "limit": products_limit}
        )
        return response

    def create_category(self, body: dict) -> Response | CreateCategoryResponse:
        """
        Создание категории
        :param body Тело запроса
        """
        endpoint = f"{self.path}/categories"
        response = self._request("POST", endpoint, refresh=True, json=body)
        return response

    def delete_category(self, category_id):
        """Удаление категории"""
        endpoint = f"{self.path}/categories/{category_id}"
        response = self._request("DELETE", endpoint, refresh=True)
        return response
