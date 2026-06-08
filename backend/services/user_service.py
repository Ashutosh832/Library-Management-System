from fastapi import HTTPException
from backend.core.database import users_collection
from backend.model.user_model import (user_serializer,users_serializer)
from backend.schema.user_schema import UserCreate,UserRole, UserUpdate,UpdateRole
from bson import ObjectId

async def create_user(user_data: dict) -> dict:
    old_user = await users_collection.find_one({
        "email" : user_data["email"] 
    })
    if old_user:
        raise HTTPException(status_code=400, detail="User already exists")
    
    result = await users_collection.insert_one(
        user_data
    )
    new_user = await users_collection.find_one({
        "_id" : result.inserted_id
    })
    return user_serializer(new_user)

async def get_all_users():
    response = await users_collection.find().to_list(length=None)
    if not response:
        raise HTTPException(status_code=404, detail="The database is empty")
    return users_serializer(response)

async def get_all_users_by_role(role : str ):
    response = await users_collection.find(
        {"role" : role}
    ).to_list(length=None)
    if not response:
        raise HTTPException(status_code=404, detail="There are no users of such role")
    return users_serializer(response)
    
async def get_user_by_email(email : str):
    response = await users_collection.find_one(
        {"email" : email}
    )
    if not response:
        raise HTTPException(status_code=400, detail="The user doesn't exist")
    return user_serializer(response)

async def delete_user(email:str):
    result = await users_collection.delete_one(
        {"email" : email}
    )
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    return {
        "message" : "The user has been deleted"
    }

async def update_user(email : str , data : UserUpdate):
    response = await users_collection.find_one(
        {"email" : email}
    )
    if not response:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    await users_collection.update_one(
        {"email" : email},
        {
            "$set" : {
                "name" : data.name
            }
        }
    )
    result = await users_collection.find_one(
        {"email" : email}
    )
    return user_serializer(result)

async def update_role(
    email: str,
    role: UserRole
):

    result = await users_collection.update_one(
        {"email": email},
        {
            "$set": {
                "role": role.value
            }
        }
    )

    if result.matched_count == 0:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {
        "message": "Role updated successfully"
    }