from backend.core.database import books_collection
from backend.model.book_model import books_serializer,book_serializer
from backend.schema.book_schema import BookCreate,BookUpdate
from fastapi import HTTPException
import asyncio
from bson import ObjectId

async def create_book(book : BookCreate):
    existing_book = await books_collection.find_one(
        {"isbn" : book.isbn}
    )
    if existing_book:
        raise HTTPException(status_code=400, detail="Book already in database")
    
    result = await books_collection.insert_one({
        "name" : book.name,
        "author" : book.author,
        "isbn" : book.isbn
    })
    new_book = await books_collection.find_one(
        {"_id" : result.inserted_id}
    )
    return book_serializer(new_book)

async def get_all_books():
    await asyncio.sleep(0.25)
    response = await books_collection.find().to_list(length=None)
    return books_serializer(response)

async def get_all_books_by_author(author : str):
    response = await books_collection.find(
        {"author" : author}
    ).to_list(length=None)
    return books_serializer(response)


# Update book
from bson import ObjectId
from fastapi import HTTPException

async def update_books(id: str, data: BookUpdate):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID format")

    existing_book = await books_collection.find_one({"_id": ObjectId(id)})
    
    if not existing_book:
        raise HTTPException(status_code=404, detail="Book not found")

    updated_data = {k: v for k, v in data.model_dump(exclude_unset=True).items() if v is not None}

    if not updated_data:
        raise HTTPException(status_code=400, detail="No data provided for update")
    
    await books_collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": updated_data}
    )
    
    result = await books_collection.find_one({"_id": ObjectId(id)})
    return book_serializer(result)

#  Delete book
async def delete_book(id : str):
    result = await books_collection.delete_one(
        {"_id" : ObjectId(id)}
    )
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=404,
            detail="The book is not found"
        )
    return {
        "Message" : "The Book is deleted"
    }
#  Search books
async def search_book(query : str):
    result = await books_collection.find(
        {"name" : {
            "$regex" : query,
            "$options" : "i"
        }}
    ).to_list(length=None)
    if not result:
        raise HTTPException(
            status_code=404,
            detail="No books found"
        )
    return books_serializer(result)