from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"
    use_external_model: bool = False
    embedding_model: str = "intfloat/multilingual-e5-small"
    top_k: int = 3
    dataset_match_threshold: float = 0.62
    enable_web_search: bool = True
    web_search_timeout_seconds: float = 8.0
    web_search_results: int = 3
    frontend_url: str = "http://localhost:3000"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
