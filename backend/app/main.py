import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.database.session import engine, SessionLocal, Base
from app.database.seed_data import seed_database
import app.models  # Ensure all SQLAlchemy models are imported

from app.api.auth import router as auth_router
from app.api.locations import router as locations_router
from app.api.crops import router as crops_router
from app.api.weather import router as weather_router
from app.api.soil import router as soil_router
from app.api.prediction import router as prediction_router
from app.api.recommendations import router as recommendations_router
from app.api.chatbot import router as chatbot_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 1. Initialize Database Tables
    Base.metadata.create_all(bind=engine)
    
    # 2. Seed Data if empty
    db = SessionLocal()
    try:
        seed_database(db)
    finally:
        db.close()
    
    yield

app = FastAPI(
    title="AI Powered Crop Yield Prediction API - Tamil Nadu",
    description="Smart Agricultural Decision Support & Yield Prediction for Tamil Nadu Farmers",
    version="2.0.0",
    lifespan=lifespan
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global Exception Handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    print(f"[API ERROR] {request.method} {request.url.path} -> {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Something went wrong while processing your request. Please try again.",
            "error_type": type(exc).__name__
        }
    )

# Static file serving for uploads
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

# Include Routers under /api
api_prefix = settings.API_V1_STR
app.include_router(auth_router, prefix=api_prefix)
app.include_router(locations_router, prefix=api_prefix)
app.include_router(crops_router, prefix=api_prefix)
app.include_router(weather_router, prefix=api_prefix)
app.include_router(soil_router, prefix=api_prefix)
app.include_router(prediction_router, prefix=api_prefix)
app.include_router(recommendations_router, prefix=api_prefix)
app.include_router(chatbot_router, prefix=api_prefix)

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "service": "AI Powered Crop Yield Prediction API (Tamil Nadu)",
        "version": "2.0.0"
    }
