import pytest
from typing import Generator, Dict
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from app.db.session import SessionLocal
from app.core.config import settings
from app.models.user import User
from app.core.security import get_password_hash

@pytest.fixture(scope="session")
def db() -> Generator:
    """Get database session"""
    yield SessionLocal()

@pytest.fixture(scope="module")
def client() -> Generator:
    """Get test client"""
    with TestClient(app) as c:
        yield c

@pytest.fixture(scope="module")
def test_user(db: Session) -> Dict[str, str]:
    """Create test user"""
    user = User(
        email="test@example.com",
        hashed_password=get_password_hash("testpassword"),
        full_name="Test User",
        is_active=True,
        is_superuser=False
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return {
        "email": "test@example.com",
        "password": "testpassword",
        "id": user.id
    }

@pytest.fixture(scope="module")
def test_superuser(db: Session) -> Dict[str, str]:
    """Create test superuser"""
    user = User(
        email="admin@example.com",
        hashed_password=get_password_hash("adminpassword"),
        full_name="Admin User",
        is_active=True,
        is_superuser=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return {
        "email": "admin@example.com",
        "password": "adminpassword",
        "id": user.id
    }

@pytest.fixture(scope="module")
def test_user_token_headers(client: TestClient, test_user: Dict[str, str]) -> Dict[str, str]:
    """Get test user token headers"""
    login_data = {
        "username": test_user["email"],
        "password": test_user["password"],
    }
    r = client.post(f"{settings.API_V1_STR}/auth/login", data=login_data)
    tokens = r.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}
    return headers

@pytest.fixture(scope="module")
def test_superuser_token_headers(client: TestClient, test_superuser: Dict[str, str]) -> Dict[str, str]:
    """Get test superuser token headers"""
    login_data = {
        "username": test_superuser["email"],
        "password": test_superuser["password"],
    }
    r = client.post(f"{settings.API_V1_STR}/auth/login", data=login_data)
    tokens = r.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}
    return headers 