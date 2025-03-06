from http import HTTPStatus
from typing import List

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.command import Command
from app.crud.command import (
    create_command,
    get_all_commands,
    get_command_by_name,
    get_command_by_command,
    get_command_by_id,
    delete_command,
)
from app.schemas.command import (
    CommandCreate,
    CommandRead,
)
from app.core.db import get_async_session
from app.core.user import current_superuser

router = APIRouter()


@router.post("/", response_model=CommandRead, dependencies=[Depends(current_superuser)])
async def create_new_command(
    command: CommandCreate, session: AsyncSession = Depends(get_async_session)
) -> Command:
    if await get_command_by_name(command.name, session):
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail="Command already exists by name",
        )
    if await get_command_by_command(command.command, session):
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail="Command already exists by command",
        )
    return await create_command(command, session)


@router.get(
    "/", response_model=List[CommandRead], dependencies=[Depends(current_superuser)]
)
async def list_commands(session: AsyncSession = Depends(get_async_session)):
    return await get_all_commands(session)


@router.delete(
    "/{command_id}",
    response_model=CommandRead,
    dependencies=[Depends(current_superuser)],
)
async def delete_command_by_id(
    command_id: int, session: AsyncSession = Depends(get_async_session)
):
    command = await get_command_by_id(command_id, session)
    if not command:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Command not found"
        )
    return await delete_command(command, session)
