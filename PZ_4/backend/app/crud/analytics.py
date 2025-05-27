from typing import List, Optional, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.financial_data import FinancialData
from app.schemas.analytics import (
    RevenueAnalysis,
    ExpenseAnalysis,
    ProfitabilityAnalysis,
    CashFlowAnalysis,
    PerformanceMetrics,
    CustomAnalysis
)

def get_revenue_analysis(
    db: Session,
    user_id: int,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
) -> RevenueAnalysis:
    """Get revenue analysis including trends and forecasts"""
    query = db.query(FinancialData).filter(
        FinancialData.user_id == user_id,
        FinancialData.type == "revenue"
    )
    
    if start_date:
        query = query.filter(FinancialData.date >= start_date)
    if end_date:
        query = query.filter(FinancialData.date <= end_date)
    
    # Calculate total revenue
    total_revenue = query.with_entities(
        func.sum(FinancialData.amount)
    ).scalar() or 0
    
    # Get revenue by category
    revenue_by_category = {}
    for category in db.query(FinancialData.category).distinct():
        category_revenue = query.filter(
            FinancialData.category == category[0]
        ).with_entities(
            func.sum(FinancialData.amount)
        ).scalar() or 0
        revenue_by_category[category[0]] = category_revenue
    
    # Get revenue trend
    revenue_trend = []
    monthly_data = query.with_entities(
        func.date_trunc('month', FinancialData.date).label('month'),
        func.sum(FinancialData.amount).label('amount')
    ).group_by('month').order_by('month').all()
    
    for month, amount in monthly_data:
        revenue_trend.append({
            "month": month,
            "amount": amount
        })
    
    # Simple revenue forecast (using moving average)
    forecast = []
    if len(revenue_trend) >= 3:
        window_size = 3
        for i in range(len(revenue_trend) - window_size + 1):
            window = revenue_trend[i:i + window_size]
            avg = sum(item["amount"] for item in window) / window_size
            forecast.append({
                "month": revenue_trend[i + window_size - 1]["month"],
                "amount": avg
            })
    
    return RevenueAnalysis(
        total_revenue=total_revenue,
        revenue_by_category=revenue_by_category,
        revenue_trend=revenue_trend,
        revenue_forecast=forecast
    )

def get_expense_analysis(
    db: Session,
    user_id: int,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
) -> ExpenseAnalysis:
    """Get expense analysis including trends and forecasts"""
    query = db.query(FinancialData).filter(
        FinancialData.user_id == user_id,
        FinancialData.type == "expense"
    )
    
    if start_date:
        query = query.filter(FinancialData.date >= start_date)
    if end_date:
        query = query.filter(FinancialData.date <= end_date)
    
    # Calculate total expenses
    total_expenses = query.with_entities(
        func.sum(FinancialData.amount)
    ).scalar() or 0
    
    # Get expenses by category
    expenses_by_category = {}
    for category in db.query(FinancialData.category).distinct():
        category_expenses = query.filter(
            FinancialData.category == category[0]
        ).with_entities(
            func.sum(FinancialData.amount)
        ).scalar() or 0
        expenses_by_category[category[0]] = category_expenses
    
    # Get expense trend
    expense_trend = []
    monthly_data = query.with_entities(
        func.date_trunc('month', FinancialData.date).label('month'),
        func.sum(FinancialData.amount).label('amount')
    ).group_by('month').order_by('month').all()
    
    for month, amount in monthly_data:
        expense_trend.append({
            "month": month,
            "amount": amount
        })
    
    # Simple expense forecast (using moving average)
    forecast = []
    if len(expense_trend) >= 3:
        window_size = 3
        for i in range(len(expense_trend) - window_size + 1):
            window = expense_trend[i:i + window_size]
            avg = sum(item["amount"] for item in window) / window_size
            forecast.append({
                "month": expense_trend[i + window_size - 1]["month"],
                "amount": avg
            })
    
    return ExpenseAnalysis(
        total_expenses=total_expenses,
        expenses_by_category=expenses_by_category,
        expense_trend=expense_trend,
        expense_forecast=forecast
    )

def get_profitability_analysis(
    db: Session,
    user_id: int,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
) -> ProfitabilityAnalysis:
    """Get profitability analysis including margins and trends"""
    revenue_analysis = get_revenue_analysis(db, user_id, start_date, end_date)
    expense_analysis = get_expense_analysis(db, user_id, start_date, end_date)
    
    net_profit = revenue_analysis.total_revenue - expense_analysis.total_expenses
    profit_margin = (net_profit / revenue_analysis.total_revenue * 100) if revenue_analysis.total_revenue > 0 else 0
    
    # Calculate profit by category
    profit_by_category = {}
    for category in set(revenue_analysis.revenue_by_category.keys()) | set(expense_analysis.expenses_by_category.keys()):
        revenue = revenue_analysis.revenue_by_category.get(category, 0)
        expenses = expense_analysis.expenses_by_category.get(category, 0)
        profit_by_category[category] = revenue - expenses
    
    # Calculate profit trend
    profit_trend = []
    for i in range(len(revenue_analysis.revenue_trend)):
        if i < len(expense_analysis.expense_trend):
            profit_trend.append({
                "month": revenue_analysis.revenue_trend[i]["month"],
                "amount": revenue_analysis.revenue_trend[i]["amount"] - expense_analysis.expense_trend[i]["amount"]
            })
    
    return ProfitabilityAnalysis(
        net_profit=net_profit,
        profit_margin=profit_margin,
        profit_by_category=profit_by_category,
        profit_trend=profit_trend
    )

def get_cash_flow_analysis(
    db: Session,
    user_id: int,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
) -> CashFlowAnalysis:
    """Get cash flow analysis including operating, investing, and financing activities"""
    query = db.query(FinancialData).filter(FinancialData.user_id == user_id)
    
    if start_date:
        query = query.filter(FinancialData.date >= start_date)
    if end_date:
        query = query.filter(FinancialData.date <= end_date)
    
    # Calculate operating cash flow
    operating_cash_flow = query.filter(
        FinancialData.type.in_(["revenue", "expense"])
    ).with_entities(
        func.sum(FinancialData.amount)
    ).scalar() or 0
    
    # Calculate investing cash flow
    investing_cash_flow = query.filter(
        FinancialData.category == "investment"
    ).with_entities(
        func.sum(FinancialData.amount)
    ).scalar() or 0
    
    # Calculate financing cash flow
    financing_cash_flow = query.filter(
        FinancialData.category == "financing"
    ).with_entities(
        func.sum(FinancialData.amount)
    ).scalar() or 0
    
    # Calculate net cash flow
    net_cash_flow = operating_cash_flow + investing_cash_flow + financing_cash_flow
    
    # Get cash flow trend
    cash_flow_trend = []
    monthly_data = query.with_entities(
        func.date_trunc('month', FinancialData.date).label('month'),
        func.sum(FinancialData.amount).label('amount')
    ).group_by('month').order_by('month').all()
    
    for month, amount in monthly_data:
        cash_flow_trend.append({
            "month": month,
            "amount": amount
        })
    
    return CashFlowAnalysis(
        net_cash_flow=net_cash_flow,
        operating_cash_flow=operating_cash_flow,
        investing_cash_flow=investing_cash_flow,
        financing_cash_flow=financing_cash_flow,
        cash_flow_trend=cash_flow_trend
    )

def get_performance_metrics(
    db: Session,
    user_id: int,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
) -> PerformanceMetrics:
    """Get key performance metrics including ROI, ROA, ROE, and other ratios"""
    # Get financial data
    revenue_analysis = get_revenue_analysis(db, user_id, start_date, end_date)
    expense_analysis = get_expense_analysis(db, user_id, start_date, end_date)
    cash_flow_analysis = get_cash_flow_analysis(db, user_id, start_date, end_date)
    
    # Calculate basic metrics
    total_revenue = revenue_analysis.total_revenue
    total_expenses = expense_analysis.total_expenses
    net_profit = total_revenue - total_expenses
    
    # Calculate ratios
    # Note: These are simplified calculations. In a real system, you would need more detailed financial data
    roi = (net_profit / total_expenses * 100) if total_expenses > 0 else 0
    roa = (net_profit / total_revenue * 100) if total_revenue > 0 else 0
    roe = (net_profit / total_revenue * 100) if total_revenue > 0 else 0  # Simplified ROE
    current_ratio = (total_revenue / total_expenses) if total_expenses > 0 else 0
    debt_to_equity = (total_expenses / total_revenue) if total_revenue > 0 else 0
    asset_turnover = (total_revenue / total_expenses) if total_expenses > 0 else 0
    
    return PerformanceMetrics(
        roi=roi,
        roa=roa,
        roe=roe,
        current_ratio=current_ratio,
        debt_to_equity=debt_to_equity,
        asset_turnover=asset_turnover
    )

def get_custom_analysis(
    db: Session,
    user_id: int,
    metrics: List[str],
    group_by: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
) -> CustomAnalysis:
    """Get custom analysis based on selected metrics and grouping"""
    query = db.query(FinancialData).filter(FinancialData.user_id == user_id)
    
    if start_date:
        query = query.filter(FinancialData.date >= start_date)
    if end_date:
        query = query.filter(FinancialData.date <= end_date)
    
    # Get data based on selected metrics
    data = {}
    for metric in metrics:
        if metric == "revenue":
            data["revenue"] = query.filter(
                FinancialData.type == "revenue"
            ).with_entities(
                func.sum(FinancialData.amount)
            ).scalar() or 0
        elif metric == "expenses":
            data["expenses"] = query.filter(
                FinancialData.type == "expense"
            ).with_entities(
                func.sum(FinancialData.amount)
            ).scalar() or 0
        elif metric == "profit":
            revenue = query.filter(
                FinancialData.type == "revenue"
            ).with_entities(
                func.sum(FinancialData.amount)
            ).scalar() or 0
            expenses = query.filter(
                FinancialData.type == "expense"
            ).with_entities(
                func.sum(FinancialData.amount)
            ).scalar() or 0
            data["profit"] = revenue - expenses
    
    # Group data if requested
    grouped_data = {}
    if group_by:
        if group_by == "category":
            for category in db.query(FinancialData.category).distinct():
                category_data = {}
                for metric in metrics:
                    if metric == "revenue":
                        category_data["revenue"] = query.filter(
                            FinancialData.category == category[0],
                            FinancialData.type == "revenue"
                        ).with_entities(
                            func.sum(FinancialData.amount)
                        ).scalar() or 0
                    elif metric == "expenses":
                        category_data["expenses"] = query.filter(
                            FinancialData.category == category[0],
                            FinancialData.type == "expense"
                        ).with_entities(
                            func.sum(FinancialData.amount)
                        ).scalar() or 0
                    elif metric == "profit":
                        revenue = query.filter(
                            FinancialData.category == category[0],
                            FinancialData.type == "revenue"
                        ).with_entities(
                            func.sum(FinancialData.amount)
                        ).scalar() or 0
                        expenses = query.filter(
                            FinancialData.category == category[0],
                            FinancialData.type == "expense"
                        ).with_entities(
                            func.sum(FinancialData.amount)
                        ).scalar() or 0
                        category_data["profit"] = revenue - expenses
                grouped_data[category[0]] = category_data
        elif group_by == "month":
            monthly_data = query.with_entities(
                func.date_trunc('month', FinancialData.date).label('month')
            ).distinct().order_by('month').all()
            
            for month in monthly_data:
                month_data = {}
                for metric in metrics:
                    if metric == "revenue":
                        month_data["revenue"] = query.filter(
                            func.date_trunc('month', FinancialData.date) == month[0],
                            FinancialData.type == "revenue"
                        ).with_entities(
                            func.sum(FinancialData.amount)
                        ).scalar() or 0
                    elif metric == "expenses":
                        month_data["expenses"] = query.filter(
                            func.date_trunc('month', FinancialData.date) == month[0],
                            FinancialData.type == "expense"
                        ).with_entities(
                            func.sum(FinancialData.amount)
                        ).scalar() or 0
                    elif metric == "profit":
                        revenue = query.filter(
                            func.date_trunc('month', FinancialData.date) == month[0],
                            FinancialData.type == "revenue"
                        ).with_entities(
                            func.sum(FinancialData.amount)
                        ).scalar() or 0
                        expenses = query.filter(
                            func.date_trunc('month', FinancialData.date) == month[0],
                            FinancialData.type == "expense"
                        ).with_entities(
                            func.sum(FinancialData.amount)
                        ).scalar() or 0
                        month_data["profit"] = revenue - expenses
                grouped_data[month[0].isoformat()] = month_data
    
    return CustomAnalysis(
        metrics=data,
        grouped_data=grouped_data if group_by else None
    ) 