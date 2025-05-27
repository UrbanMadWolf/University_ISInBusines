from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel

class ForecastRequest(BaseModel):
    start_date: datetime
    end_date: datetime
    forecast_period: int  # Number of periods to forecast
    target_metrics: List[str]  # List of metrics to forecast
    confidence_level: float = 0.95

class ForecastPoint(BaseModel):
    date: datetime
    value: float
    lower_bound: float
    upper_bound: float

class ForecastResponse(BaseModel):
    forecast_period: int
    revenue_forecast: List[ForecastPoint]
    expense_forecast: List[ForecastPoint]
    profit_forecast: List[ForecastPoint]
    confidence_intervals: Dict[str, float]

class ForecastEvaluation(BaseModel):
    mae: float  # Mean Absolute Error
    mse: float  # Mean Squared Error
    rmse: float  # Root Mean Squared Error
    r2_score: float  # R-squared score 