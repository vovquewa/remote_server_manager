import os
from dotenv import load_dotenv

load_dotenv("env/.env")

APP_TITLE = "Remote server manager"
APP_DESCRIPTION = "Service for remote management"
APP_VERSION = "0.1.0"

DEFAULT_DB_URL = "postgresql+asyncpg://postgres:QW34rty@192.168.77.65:5432/fastapi"


def get_database_url():
    db_user = os.getenv("POSTGRES_USER")
    db_password = os.getenv("POSTGRES_PASSWORD")
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")
    db_name = os.getenv("DB_NAME")
    if not all([db_user, db_password, db_host, db_port, db_name]):
        return DEFAULT_DB_URL
    return f"postgresql+asyncpg://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"


DATABASE_URL = get_database_url()
