import json
import logging
import sys

import requests
from requests import Response

from config import settings
from tests.conftest import logger


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
            logger.info(f"Payload: {kwargs['json']}")
        if kwargs.get("params"):
            logger.info(f"Params: {kwargs['params']}")
        try:
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
