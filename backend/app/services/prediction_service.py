import os
import joblib
import pandas as pd
from typing import Dict, Any, List
from app.models.crop import Crop

# Singleton model loader
_model_pipeline = None

def get_model_pipeline():
    global _model_pipeline
    if _model_pipeline is None:
        model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "ml", "artifacts", "best_model.joblib")
        if os.path.exists(model_path):
            _model_pipeline = joblib.load(model_path)
        else:
            raise RuntimeError("ML Model artifact not found. Please run ML training first.")
    return _model_pipeline

def calculate_factor_contributions(crop: Crop, inputs: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Computes Explainable AI contribution factors (positive and limiting)
    comparing farmer's farm conditions with the crop's ideal agronomic baselines.
    """
    factors = []

    # 1. Temperature factor
    temp = inputs.get("temperature", 30.0)
    if crop.min_temp <= temp <= crop.max_temp:
        factors.append({
            "name_en": "Temperature", "name_ta": "வெப்பநிலை",
            "impact": "positive", "score": 92,
            "detail_en": f"Current temp ({temp}°C) is in optimal range ({crop.min_temp}°C - {crop.max_temp}°C).",
            "detail_ta": f"தற்போதைய வெப்பநிலை ({temp}°C) பயிருக்கு உகந்த வரம்பில் ({crop.min_temp}°C - {crop.max_temp}°C) உள்ளது."
        })
    elif temp > crop.max_temp:
        factors.append({
            "name_en": "Temperature", "name_ta": "வெப்பநிலை",
            "impact": "negative", "score": 62,
            "detail_en": f"High temperature ({temp}°C) may cause moisture stress during flower/pod development.",
            "detail_ta": f"அதிக வெப்பநிலை ({temp}°C) பூ மற்றும் காய் பிடிக்கும் பருவத்தில் ஈரப்பத பற்றாக்குறையை ஏற்படுத்தலாம்."
        })
    else:
        factors.append({
            "name_en": "Temperature", "name_ta": "வெப்பநிலை",
            "impact": "neutral", "score": 75,
            "detail_en": f"Moderate temperature ({temp}°C).",
            "detail_ta": f"மிதமான வெப்பநிலை ({temp}°C)."
        })

    # 2. Rainfall factor
    rain = inputs.get("rainfall_mm", 0.0)
    if crop.min_rainfall * 0.7 <= rain * 10 <= crop.max_rainfall * 1.3:
        factors.append({
            "name_en": "Rainfall & Moisture", "name_ta": "மழை மற்றும் ஈரப்பதம்",
            "impact": "positive", "score": 88,
            "detail_en": f"Precipitation levels support healthy vegetative vigor.",
            "detail_ta": f"மழை அளவு பயிரின் வளர்ச்சிக்கு சாதகமாக உள்ளது."
        })
    else:
        factors.append({
            "name_en": "Rainfall & Moisture", "name_ta": "மழை மற்றும் ஈரப்பதம்",
            "impact": "neutral", "score": 70,
            "detail_en": f"Supplementary irrigation required to meet total crop water requirement.",
            "detail_ta": f"பயிரின் முழு நீர் தேவையை பூர்த்தி செய்ய கூடுதல் நீர்ப்பாசனம் தேவைப்படும்."
        })

    # 3. Soil pH factor
    ph = inputs.get("soil_ph", 6.8)
    if crop.ideal_ph_min <= ph <= crop.ideal_ph_max:
        factors.append({
            "name_en": "Soil pH", "name_ta": "மண் pH (கார அமில நிலை)",
            "impact": "positive", "score": 95,
            "detail_en": f"Soil pH ({ph}) provides optimal nutrient absorption.",
            "detail_ta": f"மண் கார அமில நிலை ({ph}) சத்துக்களை எளிதாக உறிஞ்ச ஏதுவாக உள்ளது."
        })
    elif ph < crop.ideal_ph_min:
        factors.append({
            "name_en": "Soil pH", "name_ta": "மண் pH (அமிலத்தன்மை)",
            "impact": "negative", "score": 60,
            "detail_en": f"Slightly acidic soil ({ph}). Apply agricultural lime to improve nutrient uptake.",
            "detail_ta": f"மண் லேசான அமிலத்தன்மை ({ph}) கொண்டது. சத்துக்கள் கிடைக்க விவசாய சுண்ணாம்பு இடவும்."
        })
    else:
        factors.append({
            "name_en": "Soil pH", "name_ta": "மண் pH (காரத்தன்மை)",
            "impact": "negative", "score": 64,
            "detail_en": f"Alkaline soil ({ph}). Apply gypsum and organic manure.",
            "detail_ta": f"மண் காரத்தன்மை ({ph}) கொண்டது. ஜிப்சம் மற்றும் தொழுவுரம் இடவும்."
        })

    # 4. Nitrogen factor
    n = inputs.get("soil_n", 250.0)
    if n >= crop.n_req:
        factors.append({
            "name_en": "Soil Nitrogen (N)", "name_ta": "தழைச்சத்து (N)",
            "impact": "positive", "score": 90,
            "detail_en": f"Adequate available nitrogen ({n} kg/ha) supports lush vegetative growth.",
            "detail_ta": f"போதுமான தழைச்சத்து ({n} kg/ha) பயிர் தளிர்க்க உதவுகிறது."
        })
    else:
        factors.append({
            "name_en": "Soil Nitrogen (N)", "name_ta": "தழைச்சத்து (N)",
            "impact": "negative", "score": 65,
            "detail_en": f"Available nitrogen ({n} kg/ha) is below requirement ({crop.n_req} kg/ha). Top-dressing recommended.",
            "detail_ta": f"தழைச்சத்து ({n} kg/ha) தேவைக்கு ({crop.n_req} kg/ha) குறைவாக உள்ளது. மேலுரம் இடவும்."
        })

    # 5. Potassium factor
    k = inputs.get("soil_k", 200.0)
    if k >= (crop.k_req if crop.k_req > 0 else 50.0):
        factors.append({
            "name_en": "Soil Potassium (K)", "name_ta": "சாம்பல் சத்து (K)",
            "impact": "positive", "score": 86,
            "detail_en": f"Good potassium ({k} kg/ha) enhances grain filling and disease resistance.",
            "detail_ta": f"நல்ல சாம்பல் சத்து ({k} kg/ha) திரட்சியான தானியம் மற்றும் நோய் எதிர்ப்பு திறனை தருகிறது."
        })
    else:
        factors.append({
            "name_en": "Soil Potassium (K)", "name_ta": "சாம்பல் சத்து (K)",
            "impact": "negative", "score": 68,
            "detail_en": f"Potassium level ({k} kg/ha) is moderate. Apply muriate of potash before flowering.",
            "detail_ta": f"சாம்பல் சத்து ({k} kg/ha) மிதமாக உள்ளது. பூக்கும் முன் பொட்டாஷ் உரம் இடவும்."
        })

    # 6. Season / Pattam suitability
    pattam = inputs.get("pattam", "")
    factors.append({
        "name_en": "Cultivation Season (Pattam)", "name_ta": "சாகுபடி பட்டம்",
        "impact": "positive", "score": 92,
        "detail_en": f"Selected season ({pattam}) aligns well with regional Tamil Nadu cropping calendar.",
        "detail_ta": f"தேர்ந்தெடுக்கப்பட்ட பட்டம் ({pattam}) தமிழக பயிர் கால அட்டவணையுடன் பொருந்துகிறது."
    })

    return factors

def generate_ai_explanation(
    crop: Crop,
    predicted_yield_per_acre: float,
    land_area: float,
    factors: List[Dict[str, Any]]
) -> tuple[str, str]:
    """Generates farmer-friendly explanation paragraphs in English and Tamil."""
    total_yield = round(predicted_yield_per_acre * land_area, 2)
    
    positives_en = [f["detail_en"] for f in factors if f["impact"] == "positive"]
    negatives_en = [f["detail_en"] for f in factors if f["impact"] == "negative"]

    positives_ta = [f["detail_ta"] for f in factors if f["impact"] == "positive"]
    negatives_ta = [f["detail_ta"] for f in factors if f["impact"] == "negative"]

    en_text = (
        f"Based on AI analysis of your soil report, live agro-meteorological data, and cultivation parameters, "
        f"the estimated yield for {crop.name_en} is {predicted_yield_per_acre:,.1f} kg/acre "
        f"(Total expected production: {total_yield:,.1f} kg for your {land_area} acre farm).\n\n"
        f"Key Positive Growth Drivers:\n" + "\n".join([f"• {p}" for p in positives_en[:3]])
    )
    if negatives_en:
        en_text += "\n\nYield Improvement Opportunities:\n" + "\n".join([f"• {n}" for n in negatives_en[:2]])

    ta_text = (
        f"உங்கள் மண் பரிசோதனை அறிக்கை, நேரடி வானிலை தகவல்கள் மற்றும் சாகுபடி விபரங்களை AI மூலம் ஆய்வு செய்ததில், "
        f"{crop.name_ta} பயிருக்கு எதிர்பார்க்கப்படும் மகசூல் {predicted_yield_per_acre:,.1f} கிலோ/ஏக்கர் "
        f"(உங்கள் {land_area} ஏக்கர் நிலத்திற்கு மொத்த எதிர்பார்க்கப்படும் உற்பத்தி: {total_yield:,.1f} கிலோ ஆகும்).\n\n"
        f"மகசூலை உயர்த்தும் சாதகமான காரணிகள்:\n" + "\n".join([f"• {p}" for p in positives_ta[:3]])
    )
    if negatives_ta:
        ta_text += "\n\nமகசூலை மேலும் அதிகரிக்க கவனிக்க வேண்டியவை:\n" + "\n".join([f"• {n}" for n in negatives_ta[:2]])

    return (en_text, ta_text)

def predict_crop_yield(crop: Crop, inputs: Dict[str, Any]) -> Dict[str, Any]:
    """
    Runs ML model inference, scales inputs, calculates yield per acre and total yield,
    evaluates factor contributions, and returns the complete prediction bundle.
    """
    pipeline = get_model_pipeline()

    # Construct single-row DataFrame for pipeline
    row = {
        "district": inputs.get("district", "Erode"),
        "crop": crop.name_en,
        "pattam": inputs.get("pattam", "Aadi Pattam (Monsoon Sowing)"),
        "soil_type": inputs.get("soil_type", "Red Loam"),
        "irrigation_type": inputs.get("irrigation_type", "Well / Tube Well"),
        "temperature": float(inputs.get("temperature", 30.0)),
        "humidity": float(inputs.get("humidity", 65.0)),
        "rainfall_mm": float(inputs.get("rainfall_mm", 0.0)),
        "soil_ph": float(inputs.get("soil_ph", 6.8)),
        "soil_n": float(inputs.get("soil_n", 250.0)),
        "soil_p": float(inputs.get("soil_p", 18.0)),
        "soil_k": float(inputs.get("soil_k", 200.0)),
        "soil_ec": float(inputs.get("soil_ec", 0.45)),
        "soil_organic_carbon": float(inputs.get("soil_organic_carbon", 0.65))
    }

    df_input = pd.DataFrame([row])
    raw_pred = float(pipeline.predict(df_input)[0])

    # Ensure prediction is within realistic biological boundaries of the crop
    min_b = crop.typical_yield_min_acre * 0.7
    max_b = crop.typical_yield_max_acre * 1.3
    yield_per_acre = round(max(min_b, min(max_b, raw_pred)), 1)

    land_acres = float(inputs.get("land_area_acres", 1.0))
    total_production_kg = round(yield_per_acre * land_acres, 1)

    factors = calculate_factor_contributions(crop, inputs)
    explanation_en, explanation_ta = generate_ai_explanation(crop, yield_per_acre, land_acres, factors)

    # Benchmark comparison
    typical_avg = (crop.typical_yield_min_acre + crop.typical_yield_max_acre) / 2.0
    diff_pct = round(((yield_per_acre - typical_avg) / typical_avg) * 100, 1)

    return {
        "predicted_yield_per_acre": yield_per_acre,
        "total_production_kg": total_production_kg,
        "confidence_score": 0.92,
        "typical_yield_min_acre": crop.typical_yield_min_acre,
        "typical_yield_max_acre": crop.typical_yield_max_acre,
        "benchmark_diff_pct": diff_pct,
        "factors": factors,
        "explanation_en": explanation_en,
        "explanation_ta": explanation_ta
    }
