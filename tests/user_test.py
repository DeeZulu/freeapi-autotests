from allure import epic, feature, story, step


from models.Users.user_logout_response import UserLogoutResponse
from tests.conftest import logged_in_user_client
from utils.support import check_status_code, compare_value


@epic("Тестирование сервиса freeapi")
@feature("Тесты /users")
class TestUsers:

    @story("Регистрация нового пользователя - успешно")
    def test_register_new_user_test_success(self, user_client, db_client, fresh_user):
        with step("Отправка запроса на регистрацию"):
            response = user_client.register(body=fresh_user)
        with step("Проверка ответа"):
            check_status_code(response.status_code, 200)
            compare_value(
                "Сообщение",
                response.message,
                'Users registered successfully and verification email has been sent on your email.'
            )
            user = db_client.get_user(fresh_user.username)
            compare_value("username", user.get("username"), fresh_user.username)
            compare_value("email", user.get("email"), fresh_user.email)

    @story("Логин пользователя - успешно")
    def test_user_login_success(self, user_client, registered_user):
        username, password = registered_user.username, registered_user.password
        with step("Отправка запроса на авторизацию"):
            response = user_client.auth({"username": username, "password": password})
        with step("Проверка ответа"):
            check_status_code(response.status_code, 200)
            compare_value("Сообщение", response.message, "User logged in successfully")

    @story("Логаут пользователя - успешно")
    def test_user_logout_success(self, logged_in_user_client):
        with step("Отправка запроса на логаут"):
            response = logged_in_user_client.logout()
        with step("Проверка ответа"):
            check_status_code(response.status_code, 200)
            data = logged_in_user_client.parse_response_body(response, UserLogoutResponse)
            compare_value("Сообщение", data.message, "User logged out")

    @story("Логаут пользователя - негативный")
    def test_user_logout_negative(self, user_client):
        with step("Отправка запроса на логаут"):
            response = user_client.logout()
        with step("Проверка ответа"):
            check_status_code(response.status_code, 401)
            message = response.json().get("message")
            compare_value("Сообщение", message, "Unauthorized request")
