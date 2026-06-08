import os
from datetime import datetime, timedelta, timezone
from pathlib import Path

import bcrypt
from bson import ObjectId
from dotenv import load_dotenv
from fastapi import Depends, Header, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from backend.core.database import users_collection
from backend.schema.user_schema import UserRole

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)

env_path = Path(__file__).resolve().parent.parent / ".env"

load_dotenv(dotenv_path=env_path)

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

if SECRET_KEY is None:
    raise ValueError(
        "JWT_SECRET_KEY not found in environment"
    )

if ALGORITHM is None:
    raise ValueError(
        "ALGORITHM not found in environment"
    )

JWT_SECRET_KEY: str = SECRET_KEY
JWT_ALGORITHM: str = ALGORITHM

def hash_password(password : str):
    password_bytes = password.encode("utf-8")
    if len(password_bytes) > 72:
        raise ValueError(
            "Password cannot exceed 72 bytes"
        )
    
    hashed_password = bcrypt.hashpw(
        password_bytes,
        bcrypt.gensalt()
    )
    return hashed_password.decode("utf-8")

def verify_password(
        plain_password : str,
        hashed_password : str
) -> bool:
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8")
    )

def create_access_token(data : dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        hours=1
    )
    to_encode.update({
        "exp" : expire
    })
    token = jwt.encode(
        to_encode,
        JWT_SECRET_KEY,
        algorithm=JWT_ALGORITHM
    )
    return token

def verify_access_token(token: str):
    try:
        payload = jwt.decode(
            token,
            JWT_SECRET_KEY,
            algorithms=[JWT_ALGORITHM]
        )
        return payload
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )
    
async def get_current_user(
    token: str = Depends(oauth2_scheme)
):
    payload = verify_access_token(token)
    # print("payload: ",payload)
    user_id = payload.get("user_id")
    user = await users_collection.find_one({
        "_id": ObjectId(user_id)
    })
    if not user:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )
    return user

async def require_admin(
    current_user = Depends(get_current_user)
):

    if current_user["role"] != UserRole.admin.value:

        raise HTTPException(
            status_code=403,
            detail="Admins only"
        )

    return current_user