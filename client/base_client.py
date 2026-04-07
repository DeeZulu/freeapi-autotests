import json

import allure
import httpx
from pydantic import BaseModel
from requests import Response

from config import settings
from models.Users.refresh_token_response import RefreshTokenResponse
from models.Users.user_login_response import UserLoginResponse
from utils.logger import logger
from utils.support import check_status_code


class BaseClient:
    def __init__(self):
        self.client = httpx.Client()
        self.base_url = settings.base_url.rstrip("/")

    def _request(self, method: str, endpoint: str, refresh: bool, **kwargs) -> Response:
        """
        Общий метод HTTP запроса
        :param method: Метод HTTP запроса
        :param endpoint: Ендпоинт запроса
        :param refresh: Стоит ли отправлять запрос на обновление токена
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
            response = self.client.request(method, url, **kwargs)
            if response.status_code == 401 and refresh and "/refresh-token" not in endpoint:
                logger.warning("AccessToken истёк")
                self.refresh_token()
                response = self.client.request(method, url, **kwargs)
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

    def auth(self, body: dict, validate=True, refresh=True) -> Response | UserLoginResponse:
        """
        Авторизует пользователя c сохранением токен в сессию
        :param body: Креды пользователя
        :param validate: Проверять ли статус код ответа
        :param refresh: Отправлять ли запрос на обновление accessToken
        :return: словарь с ответом от сервиса
        """
        response = self._request("POST", "users/login", refresh, json=body)
        if not validate:
            return response
        check_status_code(response, 200)
        login_data = UserLoginResponse.model_validate(response.json())
        access_token = login_data.data.access_token
        self.client.headers.update({"Authorization": f"Bearer {access_token}"})
        return login_data

    def refresh_token(self, refresh=True):
        """
        Обновляет access токен
        :param refresh: Отправлять ли запрос на обновление accessToken
        """
        endpoint = "users/refresh-token"
        response = self._request("POST", endpoint, refresh)
        if response.status_code == 200:
            refresh_data = RefreshTokenResponse.model_validate(response.json())
            self.client.headers.update({"Authorization": f"Bearer {refresh_data.data.access_token}"})
        else:
            logger.error("Не удалось обновить accessToken")
            raise Exception("Токен не обновлён")

    @staticmethod
    def parse_response_body(response: Response, model: BaseModel):
        """
        Валидирует тело ответа под нужный модельный класс
        :param response: Ответ от сервера
        :param model: Модельный клас Pydantic
        :return:
        """
        content_type = response.headers.get("Content-Type")
        if "/json" not in content_type:
            error_msg = f"Ожидался JSON, но пришел {content_type}. Тело: {response.text[:200]}"
            logger.error(error_msg)
            allure.attach(response.text[:200], name="Невалидный ответ", attachment_type=allure.attachment_type.TEXT)
            raise AssertionError(error_msg)
        try:
            body = model.model_validate(response.json())
        except Exception as e:
            logger.error(e)
            allure.attach(json.dumps(response.json(), indent=2))
            raise e
        return body
