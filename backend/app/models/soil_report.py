import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from app.database.session import Base

class SoilReport(Base):
    __tablename__ = "soil_reports"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    file_name = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_type = Column(String(50), nullable=False)  # pdf, image/jpeg, etc.
    
    # Extracted or manually corrected soil parameters
    soil_type = Column(String(100), default="Red Loam")
    ph = Column(Float, default=6.5)
    ec = Column(Float, default=0.5)  # Electrical conductivity dS/m
    organic_carbon = Column(Float, default=0.65)  # %
    nitrogen = Column(Float, default=240.0)  # kg/ha
    phosphorus = Column(Float, default=18.0)  # kg/ha
    potassium = Column(Float, default=220.0)  # kg/ha
    
    micronutrients = Column(JSON, default=dict)  # Zinc, Iron, Manganese, Copper, Boron
    raw_extracted_text = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="soil_reports")
    predictions = relationship("Prediction", back_populates="soil_report")
