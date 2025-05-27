from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from app.api.deps import get_current_active_user
from app.db.session import get_db
from app.models.user import User
from app.models.financial_data import FinancialData
from app.schemas.analytics import (
    FinancialSummary,
    FinancialMetrics,
    FinancialAnomalies,
    GrowthRates,
    RevenueAnalysis,
    ExpenseAnalysis,
    ProfitabilityAnalysis,
    CashFlowAnalysis,
    PerformanceMetrics,
    CustomAnalysis
)
from app.crud import analytics as crud_analytics

router = APIRouter()

@router.get("/summary", response_model=FinancialSummary)
def get_financial_summary(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    start_date: datetime,
    end_date: datetime
) -> FinancialSummary:
    """
    Get financial summary for the specified date range.
    """
    try:
        # Получаем все финансовые данные пользователя за указанный период
        financial_data = db.query(FinancialData).filter(
            FinancialData.user_id == current_user.id,
            FinancialData.date >= start_date,
            FinancialData.date <= end_date
        ).all()

        # Рассчитываем общие показатели
        total_revenue = sum(item.amount for item in financial_data if item.data_type == "revenue")
        total_expenses = sum(item.amount for item in financial_data if item.data_type == "expense")
        total_profit = total_revenue - total_expenses

        # Группируем по категориям
        category_summary = {}
        for item in financial_data:
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
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/metrics", response_model=FinancialMetrics)
def get_financial_metrics(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    start_date: datetime,
    end_date: datetime
) -> FinancialMetrics:
    """
    Get financial metrics for the specified date range.
    """
    try:
        financial_data = db.query(FinancialData).filter(
            FinancialData.user_id == current_user.id,
            FinancialData.date >= start_date,
            FinancialData.date <= end_date
        ).all()

        # Рассчитываем метрики
        total_revenue = sum(item.amount for item in financial_data if item.data_type == "revenue")
        total_expenses = sum(item.amount for item in financial_data if item.data_type == "expense")
        
        if total_revenue == 0:
            profit_margin = 0
            expense_ratio = 0
        else:
            profit_margin = (total_revenue - total_expenses) / total_revenue
            expense_ratio = total_expenses / total_revenue

        return FinancialMetrics(
            profit_margin=profit_margin,
            expense_ratio=expense_ratio,
            revenue_growth=0.0,  # TODO: Implement growth calculation
            expense_growth=0.0   # TODO: Implement growth calculation
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/anomalies", response_model=List[FinancialAnomalies])
def get_financial_anomalies(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    start_date: datetime,
    end_date: datetime
) -> List[FinancialAnomalies]:
    """
    Get financial anomalies for the specified date range.
    """
    try:
        financial_data = db.query(FinancialData).filter(
            FinancialData.user_id == current_user.id,
            FinancialData.date >= start_date,
            FinancialData.date <= end_date
        ).all()

        # TODO: Implement anomaly detection
        return []
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/growth", response_model=GrowthRates)
def get_growth_rates(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    start_date: datetime,
    end_date: datetime
) -> GrowthRates:
    """
    Get growth rates for the specified date range.
    """
    try:
        financial_data = db.query(FinancialData).filter(
            FinancialData.user_id == current_user.id,
            FinancialData.date >= start_date,
            FinancialData.date <= end_date
        ).all()

        # TODO: Implement growth rate calculation
        return GrowthRates(
            revenue_growth=0.0,
            expense_growth=0.0,
            profit_growth=0.0
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/revenue", response_model=RevenueAnalysis)
def get_revenue_analysis(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
) -> RevenueAnalysis:
    """
    Get revenue analysis including trends and forecasts.
    """
    return crud_analytics.get_revenue_analysis(
        db=db,
        user_id=current_user.id,
        start_date=start_date,
        end_date=end_date
    )

@router.get("/expenses", response_model=ExpenseAnalysis)
def get_expense_analysis(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
) -> ExpenseAnalysis:
    """
    Get expense analysis including trends and forecasts.
    """
    return crud_analytics.get_expense_analysis(
        db=db,
        user_id=current_user.id,
        start_date=start_date,
        end_date=end_date
    )

@router.get("/profitability", response_model=ProfitabilityAnalysis)
def get_profitability_analysis(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
) -> ProfitabilityAnalysis:
    """
    Get profitability analysis including margins and trends.
    """
    return crud_analytics.get_profitability_analysis(
        db=db,
        user_id=current_user.id,
        start_date=start_date,
        end_date=end_date
    )

@router.get("/cash-flow", response_model=CashFlowAnalysis)
def get_cash_flow_analysis(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
) -> CashFlowAnalysis:
    """
    Get cash flow analysis including operating, investing, and financing activities.
    """
    return crud_analytics.get_cash_flow_analysis(
        db=db,
        user_id=current_user.id,
        start_date=start_date,
        end_date=end_date
    )

@router.get("/performance", response_model=PerformanceMetrics)
def get_performance_metrics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
) -> PerformanceMetrics:
    """
    Get key performance metrics including ROI, ROA, ROE, and other ratios.
    """
    return crud_analytics.get_performance_metrics(
        db=db,
        user_id=current_user.id,
        start_date=start_date,
        end_date=end_date
    )

@router.post("/custom", response_model=CustomAnalysis)
def get_custom_analysis(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    metrics: List[str],
    group_by: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
) -> CustomAnalysis:
    """
    Get custom analysis based on selected metrics and grouping.
    """
    return crud_analytics.get_custom_analysis(
        db=db,
        user_id=current_user.id,
        metrics=metrics,
        group_by=group_by,
        start_date=start_date,
        end_date=end_date
    ) 