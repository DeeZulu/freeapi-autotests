import os.path

from pydantic_settings import BaseSettings, SettingsConfigDict

env_path = os.path.join(os.path.dirname(__file__), ".env")

class Settings(BaseSettings):
    base_url: str
    db_url: str
    username: str
    password: str
    service_username: str
    service_password: str
    model_config = SettingsConfigDict(env_file=env_path)

settings = Settings()  # noqa
