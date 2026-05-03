from allure import step, epic, feature, story

from models.Ecommerce.create_product_response import CreateProductResponse
from models.Ecommerce.get_all_products_response import GetAllProductsResponse
from models.Ecommerce.get_profile_response import GetProfileResponse
from models.Ecommerce.update_profile_request import UpdateProfileRequest
from models.Ecommerce.update_profile_response import UpdateProfileResponse
from utils.assertions import check_product_exist_in_database, check_product_not_exist_in_database
from utils.support import check_status_code, compare_values


@epic("Тестирование сервиса freeapi")
@feature("Тесты для /ecommerce")
class TestEcommerce:

    @story("Получение информации о профиле - успешно")
    def test_get_my_profile_success(self, ecommerce_auth_client):
        with step("Запрос информации о профиле"):
            response = ecommerce_auth_client.get_profile()

        with step("Проверка ответа"):
            check_status_code(response, 200)
            data = ecommerce_auth_client.parse_response_body(response, GetProfileResponse)
            compare_values("Сообщение", data.message, "User profile fetched successfully")

    @story("Редактирование информации о профиле - успешно")
    def test_update_first_and_last_name_success(self, ecommerce_auth_client):
        with step("Запрос на редактирование информации о профиле"):
            profile = UpdateProfileRequest(first_name="Dennis", last_name="Zalutskiy")
            response = ecommerce_auth_client.update_profile(body=profile)

        with step("Проверка ответа от сервера"):
            check_status_code(response, 200)
            update_profile_data = ecommerce_auth_client.parse_response_body(response, UpdateProfileResponse)
            compare_values(
                "Сообщение",
                update_profile_data.message,
                'User profile updated successfully'
            )
        with step("Проверка обновления клиента"):
            get_profile_data = ecommerce_auth_client.parse_response_body(
                ecommerce_auth_client.get_profile(),
                GetProfileResponse
            )
            compare_values("Обновлённая фамилия", get_profile_data.data.last_name, profile.last_name)
            compare_values("Обновлённое имя", get_profile_data.data.first_name, profile.first_name)

    @story("Получение списка всех продуктов - успешно")
    def test_get_all_products_success(self, ecommerce_auth_client):
        with step("Запрос списка всех продуктов"):
            page_number, products_limit = 2, 5
            response = ecommerce_auth_client.get_all_products(page_number, products_limit)

        with step("Проверка ответа с продуктами"):
            check_status_code(response, 200)
            products_data = ecommerce_auth_client.parse_response_body(response, GetAllProductsResponse)
            compare_values("Сообщение", products_data.message, 'Products fetched successfully')
            compare_values("Количество страниц", products_data.data.page, page_number)

    @story("Создание продукта - успешно")
    def test_create_product_success(self, db_client, ecommerce_auth_client, new_product_with_cleanup):
        with step("Отправка запроса на создание продукта"):
            response = new_product_with_cleanup()
            product_id = response.json()["data"]["_id"]

        with step("Проверка создания продукта"):
            check_status_code(response, 201)
            data = ecommerce_auth_client.parse_response_body(response, CreateProductResponse)
            compare_values("Сообщение", data.message, "Product created successfully")
            check_product_exist_in_database(db_client, product_id)

    @story("Удаление продукта - успешно")
    def test_delete_product(self, ecommerce_auth_client, new_product_with_cleanup, db_client):
        with step("Cоздание продукта"):
            product = new_product_with_cleanup()
            product_id = product.json()["data"]["_id"]

        with step("Отправка запроса на удаление продукта"):
            response = ecommerce_auth_client.delete_product(product_id)

        with step("Проверка удаления продукта"):
            check_status_code(response, 200)
            check_product_not_exist_in_database(db_client, product_id)
