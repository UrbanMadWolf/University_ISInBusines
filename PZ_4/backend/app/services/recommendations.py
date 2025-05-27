from typing import Dict, List, Optional
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from ..models.financial import FinancialData, Recommendation, RiskAssessment
from ..schemas.financial import RecommendationCreate
from app.schemas.recommendations import (
    FinancialHealth,
    RecommendationRequest,
    RecommendationResponse,
    RiskFactor
)

class RecommendationService:
    def __init__(self, db: Session):
        self.db = db

    def analyze_financial_health(
        self,
        user_id: int,
        start_date: datetime,
        end_date: datetime
    ) -> FinancialHealth:
        """Analyze financial health of the company"""
        data = self.db.query(FinancialData).filter(
            FinancialData.user_id == user_id,
            FinancialData.date >= start_date,
            FinancialData.date <= end_date
        ).all()

        # Calculate financial ratios
        total_revenue = sum(item.amount for item in data if item.data_type == "revenue")
        total_expenses = sum(item.amount for item in data if item.data_type == "expense")
        total_assets = sum(item.amount for item in data if item.data_type == "asset")
        total_liabilities = sum(item.amount for item in data if item.data_type == "liability")

        # Calculate ratios
        liquidity_ratio = total_assets / total_liabilities if total_liabilities != 0 else 0
        solvency_ratio = (total_assets - total_liabilities) / total_assets if total_assets != 0 else 0
        profitability_ratio = (total_revenue - total_expenses) / total_revenue if total_revenue != 0 else 0
        efficiency_ratio = total_expenses / total_revenue if total_revenue != 0 else 0

        # Calculate overall score (weighted average)
        weights = {
            "liquidity": 0.3,
            "solvency": 0.3,
            "profitability": 0.2,
            "efficiency": 0.2
        }
        overall_score = (
            liquidity_ratio * weights["liquidity"] +
            solvency_ratio * weights["solvency"] +
            profitability_ratio * weights["profitability"] +
            (1 - efficiency_ratio) * weights["efficiency"]
        )

        # Generate recommendations based on ratios
        recommendations = []
        if liquidity_ratio < 1.5:
            recommendations.append("Improve liquidity by reducing short-term liabilities or increasing current assets")
        if solvency_ratio < 0.5:
            recommendations.append("Increase solvency by reducing debt or increasing equity")
        if profitability_ratio < 0.1:
            recommendations.append("Improve profitability by increasing revenue or reducing expenses")
        if efficiency_ratio > 0.8:
            recommendations.append("Improve operational efficiency by optimizing expenses")

        return FinancialHealth(
            liquidity_ratio=liquidity_ratio,
            solvency_ratio=solvency_ratio,
            profitability_ratio=profitability_ratio,
            efficiency_ratio=efficiency_ratio,
            overall_score=overall_score,
            recommendations=recommendations
        )

    def generate_recommendations(
        self,
        user_id: int,
        request: RecommendationRequest
    ) -> RecommendationResponse:
        """Generate optimization recommendations"""
        data = self.db.query(FinancialData).filter(
            FinancialData.user_id == user_id,
            FinancialData.date >= request.start_date,
            FinancialData.date <= request.end_date
        ).all()

        recommendations = []
        expected_improvement = 0.0
        implementation_difficulty = "medium"

        # Analyze current state
        current_value = sum(
            item.amount for item in data
            if item.data_type == request.target_metric
        )

        # Generate recommendations based on target metric
        if request.target_metric == "revenue":
            recommendations.extend([
                Recommendation(
                    title="Optimize Pricing Strategy",
                    description="Review and adjust pricing to maximize revenue while maintaining competitiveness",
                    impact=0.15,
                    difficulty="medium",
                    implementation_steps=[
                        "Analyze current pricing structure",
                        "Research market prices",
                        "Implement A/B testing for new prices",
                        "Monitor results and adjust"
                    ],
                    estimated_time="2-3 months",
                    cost=5000.0
                ),
                Recommendation(
                    title="Expand Marketing Channels",
                    description="Increase marketing efforts across multiple channels to reach new customers",
                    impact=0.2,
                    difficulty="high",
                    implementation_steps=[
                        "Identify new marketing channels",
                        "Develop channel-specific strategies",
                        "Allocate budget",
                        "Launch campaigns",
                        "Track performance"
                    ],
                    estimated_time="3-4 months",
                    cost=15000.0
                )
            ])
            expected_improvement = 0.35
            implementation_difficulty = "high"

        elif request.target_metric == "expense":
            recommendations.extend([
                Recommendation(
                    title="Optimize Supply Chain",
                    description="Review and optimize supply chain to reduce costs",
                    impact=0.1,
                    difficulty="medium",
                    implementation_steps=[
                        "Audit current suppliers",
                        "Negotiate better terms",
                        "Consolidate orders",
                        "Implement inventory management system"
                    ],
                    estimated_time="2-3 months",
                    cost=3000.0
                ),
                Recommendation(
                    title="Implement Cost Control Measures",
                    description="Establish strict cost control measures across departments",
                    impact=0.15,
                    difficulty="low",
                    implementation_steps=[
                        "Review current expenses",
                        "Set department budgets",
                        "Implement approval process",
                        "Monitor spending"
                    ],
                    estimated_time="1-2 months",
                    cost=1000.0
                )
            ])
            expected_improvement = 0.25
            implementation_difficulty = "medium"

        return RecommendationResponse(
            target_metric=request.target_metric,
            recommendations=recommendations,
            expected_improvement=expected_improvement,
            implementation_difficulty=implementation_difficulty
        )

    def assess_risks(
        self,
        user_id: int,
        start_date: datetime,
        end_date: datetime
    ) -> RiskAssessment:
        """Assess financial risks"""
        data = self.db.query(FinancialData).filter(
            FinancialData.user_id == user_id,
            FinancialData.date >= start_date,
            FinancialData.date <= end_date
        ).all()

        # Calculate risk metrics
        total_revenue = sum(item.amount for item in data if item.data_type == "revenue")
        total_expenses = sum(item.amount for item in data if item.data_type == "expense")
        total_assets = sum(item.amount for item in data if item.data_type == "asset")
        total_liabilities = sum(item.amount for item in data if item.data_type == "liability")

        # Calculate risk scores
        market_risk = self._calculate_market_risk(data)
        credit_risk = self._calculate_credit_risk(data)
        operational_risk = self._calculate_operational_risk(data)
        liquidity_risk = self._calculate_liquidity_risk(data)

        # Calculate overall risk score
        weights = {
            "market": 0.3,
            "credit": 0.3,
            "operational": 0.2,
            "liquidity": 0.2
        }
        overall_risk_score = (
            market_risk * weights["market"] +
            credit_risk * weights["credit"] +
            operational_risk * weights["operational"] +
            liquidity_risk * weights["liquidity"]
        )

        # Generate risk factors
        risk_factors = []
        if market_risk > 0.7:
            risk_factors.append(
                RiskFactor(
                    name="High Market Volatility",
                    severity=0.8,
                    probability=0.6,
                    impact=0.7,
                    mitigation_strategies=[
                        "Diversify revenue streams",
                        "Develop contingency plans",
                        "Monitor market trends"
                    ]
                )
            )
        if credit_risk > 0.7:
            risk_factors.append(
                RiskFactor(
                    name="Credit Risk Exposure",
                    severity=0.7,
                    probability=0.5,
                    impact=0.6,
                    mitigation_strategies=[
                        "Strengthen credit assessment",
                        "Implement stricter payment terms",
                        "Diversify customer base"
                    ]
                )
            )

        return RiskAssessment(
            market_risk=market_risk,
            credit_risk=credit_risk,
            operational_risk=operational_risk,
            liquidity_risk=liquidity_risk,
            overall_risk_score=overall_risk_score,
            risk_factors=risk_factors
        )

    def _calculate_market_risk(self, data: List[FinancialData]) -> float:
        """Calculate market risk score based on revenue volatility and market exposure"""
        # Group data by date and calculate daily revenue
        daily_revenue = {}
        for item in data:
            if item.data_type == "revenue":
                date_str = item.date.strftime("%Y-%m-%d")
                if date_str not in daily_revenue:
                    daily_revenue[date_str] = 0
                daily_revenue[date_str] += item.amount

        if not daily_revenue:
            return 0.5  # Default risk if no data

        # Calculate revenue volatility
        revenue_values = list(daily_revenue.values())
        mean_revenue = sum(revenue_values) / len(revenue_values)
        revenue_std = (sum((x - mean_revenue) ** 2 for x in revenue_values) / len(revenue_values)) ** 0.5
        revenue_volatility = revenue_std / mean_revenue if mean_revenue > 0 else 0

        # Calculate market concentration
        category_revenue = {}
        for item in data:
            if item.data_type == "revenue":
                if item.category not in category_revenue:
                    category_revenue[item.category] = 0
                category_revenue[item.category] += item.amount

        total_revenue = sum(category_revenue.values())
        if total_revenue == 0:
            return 0.5

        # Calculate Herfindahl-Hirschman Index (HHI)
        hhi = sum((revenue / total_revenue) ** 2 for revenue in category_revenue.values())

        # Combine metrics into market risk score
        market_risk = (revenue_volatility * 0.6 + hhi * 0.4)
        return min(max(market_risk, 0), 1)  # Normalize between 0 and 1

    def _calculate_credit_risk(self, data: List[FinancialData]) -> float:
        """Calculate credit risk score based on payment patterns and debt levels"""
        # Calculate debt-to-equity ratio
        total_assets = sum(item.amount for item in data if item.data_type == "asset")
        total_liabilities = sum(item.amount for item in data if item.data_type == "liability")
        debt_to_equity = total_liabilities / total_assets if total_assets > 0 else 0

        # Calculate payment delays (if metadata contains payment information)
        payment_delays = []
        for item in data:
            if item.data_type == "revenue" and item.metadata and "payment_delay" in item.metadata:
                payment_delays.append(item.metadata["payment_delay"])

        avg_payment_delay = sum(payment_delays) / len(payment_delays) if payment_delays else 0

        # Calculate credit risk score
        credit_risk = (
            (min(debt_to_equity, 2) / 2) * 0.6 +  # Debt-to-equity component
            (min(avg_payment_delay / 30, 1)) * 0.4  # Payment delay component
        )
        return min(max(credit_risk, 0), 1)  # Normalize between 0 and 1

    def _calculate_operational_risk(self, data: List[FinancialData]) -> float:
        """Calculate operational risk score based on expense patterns and efficiency"""
        # Calculate expense volatility
        daily_expenses = {}
        for item in data:
            if item.data_type == "expense":
                date_str = item.date.strftime("%Y-%m-%d")
                if date_str not in daily_expenses:
                    daily_expenses[date_str] = 0
                daily_expenses[date_str] += item.amount

        if not daily_expenses:
            return 0.3  # Default risk if no data

        expense_values = list(daily_expenses.values())
        mean_expense = sum(expense_values) / len(expense_values)
        expense_std = (sum((x - mean_expense) ** 2 for x in expense_values) / len(expense_values)) ** 0.5
        expense_volatility = expense_std / mean_expense if mean_expense > 0 else 0

        # Calculate operational efficiency
        total_revenue = sum(item.amount for item in data if item.data_type == "revenue")
        total_expenses = sum(item.amount for item in data if item.data_type == "expense")
        efficiency_ratio = total_expenses / total_revenue if total_revenue > 0 else 1

        # Calculate operational risk score
        operational_risk = (
            expense_volatility * 0.4 +  # Expense volatility component
            (efficiency_ratio if efficiency_ratio <= 1 else 1) * 0.6  # Efficiency component
        )
        return min(max(operational_risk, 0), 1)  # Normalize between 0 and 1

    def _calculate_liquidity_risk(self, data: List[FinancialData]) -> float:
        """Calculate liquidity risk score based on cash flow and current ratio"""
        # Calculate current ratio
        current_assets = sum(
            item.amount for item in data 
            if item.data_type == "asset" and item.metadata and item.metadata.get("is_current", False)
        )
        current_liabilities = sum(
            item.amount for item in data 
            if item.data_type == "liability" and item.metadata and item.metadata.get("is_current", False)
        )
        current_ratio = current_assets / current_liabilities if current_liabilities > 0 else 0

        # Calculate cash flow coverage
        total_revenue = sum(item.amount for item in data if item.data_type == "revenue")
        total_expenses = sum(item.amount for item in data if item.data_type == "expense")
        cash_flow = total_revenue - total_expenses
        cash_flow_coverage = cash_flow / total_expenses if total_expenses > 0 else 0

        # Calculate liquidity risk score
        liquidity_risk = (
            (1 - min(current_ratio / 2, 1)) * 0.5 +  # Current ratio component
            (1 - min(cash_flow_coverage, 1)) * 0.5  # Cash flow coverage component
        )
        return min(max(liquidity_risk, 0), 1)  # Normalize between 0 and 1 