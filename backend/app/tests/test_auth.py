def test_register_and_login(client):
    # Rejestracja
    register_data = {
        "name": "Drace",
        "email": "test@example.com",
        "password": "password123",
    }
    res = client.post("/auth/register", json=register_data)
    assert res.status_code == 201
    assert res.get_json()["message"] == "User created successfully"

    # Logowanie
    login_data = {"email": "test@example.com", "password": "password123"}
    res = client.post("/auth/login", json=login_data)
    assert res.status_code == 200
    assert "access_token" in res.get_json()


def test_register_missing_fields(client):
    # Test missing email
    register_data = {"name": "Drace", "password": "password123"}
    res = client.post("/auth/register", json=register_data)
    assert res.status_code == 400
    assert "required" in res.get_json()["message"]

    # Test missing password
    register_data = {"name": "Drace", "email": "test@example.com"}
    res = client.post("/auth/register", json=register_data)
    assert res.status_code == 400
    assert "required" in res.get_json()["message"]

    # Test missing name
    register_data = {"email": "test@example.com", "password": "password123"}
    res = client.post("/auth/register", json=register_data)
    assert res.status_code == 400
    assert "required" in res.get_json()["message"]

    # Test with no JSON data
    res = client.post("/auth/register", data="not json data")
    assert res.status_code == 400
    assert "provided" in res.get_json()["message"]


def test_register_duplicate_email(client):
    # First registration
    register_data = {
        "name": "FirstUser",
        "email": "duplicate@example.com",
        "password": "password123",
    }
    res = client.post("/auth/register", json=register_data)
    assert res.status_code == 201

    # Try to register with the same email
    register_data = {
        "name": "SecondUser",
        "email": "duplicate@example.com",
        "password": "password1234",
    }
    res = client.post("/auth/register", json=register_data)
    assert res.status_code == 409
    assert "email already exists" in res.get_json()["message"]


def test_register_duplicate_name(client):
    # First registration
    register_data = {
        "name": "Drace",
        "email": "user1@example.com",
        "password": "password123",
    }
    res = client.post("/auth/register", json=register_data)
    assert res.status_code == 201

    # Try to register with the same name
    register_data = {
        "name": "Drace",
        "email": "user2@example.com",
        "password": "password1234",
    }
    res = client.post("/auth/register", json=register_data)
    assert res.status_code == 409
    assert "name already exists" in res.get_json()["message"]


def test_login_invalid_credentials(client):
    # Register a user first
    register_data = {
        "name": "Drace",
        "email": "valid@example.com",
        "password": "correctpassword",
    }
    client.post("/auth/register", json=register_data)

    # Test wrong email
    login_data = {"email": "wrong@example.com", "password": "correctpassword"}
    res = client.post("/auth/login", json=login_data)
    assert res.status_code == 401
    assert "Invalid credentials" in res.get_json()["message"]

    # Test wrong password
    login_data = {"email": "valid@example.com", "password": "wrongpassword"}
    res = client.post("/auth/login", json=login_data)
    assert res.status_code == 401
    assert "Invalid credentials" in res.get_json()["message"]


def test_login_missing_fields(client):
    # Test missing email
    login_data = {"password": "password123"}
    res = client.post("/auth/login", json=login_data)
    assert res.status_code == 401
    assert "Email and password are required" in res.get_json()["message"]

    # Test missing password
    login_data = {"email": "test@example.com"}
    res = client.post("/auth/login", json=login_data)
    assert res.status_code == 401
    assert "Email and password are required" in res.get_json()["message"]

    # Test with no JSON data
    res = client.post("/auth/login", data="not json data")
    assert res.status_code == 400
    assert "No data provided" in res.get_json()["message"]


def test_logout(client):
    # Register and login a user first
    register_data = {
        "name": "Drace",
        "email": "logout@example.com",
        "password": "password123",
    }
    client.post("/auth/register", json=register_data)

    login_data = {"email": "logout@example.com", "password": "password123"}
    client.post("/auth/login", json=login_data)

    # Test logout
    res = client.post("/auth/logout")
    assert res.status_code == 200
    assert "Logout successful" in res.get_json()["message"]


def test_login_with_empty_credentials(client):
    # Test with empty strings
    login_data = {"email": "", "password": ""}
    res = client.post("/auth/login", json=login_data)
    assert res.status_code == 401
    assert "Email and password are required" in res.get_json()["message"]
