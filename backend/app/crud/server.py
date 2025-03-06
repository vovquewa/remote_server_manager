# from sqlalchemy.orm import Session
import sys
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import AsyncSessionLocal
from app.models.server import Server
from app.schemas.server import ServerCreate
from pydantic import IPvAnyAddress


async def create_server(server: ServerCreate, session: AsyncSession) -> Server:
    server_data = server.model_dump()
    server_data["ip"] = str(server_data.get("ip"))
    db_server = Server(**server_data)
    print(db_server, file=sys.stderr)
    session.add(db_server)
    await session.commit()
    await session.refresh(db_server)
    return db_server


async def get_all_servers(session: AsyncSession):
    async with AsyncSessionLocal() as session:
        return (await session.execute(select(Server))).scalars().all()


async def get_server_by_name(name: str, session: AsyncSession):
    return (
        (await session.execute(select(Server).where(Server.name == name)))
        .scalars()
        .first()
    )


async def get_server_by_ip(ip: IPvAnyAddress, session: AsyncSession):
    return (
        (await session.execute(select(Server).where(Server.ip == ip))).scalars().first()
    )


async def get_server_by_id(id: int, session: AsyncSession):
    return (
        (await session.execute(select(Server).where(Server.id == id))).scalars().first()
    )
