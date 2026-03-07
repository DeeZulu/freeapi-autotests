
from client.user_client import UserClient
from models.Users.user_logout_response import UserLogoutResponse
from tests.conftest import test_user
from utils.support import check_status_code, compare_value
import allure



class TestUsers:

    @allure.story("Регистрация нового пользователя - успешно")
    def test_register_new_user_test_success(self, test_user):
        new_user = test_user
        client = UserClient()
        response = client.register(body=new_user)
        check_status_code(response.status_code, 200)
        user = {"password": new_user.password, "username": new_user.username}
        response = client.auth(user)
        check_status_code(response.status_code, 200)
        compare_value("Сообщение", response.message, 'User logged in successfully')

    def test_user_logout_success(self, user_client):
        response = user_client.logout()
        check_status_code(response.status_code, 200)
        data = UserLogoutResponse.model_validate(response.json())
        compare_value("Сообщение", data.message, "User logged out")

    def test_user_logout_negative(self):
        client = UserClient()
        response = client.logout()
        check_status_code(response.status_code, 401)
        message = response.json().get("message")
        compare_value("Сообщение", message, "Unauthorized request")
