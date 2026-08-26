from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database.session import get_db
from app.models.location import District, Taluk

router = APIRouter(prefix="", tags=["Locations"])

@router.get("/districts")
def get_all_districts(db: Session = Depends(get_db)):
    districts = db.query(District).order_by(District.name_en.asc()).all()
    return [
        {
            "id": d.id,
            "name_en": d.name_en,
            "name_ta": d.name_ta,
            "latitude": d.latitude,
            "longitude": d.longitude,
            "taluk_count": len(d.taluks)
        }
        for d in districts
    ]

@router.get("/taluks/{district_id}")
def get_taluks_by_district(district_id: int, db: Session = Depends(get_db)):
    district = db.query(District).filter(District.id == district_id).first()
    if not district:
        raise HTTPException(status_code=404, detail="District not found")
    
    taluks = db.query(Taluk).filter(Taluk.district_id == district_id).order_by(Taluk.name_en.asc()).all()
    return [
        {
            "id": t.id,
            "district_id": t.district_id,
            "name_en": t.name_en,
            "name_ta": t.name_ta,
            "latitude": t.latitude,
            "longitude": t.longitude
        }
        for t in taluks
    ]
