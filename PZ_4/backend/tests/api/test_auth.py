from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.tests.utils.utils import random_email, random_lower_string

def test_login(
    client: TestClient,
    test_user: dict
) -> None:
    """Test login endpoint"""
    login_data = {
        "username": test_user["email"],
        "password": test_user["password"],
    }
    r = client.post(f"{settings.API_V1_STR}/auth/login", data=login_data)
    tokens = r.json()
    assert r.status_code == 200
    assert "access_token" in tokens
    assert tokens["token_type"] == "bearer"

def test_login_wrong_password(
    client: TestClient,
    test_user: dict
) -> None:
    """Test login with wrong password"""
    login_data = {
        "username": test_user["email"],
        "password": "wrongpassword",
    }
    r = client.post(f"{settings.API_V1_STR}/auth/login", data=login_data)
    assert r.status_code == 401

def test_login_wrong_email(
    client: TestClient
) -> None:
    """Test login with wrong email"""
    login_data = {
        "username": random_email(),
        "password": random_lower_string(),
    }
    r = client.post(f"{settings.API_V1_STR}/auth/login", data=login_data)
    assert r.status_code == 401

def test_register(
    client: TestClient
) -> None:
    """Test register endpoint"""
    email = random_email()
    password = random_lower_string()
    data = {
        "email": email,
        "password": password,
        "full_name": "Test User",
    }
    r = client.post(f"{settings.API_V1_STR}/auth/register", json=data)
    assert r.status_code == 200
    created_user = r.json()
    assert created_user["email"] == email
    assert "id" in created_user

def test_register_existing_email(
    client: TestClient,
    test_user: dict
) -> None:
    """Test register with existing email"""
    data = {
        "email": test_user["email"],
        "password": random_lower_string(),
        "full_name": "Test User",
    }
    r = client.post(f"{settings.API_V1_STR}/auth/register", json=data)
    assert r.status_code == 400

def test_read_users_me(
    client: TestClient,
    test_user_token_headers: dict
) -> None:
    """Test read users me endpoint"""
    r = client.get(f"{settings.API_V1_STR}/auth/me", headers=test_user_token_headers)
    current_user = r.json()
    assert current_user
    assert current_user["email"] == test_user["email"]
    assert current_user["is_active"] is True
    assert current_user["is_superuser"] is False

def test_update_user_me(
    client: TestClient,
    test_user_token_headers: dict
) -> None:
    """Test update user me endpoint"""
    data = {"full_name": "New Name"}
    r = client.put(
        f"{settings.API_V1_STR}/auth/me",
        headers=test_user_token_headers,
        json=data,
    )
    assert r.status_code == 200
    updated_user = r.json()
    assert updated_user["full_name"] == data["full_name"]

def test_change_password(
    client: TestClient,
    test_user_token_headers: dict,
    test_user: dict
) -> None:
    """Test change password endpoint"""
    data = {
        "current_password": test_user["password"],
        "new_password": "newpassword123",
    }
    r = client.post(
        f"{settings.API_V1_STR}/auth/change-password",
        headers=test_user_token_headers,
        json=data,
    )
    assert r.status_code == 200
    assert r.json()["message"] == "Password updated successfully"

def test_change_password_wrong_password(
    client: TestClient,
    test_user_token_headers: dict
) -> None:
    """Test change password with wrong current password"""
    data = {
        "current_password": "wrongpassword",
        "new_password": "newpassword123",
    }
    r = client.post(
        f"{settings.API_V1_STR}/auth/change-password",
        headers=test_user_token_headers,
        json=data,
    )
    assert r.status_code == 400 