from backend.core.database import users_collection
from backend.schema.user_schema import UserCreate,UserLogin
from fastapi import HTTPException
from backend.core.security import hash_password,verify_password,create_access_token
from backend.services.user_service import create_user

async def signup(data : UserCreate):
    existing_user = await users_collection.find_one(
        {"email" : data.email}
    )
    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="User already exist"
        )
    hashed_password = hash_password(data.password)
    user_data = {
        "name" : data.name,
        "email" : data.email,
        "password" : hashed_password,
        "role" : data.role
    }
    return await create_user(user_data)

async def login(data : UserLogin):
    existing_user = await users_collection.find_one(
        {"email" : data.email}
    )
    if not existing_user:
        raise HTTPException(
            status_code=401,
            detail="No such User exist"
        )
    if not verify_password(data.password,existing_user["password"]):
        raise HTTPException(
            status_code=401,
            detail="invalid Credentials"
        )
    token = create_access_token({
        "user_id" : str(existing_user["_id"]),
        "role" : existing_user["role"]
    })
    return {
        "access_token": token,
        "role" : existing_user["role"],
        "email" : existing_user["email"],
        "name" : existing_user["name"],
        "token_type": "bearer"
    }