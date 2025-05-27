from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Импортируем все модели здесь, чтобы Alembic мог их найти
# from app.models.user import User  # noqa
from app.db.base_class import Base  # noqa
from app.models.user import User  # noqa
from app.models.financial_data import FinancialData  # noqa
from app.models.analysis_result import AnalysisResult  # noqa 