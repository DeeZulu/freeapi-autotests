from requests.models import Response

from client.base_client import BaseClient
from models.Users.refresh_token_response import RefreshTokenResponse
from models.Users.user_logout_response import UserLogoutResponse
from models.Users.user_register_request import UserRegisterRequest
from models.Users.user_register_response import UserRegisterResponse
from utils.support import check_status_code


class UserClient(BaseClient):

    def __init__(self):
        super().__init__()
        self.user_path = "/users"

    def register(self, body: UserRegisterRequest) -> UserRegisterResponse:
        """Регистрация нового пользователя"""
        endpoint = f"{self.user_path}/register"
        response = self._request("POST", endpoint, json=body.model_dump(), refresh=True)
        return UserRegisterResponse.model_validate(response.json())

    def login(self, body: dict):
        """
        Логин пользователя
        :param body: Креды для авторизации
        """
        pass

    def logout(self, refresh=False) -> Response:
        """Логаут пользователя"""
        endpoint = f"{self.user_path}/logout"
        response = self._request("POST", endpoint, refresh)
        return response
