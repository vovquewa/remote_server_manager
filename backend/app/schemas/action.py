from pydantic import BaseModel, Field


class ActionBase(BaseModel):
    server_id: int
    command_id: int


class ActionExecute(BaseModel):
    server_id: int = Field(description="Server ID")
    command_id: int = Field(description="Command ID")
