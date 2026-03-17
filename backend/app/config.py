from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str
    BETTER_AUTH_SECRET: str

    model_config = SettingsConfigDict(env_file="../.env")


settings = Settings()
