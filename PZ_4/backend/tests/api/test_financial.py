from datetime import datetime, timedelta
from typing import Dict, List

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.tests.utils.financial_utils import (
    create_test_financial_data,
    create_test_financial_metadata,
    create_test_financial_data_schema,
    create_test_financial_metadata_schema,
    create_test_financial_summary
)

def test_create_financial_data(
    client: TestClient,
    test_user_token_headers: dict,
    db: Session
) -> None:
    """Test creating financial data"""
    test_data = create_test_financial_data(1)[0]  # Get single record
    
    response = client.post(
        f"{settings.API_V1_STR}/financial/data",
        headers=test_user_token_headers,
        json=test_data
    )
    assert response.status_code == 200
    data = response.json()
    
    assert data["amount"] == test_data["amount"]
    assert data["category"] == test_data["category"]
    assert data["type"] == test_data["type"]
    assert data["user_id"] == test_data["user_id"]
    assert "id" in data
    assert "created_at" in data

def test_get_financial_data(
    client: TestClient,
    test_user_token_headers: dict,
    db: Session
) -> None:
    """Test getting financial data"""
    # Create test data
    test_data = create_test_financial_data(1, num_records=5)
    for data in test_data:
        client.post(
            f"{settings.API_V1_STR}/financial/data",
            headers=test_user_token_headers,
            json=data
        )
    
    response = client.get(
        f"{settings.API_V1_STR}/financial/data",
        headers=test_user_token_headers
    )
    assert response.status_code == 200
    data = response.json()
    
    assert isinstance(data, list)
    assert len(data) >= 5  # At least the records we created
    for item in data:
        assert "id" in item
        assert "amount" in item
        assert "category" in item
        assert "type" in item
        assert "user_id" in item
        assert "created_at" in item

def test_get_financial_data_with_filters(
    client: TestClient,
    test_user_token_headers: dict,
    db: Session
) -> None:
    """Test getting financial data with filters"""
    # Create test data
    test_data = create_test_financial_data(1, num_records=5)
    for data in test_data:
        client.post(
            f"{settings.API_V1_STR}/financial/data",
            headers=test_user_token_headers,
            json=data
        )
    
    # Test date range filter
    start_date = (datetime.now() - timedelta(days=30)).isoformat()
    end_date = datetime.now().isoformat()
    
    response = client.get(
        f"{settings.API_V1_STR}/financial/data",
        headers=test_user_token_headers,
        params={
            "start_date": start_date,
            "end_date": end_date
        }
    )
    assert response.status_code == 200
    data = response.json()
    
    assert isinstance(data, list)
    for item in data:
        assert start_date <= item["date"] <= end_date
    
    # Test category filter
    category = test_data[0]["category"]
    response = client.get(
        f"{settings.API_V1_STR}/financial/data",
        headers=test_user_token_headers,
        params={"category": category}
    )
    assert response.status_code == 200
    data = response.json()
    
    assert isinstance(data, list)
    for item in data:
        assert item["category"] == category

def test_update_financial_data(
    client: TestClient,
    test_user_token_headers: dict,
    db: Session
) -> None:
    """Test updating financial data"""
    # Create test data
    test_data = create_test_financial_data(1)[0]
    response = client.post(
        f"{settings.API_V1_STR}/financial/data",
        headers=test_user_token_headers,
        json=test_data
    )
    data_id = response.json()["id"]
    
    # Update data
    update_data = {
        "amount": 2000.0,
        "category": "updated_category",
        "description": "Updated description"
    }
    
    response = client.put(
        f"{settings.API_V1_STR}/financial/data/{data_id}",
        headers=test_user_token_headers,
        json=update_data
    )
    assert response.status_code == 200
    data = response.json()
    
    assert data["amount"] == update_data["amount"]
    assert data["category"] == update_data["category"]
    assert data["description"] == update_data["description"]
    assert data["id"] == data_id

def test_delete_financial_data(
    client: TestClient,
    test_user_token_headers: dict,
    db: Session
) -> None:
    """Test deleting financial data"""
    # Create test data
    test_data = create_test_financial_data(1)[0]
    response = client.post(
        f"{settings.API_V1_STR}/financial/data",
        headers=test_user_token_headers,
        json=test_data
    )
    data_id = response.json()["id"]
    
    # Delete data
    response = client.delete(
        f"{settings.API_V1_STR}/financial/data/{data_id}",
        headers=test_user_token_headers
    )
    assert response.status_code == 200
    
    # Verify deletion
    response = client.get(
        f"{settings.API_V1_STR}/financial/data/{data_id}",
        headers=test_user_token_headers
    )
    assert response.status_code == 404

def test_get_financial_summary(
    client: TestClient,
    test_user_token_headers: dict,
    db: Session
) -> None:
    """Test getting financial summary"""
    # Create test data
    test_data = create_test_financial_data(1, num_records=5)
    for data in test_data:
        client.post(
            f"{settings.API_V1_STR}/financial/data",
            headers=test_user_token_headers,
            json=data
        )
    
    response = client.get(
        f"{settings.API_V1_STR}/financial/summary",
        headers=test_user_token_headers
    )
    assert response.status_code == 200
    data = response.json()
    
    assert "total_revenue" in data
    assert "total_expenses" in data
    assert "net_profit" in data
    assert "profit_margin" in data
    assert "category_totals" in data
    assert "monthly_trends" in data

def test_create_financial_metadata(
    client: TestClient,
    test_user_token_headers: dict,
    db: Session
) -> None:
    """Test creating financial metadata"""
    test_metadata = create_test_financial_metadata(1)[0]
    
    response = client.post(
        f"{settings.API_V1_STR}/financial/metadata",
        headers=test_user_token_headers,
        json=test_metadata
    )
    assert response.status_code == 200
    data = response.json()
    
    assert data["key"] == test_metadata["key"]
    assert data["value"] == test_metadata["value"]
    assert data["category"] == test_metadata["category"]
    assert data["user_id"] == test_metadata["user_id"]
    assert "id" in data
    assert "created_at" in data

def test_get_financial_metadata(
    client: TestClient,
    test_user_token_headers: dict,
    db: Session
) -> None:
    """Test getting financial metadata"""
    # Create test metadata
    test_metadata = create_test_financial_metadata(1, num_records=3)
    for metadata in test_metadata:
        client.post(
            f"{settings.API_V1_STR}/financial/metadata",
            headers=test_user_token_headers,
            json=metadata
        )
    
    response = client.get(
        f"{settings.API_V1_STR}/financial/metadata",
        headers=test_user_token_headers
    )
    assert response.status_code == 200
    data = response.json()
    
    assert isinstance(data, list)
    assert len(data) >= 3  # At least the records we created
    for item in data:
        assert "id" in item
        assert "key" in item
        assert "value" in item
        assert "category" in item
        assert "user_id" in item
        assert "created_at" in item

def test_update_financial_metadata(
    client: TestClient,
    test_user_token_headers: dict,
    test_user: dict
) -> None:
    """Test update financial metadata endpoint"""
    # Create test data
    test_data = create_test_financial_metadata(test_user["id"], num_records=1)[0]
    r = client.post(
        f"{settings.API_V1_STR}/financial/metadata",
        headers=test_user_token_headers,
        json=test_data
    )
    created_data = r.json()
    
    # Update data
    update_data = {"value": "Updated value", "description": "Updated description"}
    r = client.put(
        f"{settings.API_V1_STR}/financial/metadata/{created_data['id']}",
        headers=test_user_token_headers,
        json=update_data
    )
    assert r.status_code == 200
    updated_data = r.json()
    assert updated_data["value"] == update_data["value"]
    assert updated_data["description"] == update_data["description"]

def test_delete_financial_metadata(
    client: TestClient,
    test_user_token_headers: dict,
    test_user: dict
) -> None:
    """Test delete financial metadata endpoint"""
    # Create test data
    test_data = create_test_financial_metadata(test_user["id"], num_records=1)[0]
    r = client.post(
        f"{settings.API_V1_STR}/financial/metadata",
        headers=test_user_token_headers,
        json=test_data
    )
    created_data = r.json()
    
    # Delete data
    r = client.delete(
        f"{settings.API_V1_STR}/financial/metadata/{created_data['id']}",
        headers=test_user_token_headers
    )
    assert r.status_code == 200
    
    # Verify deletion
    r = client.get(
        f"{settings.API_V1_STR}/financial/metadata/{created_data['id']}",
        headers=test_user_token_headers
    )
    assert r.status_code == 404 