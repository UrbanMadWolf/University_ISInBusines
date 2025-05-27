from fastapi import APIRouter

from app.api.v1.endpoints import (
    auth,
    users,
    financial,
    analytics,
    forecasting,
    recommendations
)

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(financial.router, prefix="/financial", tags=["financial"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
api_router.include_router(forecasting.router, prefix="/forecasting", tags=["forecasting"])
api_router.include_router(recommendations.router, prefix="/recommendations", tags=["recommendations"]) 