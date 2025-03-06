from typing import Optional, Union

from fastapi import Depends, Request, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_users import (
    BaseUserManager,
    FastAPIUsers,
    IntegerIDMixin,
    InvalidPasswordException,
)
from fastapi_users.exceptions import UserNotExists, UserAlreadyExists
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.config import settings
from app.core.db import get_async_session
from app.models.user import User
from app.schemas.user import UserCreate


class CustomSQLAlchemyUserDatabase(SQLAlchemyUserDatabase):
    async def get_by_username(self, username: str):
        statement = select(self.user_table).where(self.user_table.username == username)
        return await self._get_user(statement)


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    # Передаем сессию и модель в CustomSQLAlchemyUserDatabase
    yield CustomSQLAlchemyUserDatabase(session, User)


# Определяем транспорт: передавать токен будем
# через заголовок HTTP-запроса Authorization: Bearer.
# Указываем URL эндпоинта для получения токена.
bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")


# Определяем стратегию: хранение токена в виде JWT.
# def get_jwt_strategy() -> JWTStrategy:
#     # В специальный класс из настроек приложения
#     # передаётся секретное слово, используемое для генерации токена.
#     # Вторым аргументом передаём срок действия токена в секундах.
#     return JWTStrategy(secret=settings.secret, lifetime_seconds=3600)


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(
        secret=settings.secret,
        lifetime_seconds=3600,
        # encode_payload=lambda user: {"username": user.username}
    )


# Создаём объект бэкенда аутентификации с выбранными параметрами.
auth_backend = AuthenticationBackend(
    name="jwt",  # Произвольное имя бэкенда (должно быть уникальным).
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    user_db: CustomSQLAlchemyUserDatabase
    user_db_model = User

    async def validate_password(
        self,
        password: str,
        user: Union[UserCreate, User],
    ) -> None:
        if len(password) < 3:
            raise InvalidPasswordException(
                reason="Password must be at least 3 characters"
            )
        if user.username in password:
            raise InvalidPasswordException(
                reason="Password should not contain the username"
            )

    async def on_after_register(self, user: User, request: Request | None = None):
        print(f"User {user.username} has registered.")

    async def validate_user_before_create(self, user: UserCreate) -> None:
        # Проверяем, существует ли уже пользователь с таким username
        if await self.user_db.get_by_username(user.username):
            raise UserAlreadyExists()
            # raise HTTPException(
            #     status_code=status.HTTP_409_CONFLICT,
            #     detail="A user with this username already exists.",
            # )
        if await self.user_db.get_by_email(user.email):
            raise UserAlreadyExists()
            # raise HTTPException(
            #     status_code=status.HTTP_409_CONFLICT,
            #     detail="A user with this email already exists.",
            # )

    # Исправленный метод аутентификации
    async def authenticate(
        self, credentials: OAuth2PasswordRequestForm
    ) -> Optional[User]:
        """
        Authenticate and return a user following a username and a password.

        Will automatically upgrade password hash if necessary.
        """
        try:
            user = await self.user_db.get_by_username(credentials.username)
            if user is None:
                raise UserNotExists()
        except UserNotExists:
            self.password_helper.hash(credentials.password)
            return None

        verified, updated_password_hash = self.password_helper.verify_and_update(
            credentials.password, user.hashed_password
        )
        if not verified:
            return None

        if updated_password_hash is not None:
            await self.user_db.update(user, {"hashed_password": updated_password_hash})

        return user

    async def create(
        self,
        user_create: UserCreate,
        safe: bool = False,
        request: Optional[Request] = None,
    ):
        """
        Create a user in database.

        Triggers the on_after_register handler on success.

        :param user_create: The UserCreate model to create.
        :param safe: If True, sensitive values like is_superuser or is_verified
        will be ignored during the creation, defaults to False.
        :param request: Optional FastAPI request that
        triggered the operation, defaults to None.
        :raises UserAlreadyExists: A user already exists with the same e-mail.
        :return: A new user.
        """
        await self.validate_password(user_create.password, user_create)

        await self.validate_user_before_create(user_create)
        user_dict = (
            user_create.create_update_dict()
            if safe
            else user_create.create_update_dict_superuser()
        )
        password = user_dict.pop("password")
        user_dict["hashed_password"] = self.password_helper.hash(password)

        created_user = await self.user_db.create(user_dict)

        await self.on_after_register(created_user, request)

        return created_user


# Корутина, возвращающая объект класса UserManager.
async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)


fastapi_users = FastAPIUsers(get_user_manager, [auth_backend])

current_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)
