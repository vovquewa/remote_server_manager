# app/models/user.py
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Column, String

from app.core.db import Base


class User(SQLAlchemyBaseUserTable[int], Base):
    username = Column(String(15), unique=True, nullable=False)
