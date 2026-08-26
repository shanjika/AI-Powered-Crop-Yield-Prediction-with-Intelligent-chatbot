import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from app.database.session import Base

class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    crop_id = Column(Integer, ForeignKey("crops.id"), nullable=False, index=True)
    district_id = Column(Integer, ForeignKey("districts.id"), nullable=False, index=True)
    taluk_id = Column(Integer, ForeignKey("taluks.id"), nullable=False, index=True)
    soil_report_id = Column(Integer, ForeignKey("soil_reports.id"), nullable=True)

    pattam = Column(String(100), nullable=False)
    land_area_acres = Column(Float, nullable=False)
    soil_type = Column(String(100), nullable=False)
    irrigation_type = Column(String(100), default="Well / Tube Well")
    sowing_date = Column(DateTime, default=datetime.datetime.utcnow)

    # Environmental snapshot at prediction time
    temperature = Column(Float, nullable=False)
    humidity = Column(Float, nullable=False)
    rainfall_mm = Column(Float, nullable=False)
    weather_condition = Column(String(100), default="Clear")

    # Soil nutrients snapshot
    soil_ph = Column(Float, nullable=False)
    soil_n = Column(Float, nullable=False)
    soil_p = Column(Float, nullable=False)
    soil_k = Column(Float, nullable=False)
    soil_ec = Column(Float, default=0.5)
    soil_organic_carbon = Column(Float, default=0.6)

    # ML Output
    predicted_yield_per_acre = Column(Float, nullable=False)  # kg/acre
    total_production_kg = Column(Float, nullable=False)       # kg
    confidence_score = Column(Float, default=0.88)
    
    # Factor contributions (Positive and Limiting factors)
    factors_summary = Column(JSON, default=dict)
    explanation_en = Column(Text, nullable=False)
    explanation_ta = Column(Text, nullable=False)

    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="predictions")
    crop = relationship("Crop", back_populates="predictions")
    district = relationship("District", back_populates="predictions")
    taluk = relationship("Taluk", back_populates="predictions")
    soil_report = relationship("SoilReport", back_populates="predictions")
    chat_sessions = relationship("ChatSession", back_populates="prediction", cascade="all, delete-orphan")
