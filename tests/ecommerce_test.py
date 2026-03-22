from models.Ecommerce.get_profile_response import GetProfileResponse
from models.Ecommerce.update_profile_request import UpdateProfileRequest
from models.Ecommerce.update_profile_response import UpdateProfileResponse
from utils.support import check_status_code, compare_value
from allure import step, epic, feature, story


@epic("Тестирование сервиса freeapi")
@feature("Тесты для /ecommerce")
class TestEcommerce:

    @story("Получение информации о профиле")
    def test_get_my_profile(self, ecommerce_auth_client):
        with step("Запрос информации о профиле"):
            response = ecommerce_auth_client.get_profile()
        with step("Проверка ответа"):
            check_status_code(response.status_code, 200)
            data = ecommerce_auth_client.parse_response_body(response, GetProfileResponse)
            compare_value("Сообщение", data.message, "User profile fetched successfully")

    @story("Редактирование информаци о профиле")
    def test_update_profile(self, ecommerce_auth_client):
        with step("Запрос на редактирование информации о профиле"):
            profile = UpdateProfileRequest(firstName="Dennis", lastName="Zalutskiy")
            response = ecommerce_auth_client.update_profile(body=profile)
        with step("Проверка ответа от сервера"):
            check_status_code(response.status_code, 200)
            update_profile_data = ecommerce_auth_client.parse_response_body(response, UpdateProfileResponse)
            compare_value(
                "Сообщение",
                update_profile_data.message,
                'User profile updated successfully')
        with step("Проверка обновления клиента"):
            get_profile_data = ecommerce_auth_client.parse_response_body(
                ecommerce_auth_client.get_profile(),
                GetProfileResponse
            )
            compare_value("Обновлённая фамилия", get_profile_data.data.last_name, profile.last_name)
            compare_value("Обновлённое имя", get_profile_data.data.first_name, profile.first_name)
