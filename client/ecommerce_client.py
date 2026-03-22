from client.base_client import BaseClient
from models.Ecommerce.update_profile_request import UpdateProfileRequest


class EcommerceClient(BaseClient):
    def __init__(self):
        super().__init__()
        self.path = "/ecommerce"

    def get_profile(self):
        """Получить информацию о зарегистрированном профиле"""
        endpoint = f"{self.path}/profile"
        response = self._request("GET", endpoint, refresh=True)
        return response

    def update_profile(self, body: UpdateProfileRequest):
        """Частичное обновление профиля"""
        endpoint = f"{self.path}/profile"
        response = self._request(
            "PATCH",
            endpoint,
            json=body.model_dump(by_alias=True, exclude_none=True),
            refresh=True
        )
        return response
