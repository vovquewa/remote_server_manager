from pydantic import BaseModel, Field


class CommandBase(BaseModel):
    name: str
    command: str


class CommandCreate(CommandBase):
    name: str = Field(description="Command name", max_length=100, min_length=5)
    command: str = Field(
        description="Command",
    )


class CommandRead(CommandBase):
    id: int = Field(description="Command ID")

    class Config:
        from_attributes = True
