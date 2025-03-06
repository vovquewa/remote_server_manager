# app/schemas/user.py
from typing import Annotated
from fastapi_users import schemas
from pydantic import Field


class UserRead(schemas.BaseUser[int]):
    username: str


class UserCreate(schemas.BaseUserCreate):
    username: str = Field(..., title="Xyu", description="Xyyyu desc")
    # username: str = Field(..., title="Username")


class UserUpdate(schemas.BaseUserUpdate):
    username: str = Annotated[str, Field(..., title="Xyu")]
