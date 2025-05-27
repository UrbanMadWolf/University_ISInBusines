from typing import Dict, List, Optional, Any
from datetime import datetime
from pydantic import BaseModel

class RecommendationRequest(BaseModel):
    start_date: datetime
    end_date: datetime
    target_metric: str
    constraints: Dict[str, float] = {}

class Recommendation(BaseModel):
    title: str
    description: str
    impact: float
    difficulty: str
    implementation_steps: List[str]
    estimated_time: str
    cost: Optional[float] = None

class RecommendationResponse(BaseModel):
    target_metric: str
    recommendations: List[Recommendation]
    expected_improvement: float
    implementation_difficulty: str

class FinancialHealth(BaseModel):
    liquidity_ratio: float
    solvency_ratio: float
    profitability_ratio: float
    efficiency_ratio: float
    overall_score: float
    recommendations: List[str]

class RiskFactor(BaseModel):
    name: str
    severity: float
    probability: float
    impact: float
    mitigation_strategies: List[str]

class RiskAssessment(BaseModel):
    market_risk: float
    credit_risk: float
    operational_risk: float
    liquidity_risk: float
    overall_risk_score: float
    risk_factors: List[RiskFactor]

class TrendPoint(BaseModel):
    month: datetime
    amount: float

class FinancialHealthRecommendation(BaseModel):
    metrics: Dict[str, float]
    recommendations: List[Dict[str, str]]
    risk_level: str
    trends: List[TrendPoint]

class OptimizationRecommendation(BaseModel):
    category: str
    description: str
    expected_impact: Dict[str, Any]
    implementation_steps: List[str]
    priority: str

class MitigationStrategy(BaseModel):
    strategy: str
    priority: str
    expected_impact: str
    implementation_time: str

class RiskTrend(BaseModel):
    month: datetime
    risk_score: float

class RiskAssessment(BaseModel):
    risk_score: float
    risk_factors: List[RiskFactor]
    mitigation_strategies: List[MitigationStrategy]
    risk_trends: List[RiskTrend]

class StrategicRecommendation(BaseModel):
    goal: str
    description: str
    action_items: List[str]
    timeline: str
    resource_requirements: Dict[str, str] 