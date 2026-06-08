from fastapi import APIRouter,Depends
from backend.schema.user_schema import UserCreate,UserRole,UserUpdate,UpdateRole
from backend.services.user_service import (
    create_user,
    get_all_users_by_role,
    get_all_users,
    delete_user,
    update_user,
    update_role
)
from backend.core.security import require_admin

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post('/')
async def route_create_user(user_data : dict):
    return await create_user(user_data)

@router.get('/')
async def route_get_users(role : str | None = None):
    if role:
        return await get_all_users_by_role(role)
    return await get_all_users()

@router.delete("/")
async def route_delete_user(email : str):
    return await delete_user(email)

@router.patch("/")
async def route_update_user(email : str, data : UserUpdate):
    return await update_user(email,data)

@router.put("/{email}/role")
async def update_user_role(
    email: str,
    data: UpdateRole,
    current_user = Depends(require_admin)
):
    return await update_role(email, data.role)