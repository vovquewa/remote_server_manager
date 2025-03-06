from http import HTTPStatus
from typing import List

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.server import (
    create_server,
    get_all_servers,
    get_server_by_name,
    get_server_by_ip,
)
from app.schemas.server import (
    ServerCreate,
    ServerRead,
)
from app.core.db import get_async_session
from app.core.user import current_superuser

router = APIRouter()


@router.post("/", response_model=ServerRead, dependencies=[Depends(current_superuser)])
async def create_new_server(
    server: ServerCreate, session: AsyncSession = Depends(get_async_session)
):
    if await get_server_by_name(server.name, session):
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail="Server already exists by name",
        )
    if await get_server_by_ip(server.ip, session):
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail="Server already exists by IP",
        )
    return await create_server(server, session)


@router.get(
    "/", response_model=List[ServerRead], dependencies=[Depends(current_superuser)]
)
async def list_servers(session: AsyncSession = Depends(get_async_session)):
    return await get_all_servers(session)
