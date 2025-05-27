import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional

def create_test_revenue_analysis(
    user_id: int,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
) -> Dict:
    """Create test revenue analysis data"""
    if start_date is None:
        start_date = datetime.now() - timedelta(days=30)
    if end_date is None:
        end_date = datetime.now()
    
    # Generate revenue by category
    categories = ["sales", "services", "investments", "other"]
    revenue_by_category = {
        category: round(random.uniform(1000.0, 10000.0), 2)
        for category in categories
    }
    total_revenue = sum(revenue_by_category.values())
    
    # Generate revenue trend
    revenue_trend = []
    current_date = start_date
    while current_date <= end_date:
        revenue_trend.append({
            "date": current_date.isoformat(),
            "amount": round(random.uniform(total_revenue * 0.8, total_revenue * 1.2) / 30, 2)
        })
        current_date += timedelta(days=1)
    
    # Generate revenue forecast
    revenue_forecast = []
    forecast_date = end_date + timedelta(days=1)
    for _ in range(30):  # 30-day forecast
        revenue_forecast.append({
            "date": forecast_date.isoformat(),
            "amount": round(random.uniform(total_revenue * 0.8, total_revenue * 1.2) / 30, 2),
            "confidence_lower": round(random.uniform(total_revenue * 0.7, total_revenue * 0.9) / 30, 2),
            "confidence_upper": round(random.uniform(total_revenue * 1.1, total_revenue * 1.3) / 30, 2)
        })
        forecast_date += timedelta(days=1)
    
    return {
        "total_revenue": total_revenue,
        "revenue_by_category": revenue_by_category,
        "revenue_trend": revenue_trend,
        "revenue_forecast": revenue_forecast
    }

def create_test_expense_analysis(
    user_id: int,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
) -> Dict:
    """Create test expense analysis data"""
    if start_date is None:
        start_date = datetime.now() - timedelta(days=30)
    if end_date is None:
        end_date = datetime.now()
    
    # Generate expenses by category
    categories = ["operating", "personnel", "marketing", "utilities", "other"]
    expenses_by_category = {
        category: round(random.uniform(500.0, 5000.0), 2)
        for category in categories
    }
    total_expenses = sum(expenses_by_category.values())
    
    # Generate expense trend
    expense_trend = []
    current_date = start_date
    while current_date <= end_date:
        expense_trend.append({
            "date": current_date.isoformat(),
            "amount": round(random.uniform(total_expenses * 0.8, total_expenses * 1.2) / 30, 2)
        })
        current_date += timedelta(days=1)
    
    # Generate expense forecast
    expense_forecast = []
    forecast_date = end_date + timedelta(days=1)
    for _ in range(30):  # 30-day forecast
        expense_forecast.append({
            "date": forecast_date.isoformat(),
            "amount": round(random.uniform(total_expenses * 0.8, total_expenses * 1.2) / 30, 2),
            "confidence_lower": round(random.uniform(total_expenses * 0.7, total_expenses * 0.9) / 30, 2),
            "confidence_upper": round(random.uniform(total_expenses * 1.1, total_expenses * 1.3) / 30, 2)
        })
        forecast_date += timedelta(days=1)
    
    return {
        "total_expenses": total_expenses,
        "expenses_by_category": expenses_by_category,
        "expense_trend": expense_trend,
        "expense_forecast": expense_forecast
    }

def create_test_profitability_analysis(
    user_id: int,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
) -> Dict:
    """Create test profitability analysis data"""
    revenue_data = create_test_revenue_analysis(user_id, start_date, end_date)
    expense_data = create_test_expense_analysis(user_id, start_date, end_date)
    
    net_profit = revenue_data["total_revenue"] - expense_data["total_expenses"]
    profit_margin = (net_profit / revenue_data["total_revenue"] * 100) if revenue_data["total_revenue"] > 0 else 0
    
    # Generate profit trend
    profit_trend = []
    for rev, exp in zip(revenue_data["revenue_trend"], expense_data["expense_trend"]):
        profit_trend.append({
            "date": rev["date"],
            "amount": rev["amount"] - exp["amount"]
        })
    
    # Generate profit by category
    profit_by_category = {}
    for category in revenue_data["revenue_by_category"]:
        if category in expense_data["expenses_by_category"]:
            profit_by_category[category] = (
                revenue_data["revenue_by_category"][category] -
                expense_data["expenses_by_category"][category]
            )
    
    return {
        "net_profit": net_profit,
        "profit_margin": profit_margin,
        "profit_trend": profit_trend,
        "profit_by_category": profit_by_category
    }

def create_test_cash_flow_analysis(
    user_id: int,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
) -> Dict:
    """Create test cash flow analysis data"""
    if start_date is None:
        start_date = datetime.now() - timedelta(days=30)
    if end_date is None:
        end_date = datetime.now()
    
    # Generate cash flows
    operating_cash_flow = round(random.uniform(10000.0, 50000.0), 2)
    investing_cash_flow = round(random.uniform(-20000.0, -5000.0), 2)
    financing_cash_flow = round(random.uniform(-15000.0, 15000.0), 2)
    net_cash_flow = operating_cash_flow + investing_cash_flow + financing_cash_flow
    
    # Generate cash flow trend
    cash_flow_trend = []
    current_date = start_date
    while current_date <= end_date:
        cash_flow_trend.append({
            "date": current_date.isoformat(),
            "operating": round(random.uniform(operating_cash_flow * 0.8, operating_cash_flow * 1.2) / 30, 2),
            "investing": round(random.uniform(investing_cash_flow * 0.8, investing_cash_flow * 1.2) / 30, 2),
            "financing": round(random.uniform(financing_cash_flow * 0.8, financing_cash_flow * 1.2) / 30, 2)
        })
        current_date += timedelta(days=1)
    
    return {
        "net_cash_flow": net_cash_flow,
        "operating_cash_flow": operating_cash_flow,
        "investing_cash_flow": investing_cash_flow,
        "financing_cash_flow": financing_cash_flow,
        "cash_flow_trend": cash_flow_trend
    }

def create_test_performance_metrics(
    user_id: int,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
) -> Dict:
    """Create test performance metrics data"""
    # Generate financial ratios
    roi = round(random.uniform(0.05, 0.25), 4)  # 5% to 25%
    roa = round(random.uniform(0.03, 0.15), 4)  # 3% to 15%
    roe = round(random.uniform(0.08, 0.30), 4)  # 8% to 30%
    current_ratio = round(random.uniform(1.0, 3.0), 2)
    debt_to_equity = round(random.uniform(0.5, 2.0), 2)
    asset_turnover = round(random.uniform(0.5, 2.0), 2)
    
    return {
        "roi": roi,
        "roa": roa,
        "roe": roe,
        "current_ratio": current_ratio,
        "debt_to_equity": debt_to_equity,
        "asset_turnover": asset_turnover
    } 