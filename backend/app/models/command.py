from sqlalchemy import Column, String, Text
from app.core.db import Base


class Command(Base):
    name = Column(String(100), unique=True, index=True, nullable=False)
    command = Column(Text, unique=True, nullable=False)
