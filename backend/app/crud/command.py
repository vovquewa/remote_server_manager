# from sqlalchemy.orm import Session
import sys
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import AsyncSessionLocal
from app.models.command import Command
from app.schemas.command import CommandCreate
from pydantic import IPvAnyAddress


async def create_command(command: CommandCreate, session: AsyncSession) -> Command:
    command_data = command.model_dump()
    db_command = Command(**command_data)
    print(db_command, file=sys.stderr)
    session.add(db_command)
    await session.commit()
    await session.refresh(db_command)
    return db_command


async def get_all_commands(session: AsyncSession):
    async with AsyncSessionLocal() as session:
        return (await session.execute(select(Command))).scalars().all()


async def get_command_by_name(name: str, session: AsyncSession):
    return (
        (await session.execute(select(Command).where(Command.name == name)))
        .scalars()
        .first()
    )


async def get_command_by_id(id: int, session: AsyncSession):
    return (
        (await session.execute(select(Command).where(Command.id == id)))
        .scalars()
        .first()
    )


async def delete_command(command: Command, session: AsyncSession):
    await session.delete(command)
    await session.commit()
    return command


async def get_command_by_command(command: str, session: AsyncSession):
    return (
        (await session.execute(select(Command).where(Command.command == command)))
        .scalars()
        .first()
    )
