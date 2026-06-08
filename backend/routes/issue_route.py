from fastapi import APIRouter,Depends
from backend.services.issue_service import (
    issue_books,
    return_books,
    get_all_issue,
    get_active_issues,
    get_return_issues,
    get_issues_by_user
)
from backend.schema.issue_schema import IssueCreate
from backend.core.security import require_admin,get_current_user

router = APIRouter(
    prefix="/issue",
    tags=["Issue_Records"]
)

@router.post("/")
async def router_issue_record(data : IssueCreate, current_user = Depends(get_current_user)):
    print("Router: ", current_user)
    return await issue_books(data,current_user)

@router.put("/{issue_id}/return")
async def router_return_book(issue_id : str):
    return await return_books(issue_id)

@router.get("/")
async def router_get_all_issue(current_user = Depends(require_admin)):
    return await get_all_issue()

@router.get('/active')
async def router_get_active_issues(current_user = Depends(require_admin)):
    return await get_active_issues()

@router.get('/returned')
async def router_get_returned_issues(current_user = Depends(require_admin)):
    return await get_return_issues()

@router.get("/me")
async def router_get_issue_by_user(current_user = Depends(get_current_user)):
    return await get_issues_by_user(str(current_user["_id"]))