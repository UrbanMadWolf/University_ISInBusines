from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime

from app.api import deps
from app.models.user import User
from app.models.financial_data import FinancialData as FinancialDataModel
from app.schemas.financial import (
    FinancialDataCreate,
    FinancialDataUpdate,
    FinancialData as FinancialDataSchema,
    FinancialMetadataCreate,
    FinancialMetadataUpdate,
    FinancialMetadata,
    FinancialSummary
)
from app.crud import financial as crud_financial

router = APIRouter()

@router.post("/data", response_model=FinancialDataSchema)
def create_financial_data(
    *,
    db: Session = Depends(deps.get_db),
    data_in: FinancialDataCreate,
    current_user: User = Depends(deps.get_current_user)
) -> FinancialDataSchema:
    """
    Create new financial data.
    """
    data_in.user_id = current_user.id
    return crud_financial.create_financial_data(db=db, obj_in=data_in)

@router.get("/data", response_model=List[FinancialDataSchema])
def get_financial_data(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
    skip: int = 0,
    limit: int = 100,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    category: Optional[str] = None,
    type: Optional[str] = None
) -> List[FinancialDataSchema]:
    """
    Retrieve financial data with optional filters.
    """
    return crud_financial.get_financial_data(
        db=db,
        user_id=current_user.id,
        skip=skip,
        limit=limit,
        start_date=start_date,
        end_date=end_date,
        category=category,
        type=type
    )

@router.put("/data/{data_id}", response_model=FinancialDataSchema)
def update_financial_data(
    *,
    db: Session = Depends(deps.get_db),
    data_id: int,
    data_in: FinancialDataUpdate,
    current_user: User = Depends(deps.get_current_user)
) -> FinancialDataSchema:
    """
    Update financial data.
    """
    data = crud_financial.get_financial_data_by_id(db=db, data_id=data_id)
    if not data:
        raise HTTPException(status_code=404, detail="Financial data not found")
    if data.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return crud_financial.update_financial_data(db=db, db_obj=data, obj_in=data_in)

@router.delete("/data/{data_id}", response_model=FinancialDataSchema)
def delete_financial_data(
    *,
    db: Session = Depends(deps.get_db),
    data_id: int,
    current_user: User = Depends(deps.get_current_user)
) -> FinancialDataSchema:
    """
    Delete financial data.
    """
    data = crud_financial.get_financial_data_by_id(db=db, data_id=data_id)
    if not data:
        raise HTTPException(status_code=404, detail="Financial data not found")
    if data.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return crud_financial.delete_financial_data(db=db, data_id=data_id)

@router.get("/summary", response_model=FinancialSummary)
def get_financial_summary(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
) -> FinancialSummary:
    """
    Get financial summary including totals and trends.
    """
    return crud_financial.get_financial_summary(
        db=db,
        user_id=current_user.id,
        start_date=start_date,
        end_date=end_date
    )

@router.post("/metadata", response_model=FinancialMetadata)
def create_financial_metadata(
    *,
    db: Session = Depends(deps.get_db),
    metadata_in: FinancialMetadataCreate,
    current_user: User = Depends(deps.get_current_user)
) -> FinancialMetadata:
    """
    Create new financial metadata.
    """
    metadata_in.user_id = current_user.id
    return crud_financial.create_financial_metadata(db=db, obj_in=metadata_in)

@router.get("/metadata", response_model=List[FinancialMetadata])
def get_financial_metadata(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
    skip: int = 0,
    limit: int = 100,
    category: Optional[str] = None
) -> List[FinancialMetadata]:
    """
    Retrieve financial metadata with optional filters.
    """
    return crud_financial.get_financial_metadata(
        db=db,
        user_id=current_user.id,
        skip=skip,
        limit=limit,
        category=category
    )

@router.put("/metadata/{metadata_id}", response_model=FinancialMetadata)
def update_financial_metadata(
    *,
    db: Session = Depends(deps.get_db),
    metadata_id: int,
    metadata_in: FinancialMetadataUpdate,
    current_user: User = Depends(deps.get_current_user)
) -> FinancialMetadata:
    """
    Update financial metadata.
    """
    metadata = crud_financial.get_financial_metadata_by_id(db=db, metadata_id=metadata_id)
    if not metadata:
        raise HTTPException(status_code=404, detail="Financial metadata not found")
    if metadata.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return crud_financial.update_financial_metadata(db=db, db_obj=metadata, obj_in=metadata_in)

@router.delete("/metadata/{metadata_id}", response_model=FinancialMetadata)
def delete_financial_metadata(
    *,
    db: Session = Depends(deps.get_db),
    metadata_id: int,
    current_user: User = Depends(deps.get_current_user)
) -> FinancialMetadata:
    """
    Delete financial metadata.
    """
    metadata = crud_financial.get_financial_metadata_by_id(db=db, metadata_id=metadata_id)
    if not metadata:
        raise HTTPException(status_code=404, detail="Financial metadata not found")
    if metadata.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return crud_financial.delete_financial_metadata(db=db, metadata_id=metadata_id) 