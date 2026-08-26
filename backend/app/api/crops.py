from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.database.session import get_db
from app.models.crop import Crop
from app.models.pattam import Pattam

router = APIRouter(prefix="", tags=["Crops & Pattams"])

@router.get("/crops")
def get_all_crops(
    category: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Crop)
    if category:
        query = query.filter(Crop.category == category)
    if search:
        search_fmt = f"%{search}%"
        query = query.filter((Crop.name_en.ilike(search_fmt)) | (Crop.name_ta.ilike(search_fmt)))
    
    crops = query.order_by(Crop.name_en.asc()).all()
    return [
        {
            "id": c.id,
            "name_en": c.name_en,
            "name_ta": c.name_ta,
            "category": c.category,
            "duration_days": c.duration_days,
            "ideal_soil": c.ideal_soil,
            "ideal_soil_ta": c.ideal_soil_ta,
            "min_temp": c.min_temp,
            "max_temp": c.max_temp,
            "min_rainfall": c.min_rainfall,
            "max_rainfall": c.max_rainfall,
            "water_req_level": c.water_req_level,
            "water_req_level_ta": c.water_req_level_ta,
            "typical_yield_min_acre": c.typical_yield_min_acre,
            "typical_yield_max_acre": c.typical_yield_max_acre,
            "n_req": c.n_req,
            "p_req": c.p_req,
            "k_req": c.k_req
        }
        for c in crops
    ]

@router.get("/crops/{crop_id}")
def get_crop_details(crop_id: int, db: Session = Depends(get_db)):
    crop = db.query(Crop).filter(Crop.id == crop_id).first()
    if not crop:
        raise HTTPException(status_code=404, detail="Crop not found")
    return {
        "id": crop.id,
        "name_en": crop.name_en,
        "name_ta": crop.name_ta,
        "category": crop.category,
        "duration_days": crop.duration_days,
        "ideal_soil": crop.ideal_soil,
        "ideal_soil_ta": crop.ideal_soil_ta,
        "min_temp": crop.min_temp,
        "max_temp": crop.max_temp,
        "min_rainfall": crop.min_rainfall,
        "max_rainfall": crop.max_rainfall,
        "water_req_level": crop.water_req_level,
        "water_req_level_ta": crop.water_req_level_ta,
        "n_req": crop.n_req,
        "p_req": crop.p_req,
        "k_req": crop.k_req,
        "ideal_ph_min": crop.ideal_ph_min,
        "ideal_ph_max": crop.ideal_ph_max,
        "typical_yield_min_acre": crop.typical_yield_min_acre,
        "typical_yield_max_acre": crop.typical_yield_max_acre,
        "harvest_indicators_en": crop.harvest_indicators_en,
        "harvest_indicators_ta": crop.harvest_indicators_ta,
        "major_pests_en": crop.major_pests_en,
        "major_pests_ta": crop.major_pests_ta,
        "major_diseases_en": crop.major_diseases_en,
        "major_diseases_ta": crop.major_diseases_ta
    }

@router.get("/pattams")
def get_all_pattams(db: Session = Depends(get_db)):
    pattams = db.query(Pattam).all()
    return [
        {
            "id": p.id,
            "name_en": p.name_en,
            "name_ta": p.name_ta,
            "months_en": p.months_en,
            "months_ta": p.months_ta,
            "description_en": p.description_en,
            "description_ta": p.description_ta,
            "recommended_crops_en": p.recommended_crops_en,
            "recommended_crops_ta": p.recommended_crops_ta
        }
        for p in pattams
    ]
