
from fastapi import FastAPI

from app.db.database import Base, engine
from app.db import models
from app.routers import auth, tickets


# Create database tables
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="SupportFlow API",
    description="A ticket management REST API built with FastAPI",
    version="1.0.0"
)


# Register API routers
app.include_router(auth.router)
app.include_router(tickets.router)


@app.get("/health")
def health_check():
    return {"status": "healthy"}
