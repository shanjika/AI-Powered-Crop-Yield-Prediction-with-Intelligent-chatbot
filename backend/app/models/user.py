import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database.session import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(255), nullable=False)
    mobile_number = Column(String(20), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=True)
    hashed_password = Column(String(255), nullable=False)
    preferred_language = Column(String(10), default="ta")  # "ta" or "en"
    district_id = Column(Integer, ForeignKey("districts.id"), nullable=True)
    taluk_id = Column(Integer, ForeignKey("taluks.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    # Relationships
    district = relationship("District", back_populates="users")
    taluk = relationship("Taluk", back_populates="users")
    predictions = relationship("Prediction", back_populates="user", cascade="all, delete-orphan")
    soil_reports = relationship("SoilReport", back_populates="user", cascade="all, delete-orphan")
    chat_sessions = relationship("ChatSession", back_populates="user", cascade="all, delete-orphan")
