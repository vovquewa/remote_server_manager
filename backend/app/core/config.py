from pydantic_settings import BaseSettings

from app.core.constants import APP_TITLE, APP_DESCRIPTION, APP_VERSION, DATABASE_URL


class Settings(BaseSettings):
    database_url: str = DATABASE_URL
    app_title: str = APP_TITLE
    app_description: str = APP_DESCRIPTION
    app_version: str = APP_VERSION
    secret: str = "SECRET"
    first_superuser_email: str = "admin@example.com"
    first_superuser_password: str = "Passexample"
    first_superuser_username: str = "admin"

    class Config:
        env_file = "env/.env"
        extra = "ignore"


settings = Settings()
