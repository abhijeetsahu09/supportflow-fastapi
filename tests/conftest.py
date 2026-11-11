
import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.db.database import get_db, Base


# Create an isolated in-memory SQLite database for testing
test_engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    bind=test_engine,
    autoflush=False,
    expire_on_commit=False,
)


# Override the application's database dependency
def override_get_db():
    with TestingSessionLocal() as db:
        yield db


@pytest.fixture
def client():
    Base.metadata.create_all(bind=test_engine)

    app.dependency_overrides[get_db] = override_get_db

    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.clear()
        Base.metadata.drop_all(bind=test_engine)


# Shared helper for registering a user and logging in
@pytest.fixture
def register_and_login(client):

    def _register_and_login(email="alice@example.com"):
        password = "my-secure-password"

        register_response = client.post(
            "/register",
            json={
                "email": email,
                "password": password,
            },
        )

        assert register_response.status_code == 201

        login_response = client.post(
            "/login",
            data={
                "username": email,
                "password": password,
            },
        )

        assert login_response.status_code == 200

        return login_response.json()["access_token"]

    return _register_and_login
