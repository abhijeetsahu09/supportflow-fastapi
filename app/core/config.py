import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./supportflow.db"
)

SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "development-only-secret-change-this-before-deployment"
)

ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = 30
