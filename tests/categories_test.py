from allure import story, step, feature, epic

from models.Ecommerce.create_category_response import CreateCategoryResponse
from models.Ecommerce.delete_category_response import DeleteCategoryResponse
from utils.assertions import check_category_not_exist
from utils.faker import FakeGenerator
from utils.support import check_status_code, compare_values


@epic("Тестирование сервиса freeapi")
@feature("Тесты для /ecommerce/categories")
class TestCategories:

    @story("Создание категории продуктов - успешно")
    def test_create_category_success(self, ecommerce_auth_client, clear_category, request):
        with step("Оправка запроса на создание категории"):
            category_name = {"name": FakeGenerator.get_ecommerce_category()}
            response = ecommerce_auth_client.create_category(category_name)
        with step("Проверка создания категории"):
            check_status_code(response, 201)
            data = ecommerce_auth_client.parse_response_body(response, CreateCategoryResponse)
            compare_values("Сообщение", data.message, "Category created successfully")
            category_id = response.json()["data"]["_id"]
            request.node.ids_to_delete.append(category_id)

    @story("Создание категории продуктов - негативный")
    def test_create_category_negative(self, ecommerce_auth_client):
        with step("Оправка невалидного запроса на создание категории"):
            new_category = {"name": ""}
            response = ecommerce_auth_client.create_category(new_category)
        with step("Проверка создания категории"):
            check_status_code(response, 422)

    @story("Удаление категории - успешны")
    def test_delete_category(self, ecommerce_auth_client, db_client, new_category):
        with step("Отправка запроса на удаление категории"):
            category_id = new_category["data"]["_id"]
            response = ecommerce_auth_client.delete_category(category_id)
        with step("Проверка удаления категории"):
            check_status_code(response, 200)
            data = ecommerce_auth_client.parse_response_body(response, DeleteCategoryResponse)
            compare_values("Сообщение", data.message, "Category deleted successfully")
            deleted_category_id = data.data.deleted_category.id
            compare_values("ID удаляемой категории", deleted_category_id, category_id)
            check_category_not_exist(db_client, deleted_category_id)
