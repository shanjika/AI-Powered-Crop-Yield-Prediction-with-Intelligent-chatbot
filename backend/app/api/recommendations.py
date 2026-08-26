from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.user import User
from app.models.prediction import Prediction
from app.services.auth_service import get_current_user
from app.services.weather_service import get_live_weather
from app.services.recommendation_service import generate_cultivation_timeline, generate_what_to_do_now

router = APIRouter(prefix="/recommendations", tags=["Recommendations"])

@router.get("/{prediction_id}")
async def get_cultivation_action_plan(
    prediction_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    prediction = db.query(Prediction).filter(
        Prediction.id == prediction_id,
        Prediction.user_id == current_user.id
    ).first()

    if not prediction:
        raise HTTPException(status_code=404, detail="Prediction record not found.")

    crop = prediction.crop
    timeline = generate_cultivation_timeline(crop)

    # Fetch fresh live weather for dynamic alerts
    lat = prediction.taluk.latitude if prediction.taluk else prediction.district.latitude
    lon = prediction.taluk.longitude if prediction.taluk else prediction.district.longitude
    weather = await get_live_weather(lat, lon)

    what_now = generate_what_to_do_now(crop, weather)

    return {
        "prediction_id": prediction.id,
        "crop_name_en": crop.name_en,
        "crop_name_ta": crop.name_ta,
        "duration_days": crop.duration_days,
        "pattam": prediction.pattam,
        "district": prediction.district.name_en,
        "what_should_i_do_now": what_now,
        "timeline_stages": timeline,
        "fertilizer_guide_en": {
            "basal": f"5-10 tons FYM + 100% Single Super Phosphate ({crop.p_req} kg/ha) + 25% Urea.",
            "vegetative_top_dressing": f"40% Urea ({crop.n_req * 0.4:.0f} kg/ha) with irrigation at 25-30 days.",
            "flowering_booster": f"35% Urea + Muriate of Potash ({crop.k_req} kg/ha) at 45-50 days.",
            "foliar_spray": f"1% TNAU {crop.name_en} Special / Pulse Wonder during flower initiation."
        },
        "fertilizer_guide_ta": {
            "basal": f"5-10 டன் மக்கிய தொழுவுரம் + முழு அளவு சூப்பர் பாஸ்பேட் ({crop.p_req} kg/ha) + 25% யூரியா.",
            "vegetative_top_dressing": f"40% யூரியா ({crop.n_req * 0.4:.0f} kg/ha) பாசனத்துடன் 25-30 நாட்களில்.",
            "flowering_booster": f"35% யூரியா + பொட்டாஷ் ({crop.k_req} kg/ha) 45-50 நாட்களில்.",
            "foliar_spray": f"1% தமிழ்நாடு வேளாண் பல்கலைக்கழக சிறப்பு நுண்ணூட்டம் பூக்கும் தருணத்தில்."
        }
    }

@router.get("/now/{prediction_id}")
async def get_immediate_actions_only(
    prediction_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    prediction = db.query(Prediction).filter(
        Prediction.id == prediction_id,
        Prediction.user_id == current_user.id
    ).first()

    if not prediction:
        raise HTTPException(status_code=404, detail="Prediction not found.")

    crop = prediction.crop
    lat = prediction.taluk.latitude if prediction.taluk else prediction.district.latitude
    lon = prediction.taluk.longitude if prediction.taluk else prediction.district.longitude
    weather = await get_live_weather(lat, lon)

    return generate_what_to_do_now(crop, weather)
