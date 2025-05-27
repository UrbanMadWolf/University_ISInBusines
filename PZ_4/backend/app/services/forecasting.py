from typing import List, Dict, Any
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler

from app.models.financial_data import FinancialData
from app.schemas.forecasting import (
    ForecastRequest,
    ForecastResponse,
    ForecastPoint,
    ForecastEvaluation
)

class ForecastingService:
    def __init__(self, db: Session):
        self.db = db
        self.scaler = StandardScaler()

    def prepare_data(
        self,
        data: List[FinancialData],
        metric: str
    ) -> tuple[np.ndarray, np.ndarray]:
        """Prepare data for forecasting"""
        # Group data by date
        daily_data = {}
        for item in data:
            if item.data_type == metric:
                date_str = item.date.strftime("%Y-%m-%d")
                if date_str not in daily_data:
                    daily_data[date_str] = []
                daily_data[date_str].append(item.amount)

        # Calculate daily totals
        dates = sorted(daily_data.keys())
        values = [sum(daily_data[date]) for date in dates]

        # Convert dates to numeric features
        X = np.array(range(len(dates))).reshape(-1, 1)
        y = np.array(values)

        return X, y

    def generate_forecast(
        self,
        user_id: int,
        request: ForecastRequest
    ) -> ForecastResponse:
        """Generate financial forecast"""
        # Get historical data
        historical_data = self.db.query(FinancialData).filter(
            FinancialData.user_id == user_id,
            FinancialData.date >= request.start_date,
            FinancialData.date <= request.end_date
        ).all()

        forecasts = {}
        confidence_intervals = {}

        for metric in request.target_metrics:
            X, y = self.prepare_data(historical_data, metric)
            if len(X) < 2:
                continue

            # Scale the data
            X_scaled = self.scaler.fit_transform(X)
            y_scaled = self.scaler.fit_transform(y.reshape(-1, 1))

            # Train the model
            model = LinearRegression()
            model.fit(X_scaled, y_scaled)

            # Generate forecast
            future_X = np.array(range(len(X), len(X) + request.forecast_period)).reshape(-1, 1)
            future_X_scaled = self.scaler.transform(future_X)
            forecast_scaled = model.predict(future_X_scaled)
            forecast = self.scaler.inverse_transform(forecast_scaled)

            # Calculate confidence intervals
            y_pred = model.predict(X_scaled)
            mse = np.mean((y_scaled - y_pred) ** 2)
            std = np.sqrt(mse)

            forecast_points = []
            for i, (date, value) in enumerate(zip(
                [request.end_date + timedelta(days=x+1) for x in range(request.forecast_period)],
                forecast
            )):
                confidence = 1.96 * std  # 95% confidence interval
                forecast_points.append(
                    ForecastPoint(
                        date=date,
                        value=float(value[0]),
                        lower_bound=float(value[0] - confidence),
                        upper_bound=float(value[0] + confidence)
                    )
                )

            forecasts[metric] = forecast_points
            confidence_intervals[metric] = float(confidence[0])

        return ForecastResponse(
            forecast_period=request.forecast_period,
            revenue_forecast=forecasts.get("revenue", []),
            expense_forecast=forecasts.get("expense", []),
            profit_forecast=forecasts.get("profit", []),
            confidence_intervals=confidence_intervals
        )

    def evaluate_forecast(
        self,
        user_id: int,
        request: ForecastRequest
    ) -> ForecastEvaluation:
        """Evaluate forecast quality"""
        # Get historical data
        historical_data = self.db.query(FinancialData).filter(
            FinancialData.user_id == user_id,
            FinancialData.date >= request.start_date,
            FinancialData.date <= request.end_date
        ).all()

        # Split data into training and testing sets
        split_point = int(len(historical_data) * 0.8)
        train_data = historical_data[:split_point]
        test_data = historical_data[split_point:]

        # Generate forecast for test period
        test_request = ForecastRequest(
            start_date=request.start_date,
            end_date=train_data[-1].date,
            forecast_period=len(test_data),
            target_metrics=request.target_metrics,
            confidence_level=request.confidence_level
        )
        forecast = self.generate_forecast(user_id, test_request)

        # Calculate evaluation metrics
        actual_values = []
        predicted_values = []

        for metric in request.target_metrics:
            actual = [item.amount for item in test_data if item.data_type == metric]
            predicted = [point.value for point in forecast.revenue_forecast]
            
            if len(actual) == len(predicted):
                actual_values.extend(actual)
                predicted_values.extend(predicted)

        if not actual_values or not predicted_values:
            return ForecastEvaluation(
                mae=0.0,
                mse=0.0,
                rmse=0.0,
                r2_score=0.0
            )

        # Calculate metrics
        mae = np.mean(np.abs(np.array(actual_values) - np.array(predicted_values)))
        mse = np.mean((np.array(actual_values) - np.array(predicted_values)) ** 2)
        rmse = np.sqrt(mse)
        
        # Calculate R-squared
        ss_total = np.sum((np.array(actual_values) - np.mean(actual_values)) ** 2)
        ss_residual = np.sum((np.array(actual_values) - np.array(predicted_values)) ** 2)
        r2_score = 1 - (ss_residual / ss_total) if ss_total != 0 else 0

        return ForecastEvaluation(
            mae=float(mae),
            mse=float(mse),
            rmse=float(rmse),
            r2_score=float(r2_score)
        ) 