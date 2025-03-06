from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.user import current_superuser
from app.core.db import get_async_session
from app.schemas.action import ActionExecute
from app.crud.server import get_server_by_id
from app.crud.command import get_command_by_id
from app.services.action import ssh_execute

router = APIRouter()


@router.post("/", dependencies=[Depends(current_superuser)])
async def server_ssh_action(
    action: ActionExecute,
    session: AsyncSession = Depends(get_async_session),
):
    server = await get_server_by_id(action.server_id, session)
    if not server:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Server not found",
        )
    command = await get_command_by_id(action.command_id, session)
    if not command:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Command not found",
        )
    return ssh_execute(ip=str(server.ip), username="qsservice", command=command.command)
