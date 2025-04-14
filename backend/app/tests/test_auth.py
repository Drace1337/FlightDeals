def test_register_and_login(client):
    # Rejestracja
    register_data = {"email": "test@example.com", "password": "pass123"}
    res = client.post("/auth/register", json=register_data)
    assert res.status_code == 201
    assert res.get_json()["message"] == "User created successfully"

    # Logowanie
    login_data = {"email": "test@example.com", "password": "pass123"}
    res = client.post("/auth/login", json=login_data)
    assert res.status_code == 200
    assert "access_token" in res.get_json()
