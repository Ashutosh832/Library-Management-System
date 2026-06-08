from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from backend.core.database import db,create_indexes
from backend.routes.user_route import router as User_router
from backend.routes.book_route import router as Book_router
from backend.routes.issue_route import router as Issue_router
from backend.routes.login_route import router as Login_router
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app : FastAPI):
    await create_indexes()
    yield

app = FastAPI(
    lifespan=lifespan
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

routers = [
    User_router,
    Book_router,
    Issue_router,
    Login_router
]
for router in routers:
    app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("backend.main:app",host="localhost",port=8080,reload=True)