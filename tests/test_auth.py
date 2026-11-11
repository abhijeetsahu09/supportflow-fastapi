
def test_register_user(client):
    response = client.post(
        "/register",
        json={
            "email": "alice@example.com",
            "password": "my-secure-password",
        },
    )

    assert response.status_code == 201
    assert response.json()["email"] == "alice@example.com"

    # Password hash must never be exposed in the response
    assert "hash_password" not in response.json()


def test_duplicate_registration(client):
    payload = {
        "email": "alice@example.com",
        "password": "my-secure-password",
    }

    first = client.post("/register", json=payload)
    second = client.post("/register", json=payload)

    assert first.status_code == 201
    assert second.status_code == 409


def test_invalid_email_registration(client):
    response = client.post(
        "/register",
        json={
            "email": "not-an-email",
            "password": "my-secure-password",
        },
    )

    assert response.status_code == 422


def test_wrong_password(client):
    client.post(
        "/register",
        json={
            "email": "alice@example.com",
            "password": "my-secure-password",
        },
    )

    response = client.post(
        "/login",
        data={
            "username": "alice@example.com",
            "password": "wrong-password",
        },
    )

    assert response.status_code == 401
