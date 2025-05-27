import random
import string
from typing import Any, Dict, Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import SessionLocal
from app.main import app
from app.models.user import User
from app.schemas.user import UserCreate
from app.services.user import UserService

def random_lower_string() -> str:
    """Generate random string in lowercase"""
    return "".join(random.choices(string.ascii_lowercase, k=32))

def random_email() -> str:
    """Generate random email"""
    return f"{random_lower_string()}@example.com"

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
def test_user(db: Session) -> Dict[str, Any]:
    """Create test user"""
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(
        email=email,
        password=password,
        full_name="Test User",
        is_superuser=False,
    )
    user = UserService(db).create(user_in)
    return {
        "id": user.id,
        "email": user.email,
        "password": password,
        "full_name": user.full_name,
        "is_superuser": user.is_superuser,
    }

@pytest.fixture(scope="module")
def test_superuser(db: Session) -> Dict[str, Any]:
    """Create test superuser"""
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(
        email=email,
        password=password,
        full_name="Test Superuser",
        is_superuser=True,
    )
    user = UserService(db).create(user_in)
    return {
        "id": user.id,
        "email": user.email,
        "password": password,
        "full_name": user.full_name,
        "is_superuser": user.is_superuser,
    }

@pytest.fixture(scope="module")
def test_user_token_headers(
    client: TestClient, test_user: Dict[str, Any]
) -> Dict[str, str]:
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
def test_superuser_token_headers(
    client: TestClient, test_superuser: Dict[str, Any]
) -> Dict[str, str]:
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