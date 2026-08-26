from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.location import District, Taluk
from app.services.weather_service import get_live_weather

router = APIRouter(prefix="/weather", tags=["Weather"])

@router.get("/{district_id}/{taluk_id}")
async def get_weather_for_location(
    district_id: int,
    taluk_id: int,
    db: Session = Depends(get_db)
):
    district = db.query(District).filter(District.id == district_id).first()
    if not district:
        raise HTTPException(status_code=404, detail="District not found")
        
    taluk = db.query(Taluk).filter(Taluk.id == taluk_id, Taluk.district_id == district_id).first()
    
    # Use taluk coordinates or district coordinates
    lat = taluk.latitude if taluk else district.latitude
    lon = taluk.longitude if taluk else district.longitude
    loc_name = f"{taluk.name_en}, {district.name_en}" if taluk else district.name_en

    weather_data = await get_live_weather(lat, lon, location_name=loc_name)
    weather_data["district_name_en"] = district.name_en
    weather_data["district_name_ta"] = district.name_ta
    weather_data["taluk_name_en"] = taluk.name_en if taluk else ""
    weather_data["taluk_name_ta"] = taluk.name_ta if taluk else ""
    
    return weather_data
