from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class PredictionRequest(BaseModel):
    district_id: int
    taluk_id: int
    crop_id: int
    pattam: str
    land_area_acres: float = Field(..., gt=0.0, le=1000.0)
    soil_type: str = "Red Loam"
    irrigation_type: str = "Well / Tube Well"
    
    # Soil inputs (either from OCR or manual)
    soil_ph: float = Field(6.8, ge=3.5, le=11.0)
    soil_n: float = Field(250.0, ge=10.0, le=1500.0)
    soil_p: float = Field(18.0, ge=1.0, le=500.0)
    soil_k: float = Field(200.0, ge=10.0, le=1500.0)
    soil_ec: Optional[float] = 0.45
    soil_organic_carbon: Optional[float] = 0.65
    soil_report_id: Optional[int] = None

class FactorDetail(BaseModel):
    name_en: str
    name_ta: str
    impact: str  # positive, negative, neutral
    score: int
    detail_en: str
    detail_ta: str

class PredictionResponse(BaseModel):
    id: int
    crop_id: int
    crop_name_en: str
    crop_name_ta: str
    district_name_en: str
    district_name_ta: str
    taluk_name_en: str
    taluk_name_ta: str
    pattam: str
    land_area_acres: float
    soil_type: str
    
    # Environmental snapshot
    temperature: float
    humidity: float
    rainfall_mm: float
    weather_condition: str
    
    # Soil snapshot
    soil_ph: float
    soil_n: float
    soil_p: float
    soil_k: float
    
    # ML Output
    predicted_yield_per_acre: float
    total_production_kg: float
    confidence_score: float
    typical_yield_min_acre: float
    typical_yield_max_acre: float
    benchmark_diff_pct: float
    
    factors: List[FactorDetail]
    explanation_en: str
    explanation_ta: str
    created_at: str

    class Config:
        from_attributes = True

class PredictionHistoryItem(BaseModel):
    id: int
    crop_name_en: str
    crop_name_ta: str
    district_name_en: str
    taluk_name_en: str
    pattam: str
    land_area_acres: float
    predicted_yield_per_acre: float
    total_production_kg: float
    created_at: str

    class Config:
        from_attributes = True
