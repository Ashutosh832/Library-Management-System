def book_serializer(book) -> dict:
    return {
        "id" : str(book["_id"]),
        "name" : book["name"],
        "author" : book["author"],
        "isbn" : book.get("isbn")
    }

def books_serializer(books) -> list:
    return [book_serializer(book) for book in books]