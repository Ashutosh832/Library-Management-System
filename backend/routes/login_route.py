from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from backend.schema.user_schema import UserLogin, UserCreate
from backend.services.auth_service import login, signup

router = APIRouter(
    prefix="/auth",
    tags=["authentication"]
)

@router.post('/login')
async def router_login(data: OAuth2PasswordRequestForm = Depends()):
    user_data = UserLogin(email=data.username, password=data.password)
    return await login(user_data)

@router.post('/signup')
async def router_signup(data: UserCreate):
    return await signup(data)