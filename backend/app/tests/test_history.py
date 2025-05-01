from app.models import User
from app.extensions import db
from datetime import datetime, timezone


def test_search_save_and_history(client):
    # Rejestracja użytkownika
    client.post("/auth/register", json={"name": "Drace","email": "testuser@example.com", "password": "pass123"})

    # Logowanie
    login_res = client.post("/auth/login", json={"email": "testuser@example.com", "password": "pass123"})
    access_token = login_res.get_json()["access_token"]

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    search_data = {
        "origin": "CDG",
        "destination": "JFK",
        "departure_date": "2025-06-01",
        "return_date": "2025-06-10",
    }


    print("TOKEN:", access_token)
    print("HEADERS:", headers)
    print("DATA:", search_data)
    res = client.post("/search/save", json=search_data, headers=headers)
    print("RESPONSE JSON:", res.get_json())

    assert res.status_code == 201

    history_res = client.get("/history/", headers=headers)
    assert history_res.status_code == 200
    assert len(history_res.get_json()) >= 1

