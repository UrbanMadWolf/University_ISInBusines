from sqlalchemy.orm import Session
from app.core.config import settings
from app.db.base import Base  # Импортируем Base из base.py
from app.db.session import engine
from app.models.user import User
from app.models.financial_data import FinancialData
from app.core.security import get_password_hash

def init_db(db: Session) -> None:
    # Создаем таблицы
    Base.metadata.create_all(bind=engine)
    
    # Создаем суперпользователя, если его нет
    user = db.query(User).filter(User.email == "admin@example.com").first()
    if not user:
        user = User(
            email="admin@example.com",
            hashed_password=get_password_hash("admin"),
            is_superuser=True,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        
        # Add some sample financial data
        sample_data = [
            FinancialData(
                user_id=user.id,
                amount=1000.0,
                category="sales",
                type="revenue",
                description="Monthly sales",
                date="2024-01-01"
            ),
            FinancialData(
                user_id=user.id,
                amount=500.0,
                category="operating",
                type="expense",
                description="Operating expenses",
                date="2024-01-01"
            ),
        ]
        db.add_all(sample_data)
        db.commit() 