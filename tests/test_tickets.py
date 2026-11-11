
def test_tickets_require_login(client):
    response = client.get("/tickets")

    assert response.status_code == 401


def test_create_and_list_ticket(client, register_and_login):
    token = register_and_login()

    headers = {
        "Authorization": f"Bearer {token}"
    }

    create_response = client.post(
        "/tickets",
        headers=headers,
        json={
            "title": "Payment failed",
            "description": "My payment failed during checkout.",
        },
    )

    assert create_response.status_code == 201
    assert create_response.json()["title"] == "Payment failed"

    list_response = client.get(
        "/tickets",
        headers=headers,
    )

    assert list_response.status_code == 200
    assert len(list_response.json()) == 1
    assert list_response.json()[0]["title"] == "Payment failed"


def test_cannot_delete_another_users_ticket(
    client,
    register_and_login
):
    alice_token = register_and_login("alice@example.com")
    bob_token = register_and_login("bob@example.com")

    alice_headers = {
        "Authorization": f"Bearer {alice_token}"
    }

    bob_headers = {
        "Authorization": f"Bearer {bob_token}"
    }

    ticket_response = client.post(
        "/tickets",
        headers=alice_headers,
        json={
            "title": "Alice payment issue",
            "description": "Alice needs help with a payment.",
        },
    )

    assert ticket_response.status_code == 201

    ticket_id = ticket_response.json()["id"]

    delete_response = client.delete(
        f"/tickets/{ticket_id}",
        headers=bob_headers,
    )

    assert delete_response.status_code == 403

    # Verify Alice's ticket still exists
    get_response = client.get(
        f"/tickets/{ticket_id}",
        headers=alice_headers,
    )

    assert get_response.status_code == 200


def test_cannot_view_another_users_ticket(
    client,
    register_and_login
):
    alice_token = register_and_login("alice@example.com")
    bob_token = register_and_login("bob@example.com")

    alice_headers = {
        "Authorization": f"Bearer {alice_token}"
    }

    bob_headers = {
        "Authorization": f"Bearer {bob_token}"
    }

    ticket_response = client.post(
        "/tickets",
        headers=alice_headers,
        json={
            "title": "Alice payment issue",
            "description": "Alice needs help with a payment.",
        },
    )

    assert ticket_response.status_code == 201

    ticket_id = ticket_response.json()["id"]

    response = client.get(
        f"/tickets/{ticket_id}",
        headers=bob_headers,
    )

    assert response.status_code == 403


def test_delete_nonexistent_ticket(client, register_and_login):
    token = register_and_login()

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = client.delete(
        "/tickets/99999",
        headers=headers,
    )

    assert response.status_code == 404
