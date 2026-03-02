import os.path

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

env_path = os.path.join(os.path.dirname(__file__), ".env")

class Settings(BaseSettings):
    base_url: str = Field(validation_alias="BASE_URL")
    model_config = SettingsConfigDict(env_file=env_path)

settings = Settings()  # noqa
