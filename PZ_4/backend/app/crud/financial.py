from typing import List, Optional, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.financial_data import FinancialData
from app.models.financial_metadata import FinancialMetadata
from app.schemas.financial import (
    FinancialDataCreate,
    FinancialDataUpdate,
    FinancialMetadataCreate,
    FinancialMetadataUpdate,
    FinancialSummary,
    FinancialData as FinancialDataSchema,
    FinancialMetadata as FinancialMetadataSchema
)

def create_financial_data(
    db: Session,
    obj_in: FinancialDataCreate
) -> FinancialDataSchema:
    """Create new financial data entry"""
    db_obj = FinancialData(
        user_id=obj_in.user_id,
        amount=obj_in.amount,
        category=obj_in.category,
        type=obj_in.type,
        description=obj_in.description,
        date=obj_in.date
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return FinancialDataSchema.from_orm(db_obj)

def get_financial_data(
    db: Session,
    user_id: int,
    skip: int = 0,
    limit: int = 100,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    category: Optional[str] = None,
    type: Optional[str] = None
) -> List[FinancialDataSchema]:
    """Get financial data with filters"""
    query = db.query(FinancialData).filter(FinancialData.user_id == user_id)
    
    if start_date:
        query = query.filter(FinancialData.date >= start_date)
    if end_date:
        query = query.filter(FinancialData.date <= end_date)
    if category:
        query = query.filter(FinancialData.category == category)
    if type:
        query = query.filter(FinancialData.type == type)
    
    return [FinancialDataSchema.from_orm(obj) for obj in query.order_by(FinancialData.date.desc()).offset(skip).limit(limit).all()]

def get_financial_data_by_id(
    db: Session,
    data_id: int
) -> Optional[FinancialDataSchema]:
    """Get financial data by ID"""
    obj = db.query(FinancialData).filter(FinancialData.id == data_id).first()
    return FinancialDataSchema.from_orm(obj) if obj else None

def update_financial_data(
    db: Session,
    db_obj: FinancialData,
    obj_in: FinancialDataUpdate
) -> FinancialDataSchema:
    """Update financial data"""
    update_data = obj_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_obj, field, value)
    
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return FinancialDataSchema.from_orm(db_obj)

def delete_financial_data(
    db: Session,
    data_id: int
) -> FinancialDataSchema:
    """Delete financial data"""
    obj = db.query(FinancialData).get(data_id)
    db.delete(obj)
    db.commit()
    return FinancialDataSchema.from_orm(obj)

def create_financial_metadata(
    db: Session,
    obj_in: FinancialMetadataCreate
) -> FinancialMetadataSchema:
    """Create new financial metadata"""
    db_obj = FinancialMetadata(
        user_id=obj_in.user_id,
        key=obj_in.key,
        value=obj_in.value,
        category=obj_in.category,
        description=obj_in.description
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return FinancialMetadataSchema.from_orm(db_obj)

def get_financial_metadata(
    db: Session,
    user_id: int,
    skip: int = 0,
    limit: int = 100,
    category: Optional[str] = None
) -> List[FinancialMetadataSchema]:
    """Get financial metadata with filters"""
    query = db.query(FinancialMetadata).filter(FinancialMetadata.user_id == user_id)
    
    if category:
        query = query.filter(FinancialMetadata.category == category)
    
    return [FinancialMetadataSchema.from_orm(obj) for obj in query.offset(skip).limit(limit).all()]

def get_financial_metadata_by_id(
    db: Session,
    metadata_id: int
) -> Optional[FinancialMetadataSchema]:
    """Get financial metadata by ID"""
    obj = db.query(FinancialMetadata).filter(FinancialMetadata.id == metadata_id).first()
    return FinancialMetadataSchema.from_orm(obj) if obj else None

def update_financial_metadata(
    db: Session,
    db_obj: FinancialMetadata,
    obj_in: FinancialMetadataUpdate
) -> FinancialMetadataSchema:
    """Update financial metadata"""
    update_data = obj_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_obj, field, value)
    
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return FinancialMetadataSchema.from_orm(db_obj)

def delete_financial_metadata(
    db: Session,
    metadata_id: int
) -> FinancialMetadataSchema:
    """Delete financial metadata"""
    obj = db.query(FinancialMetadata).get(metadata_id)
    db.delete(obj)
    db.commit()
    return FinancialMetadataSchema.from_orm(obj)

def get_financial_summary(
    db: Session,
    user_id: int,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
) -> FinancialSummary:
    """Get financial summary including totals and trends"""
    query = db.query(FinancialData).filter(FinancialData.user_id == user_id)
    
    if start_date:
        query = query.filter(FinancialData.date >= start_date)
    if end_date:
        query = query.filter(FinancialData.date <= end_date)
    
    # Calculate totals
    revenue = query.filter(FinancialData.type == "revenue").with_entities(
        func.sum(FinancialData.amount)
    ).scalar() or 0
    
    expenses = query.filter(FinancialData.type == "expense").with_entities(
        func.sum(FinancialData.amount)
    ).scalar() or 0
    
    net_profit = revenue - expenses
    profit_margin = (net_profit / revenue * 100) if revenue > 0 else 0
    
    # Get category totals
    category_totals = {}
    for category in db.query(FinancialData.category).distinct():
        category_revenue = query.filter(
            FinancialData.category == category[0],
            FinancialData.type == "revenue"
        ).with_entities(func.sum(FinancialData.amount)).scalar() or 0
        
        category_expenses = query.filter(
            FinancialData.category == category[0],
            FinancialData.type == "expense"
        ).with_entities(func.sum(FinancialData.amount)).scalar() or 0
        
        category_totals[category[0]] = {
            "revenue": category_revenue,
            "expenses": category_expenses,
            "net": category_revenue - category_expenses
        }
    
    # Get monthly trends
    monthly_trends = []
    monthly_data = query.with_entities(
        func.date_trunc('month', FinancialData.date).label('month'),
        FinancialData.type,
        func.sum(FinancialData.amount).label('amount')
    ).group_by('month', FinancialData.type).order_by('month').all()
    
    current_month = None
    month_data = {}
    for month, type_, amount in monthly_data:
        if month != current_month:
            if current_month and month_data:
                monthly_trends.append({
                    "month": current_month,
                    "revenue": month_data.get("revenue", 0),
                    "expenses": month_data.get("expense", 0),
                    "net": month_data.get("revenue", 0) - month_data.get("expense", 0)
                })
            current_month = month
            month_data = {}
        month_data[type_] = amount
    
    if current_month and month_data:
        monthly_trends.append({
            "month": current_month,
            "revenue": month_data.get("revenue", 0),
            "expenses": month_data.get("expense", 0),
            "net": month_data.get("revenue", 0) - month_data.get("expense", 0)
        })
    
    return FinancialSummary(
        total_revenue=revenue,
        total_expenses=expenses,
        net_profit=net_profit,
        profit_margin=profit_margin,
        category_totals=category_totals,
        monthly_trends=monthly_trends
    ) 