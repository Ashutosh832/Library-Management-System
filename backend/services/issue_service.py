from backend.schema.issue_schema import IssueCreate,IssueStatus
from backend.model.issue_model import issue_serializer,issues_serializer
from backend.core.database import (users_collection,books_collection,issue_collection)
from datetime import timezone, datetime
from bson import ObjectId
from fastapi import HTTPException,Depends

async def issue_books(issue_data : IssueCreate,current_user):
    user = await users_collection.find_one(
        {"_id" : current_user["_id"]}
    )
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    book = await books_collection.find_one(
        {"_id" : ObjectId(issue_data.book_id)}
    )
    if not book:
        raise HTTPException(
            status_code=404, 
            detail="Book not found"
        )
    issue_record = {
        "book_id" : issue_data.book_id,
        "book_name" : book["name"],
        "user_id" : str(current_user["_id"]),
        "user" : current_user["name"],
        "issue_date" : datetime.now(timezone.utc),
        "return_date" : None,
        "status" : IssueStatus.issued
    }
    result = await issue_collection.insert_one(issue_record)
    new_issue = await issue_collection.find_one(
        {"_id" : result.inserted_id}
    )
    return issue_serializer(new_issue)

async def return_books(issue_id : str):
    issue = await issue_collection.find_one(
        {"_id" : ObjectId(issue_id)}
    )
    if not issue:
        raise HTTPException(
            status_code=404,
            detail="There exist no such issue Record"
        )
    if issue["status"] == IssueStatus.returned:
        raise HTTPException(
            status_code=406,
            detail="The book is already returned"
        )
    result = await issue_collection.update_one(
        {"_id" : issue["_id"]},
        {
            "$set" : {
                "return_date" : datetime.now(timezone.utc),
                "status" : IssueStatus.returned
            }
        }
    )
    return {
        "message": "success"
        if result.acknowledged
        else "Failed"
    }

async def get_all_issue():
    result = await issue_collection.find(
        {},
        {}
    ).to_list(length=None)
    if not result:
        raise HTTPException(
            status_code=404, 
            detail="No Issue Record found in the database"
        )
    return issues_serializer(result)

# Get active issues
async def get_active_issues():
    result = await issue_collection.find(
        {"status" : IssueStatus.issued}
    ).to_list(length=None)
    if not result:
        raise HTTPException(
            status_code=404,
            detail="No issue is active"
        )
    return issues_serializer(result)
# Get returned issues
async def get_return_issues():
    result = await issue_collection.find(
        {"status" : IssueStatus.returned}
    ).to_list(length=None)
    if not result:
        raise HTTPException(
            status_code=404,
            detail="No issue is returned"
        )
    return issues_serializer(result)
# Get issues by user
async def get_issues_by_user(id : str):
    user = await users_collection.find_one(
        {"_id" : ObjectId(id)}
    )
    if not user:
        raise HTTPException(
            status_code=404,
            detail="No such user"
        )
    issue = await issue_collection.find({
            "user_id" : id,
            "status" : IssueStatus.issued
        }
    ).to_list(length=None)
    if not issue:
        raise HTTPException(
            status_code=404,
            detail="User has no active Issues"
        )
    return issues_serializer(issue)