from fastapi import APIRouter, Depends


from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.user import (
    auth_backend,
    fastapi_users,
    current_superuser,
)
from app.schemas.user import UserCreate, UserRead, UserUpdate
from app.core.db import get_async_session
from app.models import User

router = APIRouter()

router.include_router(
    # В роутер аутентификации
    # передается объект бэкенда аутентификации.
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)


@router.get(
    "/users",
    dependencies=[Depends(current_superuser)],
    response_model=list[UserRead],
    tags=["users"],
)
async def get_all_users(session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(User))
    return result.scalars().all()


# async def list_users(session: AsyncSession):
#     return await {'test'}
#     return await fastapi_users.user_db.all()

# # Сохраняем роутер в переменную.
# users_router = fastapi_users.get_users_router(UserRead, UserUpdate)
# # Из списка эндпоинтов роутера исключаем ненужную ручку.
# users_router.routes = [
#     rout for rout in users_router.routes if rout.name != 'users:delete_user'
# ]
# # Подключаем изменённый роутер по старому адресу.
# router.include_router(
#     users_router,
#     prefix='/users',
#     tags=['users'],
# )
