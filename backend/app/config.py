import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str
    BETTER_AUTH_SECRET: str
    OPENAI_API_KEY: str

    model_config = SettingsConfigDict(env_file="../.env")


settings = Settings()

# Export keys to environment so OpenAI SDK and MCP subprocess can access them
os.environ.setdefault("OPENAI_API_KEY", settings.OPENAI_API_KEY)
os.environ.setdefault("DATABASE_URL", settings.DATABASE_URL)
os.environ.setdefault("BETTER_AUTH_SECRET", settings.BETTER_AUTH_SECRET)
