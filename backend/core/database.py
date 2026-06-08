from motor.motor_asyncio import AsyncIOMotorClient
client = AsyncIOMotorClient("mongodb://localhost:27017")

db = client["Library_db"]

books_collection = db["books"]
users_collection = db["users"]
issue_collection = db["issueRecord"]
    
print("Database connected")

async def create_indexes():

    await users_collection.create_index(
        "email",
        unique=True
    )

    await books_collection.create_index(
        "isbn",
        unique=True
    )

    print("Indexes created")
