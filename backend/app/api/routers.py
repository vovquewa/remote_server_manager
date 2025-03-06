from fastapi import APIRouter

from app.api.endpoints import user_router, server_router, command_router, action_router

main_router = APIRouter()
main_router.include_router(action_router, prefix="/actions", tags=["Actions"])
main_router.include_router(server_router, prefix="/servers", tags=["Servers"])
main_router.include_router(command_router, prefix="/commands", tags=["Commands"])
main_router.include_router(user_router)
