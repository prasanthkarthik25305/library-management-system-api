from fastapi import FastAPI
from app.database import Base, engine

from app.routers.book_router import router as book_router
from app.routers.member_router import router as member_router
from app.routers.transaction_router import router as transaction_router

import os

app = FastAPI(title="Library Management System API")

Base.metadata.create_all(bind=engine)

app.include_router(book_router)
app.include_router(member_router)
app.include_router(transaction_router)

# -------------------------------
# Render / Production Entry Point
# -------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000))
    )
