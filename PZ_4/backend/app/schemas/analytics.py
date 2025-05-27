from typing import Dict, List, Optional
from pydantic import BaseModel
from datetime import datetime

class CategorySummary(BaseModel):
    revenue: float
    expenses: float
    profit: float

class FinancialSummary(BaseModel):
    total_revenue: float
    total_expenses: float
    total_profit: float
    category_summary: Dict[str, CategorySummary]

class FinancialMetrics(BaseModel):
    profit_margin: float
    expense_ratio: float
    revenue_growth: float
    expense_growth: float

class FinancialAnomalies(BaseModel):
    date: str
    metric: str
    value: float
    expected_value: float
    deviation: float
    description: str

class GrowthRates(BaseModel):
    revenue_growth: float
    expense_growth: float
    profit_growth: float

class TrendPoint(BaseModel):
    month: datetime
    amount: float

class RevenueAnalysis(BaseModel):
    total_revenue: float
    revenue_by_category: Dict[str, float]
    revenue_trend: List[TrendPoint]
    revenue_forecast: List[TrendPoint]

class ExpenseAnalysis(BaseModel):
    total_expenses: float
    expenses_by_category: Dict[str, float]
    expense_trend: List[TrendPoint]
    expense_forecast: List[TrendPoint]

class ProfitabilityAnalysis(BaseModel):
    net_profit: float
    profit_margin: float
    profit_by_category: Dict[str, float]
    profit_trend: List[TrendPoint]

class CashFlowAnalysis(BaseModel):
    net_cash_flow: float
    operating_cash_flow: float
    investing_cash_flow: float
    financing_cash_flow: float
    cash_flow_trend: List[TrendPoint]

class PerformanceMetrics(BaseModel):
    roi: float  # Return on Investment
    roa: float  # Return on Assets
    roe: float  # Return on Equity
    current_ratio: float
    debt_to_equity: float
    asset_turnover: float

class CustomAnalysis(BaseModel):
    metrics: Dict[str, float]
    grouped_data: Optional[Dict[str, Dict[str, float]]] = None 