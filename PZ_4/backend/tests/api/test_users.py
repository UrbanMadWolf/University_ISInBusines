from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.tests.utils.utils import random_email, random_lower_string

def test_read_users(
    client: TestClient,
    test_superuser_token_headers: dict
) -> None:
    """Test read users endpoint"""
    r = client.get(f"{settings.API_V1_STR}/users/", headers=test_superuser_token_headers)
    users = r.json()
    assert r.status_code == 200
    assert len(users) > 0

def test_read_users_normal_user(
    client: TestClient,
    test_user_token_headers: dict
) -> None:
    """Test read users endpoint with normal user"""
    r = client.get(f"{settings.API_V1_STR}/users/", headers=test_user_token_headers)
    assert r.status_code == 403

def test_create_user(
    client: TestClient,
    test_superuser_token_headers: dict
) -> None:
    """Test create user endpoint"""
    data = {
        "email": random_email(),
        "password": random_lower_string(),
        "full_name": "Test User",
        "is_superuser": False,
    }
    r = client.post(
        f"{settings.API_V1_STR}/users/",
        headers=test_superuser_token_headers,
        json=data,
    )
    assert r.status_code == 200
    created_user = r.json()
    assert created_user["email"] == data["email"]
    assert created_user["is_superuser"] == data["is_superuser"]
    assert "id" in created_user

def test_create_user_existing_email(
    client: TestClient,
    test_superuser_token_headers: dict,
    test_user: dict
) -> None:
    """Test create user with existing email"""
    data = {
        "email": test_user["email"],
        "password": random_lower_string(),
        "full_name": "Test User",
        "is_superuser": False,
    }
    r = client.post(
        f"{settings.API_V1_STR}/users/",
        headers=test_superuser_token_headers,
        json=data,
    )
    assert r.status_code == 400

def test_read_user(
    client: TestClient,
    test_superuser_token_headers: dict,
    test_user: dict
) -> None:
    """Test read user endpoint"""
    r = client.get(
        f"{settings.API_V1_STR}/users/{test_user['id']}",
        headers=test_superuser_token_headers,
    )
    user = r.json()
    assert r.status_code == 200
    assert user["email"] == test_user["email"]
    assert user["id"] == test_user["id"]

def test_read_user_normal_user(
    client: TestClient,
    test_user_token_headers: dict,
    test_user: dict
) -> None:
    """Test read user endpoint with normal user"""
    r = client.get(
        f"{settings.API_V1_STR}/users/{test_user['id']}",
        headers=test_user_token_headers,
    )
    assert r.status_code == 403

def test_update_user(
    client: TestClient,
    test_superuser_token_headers: dict,
    test_user: dict
) -> None:
    """Test update user endpoint"""
    data = {"full_name": "Updated Name"}
    r = client.put(
        f"{settings.API_V1_STR}/users/{test_user['id']}",
        headers=test_superuser_token_headers,
        json=data,
    )
    assert r.status_code == 200
    updated_user = r.json()
    assert updated_user["full_name"] == data["full_name"]
    assert updated_user["email"] == test_user["email"]

def test_update_user_normal_user(
    client: TestClient,
    test_user_token_headers: dict,
    test_user: dict
) -> None:
    """Test update user endpoint with normal user"""
    data = {"full_name": "Updated Name"}
    r = client.put(
        f"{settings.API_V1_STR}/users/{test_user['id']}",
        headers=test_user_token_headers,
        json=data,
    )
    assert r.status_code == 403

def test_delete_user(
    client: TestClient,
    test_superuser_token_headers: dict,
    test_user: dict
) -> None:
    """Test delete user endpoint"""
    r = client.delete(
        f"{settings.API_V1_STR}/users/{test_user['id']}",
        headers=test_superuser_token_headers,
    )
    assert r.status_code == 200
    deleted_user = r.json()
    assert deleted_user["id"] == test_user["id"]
    assert deleted_user["email"] == test_user["email"]

def test_delete_user_normal_user(
    client: TestClient,
    test_user_token_headers: dict,
    test_user: dict
) -> None:
    """Test delete user endpoint with normal user"""
    r = client.delete(
        f"{settings.API_V1_STR}/users/{test_user['id']}",
        headers=test_user_token_headers,
    )
    assert r.status_code == 403 