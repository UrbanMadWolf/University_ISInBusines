import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional

from app.schemas.forecast import (
    ForecastRequest,
    ForecastResponse,
    ForecastMetrics
)

def create_test_forecast_data(
    user_id: int,
    num_records: int = 30,
    start_date: Optional[datetime] = None
) -> List[Dict]:
    """Create test forecast data records"""
    if start_date is None:
        start_date = datetime.now() - timedelta(days=num_records)
    
    # Generate base amount and trend
    base_amount = random.uniform(1000.0, 5000.0)
    daily_trend = random.uniform(-50.0, 50.0)
    seasonal_variation = random.uniform(-0.2, 0.2)
    
    data = []
    for i in range(num_records):
        # Add trend and seasonal variation
        amount = base_amount + (daily_trend * i)
        amount *= (1 + seasonal_variation * random.uniform(-1, 1))
        
        # Add some random noise
        amount += random.uniform(-100.0, 100.0)
        
        record = {
            "date": (start_date + timedelta(days=i)).isoformat(),
            "amount": round(amount, 2),
            "category": random.choice(["revenue", "expense"]),
            "type": "forecast",
            "user_id": user_id
        }
        data.append(record)
    
    return data

def create_test_forecast_request(
    user_id: int,
    forecast_period: int = 30,
    confidence_level: float = 0.95
) -> ForecastRequest:
    """Create test forecast request"""
    return ForecastRequest(
        user_id=user_id,
        forecast_period=forecast_period,
        confidence_level=confidence_level,
        start_date=datetime.now().isoformat(),
        end_date=(datetime.now() + timedelta(days=forecast_period)).isoformat()
    )

def create_test_forecast_response(
    request: ForecastRequest,
    actual_values: Optional[List[Dict]] = None
) -> ForecastResponse:
    """Create test forecast response"""
    if actual_values is None:
        actual_values = create_test_forecast_data(
            request.user_id,
            num_records=request.forecast_period
        )
    
    # Generate forecasts
    forecasts = []
    base_amount = actual_values[-1]["amount"] if actual_values else 1000.0
    daily_trend = random.uniform(-50.0, 50.0)
    
    for i in range(request.forecast_period):
        amount = base_amount + (daily_trend * i)
        amount += random.uniform(-100.0, 100.0)  # Add noise
        
        forecasts.append({
            "date": (datetime.now() + timedelta(days=i)).isoformat(),
            "amount": round(amount, 2),
            "confidence_lower": round(amount * 0.9, 2),
            "confidence_upper": round(amount * 1.1, 2)
        })
    
    # Calculate metrics
    metrics = ForecastMetrics(
        mae=round(random.uniform(50.0, 200.0), 2),
        mse=round(random.uniform(2500.0, 40000.0), 2),
        rmse=round(random.uniform(50.0, 200.0), 2),
        r_squared=round(random.uniform(0.7, 0.95), 4)
    )
    
    return ForecastResponse(
        id=random.randint(1, 1000),
        user_id=request.user_id,
        forecasts=forecasts,
        actual_values=actual_values,
        metrics=metrics,
        created_at=datetime.now().isoformat(),
        forecast_period=request.forecast_period,
        confidence_level=request.confidence_level
    ) 