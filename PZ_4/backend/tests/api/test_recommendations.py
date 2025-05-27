from datetime import datetime, timedelta
from typing import Dict, List

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.tests.utils.financial_utils import create_test_financial_data
from app.tests.utils.recommendation_utils import (
    create_test_financial_health,
    create_test_recommendation_request,
    create_test_recommendation_response,
    create_test_risk_assessment,
    create_test_risk_assessment_request,
    create_test_risk_assessment_response
)

def test_get_financial_health(
    client: TestClient,
    test_user_token_headers: dict,
    db: Session
) -> None:
    """Test getting financial health recommendations"""
    response = client.get(
        f"{settings.API_V1_STR}/recommendations/financial-health",
        headers=test_user_token_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert "metrics" in data
    assert "recommendations" in data
    assert "risk_level" in data
    assert "trends" in data
    assert isinstance(data["recommendations"], list)
    assert isinstance(data["trends"], list)

def test_get_financial_health_with_date_range(
    client: TestClient,
    test_user_token_headers: dict,
    db: Session
) -> None:
    """Test getting financial health recommendations with date range"""
    start_date = (datetime.now() - timedelta(days=30)).isoformat()
    end_date = datetime.now().isoformat()
    
    response = client.get(
        f"{settings.API_V1_STR}/recommendations/financial-health",
        headers=test_user_token_headers,
        params={
            "start_date": start_date,
            "end_date": end_date
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "metrics" in data
    assert "recommendations" in data
    assert "risk_level" in data
    assert "trends" in data
    assert all(
        start_date <= item["date"] <= end_date
        for item in data["trends"]
    )

def test_get_optimization_recommendations(
    client: TestClient,
    test_user_token_headers: dict,
    db: Session
) -> None:
    """Test getting optimization recommendations"""
    request_data = create_test_recommendation_request(1)
    response = client.post(
        f"{settings.API_V1_STR}/recommendations/optimize",
        headers=test_user_token_headers,
        json=request_data.dict()
    )
    assert response.status_code == 200
    data = response.json()
    assert "recommendations" in data
    assert "expected_impact" in data
    assert "implementation_steps" in data
    assert "priority" in data
    assert isinstance(data["recommendations"], list)
    assert isinstance(data["implementation_steps"], list)

def test_get_risk_assessment(
    client: TestClient,
    test_user_token_headers: dict,
    db: Session
) -> None:
    """Test getting risk assessment"""
    response = client.get(
        f"{settings.API_V1_STR}/recommendations/risk-assessment",
        headers=test_user_token_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert "risk_score" in data
    assert "risk_factors" in data
    assert "mitigation_strategies" in data
    assert "risk_trends" in data
    assert isinstance(data["risk_factors"], list)
    assert isinstance(data["mitigation_strategies"], list)
    assert isinstance(data["risk_trends"], list)

def test_get_risk_assessment_with_date_range(
    client: TestClient,
    test_user_token_headers: dict,
    db: Session
) -> None:
    """Test getting risk assessment with date range"""
    start_date = (datetime.now() - timedelta(days=30)).isoformat()
    end_date = datetime.now().isoformat()
    
    response = client.get(
        f"{settings.API_V1_STR}/recommendations/risk-assessment",
        headers=test_user_token_headers,
        params={
            "start_date": start_date,
            "end_date": end_date
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "risk_score" in data
    assert "risk_factors" in data
    assert "mitigation_strategies" in data
    assert "risk_trends" in data
    assert all(
        start_date <= item["date"] <= end_date
        for item in data["risk_trends"]
    )

def test_get_strategic_recommendations(
    client: TestClient,
    test_user_token_headers: dict,
    db: Session
) -> None:
    """Test getting strategic recommendations"""
    response = client.get(
        f"{settings.API_V1_STR}/recommendations/strategic",
        headers=test_user_token_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert "strategic_goals" in data
    assert "action_items" in data
    assert "timeline" in data
    assert "resource_requirements" in data
    assert isinstance(data["strategic_goals"], list)
    assert isinstance(data["action_items"], list)
    assert isinstance(data["timeline"], list)
    assert isinstance(data["resource_requirements"], dict)

def test_get_financial_health_with_date_range():
    """Test getting financial health recommendations with date range"""
    user_id = 1
    start_date = (datetime.now() - timedelta(days=30)).isoformat()
    end_date = datetime.now().isoformat()
    
    response = client.get(
        f"/api/v1/recommendations/health/{user_id}",
        params={"start_date": start_date, "end_date": end_date}
    )
    assert response.status_code == 200
    data = response.json()
    
    assert "metrics" in data
    assert "recommendations" in data
    assert "risk_level" in data
    assert "trends" in data

def test_get_optimization_recommendations():
    """Test getting optimization recommendations"""
    user_id = 1
    request = create_test_recommendation_request(user_id)
    
    response = client.post(
        f"/api/v1/recommendations/optimize/{user_id}",
        json=request.dict()
    )
    assert response.status_code == 200
    data = response.json()
    
    assert "recommendations" in data
    assert "expected_impact" in data
    assert "implementation_steps" in data
    assert "priority" in data
    
    recommendations = data["recommendations"]
    assert isinstance(recommendations, list)
    assert len(recommendations) > 0
    for rec in recommendations:
        assert "title" in rec
        assert "description" in rec
        assert "impact" in rec
        assert "priority" in rec

def test_get_risk_assessment():
    """Test getting risk assessment"""
    user_id = 1
    request = create_test_risk_assessment_request(user_id)
    
    response = client.post(
        f"/api/v1/recommendations/risk/{user_id}",
        json=request.dict()
    )
    assert response.status_code == 200
    data = response.json()
    
    assert "risk_score" in data
    assert "risk_factors" in data
    assert "mitigation_strategies" in data
    assert "risk_trends" in data
    
    risk_factors = data["risk_factors"]
    assert isinstance(risk_factors, list)
    assert len(risk_factors) > 0
    for factor in risk_factors:
        assert "name" in factor
        assert "severity" in factor
        assert "probability" in factor
        assert "impact" in factor

def test_get_risk_assessment_with_date_range():
    """Test getting risk assessment with date range"""
    user_id = 1
    start_date = (datetime.now() - timedelta(days=30)).isoformat()
    end_date = datetime.now().isoformat()
    
    request = create_test_risk_assessment_request(
        user_id,
        start_date=start_date,
        end_date=end_date
    )
    
    response = client.post(
        f"/api/v1/recommendations/risk/{user_id}",
        json=request.dict()
    )
    assert response.status_code == 200
    data = response.json()
    
    assert "risk_score" in data
    assert "risk_factors" in data
    assert "mitigation_strategies" in data
    assert "risk_trends" in data

def test_get_strategic_recommendations():
    """Test getting strategic recommendations"""
    user_id = 1
    response = client.get(f"/api/v1/recommendations/strategic/{user_id}")
    assert response.status_code == 200
    data = response.json()
    
    assert "strategic_goals" in data
    assert "action_items" in data
    assert "timeline" in data
    assert "resource_requirements" in data
    
    strategic_goals = data["strategic_goals"]
    assert isinstance(strategic_goals, list)
    assert len(strategic_goals) > 0
    for goal in strategic_goals:
        assert "title" in goal
        assert "description" in goal
        assert "timeframe" in goal
        assert "success_metrics" in goal 