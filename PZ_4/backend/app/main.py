from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.api import api_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Подключаем роутеры
app.include_router(api_router, prefix=settings.API_V1_STR)

# Базовые маршруты
@app.get("/")
def root():
    return {"message": "Welcome to Financial Analysis API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"} 