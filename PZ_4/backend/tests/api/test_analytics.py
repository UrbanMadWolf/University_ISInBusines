from datetime import datetime, timedelta
from typing import Dict, List

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.tests.utils.financial_utils import create_test_financial_data
from app.tests.utils.analytics_utils import (
    create_test_revenue_analysis,
    create_test_expense_analysis,
    create_test_profitability_analysis,
    create_test_cash_flow_analysis,
    create_test_performance_metrics
)

def test_get_financial_summary(
    client: TestClient,
    test_user_token_headers: dict,
    test_user: dict
) -> None:
    """Test get financial summary endpoint"""
    # Create test data
    test_data = create_test_financial_data(test_user["id"], num_records=5)
    for data in test_data:
        client.post(
            f"{settings.API_V1_STR}/financial/data",
            headers=test_user_token_headers,
            json=data
        )
    
    # Get summary
    r = client.get(
        f"{settings.API_V1_STR}/analytics/summary",
        headers=test_user_token_headers
    )
    assert r.status_code == 200
    summary = r.json()
    assert "total_revenue" in summary
    assert "total_expenses" in summary
    assert "net_profit" in summary
    assert "profit_margin" in summary

def test_get_financial_summary_with_date_range(
    client: TestClient,
    test_user_token_headers: dict,
    test_user: dict
) -> None:
    """Test get financial summary with date range"""
    # Create test data
    test_data = create_test_financial_data(test_user["id"], num_records=5)
    for data in test_data:
        client.post(
            f"{settings.API_V1_STR}/financial/data",
            headers=test_user_token_headers,
            json=data
        )
    
    # Get summary with date range
    start_date = (datetime.now() - timedelta(days=30)).isoformat()
    end_date = datetime.now().isoformat()
    r = client.get(
        f"{settings.API_V1_STR}/analytics/summary?start_date={start_date}&end_date={end_date}",
        headers=test_user_token_headers
    )
    assert r.status_code == 200
    summary = r.json()
    assert "total_revenue" in summary
    assert "total_expenses" in summary
    assert "net_profit" in summary
    assert "profit_margin" in summary

def test_get_category_analysis(
    client: TestClient,
    test_user_token_headers: dict,
    test_user: dict
) -> None:
    """Test get category analysis endpoint"""
    # Create test data
    test_data = create_test_financial_data(test_user["id"], num_records=5)
    for data in test_data:
        client.post(
            f"{settings.API_V1_STR}/financial/data",
            headers=test_user_token_headers,
            json=data
        )
    
    # Get category analysis
    r = client.get(
        f"{settings.API_V1_STR}/analytics/categories",
        headers=test_user_token_headers
    )
    assert r.status_code == 200
    analysis = r.json()
    assert "revenue_by_category" in analysis
    assert "expenses_by_category" in analysis
    assert "category_trends" in analysis

def test_get_trend_analysis(
    client: TestClient,
    test_user_token_headers: dict,
    test_user: dict
) -> None:
    """Test get trend analysis endpoint"""
    # Create test data
    test_data = create_test_financial_data(test_user["id"], num_records=5)
    for data in test_data:
        client.post(
            f"{settings.API_V1_STR}/financial/data",
            headers=test_user_token_headers,
            json=data
        )
    
    # Get trend analysis
    r = client.get(
        f"{settings.API_V1_STR}/analytics/trends",
        headers=test_user_token_headers
    )
    assert r.status_code == 200
    analysis = r.json()
    assert "revenue_trend" in analysis
    assert "expense_trend" in analysis
    assert "profit_trend" in analysis
    assert "growth_rate" in analysis

def test_get_comparative_analysis(
    client: TestClient,
    test_user_token_headers: dict,
    test_user: dict
) -> None:
    """Test get comparative analysis endpoint"""
    # Create test data
    test_data = create_test_financial_data(test_user["id"], num_records=5)
    for data in test_data:
        client.post(
            f"{settings.API_V1_STR}/financial/data",
            headers=test_user_token_headers,
            json=data
        )
    
    # Get comparative analysis
    r = client.get(
        f"{settings.API_V1_STR}/analytics/comparative",
        headers=test_user_token_headers
    )
    assert r.status_code == 200
    analysis = r.json()
    assert "period_comparison" in analysis
    assert "year_over_year" in analysis
    assert "month_over_month" in analysis

def test_get_forecast_analysis(
    client: TestClient,
    test_user_token_headers: dict,
    test_user: dict
) -> None:
    """Test get forecast analysis endpoint"""
    # Create test data
    test_data = create_test_financial_data(test_user["id"], num_records=5)
    for data in test_data:
        client.post(
            f"{settings.API_V1_STR}/financial/data",
            headers=test_user_token_headers,
            json=data
        )
    
    # Get forecast analysis
    r = client.get(
        f"{settings.API_V1_STR}/analytics/forecast",
        headers=test_user_token_headers
    )
    assert r.status_code == 200
    analysis = r.json()
    assert "revenue_forecast" in analysis
    assert "expense_forecast" in analysis
    assert "profit_forecast" in analysis
    assert "confidence_intervals" in analysis

def test_get_risk_analysis(
    client: TestClient,
    test_user_token_headers: dict,
    test_user: dict
) -> None:
    """Test get risk analysis endpoint"""
    # Create test data
    test_data = create_test_financial_data(test_user["id"], num_records=5)
    for data in test_data:
        client.post(
            f"{settings.API_V1_STR}/financial/data",
            headers=test_user_token_headers,
            json=data
        )
    
    # Get risk analysis
    r = client.get(
        f"{settings.API_V1_STR}/analytics/risks",
        headers=test_user_token_headers
    )
    assert r.status_code == 200
    analysis = r.json()
    assert "risk_scores" in analysis
    assert "risk_factors" in analysis
    assert "mitigation_strategies" in analysis

def test_get_revenue_analysis(
    client: TestClient,
    test_user_token_headers: dict,
    db: Session
) -> None:
    """Test getting revenue analysis"""
    response = client.get(
        f"{settings.API_V1_STR}/analytics/revenue",
        headers=test_user_token_headers
    )
    assert response.status_code == 200
    data = response.json()
    
    assert "total_revenue" in data
    assert "revenue_by_category" in data
    assert "revenue_trend" in data
    assert "revenue_forecast" in data
    
    revenue_by_category = data["revenue_by_category"]
    assert isinstance(revenue_by_category, dict)
    assert len(revenue_by_category) > 0
    
    revenue_trend = data["revenue_trend"]
    assert isinstance(revenue_trend, list)
    assert len(revenue_trend) > 0
    for item in revenue_trend:
        assert "date" in item
        assert "amount" in item

def test_get_revenue_analysis_with_date_range(
    client: TestClient,
    test_user_token_headers: dict,
    db: Session
) -> None:
    """Test getting revenue analysis with date range"""
    start_date = (datetime.now() - timedelta(days=30)).isoformat()
    end_date = datetime.now().isoformat()
    
    response = client.get(
        f"{settings.API_V1_STR}/analytics/revenue",
        headers=test_user_token_headers,
        params={
            "start_date": start_date,
            "end_date": end_date
        }
    )
    assert response.status_code == 200
    data = response.json()
    
    assert "total_revenue" in data
    assert "revenue_by_category" in data
    assert "revenue_trend" in data
    assert "revenue_forecast" in data
    
    revenue_trend = data["revenue_trend"]
    assert all(
        start_date <= item["date"] <= end_date
        for item in revenue_trend
    )

def test_get_expense_analysis(
    client: TestClient,
    test_user_token_headers: dict,
    db: Session
) -> None:
    """Test getting expense analysis"""
    response = client.get(
        f"{settings.API_V1_STR}/analytics/expenses",
        headers=test_user_token_headers
    )
    assert response.status_code == 200
    data = response.json()
    
    assert "total_expenses" in data
    assert "expenses_by_category" in data
    assert "expense_trend" in data
    assert "expense_forecast" in data
    
    expenses_by_category = data["expenses_by_category"]
    assert isinstance(expenses_by_category, dict)
    assert len(expenses_by_category) > 0
    
    expense_trend = data["expense_trend"]
    assert isinstance(expense_trend, list)
    assert len(expense_trend) > 0
    for item in expense_trend:
        assert "date" in item
        assert "amount" in item

def test_get_expense_analysis_with_date_range(
    client: TestClient,
    test_user_token_headers: dict,
    db: Session
) -> None:
    """Test getting expense analysis with date range"""
    start_date = (datetime.now() - timedelta(days=30)).isoformat()
    end_date = datetime.now().isoformat()
    
    response = client.get(
        f"{settings.API_V1_STR}/analytics/expenses",
        headers=test_user_token_headers,
        params={
            "start_date": start_date,
            "end_date": end_date
        }
    )
    assert response.status_code == 200
    data = response.json()
    
    assert "total_expenses" in data
    assert "expenses_by_category" in data
    assert "expense_trend" in data
    assert "expense_forecast" in data
    
    expense_trend = data["expense_trend"]
    assert all(
        start_date <= item["date"] <= end_date
        for item in expense_trend
    )

def test_get_profitability_analysis(
    client: TestClient,
    test_user_token_headers: dict,
    db: Session
) -> None:
    """Test getting profitability analysis"""
    response = client.get(
        f"{settings.API_V1_STR}/analytics/profitability",
        headers=test_user_token_headers
    )
    assert response.status_code == 200
    data = response.json()
    
    assert "net_profit" in data
    assert "profit_margin" in data
    assert "profit_trend" in data
    assert "profit_by_category" in data
    
    profit_trend = data["profit_trend"]
    assert isinstance(profit_trend, list)
    assert len(profit_trend) > 0
    for item in profit_trend:
        assert "date" in item
        assert "amount" in item
    
    profit_by_category = data["profit_by_category"]
    assert isinstance(profit_by_category, dict)
    assert len(profit_by_category) > 0

def test_get_cash_flow_analysis(
    client: TestClient,
    test_user_token_headers: dict,
    db: Session
) -> None:
    """Test getting cash flow analysis"""
    response = client.get(
        f"{settings.API_V1_STR}/analytics/cash-flow",
        headers=test_user_token_headers
    )
    assert response.status_code == 200
    data = response.json()
    
    assert "net_cash_flow" in data
    assert "operating_cash_flow" in data
    assert "investing_cash_flow" in data
    assert "financing_cash_flow" in data
    assert "cash_flow_trend" in data
    
    cash_flow_trend = data["cash_flow_trend"]
    assert isinstance(cash_flow_trend, list)
    assert len(cash_flow_trend) > 0
    for item in cash_flow_trend:
        assert "date" in item
        assert "operating" in item
        assert "investing" in item
        assert "financing" in item

def test_get_performance_metrics(
    client: TestClient,
    test_user_token_headers: dict,
    db: Session
) -> None:
    """Test getting performance metrics"""
    response = client.get(
        f"{settings.API_V1_STR}/analytics/performance",
        headers=test_user_token_headers
    )
    assert response.status_code == 200
    data = response.json()
    
    assert "roi" in data
    assert "roa" in data
    assert "roe" in data
    assert "current_ratio" in data
    assert "debt_to_equity" in data
    assert "asset_turnover" in data
    
    # Verify metric ranges
    assert 0 <= data["roi"] <= 1
    assert 0 <= data["roa"] <= 1
    assert 0 <= data["roe"] <= 1
    assert data["current_ratio"] > 0
    assert data["debt_to_equity"] >= 0
    assert data["asset_turnover"] > 0

def test_get_custom_analysis(
    client: TestClient,
    test_user_token_headers: dict,
    db: Session
) -> None:
    """Test getting custom analysis"""
    metrics = ["revenue", "expenses", "profit"]
    grouping = "category"
    time_period = "monthly"
    
    response = client.post(
        f"{settings.API_V1_STR}/analytics/custom",
        headers=test_user_token_headers,
        json={
            "metrics": metrics,
            "grouping": grouping,
            "time_period": time_period
        }
    )
    assert response.status_code == 200
    data = response.json()
    
    assert "metrics" in data
    assert "grouped_data" in data
    assert "time_period" in data
    
    assert data["time_period"] == time_period
    assert all(metric in data["metrics"] for metric in metrics)
    
    grouped_data = data["grouped_data"]
    assert isinstance(grouped_data, dict)
    assert len(grouped_data) > 0
    for group in grouped_data.values():
        assert all(metric in group for metric in metrics) 