import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional

from app.schemas.recommendation import (
    RecommendationRequest,
    RecommendationResponse,
    RiskAssessmentRequest,
    RiskAssessmentResponse
)

def create_test_recommendation_request(
    user_id: int,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
) -> RecommendationRequest:
    """Create test recommendation request"""
    if start_date is None:
        start_date = datetime.now() - timedelta(days=30)
    if end_date is None:
        end_date = datetime.now()
    
    return RecommendationRequest(
        user_id=user_id,
        start_date=start_date.isoformat(),
        end_date=end_date.isoformat(),
        focus_areas=["revenue", "expenses", "profitability"],
        priority_level="high"
    )

def create_test_recommendation_response(
    request: RecommendationRequest
) -> RecommendationResponse:
    """Create test recommendation response"""
    recommendations = [
        {
            "title": "Optimize Revenue Streams",
            "description": "Implement dynamic pricing strategy",
            "impact": "Increase revenue by 15%",
            "priority": "high",
            "implementation_steps": [
                "Analyze current pricing",
                "Identify price elasticity",
                "Implement new pricing model"
            ]
        },
        {
            "title": "Reduce Operating Costs",
            "description": "Streamline operational processes",
            "impact": "Decrease expenses by 10%",
            "priority": "medium",
            "implementation_steps": [
                "Audit current processes",
                "Identify inefficiencies",
                "Implement automation"
            ]
        },
        {
            "title": "Improve Profit Margins",
            "description": "Focus on high-margin products",
            "impact": "Increase profit margin by 5%",
            "priority": "high",
            "implementation_steps": [
                "Analyze product margins",
                "Adjust product mix",
                "Optimize pricing"
            ]
        }
    ]
    
    return RecommendationResponse(
        user_id=request.user_id,
        recommendations=recommendations,
        expected_impact={
            "revenue_increase": "15%",
            "cost_reduction": "10%",
            "profit_margin_improvement": "5%"
        },
        implementation_steps=[
            "Phase 1: Analysis and Planning",
            "Phase 2: Implementation",
            "Phase 3: Monitoring and Adjustment"
        ],
        priority="high"
    )

def create_test_risk_assessment_request(
    user_id: int,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
) -> RiskAssessmentRequest:
    """Create test risk assessment request"""
    if start_date is None:
        start_date = datetime.now() - timedelta(days=30)
    if end_date is None:
        end_date = datetime.now()
    
    return RiskAssessmentRequest(
        user_id=user_id,
        start_date=start_date.isoformat(),
        end_date=end_date.isoformat(),
        risk_categories=["financial", "operational", "market"],
        assessment_depth="comprehensive"
    )

def create_test_risk_assessment_response(
    request: RiskAssessmentRequest
) -> RiskAssessmentResponse:
    """Create test risk assessment response"""
    risk_factors = [
        {
            "name": "Market Volatility",
            "severity": "high",
            "probability": "medium",
            "impact": "Significant impact on revenue",
            "mitigation": "Diversify revenue streams"
        },
        {
            "name": "Operational Inefficiency",
            "severity": "medium",
            "probability": "high",
            "impact": "Increased costs",
            "mitigation": "Process optimization"
        },
        {
            "name": "Competitive Pressure",
            "severity": "high",
            "probability": "high",
            "impact": "Market share loss",
            "mitigation": "Product differentiation"
        }
    ]
    
    mitigation_strategies = [
        {
            "strategy": "Revenue Diversification",
            "implementation": "Develop new product lines",
            "timeline": "6 months",
            "resources": "Product development team"
        },
        {
            "strategy": "Cost Optimization",
            "implementation": "Automate manual processes",
            "timeline": "3 months",
            "resources": "IT department"
        },
        {
            "strategy": "Market Positioning",
            "implementation": "Enhance brand value",
            "timeline": "12 months",
            "resources": "Marketing team"
        }
    ]
    
    risk_trends = [
        {
            "date": (datetime.now() - timedelta(days=i)).isoformat(),
            "risk_score": round(random.uniform(0.3, 0.7), 2),
            "trend": random.choice(["increasing", "stable", "decreasing"])
        }
        for i in range(30)
    ]
    
    return RiskAssessmentResponse(
        user_id=request.user_id,
        risk_score=round(random.uniform(0.3, 0.7), 2),
        risk_factors=risk_factors,
        mitigation_strategies=mitigation_strategies,
        risk_trends=risk_trends,
        overall_risk_level="medium",
        assessment_date=datetime.now().isoformat()
    ) 