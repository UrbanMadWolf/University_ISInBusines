import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional

from app.schemas.financial import (
    FinancialDataCreate,
    FinancialDataUpdate,
    FinancialMetadataCreate,
    FinancialMetadataUpdate,
    FinancialData,
    FinancialMetadata
)

def random_amount() -> float:
    """Generate random amount between 100 and 10000"""
    return round(random.uniform(100, 10000), 2)

def random_date(start_date: datetime = None) -> datetime:
    """Generate random date within last year"""
    if start_date is None:
        start_date = datetime.now() - timedelta(days=365)
    end_date = datetime.now()
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    return start_date + timedelta(days=random_number_of_days)

def create_test_financial_data(
    user_id: int,
    num_records: int = 1,
    start_date: Optional[datetime] = None
) -> List[Dict]:
    """Create test financial data records"""
    if start_date is None:
        start_date = datetime.now() - timedelta(days=30)
    
    categories = ["revenue", "expenses", "investment", "loan", "other"]
    types = ["income", "expense", "transfer"]
    sources = ["sales", "salary", "investment", "loan", "other"]
    statuses = ["completed", "pending", "failed"]
    
    data = []
    for i in range(num_records):
        record = {
            "date": (start_date + timedelta(days=i)).isoformat(),
            "amount": round(random.uniform(100.0, 10000.0), 2),
            "category": random.choice(categories),
            "description": f"Test transaction {i+1}",
            "type": random.choice(types),
            "source": random.choice(sources),
            "status": random.choice(statuses),
            "user_id": user_id
        }
        data.append(record)
    
    return data

def create_test_financial_metadata(
    user_id: int,
    num_records: int = 1
) -> List[Dict]:
    """Create test financial metadata records"""
    metadata_keys = [
        "business_type",
        "industry",
        "fiscal_year_start",
        "currency",
        "tax_rate"
    ]
    metadata_values = {
        "business_type": ["retail", "service", "manufacturing", "technology"],
        "industry": ["retail", "technology", "healthcare", "finance"],
        "fiscal_year_start": ["01-01", "04-01", "07-01", "10-01"],
        "currency": ["USD", "EUR", "GBP", "JPY"],
        "tax_rate": ["10%", "15%", "20%", "25%"]
    }
    
    data = []
    for _ in range(num_records):
        key = random.choice(metadata_keys)
        record = {
            "key": key,
            "value": random.choice(metadata_values[key]),
            "category": "business_info",
            "description": f"Test metadata for {key}",
            "user_id": user_id
        }
        data.append(record)
    
    return data

def create_test_financial_data_schema(
    user_id: int,
    num_records: int = 1
) -> List[FinancialDataCreate]:
    """Create test financial data schema objects"""
    data = create_test_financial_data(user_id, num_records)
    return [FinancialDataCreate(**record) for record in data]

def create_test_financial_metadata_schema(
    user_id: int,
    num_records: int = 1
) -> List[FinancialMetadataCreate]:
    """Create test financial metadata schema objects"""
    data = create_test_financial_metadata(user_id, num_records)
    return [FinancialMetadataCreate(**record) for record in data]

def create_test_financial_summary(
    user_id: int,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
) -> Dict:
    """Create test financial summary data"""
    if start_date is None:
        start_date = datetime.now() - timedelta(days=30)
    if end_date is None:
        end_date = datetime.now()
    
    # Generate test data
    data = create_test_financial_data(
        user_id,
        num_records=30,
        start_date=start_date
    )
    
    # Calculate summary metrics
    total_revenue = sum(
        record["amount"]
        for record in data
        if record["type"] == "income"
    )
    total_expenses = sum(
        record["amount"]
        for record in data
        if record["type"] == "expense"
    )
    net_profit = total_revenue - total_expenses
    
    # Calculate category totals
    category_totals = {}
    for record in data:
        category = record["category"]
        if category not in category_totals:
            category_totals[category] = 0
        category_totals[category] += record["amount"]
    
    # Generate monthly trends
    monthly_trends = []
    current_date = start_date
    while current_date <= end_date:
        month_data = [
            record for record in data
            if record["date"].startswith(current_date.strftime("%Y-%m"))
        ]
        monthly_trends.append({
            "month": current_date.strftime("%Y-%m"),
            "revenue": sum(
                record["amount"]
                for record in month_data
                if record["type"] == "income"
            ),
            "expenses": sum(
                record["amount"]
                for record in month_data
                if record["type"] == "expense"
            )
        })
        current_date = (current_date.replace(day=1) + timedelta(days=32)).replace(day=1)
    
    return {
        "total_revenue": total_revenue,
        "total_expenses": total_expenses,
        "net_profit": net_profit,
        "profit_margin": (net_profit / total_revenue * 100) if total_revenue > 0 else 0,
        "category_totals": category_totals,
        "monthly_trends": monthly_trends
    } 