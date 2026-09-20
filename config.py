from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    bot_token: str
    gigachat_credentials: str
    admin_ids: List[int] = []

    gigachat_model: str = "GigaChat-Pro"


settings = Settings()