from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.user import User
from app.models.crop import Crop
from app.models.location import District, Taluk
from app.models.prediction import Prediction
from app.schemas.prediction import PredictionRequest, PredictionResponse, PredictionHistoryItem
from app.services.auth_service import get_current_user
from app.services.weather_service import get_live_weather
from app.services.prediction_service import predict_crop_yield

router = APIRouter(prefix="", tags=["Crop Yield Prediction"])

@router.post("/predict", response_model=PredictionResponse)
async def predict_yield(
    req: PredictionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # 1. Validate Crop
    crop = db.query(Crop).filter(Crop.id == req.crop_id).first()
    if not crop:
        raise HTTPException(status_code=404, detail="Selected crop not found.")

    # 2. Validate Location
    district = db.query(District).filter(District.id == req.district_id).first()
    if not district:
        raise HTTPException(status_code=404, detail="Selected district not found.")

    taluk = db.query(Taluk).filter(Taluk.id == req.taluk_id, Taluk.district_id == req.district_id).first()
    if not taluk:
        raise HTTPException(status_code=404, detail="Selected taluk not found for this district.")

    # 3. Fetch real-time weather
    lat = taluk.latitude if taluk else district.latitude
    lon = taluk.longitude if taluk else district.longitude
    weather = await get_live_weather(lat, lon)

    # 4. Prepare feature payload for ML model
    ml_inputs = {
        "district": district.name_en,
        "crop": crop.name_en,
        "pattam": req.pattam,
        "soil_type": req.soil_type,
        "irrigation_type": req.irrigation_type,
        "land_area_acres": req.land_area_acres,
        "temperature": weather.get("temperature", 30.0),
        "humidity": weather.get("humidity", 65.0),
        "rainfall_mm": weather.get("rainfall_mm", 0.0),
        "soil_ph": req.soil_ph,
        "soil_n": req.soil_n,
        "soil_p": req.soil_p,
        "soil_k": req.soil_k,
        "soil_ec": req.soil_ec or 0.45,
        "soil_organic_carbon": req.soil_organic_carbon or 0.65
    }

    # 5. Run ML Model Prediction
    pred_result = predict_crop_yield(crop, ml_inputs)

    # 6. Save Prediction Record in Database
    prediction = Prediction(
        user_id=current_user.id,
        crop_id=crop.id,
        district_id=district.id,
        taluk_id=taluk.id,
        soil_report_id=req.soil_report_id,
        pattam=req.pattam,
        land_area_acres=req.land_area_acres,
        soil_type=req.soil_type,
        irrigation_type=req.irrigation_type,
        temperature=ml_inputs["temperature"],
        humidity=ml_inputs["humidity"],
        rainfall_mm=ml_inputs["rainfall_mm"],
        weather_condition=weather.get("condition_en", "Clear Sky"),
        soil_ph=req.soil_ph,
        soil_n=req.soil_n,
        soil_p=req.soil_p,
        soil_k=req.soil_k,
        soil_ec=req.soil_ec or 0.45,
        soil_organic_carbon=req.soil_organic_carbon or 0.65,
        predicted_yield_per_acre=pred_result["predicted_yield_per_acre"],
        total_production_kg=pred_result["total_production_kg"],
        confidence_score=pred_result["confidence_score"],
        factors_summary={"factors": pred_result["factors"]},
        explanation_en=pred_result["explanation_en"],
        explanation_ta=pred_result["explanation_ta"]
    )
    db.add(prediction)
    db.commit()
    db.refresh(prediction)

    return PredictionResponse(
        id=prediction.id,
        crop_id=crop.id,
        crop_name_en=crop.name_en,
        crop_name_ta=crop.name_ta,
        district_name_en=district.name_en,
        district_name_ta=district.name_ta,
        taluk_name_en=taluk.name_en,
        taluk_name_ta=taluk.name_ta,
        pattam=prediction.pattam,
        land_area_acres=prediction.land_area_acres,
        soil_type=prediction.soil_type,
        temperature=prediction.temperature,
        humidity=prediction.humidity,
        rainfall_mm=prediction.rainfall_mm,
        weather_condition=prediction.weather_condition,
        soil_ph=prediction.soil_ph,
        soil_n=prediction.soil_n,
        soil_p=prediction.soil_p,
        soil_k=prediction.soil_k,
        predicted_yield_per_acre=prediction.predicted_yield_per_acre,
        total_production_kg=prediction.total_production_kg,
        confidence_score=prediction.confidence_score,
        typical_yield_min_acre=pred_result["typical_yield_min_acre"],
        typical_yield_max_acre=pred_result["typical_yield_max_acre"],
        benchmark_diff_pct=pred_result["benchmark_diff_pct"],
        factors=pred_result["factors"],
        explanation_en=prediction.explanation_en,
        explanation_ta=prediction.explanation_ta,
        created_at=prediction.created_at.strftime("%Y-%m-%d %H:%M:%S")
    )

@router.get("/predictions")
def get_user_predictions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    preds = db.query(Prediction).filter(
        Prediction.user_id == current_user.id
    ).order_by(Prediction.created_at.desc()).all()

    return [
        {
            "id": p.id,
            "crop_id": p.crop_id,
            "crop_name_en": p.crop.name_en,
            "crop_name_ta": p.crop.name_ta,
            "district_name_en": p.district.name_en,
            "taluk_name_en": p.taluk.name_en if p.taluk else "",
            "pattam": p.pattam,
            "land_area_acres": p.land_area_acres,
            "predicted_yield_per_acre": p.predicted_yield_per_acre,
            "total_production_kg": p.total_production_kg,
            "created_at": p.created_at.strftime("%Y-%m-%d %H:%M")
        }
        for p in preds
    ]

@router.get("/predictions/{prediction_id}", response_model=PredictionResponse)
def get_prediction_by_id(
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
    typical_avg = (crop.typical_yield_min_acre + crop.typical_yield_max_acre) / 2.0
    diff_pct = round(((prediction.predicted_yield_per_acre - typical_avg) / typical_avg) * 100, 1)
    factors = prediction.factors_summary.get("factors", []) if prediction.factors_summary else []

    return PredictionResponse(
        id=prediction.id,
        crop_id=crop.id,
        crop_name_en=crop.name_en,
        crop_name_ta=crop.name_ta,
        district_name_en=prediction.district.name_en,
        district_name_ta=prediction.district.name_ta,
        taluk_name_en=prediction.taluk.name_en if prediction.taluk else "",
        taluk_name_ta=prediction.taluk.name_ta if prediction.taluk else "",
        pattam=prediction.pattam,
        land_area_acres=prediction.land_area_acres,
        soil_type=prediction.soil_type,
        temperature=prediction.temperature,
        humidity=prediction.humidity,
        rainfall_mm=prediction.rainfall_mm,
        weather_condition=prediction.weather_condition,
        soil_ph=prediction.soil_ph,
        soil_n=prediction.soil_n,
        soil_p=prediction.soil_p,
        soil_k=prediction.soil_k,
        predicted_yield_per_acre=prediction.predicted_yield_per_acre,
        total_production_kg=prediction.total_production_kg,
        confidence_score=prediction.confidence_score,
        typical_yield_min_acre=crop.typical_yield_min_acre,
        typical_yield_max_acre=crop.typical_yield_max_acre,
        benchmark_diff_pct=diff_pct,
        factors=factors,
        explanation_en=prediction.explanation_en,
        explanation_ta=prediction.explanation_ta,
        created_at=prediction.created_at.strftime("%Y-%m-%d %H:%M:%S")
    )
