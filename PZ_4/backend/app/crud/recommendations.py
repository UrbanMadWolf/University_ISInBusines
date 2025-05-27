from typing import List, Optional, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.financial_data import FinancialData
from app.schemas.recommendations import (
    FinancialHealthRecommendation,
    OptimizationRecommendation,
    RiskAssessment,
    StrategicRecommendation
)

def get_financial_health(
    db: Session,
    user_id: int,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
) -> FinancialHealthRecommendation:
    """Get financial health recommendations"""
    query = db.query(FinancialData).filter(FinancialData.user_id == user_id)
    
    if start_date:
        query = query.filter(FinancialData.date >= start_date)
    if end_date:
        query = query.filter(FinancialData.date <= end_date)
    
    # Calculate key metrics
    total_revenue = query.filter(
        FinancialData.type == "revenue"
    ).with_entities(
        func.sum(FinancialData.amount)
    ).scalar() or 0
    
    total_expenses = query.filter(
        FinancialData.type == "expense"
    ).with_entities(
        func.sum(FinancialData.amount)
    ).scalar() or 0
    
    # Calculate ratios
    liquidity_ratio = (total_revenue / total_expenses) if total_expenses > 0 else 0
    debt_ratio = (total_expenses / total_revenue) if total_revenue > 0 else 0
    profit_margin = ((total_revenue - total_expenses) / total_revenue * 100) if total_revenue > 0 else 0
    roi = ((total_revenue - total_expenses) / total_expenses * 100) if total_expenses > 0 else 0
    
    # Generate recommendations based on metrics
    recommendations = []
    if liquidity_ratio < 1.5:
        recommendations.append({
            "type": "liquidity",
            "description": "Improve liquidity ratio by reducing expenses or increasing revenue",
            "impact": "High",
            "priority": "High"
        })
    
    if debt_ratio > 0.7:
        recommendations.append({
            "type": "debt",
            "description": "Reduce debt ratio by increasing revenue or reducing expenses",
            "impact": "High",
            "priority": "High"
        })
    
    if profit_margin < 10:
        recommendations.append({
            "type": "profitability",
            "description": "Improve profit margin by optimizing costs or increasing prices",
            "impact": "Medium",
            "priority": "Medium"
        })
    
    if roi < 15:
        recommendations.append({
            "type": "investment",
            "description": "Improve ROI by optimizing investments or reducing costs",
            "impact": "Medium",
            "priority": "Medium"
        })
    
    # Determine risk level
    risk_level = "Low"
    if liquidity_ratio < 1 or debt_ratio > 0.8 or profit_margin < 5:
        risk_level = "High"
    elif liquidity_ratio < 1.2 or debt_ratio > 0.6 or profit_margin < 8:
        risk_level = "Medium"
    
    # Get trends
    trends = []
    monthly_data = query.with_entities(
        func.date_trunc('month', FinancialData.date).label('month'),
        func.sum(FinancialData.amount).label('amount')
    ).group_by('month').order_by('month').all()
    
    for month, amount in monthly_data:
        trends.append({
            "month": month,
            "amount": float(amount)
        })
    
    return FinancialHealthRecommendation(
        metrics={
            "liquidity_ratio": float(liquidity_ratio),
            "debt_ratio": float(debt_ratio),
            "profit_margin": float(profit_margin),
            "roi": float(roi)
        },
        recommendations=recommendations,
        risk_level=risk_level,
        trends=trends
    )

def get_optimization_recommendations(
    db: Session,
    user_id: int,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
) -> List[OptimizationRecommendation]:
    """Get optimization recommendations"""
    query = db.query(FinancialData).filter(FinancialData.user_id == user_id)
    
    if start_date:
        query = query.filter(FinancialData.date >= start_date)
    if end_date:
        query = query.filter(FinancialData.date <= end_date)
    
    # Get expenses by category
    expenses_by_category = {}
    for category in db.query(FinancialData.category).distinct():
        category_expenses = query.filter(
            FinancialData.category == category[0],
            FinancialData.type == "expense"
        ).with_entities(
            func.sum(FinancialData.amount)
        ).scalar() or 0
        expenses_by_category[category[0]] = category_expenses
    
    # Generate optimization recommendations
    recommendations = []
    
    # Analyze expense categories
    total_expenses = sum(expenses_by_category.values())
    for category, amount in expenses_by_category.items():
        percentage = (amount / total_expenses * 100) if total_expenses > 0 else 0
        
        if percentage > 30:
            recommendations.append(OptimizationRecommendation(
                category=category,
                description=f"High expenses in {category} category",
                expected_impact={
                    "cost_reduction": float(amount * 0.2),  # 20% potential reduction
                    "efficiency_improvement": "Medium",
                    "roi_improvement": "High"
                },
                implementation_steps=[
                    "Analyze current spending patterns",
                    "Identify cost-saving opportunities",
                    "Implement cost control measures",
                    "Monitor results"
                ],
                priority="High"
            ))
        elif percentage > 20:
            recommendations.append(OptimizationRecommendation(
                category=category,
                description=f"Moderate expenses in {category} category",
                expected_impact={
                    "cost_reduction": float(amount * 0.1),  # 10% potential reduction
                    "efficiency_improvement": "Low",
                    "roi_improvement": "Medium"
                },
                implementation_steps=[
                    "Review current processes",
                    "Identify optimization opportunities",
                    "Implement improvements",
                    "Track results"
                ],
                priority="Medium"
            ))
    
    return recommendations

def get_risk_assessment(
    db: Session,
    user_id: int,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
) -> RiskAssessment:
    """Get risk assessment"""
    query = db.query(FinancialData).filter(FinancialData.user_id == user_id)
    
    if start_date:
        query = query.filter(FinancialData.date >= start_date)
    if end_date:
        query = query.filter(FinancialData.date <= end_date)
    
    # Calculate risk factors
    total_revenue = query.filter(
        FinancialData.type == "revenue"
    ).with_entities(
        func.sum(FinancialData.amount)
    ).scalar() or 0
    
    total_expenses = query.filter(
        FinancialData.type == "expense"
    ).with_entities(
        func.sum(FinancialData.amount)
    ).scalar() or 0
    
    # Calculate risk score (0-100)
    risk_score = 0
    
    # Revenue risk
    if total_revenue == 0:
        risk_score += 30
    elif total_revenue < total_expenses:
        risk_score += 20
    
    # Expense risk
    if total_expenses > total_revenue * 1.5:
        risk_score += 30
    elif total_expenses > total_revenue:
        risk_score += 20
    
    # Identify risk factors
    risk_factors = []
    
    if total_revenue == 0:
        risk_factors.append({
            "factor": "No revenue",
            "severity": "High",
            "probability": "High",
            "impact": "Critical"
        })
    elif total_revenue < total_expenses:
        risk_factors.append({
            "factor": "Revenue below expenses",
            "severity": "High",
            "probability": "Medium",
            "impact": "High"
        })
    
    if total_expenses > total_revenue * 1.5:
        risk_factors.append({
            "factor": "High expense ratio",
            "severity": "Medium",
            "probability": "High",
            "impact": "High"
        })
    
    # Generate mitigation strategies
    mitigation_strategies = []
    
    if total_revenue == 0:
        mitigation_strategies.append({
            "strategy": "Develop revenue generation plan",
            "priority": "High",
            "expected_impact": "High",
            "implementation_time": "1-3 months"
        })
    
    if total_expenses > total_revenue:
        mitigation_strategies.append({
            "strategy": "Implement cost reduction measures",
            "priority": "High",
            "expected_impact": "Medium",
            "implementation_time": "1-2 months"
        })
    
    # Get risk trends
    risk_trends = []
    monthly_data = query.with_entities(
        func.date_trunc('month', FinancialData.date).label('month'),
        func.sum(FinancialData.amount).label('amount')
    ).group_by('month').order_by('month').all()
    
    for month, amount in monthly_data:
        risk_trends.append({
            "month": month,
            "risk_score": float(risk_score)  # Simplified trend
        })
    
    return RiskAssessment(
        risk_score=risk_score,
        risk_factors=risk_factors,
        mitigation_strategies=mitigation_strategies,
        risk_trends=risk_trends
    )

def get_strategic_recommendations(
    db: Session,
    user_id: int,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
) -> List[StrategicRecommendation]:
    """Get strategic recommendations"""
    query = db.query(FinancialData).filter(FinancialData.user_id == user_id)
    
    if start_date:
        query = query.filter(FinancialData.date >= start_date)
    if end_date:
        query = query.filter(FinancialData.date <= end_date)
    
    # Get financial health
    financial_health = get_financial_health(db, user_id, start_date, end_date)
    
    # Get risk assessment
    risk_assessment = get_risk_assessment(db, user_id, start_date, end_date)
    
    # Generate strategic recommendations
    recommendations = []
    
    # Revenue growth strategy
    if financial_health.metrics["profit_margin"] < 10:
        recommendations.append(StrategicRecommendation(
            goal="Increase revenue and profitability",
            description="Implement strategies to increase revenue and improve profit margins",
            action_items=[
                "Review pricing strategy",
                "Identify new revenue streams",
                "Optimize sales channels",
                "Improve customer retention"
            ],
            timeline="6-12 months",
            resource_requirements={
                "budget": "Medium",
                "personnel": "Medium",
                "technology": "Low"
            }
        ))
    
    # Cost optimization strategy
    if financial_health.metrics["debt_ratio"] > 0.6:
        recommendations.append(StrategicRecommendation(
            goal="Optimize costs and reduce debt",
            description="Implement cost optimization strategies and reduce debt burden",
            action_items=[
                "Review and optimize expenses",
                "Implement cost control measures",
                "Develop debt reduction plan",
                "Improve operational efficiency"
            ],
            timeline="3-6 months",
            resource_requirements={
                "budget": "Low",
                "personnel": "Medium",
                "technology": "Medium"
            }
        ))
    
    # Risk management strategy
    if risk_assessment.risk_score > 50:
        recommendations.append(StrategicRecommendation(
            goal="Improve risk management",
            description="Implement comprehensive risk management strategies",
            action_items=[
                "Develop risk management framework",
                "Implement risk monitoring systems",
                "Create contingency plans",
                "Train staff on risk management"
            ],
            timeline="3-6 months",
            resource_requirements={
                "budget": "Medium",
                "personnel": "High",
                "technology": "High"
            }
        ))
    
    return recommendations 