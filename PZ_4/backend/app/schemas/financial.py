from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class FinancialDataBase(BaseModel):
    """Базовая схема для финансовых данных"""
    amount: float
    category: str
    type: str
    description: Optional[str] = None
    date: datetime

class FinancialDataCreate(FinancialDataBase):
    """Схема для создания финансовых данных"""
    user_id: int

class FinancialDataUpdate(BaseModel):
    """Схема для обновления финансовых данных"""
    amount: Optional[float] = None
    category: Optional[str] = None
    type: Optional[str] = None
    description: Optional[str] = None
    date: Optional[datetime] = None

class FinancialData(FinancialDataBase):
    """Схема для отображения финансовых данных"""
    id: int
    user_id: int

    class Config:
        from_attributes = True

class FinancialMetadataBase(BaseModel):
    """Базовая схема для финансовых метаданных"""
    key: str
    value: str
    category: Optional[str] = None
    description: Optional[str] = None

class FinancialMetadataCreate(FinancialMetadataBase):
    """Схема для создания финансовых метаданных"""
    user_id: int

class FinancialMetadataUpdate(BaseModel):
    """Схема для обновления финансовых метаданных"""
    key: Optional[str] = None
    value: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None

class FinancialMetadata(FinancialMetadataBase):
    """Схема для отображения финансовых метаданных"""
    id: int
    user_id: int

    class Config:
        from_attributes = True

class CategoryTotal(BaseModel):
    """Схема для категорийного общего баланса"""
    revenue: float
    expenses: float
    net: float

class MonthlyTrend(BaseModel):
    """Схема для ежемесячного тренда"""
    month: datetime
    revenue: float
    expenses: float
    net: float

class FinancialSummary(BaseModel):
    """Схема для финансового свода"""
    total_revenue: float
    total_expenses: float
    net_profit: float
    profit_margin: float
    category_totals: Dict[str, CategoryTotal]
    monthly_trends: List[MonthlyTrend]

class FinancialMetricBase(BaseModel):
    """Базовая схема для финансовых метрик"""
    date: datetime
    metric_name: str
    value: float
    target_value: Optional[float] = None
    threshold: Optional[float] = None
    metadata: Optional[Dict[str, Any]] = None

class FinancialMetricCreate(FinancialMetricBase):
    """Схема для создания финансовых метрик"""
    pass

class FinancialMetricUpdate(BaseModel):
    """Схема для обновления финансовых метрик"""
    value: Optional[float] = None
    target_value: Optional[float] = None
    threshold: Optional[float] = None
    metadata: Optional[Dict[str, Any]] = None

class FinancialMetric(FinancialMetricBase):
    """Схема для отображения финансовых метрик"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ForecastBase(BaseModel):
    """Базовая схема для прогнозов"""
    date: datetime
    metric_name: str
    forecast_value: float
    confidence_interval_lower: Optional[float] = None
    confidence_interval_upper: Optional[float] = None
    model_version: str
    metadata: Optional[Dict[str, Any]] = None

class ForecastCreate(ForecastBase):
    """Схема для создания прогнозов"""
    pass

class Forecast(ForecastBase):
    """Схема для отображения прогнозов"""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class RecommendationBase(BaseModel):
    """Базовая схема для рекомендаций"""
    date: datetime
    action: str
    expected_impact: float = Field(..., ge=0, le=1)
    confidence: float = Field(..., ge=0, le=1)
    cost: Optional[float] = None
    priority: Optional[int] = None
    status: str = "pending"
    metadata: Optional[Dict[str, Any]] = None

class RecommendationCreate(RecommendationBase):
    """Схема для создания рекомендаций"""
    pass

class RecommendationUpdate(BaseModel):
    """Схема для обновления рекомендаций"""
    action: Optional[str] = None
    expected_impact: Optional[float] = Field(None, ge=0, le=1)
    confidence: Optional[float] = Field(None, ge=0, le=1)
    cost: Optional[float] = None
    priority: Optional[int] = None
    status: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class Recommendation(RecommendationBase):
    """Схема для отображения рекомендаций"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class RiskAssessmentBase(BaseModel):
    """Базовая схема для оценки рисков"""
    date: datetime
    risk_name: str
    probability: float = Field(..., ge=0, le=1)
    impact: float = Field(..., ge=0, le=1)
    severity: str
    mitigation_strategy: Optional[str] = None
    status: str = "active"
    metadata: Optional[Dict[str, Any]] = None

class RiskAssessmentCreate(RiskAssessmentBase):
    """Схема для создания оценки рисков"""
    pass

class RiskAssessmentUpdate(BaseModel):
    """Схема для обновления оценки рисков"""
    probability: Optional[float] = Field(None, ge=0, le=1)
    impact: Optional[float] = Field(None, ge=0, le=1)
    severity: Optional[str] = None
    mitigation_strategy: Optional[str] = None
    status: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class RiskAssessment(RiskAssessmentBase):
    """Схема для отображения оценки рисков"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True 