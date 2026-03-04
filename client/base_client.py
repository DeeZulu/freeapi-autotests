import json

import requests
from requests import Response

from config import settings
from models.Users.refresh_token_response import RefreshTokenResponse
from models.Users.user_login_response import UserLoginResponse
from utils.logger import logger
from utils.support import check_status_code


class BaseClient:
    def __init__(self):
        self.session = requests.session()
        self.base_url = settings.base_url.rstrip("/")

    def _request(self, method: str, endpoint: str, **kwargs) -> Response:
        """
        Общий метод HTTP запроса
        :param method: Метод HTTP запроса
        :return: Объект Response
        """
        if not endpoint.startswith("/"):
            endpoint = "/" + endpoint
        url = f"{self.base_url}{endpoint}"
        logger.info(f"--> {method} {url}")

        if kwargs.get("json"):
            logger.info(f"Body: {kwargs['json']}")
        if kwargs.get("params"):
            logger.info(f"Params: {kwargs['params']}")
        try:
            response = self.session.request(method, url, **kwargs)
            if response.status_code == 401 and "/refresh-token" not in endpoint:
                logger.warning("AccessToken истёк")
                self.refresh_token()
                response = self.session.request(method, url, **kwargs)
            logger.info(f"<-- Status: {response.status_code}")
            content_type = response.headers.get("Content-Type", "")

            if "json" in content_type:
                logger.info(f"Body: {json.dumps(response.json(), indent=2)}")
            elif "html" in content_type:
                logger.info(f"Body: {response.text[:100]}")
            else:
                logger.info(f"Body: {response.text[:200]}")
            return response
        except Exception as e:
            logger.error(e)
            raise e

    def auth(self, body: dict) -> UserLoginResponse:
        """
        Авторизует пользователя и сохраняет токен в сессию
        :param body: Креды пользователя
        :return: словарь с ответом от сервиса
        """
        response = self._request("POST", "users/login", json=body)
        check_status_code(response.status_code, 200)
        login_data = UserLoginResponse.model_validate(response.json())
        access_token = login_data.data.access_token
        self.session.headers.update({"Authorization": f"Bearer {access_token}"})
        return login_data

    def refresh_token(self):
        """Обновление токена"""
        endpoint = "users/refresh-token"
        response = self._request("POST", endpoint)
        if response.status_code == 200:
            refresh_data = RefreshTokenResponse.model_validate(response.json())
            self.session.headers.update({"Authorization": f"Bearer {refresh_data.data.access_token}"})
        else:
            logger.error("Не удалось обновить accessToken")
            raise Exception("Токен не обновлён")
