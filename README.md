# SupportFlow - Ticket Management API

A RESTful ticket management API built with **Python, FastAPI, and PostgreSQL**. SupportFlow provides user authentication and secure ticket management with JWT-based authorization.

## Features

- **User Authentication:** User registration and login.
- **Password Security:** Secure password hashing using Argon2.
- **JWT Authentication:** Token-based authentication and protected endpoints.
- **Ticket Management:** Create, retrieve, list, and delete support tickets.
- **Authorization:** Users can access and delete only their own tickets.
- **Database Integration:** SQLAlchemy ORM with PostgreSQL.
- **Automated Testing:** API tests using pytest and FastAPI TestClient.
- **Containerization:** Docker and Docker Compose support.

## Tech Stack

| Category | Technologies |
|---|---|
| Language | Python |
| Backend Framework | FastAPI |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Authentication | JWT, PyJWT |
| Password Hashing | Argon2, pwdlib |
| Testing | pytest, HTTPX |
| Package Management | uv |
| Containerization | Docker, Docker Compose |

## Project Structure

```text
supportflow-fastapi/
├── app/
│   ├── core/
│   ├── db/
│   ├── schemas/
│   ├── routers/
│   └── main.py
├── tests/
├── .env.example
├── Dockerfile
├── compose.yaml
├── pyproject.toml
├── uv.lock
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.11 or later
- [uv](https://docs.astral.sh/uv/)
- PostgreSQL (or Docker)

### 1. Clone the repository

```bash
git clone https://github.com/abhijeetsahu09/supportflow-fastapi.git
cd supportflow-fastapi
```

### 2. Install dependencies

```bash
uv sync
```

### 3. Configure environment variables

Create a `.env` file in the project root using `.env.example` as a reference.

Configure your database connection and a strong secret key.

### 4. Run the application

```bash
uv run uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

### 5. Explore the API documentation

FastAPI provides interactive API documentation:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Running with Docker

Make sure Docker Desktop is running, then execute:

```bash
docker compose up --build
```

Docker Compose starts the API and PostgreSQL services.

To stop the containers:

```bash
docker compose down
```

To stop the containers and delete the database volume as well:

```bash
docker compose down -v
```

**Warning:** The `-v` option deletes the persisted PostgreSQL data.

## Running Tests

Run the automated test suite:

```bash
uv run pytest -v
```

The tests use an isolated SQLite database, keeping test data separate from your development database.

## API Endpoints

| Method | Endpoint | Description | Access |
|---|---|---|---|
| POST | `/auth/register` | Register a new user | Public |
| POST | `/auth/login` | Authenticate and receive a JWT | Public |
| GET | `/users/me` | Retrieve the current user | Authenticated |
| POST | `/tickets` | Create a ticket | Authenticated |
| GET | `/tickets` | List the current user's tickets | Authenticated |
| GET | `/tickets/{ticket_id}` | Retrieve a ticket | Authenticated |
| DELETE | `/tickets/{ticket_id}` | Delete an owned ticket | Authenticated |

All protected endpoints require a valid JWT access token.

*Adjust the endpoint paths above if your actual router prefixes differ.*

## Security

- Passwords are hashed rather than stored as plain text.
- Protected routes require JWT authentication.
- Ticket ownership is checked before allowing access or deletion.
- Secrets and database credentials are supplied through environment variables.

## Future Improvements

- Database migrations with Alembic.
- Ticket updates and status management.
- Pagination and filtering.
- Role-based access control.
- Continuous integration with GitHub Actions.