from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class FinancialData(Base):
    """Модель для хранения финансовых данных"""
    __tablename__ = "financial_data"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, nullable=False)
    revenue = Column(Float, nullable=False)
    expenses = Column(Float, nullable=False)
    profit = Column(Float, nullable=False)
    category = Column(String, nullable=False)
    subcategory = Column(String, nullable=True)
    metadata = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class FinancialMetric(Base):
    """Модель для хранения финансовых метрик"""
    __tablename__ = "financial_metrics"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, nullable=False)
    metric_name = Column(String, nullable=False)
    value = Column(Float, nullable=False)
    target_value = Column(Float, nullable=True)
    threshold = Column(Float, nullable=True)
    metadata = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Forecast(Base):
    """Модель для хранения прогнозов"""
    __tablename__ = "forecasts"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, nullable=False)
    metric_name = Column(String, nullable=False)
    forecast_value = Column(Float, nullable=False)
    confidence_interval_lower = Column(Float, nullable=True)
    confidence_interval_upper = Column(Float, nullable=True)
    model_version = Column(String, nullable=False)
    metadata = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Recommendation(Base):
    """Модель для хранения рекомендаций"""
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, nullable=False)
    action = Column(String, nullable=False)
    expected_impact = Column(Float, nullable=False)
    confidence = Column(Float, nullable=False)
    cost = Column(Float, nullable=True)
    priority = Column(Integer, nullable=True)
    status = Column(String, nullable=False, default="pending")
    metadata = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class RiskAssessment(Base):
    """Модель для хранения оценки рисков"""
    __tablename__ = "risk_assessments"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, nullable=False)
    risk_name = Column(String, nullable=False)
    probability = Column(Float, nullable=False)
    impact = Column(Float, nullable=False)
    severity = Column(String, nullable=False)
    mitigation_strategy = Column(String, nullable=True)
    status = Column(String, nullable=False, default="active")
    metadata = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow) 