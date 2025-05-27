from typing import Dict, List, Optional
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func
from scipy import stats
from ..models.financial import FinancialData, FinancialMetric
from ..schemas.financial import FinancialDataCreate, FinancialMetricCreate
from app.schemas.analytics import (
    FinancialSummary,
    FinancialMetrics,
    FinancialAnomalies,
    GrowthRates
)

class AnalyticsService:
    def __init__(self, db: Session):
        self.db = db

    def get_financial_summary(
        self,
        user_id: int,
        start_date: datetime,
        end_date: datetime
    ) -> FinancialSummary:
        """Get financial summary for the period"""
        data = self.db.query(FinancialData).filter(
            FinancialData.user_id == user_id,
            FinancialData.date >= start_date,
            FinancialData.date <= end_date
        ).all()

        total_revenue = sum(item.amount for item in data if item.data_type == "revenue")
        total_expenses = sum(item.amount for item in data if item.data_type == "expense")
        total_profit = total_revenue - total_expenses

        category_summary = {}
        for item in data:
            if item.category not in category_summary:
                category_summary[item.category] = {
                    "revenue": 0,
                    "expenses": 0,
                    "profit": 0
                }
            if item.data_type == "revenue":
                category_summary[item.category]["revenue"] += item.amount
            elif item.data_type == "expense":
                category_summary[item.category]["expenses"] += item.amount
            category_summary[item.category]["profit"] = (
                category_summary[item.category]["revenue"] -
                category_summary[item.category]["expenses"]
            )

        return FinancialSummary(
            total_revenue=total_revenue,
            total_expenses=total_expenses,
            total_profit=total_profit,
            category_summary=category_summary
        )

    def get_financial_metrics(
        self,
        user_id: int,
        start_date: datetime,
        end_date: datetime
    ) -> FinancialMetrics:
        """Calculate financial metrics"""
        data = self.db.query(FinancialData).filter(
            FinancialData.user_id == user_id,
            FinancialData.date >= start_date,
            FinancialData.date <= end_date
        ).all()

        total_revenue = sum(item.amount for item in data if item.data_type == "revenue")
        total_expenses = sum(item.amount for item in data if item.data_type == "expense")
        
        if total_revenue == 0:
            profit_margin = 0
            expense_ratio = 0
        else:
            profit_margin = (total_revenue - total_expenses) / total_revenue
            expense_ratio = total_expenses / total_revenue

        # Calculate growth rates
        previous_period_start = start_date - (end_date - start_date)
        previous_data = self.db.query(FinancialData).filter(
            FinancialData.user_id == user_id,
            FinancialData.date >= previous_period_start,
            FinancialData.date < start_date
        ).all()

        prev_revenue = sum(item.amount for item in previous_data if item.data_type == "revenue")
        prev_expenses = sum(item.amount for item in previous_data if item.data_type == "expense")

        if prev_revenue == 0:
            revenue_growth = 0
        else:
            revenue_growth = (total_revenue - prev_revenue) / prev_revenue

        if prev_expenses == 0:
            expense_growth = 0
        else:
            expense_growth = (total_expenses - prev_expenses) / prev_expenses

        return FinancialMetrics(
            profit_margin=profit_margin,
            expense_ratio=expense_ratio,
            revenue_growth=revenue_growth,
            expense_growth=expense_growth
        )

    def detect_anomalies(
        self,
        user_id: int,
        start_date: datetime,
        end_date: datetime
    ) -> List[FinancialAnomalies]:
        """Detect anomalies in financial data"""
        data = self.db.query(FinancialData).filter(
            FinancialData.user_id == user_id,
            FinancialData.date >= start_date,
            FinancialData.date <= end_date
        ).all()

        anomalies = []
        
        # Group data by date and type
        daily_data = {}
        for item in data:
            date_str = item.date.strftime("%Y-%m-%d")
            if date_str not in daily_data:
                daily_data[date_str] = {"revenue": [], "expense": []}
            daily_data[date_str][item.data_type].append(item.amount)

        # Calculate daily totals
        daily_totals = {
            date: {
                "revenue": sum(amounts),
                "expense": sum(amounts)
            }
            for date, amounts in daily_data.items()
        }

        # Detect anomalies using Z-score
        for metric in ["revenue", "expense"]:
            values = [totals[metric] for totals in daily_totals.values()]
            if len(values) < 2:
                continue

            mean = np.mean(values)
            std = np.std(values)
            if std == 0:
                continue

            for date, totals in daily_totals.items():
                z_score = (totals[metric] - mean) / std
                if abs(z_score) > 2:  # Threshold for anomaly
                    anomalies.append(
                        FinancialAnomalies(
                            date=date,
                            metric=metric,
                            value=totals[metric],
                            expected_value=mean,
                            deviation=z_score,
                            description=f"Unusual {metric} value detected"
                        )
                    )

        return anomalies

    def calculate_growth_rates(
        self,
        user_id: int,
        start_date: datetime,
        end_date: datetime
    ) -> GrowthRates:
        """Calculate growth rates for financial metrics"""
        current_data = self.db.query(FinancialData).filter(
            FinancialData.user_id == user_id,
            FinancialData.date >= start_date,
            FinancialData.date <= end_date
        ).all()

        period_length = end_date - start_date
        previous_period_start = start_date - period_length
        previous_data = self.db.query(FinancialData).filter(
            FinancialData.user_id == user_id,
            FinancialData.date >= previous_period_start,
            FinancialData.date < start_date
        ).all()

        # Calculate current period totals
        current_revenue = sum(item.amount for item in current_data if item.data_type == "revenue")
        current_expenses = sum(item.amount for item in current_data if item.data_type == "expense")
        current_profit = current_revenue - current_expenses

        # Calculate previous period totals
        prev_revenue = sum(item.amount for item in previous_data if item.data_type == "revenue")
        prev_expenses = sum(item.amount for item in previous_data if item.data_type == "expense")
        prev_profit = prev_revenue - prev_expenses

        # Calculate growth rates
        revenue_growth = (current_revenue - prev_revenue) / prev_revenue if prev_revenue != 0 else 0
        expense_growth = (current_expenses - prev_expenses) / prev_expenses if prev_expenses != 0 else 0
        profit_growth = (current_profit - prev_profit) / prev_profit if prev_profit != 0 else 0

        return GrowthRates(
            revenue_growth=revenue_growth,
            expense_growth=expense_growth,
            profit_growth=profit_growth
        )

    def calculate_financial_summary(self, start_date: datetime, end_date: datetime) -> Dict:
        """
        Расчет сводных финансовых показателей за период
        """
        # Получаем данные из БД
        financial_data = self.db.query(FinancialData).filter(
            FinancialData.date.between(start_date, end_date)
        ).all()

        # Преобразуем в DataFrame для удобства анализа
        df = pd.DataFrame([{
            'date': data.date,
            'revenue': data.revenue,
            'expenses': data.expenses,
            'profit': data.profit,
            'category': data.category
        } for data in financial_data])

        if df.empty:
            return {
                "total_revenue": 0,
                "total_expenses": 0,
                "net_profit": 0,
                "profit_margin": 0,
                "category_breakdown": {}
            }

        # Рассчитываем основные показатели
        total_revenue = df['revenue'].sum()
        total_expenses = df['expenses'].sum()
        net_profit = df['profit'].sum()
        profit_margin = net_profit / total_revenue if total_revenue > 0 else 0

        # Анализ по категориям
        category_breakdown = df.groupby('category').agg({
            'revenue': 'sum',
            'expenses': 'sum',
            'profit': 'sum'
        }).to_dict('index')

        return {
            "total_revenue": total_revenue,
            "total_expenses": total_expenses,
            "net_profit": net_profit,
            "profit_margin": profit_margin,
            "category_breakdown": category_breakdown
        }

    def calculate_financial_metrics(self, start_date: datetime, end_date: datetime) -> Dict:
        """
        Расчет ключевых финансовых метрик
        """
        # Получаем данные из БД
        financial_data = self.db.query(FinancialData).filter(
            FinancialData.date.between(start_date, end_date)
        ).all()

        df = pd.DataFrame([{
            'date': data.date,
            'revenue': data.revenue,
            'expenses': data.expenses,
            'profit': data.profit
        } for data in financial_data])

        if df.empty:
            return {
                "roi": 0,
                "current_ratio": 0,
                "debt_to_equity": 0,
                "trends": {}
            }

        # Рассчитываем ROI (Return on Investment)
        total_investment = df['expenses'].sum()
        roi = df['profit'].sum() / total_investment if total_investment > 0 else 0

        # Рассчитываем текущий коэффициент (Current Ratio)
        # Предполагаем, что текущие активы = выручка, текущие обязательства = расходы
        current_ratio = df['revenue'].sum() / df['expenses'].sum() if df['expenses'].sum() > 0 else 0

        # Рассчитываем коэффициент долга к собственному капиталу (Debt to Equity)
        # Упрощенный расчет: долг = расходы, собственный капитал = прибыль
        debt_to_equity = df['expenses'].sum() / df['profit'].sum() if df['profit'].sum() > 0 else 0

        # Анализ трендов
        df['month'] = df['date'].dt.to_period('M')
        monthly_trends = df.groupby('month').agg({
            'revenue': 'sum',
            'expenses': 'sum',
            'profit': 'sum'
        }).to_dict('index')

        return {
            "roi": roi,
            "current_ratio": current_ratio,
            "debt_to_equity": debt_to_equity,
            "trends": monthly_trends
        }

    def detect_anomalies(self, start_date: datetime, end_date: datetime) -> List[Dict]:
        """
        Выявление аномалий в финансовых данных
        """
        # Получаем данные из БД
        financial_data = self.db.query(FinancialData).filter(
            FinancialData.date.between(start_date, end_date)
        ).all()

        df = pd.DataFrame([{
            'date': data.date,
            'revenue': data.revenue,
            'expenses': data.expenses,
            'profit': data.profit
        } for data in financial_data])

        if df.empty:
            return []

        anomalies = []

        # Выявляем аномалии в выручке
        revenue_mean = df['revenue'].mean()
        revenue_std = df['revenue'].std()
        revenue_anomalies = df[abs(df['revenue'] - revenue_mean) > 2 * revenue_std]

        for _, row in revenue_anomalies.iterrows():
            anomalies.append({
                "date": row['date'],
                "metric": "revenue",
                "value": row['revenue'],
                "expected_range": [revenue_mean - 2 * revenue_std, revenue_mean + 2 * revenue_std],
                "deviation": (row['revenue'] - revenue_mean) / revenue_std
            })

        # Выявляем аномалии в расходах
        expenses_mean = df['expenses'].mean()
        expenses_std = df['expenses'].std()
        expenses_anomalies = df[abs(df['expenses'] - expenses_mean) > 2 * expenses_std]

        for _, row in expenses_anomalies.iterrows():
            anomalies.append({
                "date": row['date'],
                "metric": "expenses",
                "value": row['expenses'],
                "expected_range": [expenses_mean - 2 * expenses_std, expenses_mean + 2 * expenses_std],
                "deviation": (row['expenses'] - expenses_mean) / expenses_std
            })

        return anomalies

    def calculate_growth_rates(self, start_date: datetime, end_date: datetime) -> Dict:
        """
        Расчет темпов роста финансовых показателей
        """
        # Получаем данные из БД
        financial_data = self.db.query(FinancialData).filter(
            FinancialData.date.between(start_date, end_date)
        ).all()

        df = pd.DataFrame([{
            'date': data.date,
            'revenue': data.revenue,
            'expenses': data.expenses,
            'profit': data.profit
        } for data in financial_data])

        if df.empty:
            return {
                "revenue_growth": 0,
                "expenses_growth": 0,
                "profit_growth": 0
            }

        # Сортируем по дате
        df = df.sort_values('date')

        # Рассчитываем темпы роста
        revenue_growth = (df['revenue'].iloc[-1] / df['revenue'].iloc[0] - 1) * 100
        expenses_growth = (df['expenses'].iloc[-1] / df['expenses'].iloc[0] - 1) * 100
        profit_growth = (df['profit'].iloc[-1] / df['profit'].iloc[0] - 1) * 100

        return {
            "revenue_growth": revenue_growth,
            "expenses_growth": expenses_growth,
            "profit_growth": profit_growth
        } 