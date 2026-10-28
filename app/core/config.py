from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Lume"
    app_env: str = "dev"

    postgres_user: str = "postgres"
    postgres_password: str = "postgres"
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_db: str = "mind_agent"

    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/mind_agent"

    qdrant_host: str = "localhost"
    qdrant_port: int = 6333
    qdrant_collection: str = "notes"

    openai_api_key: str = ""
    openai_base_url: str = ""
    embedding_model: str = "bge-m3"
    llm_model: str = "qwen2.5-7b"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


@lru_cache
def get_settings() -> Settings:
    return Settings()
