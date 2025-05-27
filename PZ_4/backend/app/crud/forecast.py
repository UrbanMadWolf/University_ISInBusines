from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func
import numpy as np
from sklearn.linear_model import LinearRegression

from app.models.financial_data import FinancialData
from app.schemas.forecast import (
    Forecast,
    ForecastEvaluation,
    ForecastHistory,
    ForecastDetails
)

def generate_forecast(
    db: Session,
    user_id: int,
    metric: str,
    forecast_periods: int = 12,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
) -> Forecast:
    """Generate forecast for specified metric"""
    # Get historical data
    query = db.query(FinancialData).filter(FinancialData.user_id == user_id)
    
    if start_date:
        query = query.filter(FinancialData.date >= start_date)
    if end_date:
        query = query.filter(FinancialData.date <= end_date)
    
    # Get monthly data
    monthly_data = query.with_entities(
        func.date_trunc('month', FinancialData.date).label('month'),
        func.sum(FinancialData.amount).label('amount')
    ).group_by('month').order_by('month').all()
    
    if len(monthly_data) < 3:
        raise ValueError("Insufficient historical data for forecasting")
    
    # Prepare data for forecasting
    X = np.array(range(len(monthly_data))).reshape(-1, 1)
    y = np.array([data[1] for data in monthly_data])
    
    # Train linear regression model
    model = LinearRegression()
    model.fit(X, y)
    
    # Generate forecast
    future_X = np.array(range(len(monthly_data), len(monthly_data) + forecast_periods)).reshape(-1, 1)
    forecast_values = model.predict(future_X)
    
    # Calculate performance metrics
    y_pred = model.predict(X)
    mae = np.mean(np.abs(y - y_pred))
    mse = np.mean((y - y_pred) ** 2)
    rmse = np.sqrt(mse)
    r2 = model.score(X, y)
    
    # Prepare forecast data
    forecast_data = []
    for i, value in enumerate(forecast_values):
        forecast_date = monthly_data[-1][0] + timedelta(days=30 * (i + 1))
        forecast_data.append({
            "date": forecast_date,
            "value": float(value)
        })
    
    # Prepare actual data
    actual_data = []
    for date, value in monthly_data:
        actual_data.append({
            "date": date,
            "value": float(value)
        })
    
    return Forecast(
        metric=metric,
        forecast_periods=forecast_periods,
        forecast_data=forecast_data,
        actual_data=actual_data,
        performance_metrics={
            "mae": float(mae),
            "mse": float(mse),
            "rmse": float(rmse),
            "r2": float(r2)
        }
    )

def evaluate_forecast(
    db: Session,
    user_id: int,
    metric: str,
    forecast_periods: int = 12,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
) -> ForecastEvaluation:
    """Evaluate forecast accuracy"""
    # Generate forecast
    forecast = generate_forecast(db, user_id, metric, forecast_periods, start_date, end_date)
    
    # Get actual values for forecast period
    query = db.query(FinancialData).filter(FinancialData.user_id == user_id)
    if start_date:
        query = query.filter(FinancialData.date >= start_date)
    if end_date:
        query = query.filter(FinancialData.date <= end_date)
    
    actual_values = query.with_entities(
        func.date_trunc('month', FinancialData.date).label('month'),
        func.sum(FinancialData.amount).label('amount')
    ).group_by('month').order_by('month').all()
    
    # Calculate evaluation metrics
    actual = np.array([value[1] for value in actual_values])
    predicted = np.array([point["value"] for point in forecast.forecast_data])
    
    mae = np.mean(np.abs(actual - predicted))
    mse = np.mean((actual - predicted) ** 2)
    rmse = np.sqrt(mse)
    r2 = 1 - np.sum((actual - predicted) ** 2) / np.sum((actual - np.mean(actual)) ** 2)
    
    return ForecastEvaluation(
        metric=metric,
        forecast_periods=forecast_periods,
        actual_vs_predicted=[
            {
                "date": actual_values[i][0],
                "actual": float(actual[i]),
                "predicted": float(predicted[i])
            }
            for i in range(min(len(actual), len(predicted)))
        ],
        metrics={
            "mae": float(mae),
            "mse": float(mse),
            "rmse": float(rmse),
            "r2": float(r2)
        }
    )

def get_forecast_history(
    db: Session,
    user_id: int,
    metric: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
) -> List[ForecastHistory]:
    """Get forecast history"""
    # This is a simplified implementation
    # In a real system, you would store forecast history in a separate table
    query = db.query(FinancialData).filter(FinancialData.user_id == user_id)
    
    if start_date:
        query = query.filter(FinancialData.date >= start_date)
    if end_date:
        query = query.filter(FinancialData.date <= end_date)
    
    # Get monthly data
    monthly_data = query.with_entities(
        func.date_trunc('month', FinancialData.date).label('month'),
        func.sum(FinancialData.amount).label('amount')
    ).group_by('month').order_by('month').all()
    
    # Generate forecast history
    history = []
    for i in range(len(monthly_data) - 3):
        training_data = monthly_data[:i+3]
        actual_value = monthly_data[i+3][1]
        
        # Simple moving average forecast
        forecast_value = sum(data[1] for data in training_data) / len(training_data)
        
        history.append(ForecastHistory(
            date=monthly_data[i+3][0],
            metric=metric or "amount",
            actual_value=float(actual_value),
            forecast_value=float(forecast_value),
            error=float(actual_value - forecast_value)
        ))
    
    return history

def get_forecast_details(
    db: Session,
    user_id: int,
    metric: str,
    forecast_periods: int = 12,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
) -> ForecastDetails:
    """Get detailed forecast information"""
    # Generate forecast
    forecast = generate_forecast(db, user_id, metric, forecast_periods, start_date, end_date)
    
    # Get forecast history
    history = get_forecast_history(db, user_id, metric, start_date, end_date)
    
    # Calculate additional metrics
    forecast_values = [point["value"] for point in forecast.forecast_data]
    actual_values = [point["value"] for point in forecast.actual_data]
    
    forecast_mean = np.mean(forecast_values)
    forecast_std = np.std(forecast_values)
    actual_mean = np.mean(actual_values)
    actual_std = np.std(actual_values)
    
    return ForecastDetails(
        metric=metric,
        forecast_periods=forecast_periods,
        forecast_data=forecast.forecast_data,
        actual_data=forecast.actual_data,
        performance_metrics=forecast.performance_metrics,
        forecast_history=history,
        additional_metrics={
            "forecast_mean": float(forecast_mean),
            "forecast_std": float(forecast_std),
            "actual_mean": float(actual_mean),
            "actual_std": float(actual_std)
        }
    ) 