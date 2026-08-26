from sqlalchemy import Column, Integer, String, Float, Text
from sqlalchemy.orm import relationship
from app.database.session import Base

class Crop(Base):
    __tablename__ = "crops"

    id = Column(Integer, primary_key=True, index=True)
    name_en = Column(String(100), unique=True, index=True, nullable=False)
    name_ta = Column(String(100), nullable=False)
    category = Column(String(50), nullable=False)  # Cereals, Pulses, Oilseeds, Commercial, Fruits, Vegetables, Spices
    duration_days = Column(Integer, nullable=False)  # e.g., 120
    ideal_soil = Column(String(255), nullable=False)
    ideal_soil_ta = Column(String(255), nullable=False)
    min_temp = Column(Float, nullable=False)
    max_temp = Column(Float, nullable=False)
    min_rainfall = Column(Float, nullable=False)
    max_rainfall = Column(Float, nullable=False)
    water_req_level = Column(String(50), nullable=False)  # Low, Medium, High
    water_req_level_ta = Column(String(50), nullable=False)
    n_req = Column(Float, nullable=False)  # kg/ha or kg/acre benchmark
    p_req = Column(Float, nullable=False)
    k_req = Column(Float, nullable=False)
    ideal_ph_min = Column(Float, default=6.0)
    ideal_ph_max = Column(Float, default=7.5)
    typical_yield_min_acre = Column(Float, nullable=False)  # kg/acre
    typical_yield_max_acre = Column(Float, nullable=False)  # kg/acre
    harvest_indicators_en = Column(Text, nullable=False)
    harvest_indicators_ta = Column(Text, nullable=False)
    major_pests_en = Column(Text, nullable=False)
    major_pests_ta = Column(Text, nullable=False)
    major_diseases_en = Column(Text, nullable=False)
    major_diseases_ta = Column(Text, nullable=False)

    predictions = relationship("Prediction", back_populates="crop")
