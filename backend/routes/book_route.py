from fastapi import APIRouter,HTTPException,Depends
from backend.schema.book_schema import BookCreate,BookUpdate
from backend.schema.user_schema import UserRole
from backend.core.security import get_current_user
from backend.services.book_service import (
    create_book,
    get_all_books,
    get_all_books_by_author,
    update_books,
    delete_book,
    search_book
    )
router = APIRouter(
    prefix="/books",
    tags=["books"]
)

@router.post("/")
async def post_create_book(book: BookCreate, current_user = Depends(get_current_user)):
    if current_user["role"] != UserRole.admin.value:
        raise HTTPException(
            status_code=403,
            detail="Admins only"
        )
    return await create_book(book)

@router.get('/')
async def get_books(author : str | None = None):
    if author:
        return await get_all_books_by_author(author)
    return await get_all_books()

@router.patch('/{id}')
async def route_update_books(id: str, data: BookUpdate, current_user = Depends(get_current_user)):
    if current_user["role"] != UserRole.admin.value:
        raise HTTPException(
            status_code=403,
            detail="Admins only"
        )
    return await update_books(id, data)

@router.delete('/{id}')
async def route_delete_book(id : str, current_user = Depends(get_current_user)):
    if current_user["role"] != UserRole.admin.value:
        raise HTTPException(
            status_code=403,
            detail="Admins only"
        )
    return await delete_book(id)

@router.get("/search")
async def route_search_book(query : str):
    return await search_book(query)