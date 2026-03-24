from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str
    BETTER_AUTH_SECRET: str
    OPENAI_API_KEY: str

    model_config = SettingsConfigDict(env_file="../.env")


settings = Settings()
