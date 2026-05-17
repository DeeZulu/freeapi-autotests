from allure import epic, feature, story, step

from models.Users.user_login_response import UserLoginResponse
from models.Users.user_logout_response import UserLogoutResponse
from tests.conftest import logged_in_user_client
from utils.support import check_status_code, compare_values


@epic("Тестирование сервиса freeapi")
@feature("Тесты /users")
class TestUsers:

    @story("Регистрация нового пользователя - успешно")
    def test_register_new_user_test_success(self, user_client, db_client, fresh_user):
        with step("Отправка запроса на регистрацию"):
            response = user_client.register(body=fresh_user)

        with step("Проверка ответа"):
            check_status_code(response, 200)
            compare_values("Сообщение", response.message,
                           'Users registered successfully and verification email has been sent on your email.')
            user = db_client.get_user(fresh_user.username)
            compare_values("username", user.get("username"), fresh_user.username)
            compare_values("email", user.get("email"), fresh_user.email)

    @story("Логин пользователя - успешно")
    def test_user_login_success(self, user_client, registered_user):
        username, password = registered_user.username, registered_user.password
        with step("Отправка запроса на авторизацию"):
            response = user_client.login({"username": username, "password": password})

        with step("Проверка ответа"):
            check_status_code(response, 200)
            data = user_client.parse_response_body(response, UserLoginResponse)
            compare_values("Сообщение", data.message, "User logged in successfully")

    @story("Логин пользователя - негативный (неверный пароль)")
    def test_user_login_wrong_password(self, user_client, registered_user):
        username = registered_user.username
        with step("Отправка запроса на авторизацию"):
            response = user_client.login({"username": username, "password": "wrong_pass_qwerty123"})

        with step("Проверка негативного ответа"):
            check_status_code(response, 401)
            compare_values(
                "Сообщение об ошибке",
                response.json().get("message"),
                'Invalid user credentials'
            )

    @story("Логин пользователя - негативный (неверный пароль)")
    def test_user_login_user_not_found(self, user_client):
        with step("Отправка запроса на авторизацию"):
            response = user_client.login({"username": "not_existent_user", "password": "qwerty123"})

        with step("Проверка негативного ответа"):
            check_status_code(response, 404)
            compare_values(
                "Сообщение об ошибке",
                response.json().get("message"),
                'User does not exist'
            )

    @story("Логаут пользователя - успешно")
    def test_user_logout_success(self, logged_in_user_client):
        with step("Отправка запроса на логаут"):
            response = logged_in_user_client.logout()

        with step("Проверка ответа"):
            check_status_code(response, 200)
            data = logged_in_user_client.parse_response_body(response, UserLogoutResponse)
            compare_values("Сообщение", data.message, "User logged out")

    @story("Логаут пользователя - негативный")
    def test_user_logout_negative(self, user_client):
        with step("Отправка запроса на логаут"):
            response = user_client.logout()

        with step("Проверка ответа"):
            check_status_code(response, 401)
            message = response.json().get("message")
            compare_values("Сообщение", message, "Unauthorized request")
