"""App settings, loaded from environment variables (or a local .env file)."""
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    openai_api_key: str
    openai_model: str
    max_cv_chars: int = 15000  # reject CVs longer than this
    max_file_mb: int = 4

    # Tells pydantic to also read a local .env file
    model_config = SettingsConfigDict(env_file=".env")


@lru_cache  # build the settings only once and reuse them
def get_settings() -> Settings:
    return Settings()
