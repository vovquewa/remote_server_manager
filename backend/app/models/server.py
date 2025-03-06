from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import INET
from app.core.db import Base


class Server(Base):
    name = Column(String(100), unique=True, index=True, nullable=False)
    ip = Column(INET, unique=True, index=True, nullable=False)
    username = Column(String(100), nullable=True)
