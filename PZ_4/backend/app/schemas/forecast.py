from typing import List, Dict, Optional
from datetime import datetime
from pydantic import BaseModel

class ForecastPoint(BaseModel):
    date: datetime
    value: float

class Forecast(BaseModel):
    metric: str
    forecast_periods: int
    forecast_data: List[ForecastPoint]
    actual_data: List[ForecastPoint]
    performance_metrics: Dict[str, float]

class ActualVsPredicted(BaseModel):
    date: datetime
    actual: float
    predicted: float

class ForecastEvaluation(BaseModel):
    metric: str
    forecast_periods: int
    actual_vs_predicted: List[ActualVsPredicted]
    metrics: Dict[str, float]

class ForecastHistory(BaseModel):
    date: datetime
    metric: str
    actual_value: float
    forecast_value: float
    error: float

class ForecastDetails(BaseModel):
    metric: str
    forecast_periods: int
    forecast_data: List[ForecastPoint]
    actual_data: List[ForecastPoint]
    performance_metrics: Dict[str, float]
    forecast_history: List[ForecastHistory]
    additional_metrics: Dict[str, float] 