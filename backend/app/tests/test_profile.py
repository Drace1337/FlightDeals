import pytest
from unittest.mock import patch, MagicMock
from werkzeug.security import generate_password_hash


@patch("app.routes.profile_routes.User")
def test_get_profile_success(mock_user_model, client, auth_headers):
    """Test retrieving user profile successfully."""
    mock_user = MagicMock()
    mock_user.email = "user@example.com"
    mock_user.name = "Drace"
    mock_user_model.query.get.return_value = mock_user

    response = client.get("/profile", headers=auth_headers)

    assert response.status_code == 200
    assert response.get_json() == {
        "email": "user@example.com",
        "name": "Drace",
    }


@patch("app.routes.profile_routes.User")
def test_get_profile_user_not_found(mock_user_model, client, auth_headers):
    """Test retrieving user profile when user is not found."""
    mock_user_model.query.get.return_value = None

    response = client.get("/profile", headers=auth_headers)

    assert response.status_code == 404
    assert response.get_json() == {"message": "User not found"}


@patch("app.routes.profile_routes.User")
@patch("app.routes.profile_routes.db")
def test_update_profile_success(mock_db, mock_user_model, client, auth_headers):
    """Test updating user profile successfully."""
    mock_user = MagicMock()
    mock_user.email = "old@example.com"
    mock_user.name = "Old Drace"
    mock_user_model.query.get.return_value = mock_user
    mock_user_model.query.filter_by.return_value.first.side_effect = [None, None]

    response = client.put(
        "/profile",
        headers=auth_headers,
        json={"email": "new@example.com", "name": "New Drace"},
    )

    assert response.status_code == 200
    assert response.get_json() == {"message": "Profile updated successfully"}
    assert mock_user.email == "new@example.com"
    assert mock_user.name == "New Drace"
    mock_db.session.commit.assert_called_once()


@patch("app.routes.profile_routes.User")
def test_update_profile_user_not_found(mock_user_model, client, auth_headers):
    """Test updating user profile when user is not found."""
    mock_user_model.query.get.return_value = None

    response = client.put("/profile", headers=auth_headers, json={"name": "Drace"})

    assert response.status_code == 404
    assert response.get_json() == {"message": "User not found"}


@patch("app.routes.profile_routes.User")
def test_update_profile_conflict_email(mock_user_model, client, auth_headers):
    """Test updating user profile with an email that already exists."""
    mock_user = MagicMock()
    mock_user.email = "old@example.com"
    mock_user.name = "Drace"
    mock_user_model.query.get.return_value = mock_user
    mock_user_model.query.filter_by.return_value.first.return_value = True  

    response = client.put(
        "/profile", headers=auth_headers, json={"email": "existing@example.com"}
    )

    assert response.status_code == 409
    assert response.get_json() == {"message": "User with such email already exists"}


@patch("app.routes.profile_routes.User")
def test_update_profile_conflict_name(mock_user_model, client, auth_headers):
    """Test updating user profile with a name that already exists."""
    mock_user = MagicMock()
    mock_user.email = "user@example.com"
    mock_user.name = "Drace"
    mock_user_model.query.get.return_value = mock_user

    mock_query = MagicMock()
    mock_query.first.return_value = True
    mock_user_model.query.filter_by.return_value = mock_query

    response = client.put(
        "/profile",
        headers=auth_headers,
        json={"name": "Existing Name"}
    )

    assert response.status_code == 409
    assert response.get_json() == {"message": "User with such name already exists"}



@patch("app.routes.profile_routes.User")
@patch("app.routes.profile_routes.db")
def test_update_password_success(mock_db, mock_user_model, client, auth_headers):
    """Test updating user password successfully."""
    current_password = "password123"
    new_password = "password456"
    hashed = generate_password_hash(current_password)

    mock_user = MagicMock()
    mock_user.password = hashed
    mock_user_model.query.get.return_value = mock_user

    response = client.put(
        "/profile/password",
        headers=auth_headers,
        json={"current_password": current_password, "new_password": new_password},
    )

    assert response.status_code == 200
    assert response.get_json() == {"message": "Password updated successfully"}
    mock_db.session.commit.assert_called_once()


@patch("app.routes.profile_routes.User")
def test_update_password_user_not_found(mock_user_model, client, auth_headers):
    """Test updating password when user is not found."""
    mock_user_model.query.get.return_value = None

    response = client.put(
        "/profile/password",
        headers=auth_headers,
        json={"current_password": "password123", "new_password": "password456"},
    )

    assert response.status_code == 404
    assert response.get_json() == {"message": "User not found"}


@patch("app.routes.profile_routes.User")
def test_update_password_missing_fields(mock_user_model, client, auth_headers):
    """Test updating password with missing fields."""
    mock_user = MagicMock()
    mock_user_model.query.get.return_value = mock_user

    response = client.put(
        "/profile/password", headers=auth_headers, json={"current_password": "password123"}
    )

    assert response.status_code == 400
    assert response.get_json() == {"message": "Current and new password are required"}


@patch("app.routes.profile_routes.User")
def test_update_password_wrong_current_password(mock_user_model, client, auth_headers):
    """Test updating password with incorrect current password."""
    mock_user = MagicMock()
    mock_user.password = generate_password_hash("password123")
    mock_user_model.query.get.return_value = mock_user

    response = client.put(
        "/profile/password",
        headers=auth_headers,
        json={"current_password": "wrongpass", "new_password": "password456"},
    )

    assert response.status_code == 401
    assert response.get_json() == {"message": "Current password is incorrect"}
