import pytest
from unittest.mock import patch, MagicMock

def make_fake_history_entry(id=1):
    fake_entry = MagicMock()
    fake_entry.to_dict.return_value = {
        "id": id,
        "origin": "CDG",
        "destination": "JFK",
        "departure_date": "2025-06-01",
        "return_date": "2025-06-10",
    }
    return fake_entry

@patch("app.routes.history_routes.get_user_history")
def test_get_history_success(mock_get_history, client, auth_headers):
    mock_get_history.return_value = [make_fake_history_entry(), make_fake_history_entry(id=2)]

    response = client.get("/history/", headers=auth_headers)

    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert set(data[0].keys()) >= {"id", "origin", "destination", "departure_date", "return_date"}

@patch("app.routes.history_routes.get_user_history")
def test_get_history_empty(mock_get_history, client, auth_headers):
    mock_get_history.return_value = []

    response = client.get("/history/", headers=auth_headers)

    assert response.status_code == 200
    assert response.get_json() == []

@patch("app.routes.history_routes.get_user_history")
def test_get_history_service_raises(mock_get_history, client, auth_headers):
    mock_get_history.side_effect = Exception("DB error")

    response = client.get("/history/", headers=auth_headers)

    assert response.status_code == 500
    assert response.get_json() == {"error": "DB error"}

def test_get_history_no_auth(client):
    response = client.get("/history/")
    assert response.status_code == 401
