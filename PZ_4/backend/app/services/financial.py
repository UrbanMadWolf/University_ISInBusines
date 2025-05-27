from typing import List, Optional, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.financial_data import FinancialData
from app.schemas.financial import FinancialDataCreate, FinancialDataUpdate

class FinancialService:
    def __init__(self, db: Session):
        self.db = db

    def create(self, user_id: int, data: FinancialDataCreate) -> FinancialData:
        """Create new financial data entry"""
        db_item = FinancialData(
            user_id=user_id,
            data_type=data.data_type,
            amount=data.amount,
            currency=data.currency,
            category=data.category,
            description=data.description,
            date=data.date,
            metadata=data.metadata
        )
        self.db.add(db_item)
        self.db.commit()
        self.db.refresh(db_item)
        return db_item

    def get(self, user_id: int, item_id: int) -> Optional[FinancialData]:
        """Get financial data by ID"""
        return self.db.query(FinancialData).filter(
            FinancialData.id == item_id,
            FinancialData.user_id == user_id
        ).first()

    def list(
        self,
        user_id: int,
        skip: int = 0,
        limit: int = 100,
        data_type: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[FinancialData]:
        """List financial data with filters"""
        query = self.db.query(FinancialData).filter(FinancialData.user_id == user_id)
        
        if data_type:
            query = query.filter(FinancialData.data_type == data_type)
        if start_date:
            query = query.filter(FinancialData.date >= start_date)
        if end_date:
            query = query.filter(FinancialData.date <= end_date)
        
        return query.offset(skip).limit(limit).all()

    def update(
        self,
        user_id: int,
        item_id: int,
        data: FinancialDataUpdate
    ) -> Optional[FinancialData]:
        """Update financial data"""
        db_item = self.get(user_id, item_id)
        if not db_item:
            return None
        
        update_data = data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_item, field, value)
        
        self.db.add(db_item)
        self.db.commit()
        self.db.refresh(db_item)
        return db_item

    def delete(self, user_id: int, item_id: int) -> bool:
        """Delete financial data"""
        db_item = self.get(user_id, item_id)
        if not db_item:
            return False
        
        self.db.delete(db_item)
        self.db.commit()
        return True

    def get_summary(
        self,
        user_id: int,
        start_date: datetime,
        end_date: datetime
    ) -> Dict[str, Any]:
        """Get financial summary for the period"""
        data = self.list(
            user_id=user_id,
            start_date=start_date,
            end_date=end_date
        )
        
        total_revenue = sum(item.amount for item in data if item.data_type == "revenue")
        total_expenses = sum(item.amount for item in data if item.data_type == "expense")
        total_profit = total_revenue - total_expenses
        
        category_summary = {}
        for item in data:
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
        
        return {
            "total_revenue": total_revenue,
            "total_expenses": total_expenses,
            "total_profit": total_profit,
            "category_summary": category_summary
        }

    def get_metrics(
        self,
        user_id: int,
        start_date: datetime,
        end_date: datetime
    ) -> Dict[str, float]:
        """Calculate financial metrics"""
        data = self.list(
            user_id=user_id,
            start_date=start_date,
            end_date=end_date
        )
        
        total_revenue = sum(item.amount for item in data if item.data_type == "revenue")
        total_expenses = sum(item.amount for item in data if item.data_type == "expense")
        
        if total_revenue == 0:
            profit_margin = 0
            expense_ratio = 0
        else:
            profit_margin = (total_revenue - total_expenses) / total_revenue
            expense_ratio = total_expenses / total_revenue
        
        return {
            "profit_margin": profit_margin,
            "expense_ratio": expense_ratio
        } 