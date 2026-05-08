from requests.models import Response

from client.base_client import BaseClient
from models.Users.user_register_request import UserRegisterRequest
from models.Users.user_register_response import UserRegisterResponse


class UserClient(BaseClient):

    def __init__(self):
        super().__init__()
        self.user_path = "/users"

    def register(self, body: UserRegisterRequest) -> UserRegisterResponse:
        """Регистрация нового пользователя"""
        endpoint = f"{self.user_path}/register"
        response = self._request("POST", endpoint, json=body.model_dump(), refresh=True)
        return UserRegisterResponse.model_validate(response.json())

    def login(self, body: dict, refresh=False) -> Response:
        """
        Логин пользователя
        :param body Креды для авторизации
        :param refresh Надо ли обновлять accessToken в случае 401 ответа
        """
        endpoint = f"{self.user_path}/login"
        response = self._request("POST", endpoint, refresh, json=body)
        return response

    def logout(self, refresh=False) -> Response:
        """
        Логаут пользователя
        :param refresh Надо ли обновлять accessToken в случае 401 ответа
        """
        endpoint = f"{self.user_path}/logout"
        return self._request("POST", endpoint, refresh)

    def verify_email_by_token(self, verification_token: str, refresh=True):
        """
        Проверка адреса электронной почты по верификационному токену
        :param verification_token Токен верификации
        :param refresh Надо ли обновлять accessToken в случае 401 ответа
        """
        endpoint = f"{self.user_path}/verify-email/{verification_token}"
        return self._request("GET", endpoint, refresh)
