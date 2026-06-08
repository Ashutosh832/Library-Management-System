from pydantic import BaseModel
from enum import Enum

class UserRole(str,Enum):
    student = "student"
    admin = "admin"

class UserCreate(BaseModel):
    name : str
    email : str
    password : str
    role : UserRole

class UserLogin(BaseModel):
    email : str
    password : str
    
class UserResponse(BaseModel):
    id: str
    name : str
    email : str
    role : UserRole

class UserUpdate(BaseModel):
    name : str

class UpdateRole(BaseModel):
    role : UserRole