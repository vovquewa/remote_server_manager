from pydantic import BaseModel, IPvAnyAddress, Field

from app.core import user


class ServerBase(BaseModel):
    name: str
    ip: IPvAnyAddress
    username: str


class ServerCreate(ServerBase):
    name: str = Field(description="Server name", max_length=100, min_length=5)
    ip: IPvAnyAddress = Field(
        description="Server IP",
    )
    username: str = Field(
        description="Server username",
    )


class ServerRead(ServerBase):
    id: int = Field(description="Server ID")

    class Config:
        from_attributes = True
