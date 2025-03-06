from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from app.api.routers import main_router

# from app.core.constants import APP_TITLE, APP_DESCRIPTION, APP_VERSION
from app.core.config import settings
from app.core.init_db import create_first_superuser


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Действия при старте приложения
    await create_first_superuser()
    yield
    # Действия при завершении приложения (опционально)
    print("Shutting down...")


app = FastAPI(
    title=settings.app_title,
    description=settings.app_description,
    version=settings.app_version,
    lifespan=lifespan,
)

# app.include_router(server_router, prefix="/servers", tags=["Servers"])
app.include_router(main_router)


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",  # Имя файла и экземпляра приложения (main.py -> app)
        host="0.0.0.0",
        port=8000,
        reload=True,  # Для автообновления (опционально для разработки)
    )
