from typing import Optional, List
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash, verify_password

class UserService:
    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        return self.db.query(User).filter(User.email == email).first()

    def get_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        return self.db.query(User).filter(User.id == user_id).first()

    def create(self, user_data: UserCreate) -> Optional[User]:
        """Create new user"""
        try:
            db_user = User(
                email=user_data.email,
                hashed_password=get_password_hash(user_data.password),
                full_name=user_data.full_name,
                is_active=True,
                is_superuser=False
            )
            self.db.add(db_user)
            self.db.commit()
            self.db.refresh(db_user)
            return db_user
        except IntegrityError:
            self.db.rollback()
            return None

    def update(self, user_id: int, user_data: UserUpdate) -> Optional[User]:
        """Update user data"""
        db_user = self.get_by_id(user_id)
        if not db_user:
            return None

        update_data = user_data.dict(exclude_unset=True)
        if "password" in update_data:
            update_data["hashed_password"] = get_password_hash(update_data.pop("password"))

        for field, value in update_data.items():
            setattr(db_user, field, value)

        try:
            self.db.add(db_user)
            self.db.commit()
            self.db.refresh(db_user)
            return db_user
        except IntegrityError:
            self.db.rollback()
            return None

    def authenticate(self, email: str, password: str) -> Optional[User]:
        """Authenticate user"""
        user = self.get_by_email(email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def is_active(self, user: User) -> bool:
        """Check if user is active"""
        return user.is_active

    def is_superuser(self, user: User) -> bool:
        """Check if user is superuser"""
        return user.is_superuser

    def list_users(
        self,
        skip: int = 0,
        limit: int = 100,
        is_active: Optional[bool] = None
    ) -> List[User]:
        """List users with optional filters"""
        query = self.db.query(User)
        if is_active is not None:
            query = query.filter(User.is_active == is_active)
        return query.offset(skip).limit(limit).all()

    def delete(self, user_id: int) -> bool:
        """Delete user"""
        user = self.get_by_id(user_id)
        if not user:
            return False
        try:
            self.db.delete(user)
            self.db.commit()
            return True
        except Exception:
            self.db.rollback()
            return False

    def update_last_login(self, user_id: int) -> Optional[User]:
        """Update user's last login timestamp"""
        user = self.get_by_id(user_id)
        if not user:
            return None
        user.last_login = datetime.utcnow()
        try:
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
            return user
        except Exception:
            self.db.rollback()
            return None

    def change_password(self, user_id: int, current_password: str, new_password: str) -> bool:
        """Change user password"""
        user = self.get_by_id(user_id)
        if not user:
            return False
        if not verify_password(current_password, user.hashed_password):
            return False
        user.hashed_password = get_password_hash(new_password)
        try:
            self.db.add(user)
            self.db.commit()
            return True
        except Exception:
            self.db.rollback()
            return False 