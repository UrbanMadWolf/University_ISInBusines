import pytest
from datetime import datetime, timedelta
from typing import Dict, List

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.tests.utils.forecast_utils import (
    create_test_forecast_data,
    create_test_forecast_request,
    create_test_forecast_response
)

def test_generate_forecast(
    client: TestClient,
    test_user_token_headers: dict,
    db: Session
) -> None:
    """Test generating a forecast"""
    # Create test data
    test_data = create_test_forecast_data(1, num_records=30)
    for data in test_data:
        client.post(
            f"{settings.API_V1_STR}/financial/data",
            headers=test_user_token_headers,
            json=data
        )
    
    # Generate forecast
    request = create_test_forecast_request(1)
    response = client.post(
        f"{settings.API_V1_STR}/forecast/generate",
        headers=test_user_token_headers,
        json=request.dict()
    )
    assert response.status_code == 200
    data = response.json()
    
    assert "forecasts" in data
    assert "actual_values" in data
    assert "metrics" in data
    
    forecasts = data["forecasts"]
    assert isinstance(forecasts, list)
    assert len(forecasts) == request.forecast_period
    for forecast in forecasts:
        assert "date" in forecast
        assert "amount" in forecast
        assert "confidence_lower" in forecast
        assert "confidence_upper" in forecast
    
    metrics = data["metrics"]
    assert "mae" in metrics
    assert "mse" in metrics
    assert "rmse" in metrics
    assert "r_squared" in metrics

def test_generate_forecast_without_data(
    client: TestClient,
    test_user_token_headers: dict,
    db: Session
) -> None:
    """Test generating a forecast without historical data"""
    request = create_test_forecast_request(1)
    response = client.post(
        f"{settings.API_V1_STR}/forecast/generate",
        headers=test_user_token_headers,
        json=request.dict()
    )
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "insufficient historical data" in data["detail"].lower()

def test_generate_forecast_with_insufficient_data(
    client: TestClient,
    test_user_token_headers: dict,
    db: Session
) -> None:
    """Test generating a forecast with insufficient data"""
    # Create minimal test data
    test_data = create_test_forecast_data(1, num_records=5)
    for data in test_data:
        client.post(
            f"{settings.API_V1_STR}/financial/data",
            headers=test_user_token_headers,
            json=data
        )
    
    request = create_test_forecast_request(1, forecast_period=30)
    response = client.post(
        f"{settings.API_V1_STR}/forecast/generate",
        headers=test_user_token_headers,
        json=request.dict()
    )
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "insufficient historical data" in data["detail"].lower()

def test_evaluate_forecast(
    client: TestClient,
    test_user_token_headers: dict,
    db: Session
) -> None:
    """Test evaluating a forecast"""
    # Create test data and generate forecast
    test_data = create_test_forecast_data(1, num_records=30)
    for data in test_data:
        client.post(
            f"{settings.API_V1_STR}/financial/data",
            headers=test_user_token_headers,
            json=data
        )
    
    request = create_test_forecast_request(1)
    forecast_response = client.post(
        f"{settings.API_V1_STR}/forecast/generate",
        headers=test_user_token_headers,
        json=request.dict()
    )
    forecast_data = forecast_response.json()
    
    # Evaluate forecast
    response = client.post(
        f"{settings.API_V1_STR}/forecast/evaluate",
        headers=test_user_token_headers,
        json={
            "forecast_id": forecast_data["id"],
            "actual_values": test_data[-10:]  # Use last 10 records for evaluation
        }
    )
    assert response.status_code == 200
    data = response.json()
    
    assert "metrics" in data
    assert "actual_vs_predicted" in data
    
    metrics = data["metrics"]
    assert "mae" in metrics
    assert "mse" in metrics
    assert "rmse" in metrics
    assert "r_squared" in metrics
    
    actual_vs_predicted = data["actual_vs_predicted"]
    assert isinstance(actual_vs_predicted, list)
    assert len(actual_vs_predicted) > 0
    for item in actual_vs_predicted:
        assert "date" in item
        assert "actual" in item
        assert "predicted" in item

def test_get_forecast_history(
    client: TestClient,
    test_user_token_headers: dict,
    db: Session
) -> None:
    """Test getting forecast history"""
    response = client.get(
        f"{settings.API_V1_STR}/forecast/history",
        headers=test_user_token_headers
    )
    assert response.status_code == 200
    data = response.json()
    
    assert isinstance(data, list)
    if len(data) > 0:
        forecast = data[0]
        assert "id" in forecast
        assert "user_id" in forecast
        assert "created_at" in forecast
        assert "forecast_period" in forecast
        assert "confidence_level" in forecast

def test_get_forecast_details(
    client: TestClient,
    test_user_token_headers: dict,
    db: Session
) -> None:
    """Test getting forecast details"""
    # First generate a forecast
    test_data = create_test_forecast_data(1, num_records=30)
    for data in test_data:
        client.post(
            f"{settings.API_V1_STR}/financial/data",
            headers=test_user_token_headers,
            json=data
        )
    
    request = create_test_forecast_request(1)
    forecast_response = client.post(
        f"{settings.API_V1_STR}/forecast/generate",
        headers=test_user_token_headers,
        json=request.dict()
    )
    forecast_data = forecast_response.json()
    
    # Get forecast details
    response = client.get(
        f"{settings.API_V1_STR}/forecast/{forecast_data['id']}",
        headers=test_user_token_headers
    )
    assert response.status_code == 200
    data = response.json()
    
    assert "id" in data
    assert "user_id" in data
    assert "forecasts" in data
    assert "actual_values" in data
    assert "metrics" in data
    assert "created_at" in data
    assert "forecast_period" in data
    assert "confidence_level" in data
    
    forecasts = data["forecasts"]
    assert isinstance(forecasts, list)
    assert len(forecasts) == request.forecast_period
    for forecast in forecasts:
        assert "date" in forecast
        assert "amount" in forecast
        assert "confidence_lower" in forecast
        assert "confidence_upper" in forecast 