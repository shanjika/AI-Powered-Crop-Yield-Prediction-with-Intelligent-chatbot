import datetime
from typing import Dict, Any, List
from app.models.crop import Crop

def generate_cultivation_timeline(crop: Crop, sowing_date_str: str = None) -> List[Dict[str, Any]]:
    """
    Generates a scientifically structured, stage-by-stage cultivation timeline
    from Day 1 to Harvest based on the specific crop duration.
    """
    duration = crop.duration_days
    
    stages = [
        {
            "stage_number": 1,
            "title_en": "Land Preparation & Basal Application",
            "title_ta": "நிலம் தயாரித்தல் & அடி உரம் இடுதல்",
            "timeline_days": f"Day 1 - {min(14, int(duration * 0.12))}",
            "is_current": True,
            "status": "in_progress",
            "tasks_en": [
                "Deep ploughing (2-3 passes) followed by rotavator leveling.",
                f"Apply 5-10 tons of well-decomposed FYM/Compost per acre.",
                f"Incorporate basal nutrients: 50% Phosphorus ({crop.p_req * 0.5:.0f} kg/ha equivalent) + 25% Nitrogen.",
                "Form ridges & furrows or raised beds with proper irrigation channels."
            ],
            "tasks_ta": [
                "நிலத்தை 2-3 முறை நன்கு உழுது சமன்படுத்தவும்.",
                "ஏக்கருக்கு 5-10 டன் நன்கு மக்கிய தொழுவுரம் அல்லது மண்புழு உரம் இடவும்.",
                f"அடி உரங்களை இடவும்: 50% மணிச்சத்து ({crop.p_req * 0.5:.0f} kg/ha) + 25% தழைச்சத்து.",
                "சரியான வடிகால் மற்றும் நீர்ப்பாசன பாத்திகளை அமைக்கவும்."
            ]
        },
        {
            "stage_number": 2,
            "title_en": "Seed Treatment & Sowing / Transplanting",
            "title_ta": "விதை நேர்த்தி & விதைப்பு / நடவு",
            "timeline_days": f"Day {min(15, int(duration * 0.12)) + 1} - {int(duration * 0.25)}",
            "is_current": False,
            "status": "upcoming",
            "tasks_en": [
                "Treat certified seeds with Pseudomonas fluorescens (10g/kg) or Trichoderma viride.",
                "Maintain recommended plant-to-plant spacing for optimum population density.",
                "Provide light life irrigation immediately after sowing/transplanting.",
                "Check for uniform germination within 5-7 days."
            ],
            "tasks_ta": [
                "விதைகளை சூடோமோனாஸ் (10 கிராம்/கிலோ) அல்லது டிரைக்கோடெர்மா விரிடி கொண்டு நேர்த்தி செய்யவும்.",
                "பரிந்துரைக்கப்பட்ட பயிர் இடைவெளியை பராமரிக்கவும்.",
                "விதைப்பு அல்லது நடவு செய்தவுடன் உயிர்த்தண்ணீர் பாய்ச்சவும்.",
                "5-7 நாட்களில் சீரான முளைப்புத் திறனை கண்காணிக்கவும்."
            ]
        },
        {
            "stage_number": 3,
            "title_en": "Vegetative Growth & Weed Management",
            "title_ta": "பயிர் வளர்ச்சி & களை மேலாண்மை",
            "timeline_days": f"Day {int(duration * 0.25) + 1} - {int(duration * 0.50)}",
            "is_current": False,
            "status": "upcoming",
            "tasks_en": [
                "Perform first weeding/hoeing at 20-25 days after sowing.",
                f"Apply first top-dressing of Nitrogen ({crop.n_req * 0.4:.0f} kg/ha) with irrigation.",
                f"Monitor field for early pests: {crop.major_pests_en.split(',')[0] if crop.major_pests_en else 'Aphids'}.",
                "Spray 1% Panchagavya or neem oil (3ml/L) as prophylactic bio-protection."
            ],
            "tasks_ta": [
                "விதைத்த 20-25 நாட்களில் முதல் களையெடுத்து மண் அணைக்கவும்.",
                f"முதல் மேலுரமாக தழைச்சத்து ({crop.n_req * 0.4:.0f} kg/ha) இட்டு பாசனம் செய்யவும்.",
                f"ஆரம்பகால பூச்சிகளை கண்காணிக்கவும்: {crop.major_pests_ta.split(',')[0] if crop.major_pests_ta else 'அசுவினி'}.",
                "முன்னெச்சரிக்கையாக 1% பஞ்சகவ்யா அல்லது வேப்பெண்ணெய் (3 மி.லி/லி) தெளிக்கவும்."
            ]
        },
        {
            "stage_number": 4,
            "title_en": "Flowering & Nutrient Top-Dressing",
            "title_ta": "பூ பூக்கும் பருவம் & ஊட்டச்சத்து மேலாண்மை",
            "timeline_days": f"Day {int(duration * 0.50) + 1} - {int(duration * 0.75)}",
            "is_current": False,
            "status": "upcoming",
            "tasks_en": [
                f"Apply final booster dose of Potassium ({crop.k_req * 0.5:.0f} kg/ha) for grain/pod filling.",
                "Foliar spray of 1% Pulse Wonder / TNAU Crop Booster / Micronutrient mix.",
                "Crucial irrigation stage: Maintain adequate soil moisture, avoid water stress.",
                f"Pest vigilance for: {crop.major_pests_en}."
            ],
            "tasks_ta": [
                f"காய்/மணி பிடிக்கும் பருவத்திற்கு பொட்டாஷ் ({crop.k_req * 0.5:.0f} kg/ha) மேலுரம் இடவும்.",
                "1% பயிர் பூஸ்டர் அல்லது தமிழ்நாடு வேளாண் பல்கலை நுண்ணூட்டக் கலவை இலைவழியாக தெளிக்கவும்.",
                "முக்கிய நீர்ப்பாசன தருணம்: வறட்சி ஏற்படாமல் சீரான ஈரப்பதம் காக்கவும்.",
                f"பூச்சி கண்காணிப்பு: {crop.major_pests_ta}."
            ]
        },
        {
            "stage_number": 5,
            "title_en": "Maturity & Grain/Fruit Development",
            "title_ta": "முதிர்ச்சி பருவம் & காய்/பழம் திரட்சி",
            "timeline_days": f"Day {int(duration * 0.75) + 1} - {int(duration * 0.92)}",
            "is_current": False,
            "status": "upcoming",
            "tasks_en": [
                "Withhold nitrogen fertilization to prevent unwanted vegetative growth.",
                "Stop irrigation 7-10 days before intended harvest for uniform ripening.",
                f"Check harvest maturity indicators: {crop.harvest_indicators_en}"
            ],
            "tasks_ta": [
                "தேவையற்ற தழை வளர்ச்சியைத் தடுக்க தழைச்சத்து உரங்களை நிறுத்தவும்.",
                "சீரான முதிர்ச்சிக்கு அறுவடைக்கு 7-10 நாட்களுக்கு முன் நீர்ப்பாசனத்தை நிறுத்தவும்.",
                f"அறுவடைக்குரிய அறிகுறிகளை கவனிக்கவும்: {crop.harvest_indicators_ta}"
            ]
        },
        {
            "stage_number": 6,
            "title_en": "Harvesting & Post-Harvest Management",
            "title_ta": "அறுவடை & அறுவடைக்கு பின் மேலாண்மை",
            "timeline_days": f"Day {int(duration * 0.92) + 1} - {duration}",
            "is_current": False,
            "status": "upcoming",
            "tasks_en": [
                "Harvest in early morning hours on a bright sunny day.",
                "Thresh, clean, and dry to safe moisture level (10-12% for grains/pulses).",
                "Store in clean, moisture-proof hermetic bags or produce cold storage."
            ],
            "tasks_ta": [
                "நல்ல வெயில் உள்ள நாளில் அதிகாலையில் அறுவடை செய்யவும்.",
                "கதிரடித்து சுத்தம் செய்து ஈரப்பதம் 10-12% வரும் வரை உலர வைக்கவும்.",
                "பூச்சி தாக்காத வகையில் பாதுகாப்பான சுத்தமான சேமிப்புக் கிடங்கில் வைக்கவும்."
            ]
        }
    ]
    return stages

def generate_what_to_do_now(crop: Crop, weather: Dict[str, Any], soil: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Generates dynamic date-aware, weather-aware immediate action items for the farmer.
    """
    temp = weather.get("temperature", 31.0)
    rain = weather.get("rainfall_mm", 0.0)
    cond = weather.get("condition_en", "Clear Sky")

    today_actions_en = [
        "Inspect soil moisture in the root zone before scheduling irrigation.",
        f"Conduct early morning field scouting for {crop.major_pests_en.split(',')[0] if crop.major_pests_en else 'leaf sucking pests'}."
    ]
    today_actions_ta = [
        "பாசனம் செய்வதற்கு முன் வேர் பகுதியில் மண் ஈரப்பதத்தை சரிபார்க்கவும்.",
        f"அதிகாலையில் பயிரை ஆய்வு செய்து {crop.major_pests_ta.split(',')[0] if crop.major_pests_ta else 'இலைப்பேன்/அசுவினி'} தென்படுகிறதா என பார்க்கவும்."
    ]

    # Weather-specific alerts
    weather_alert_en = None
    weather_alert_ta = None

    if rain > 15.0 or "Rain" in cond:
        today_actions_en.append("Heavy rain alert: Avoid irrigation and inspect drainage to prevent water stagnation.")
        today_actions_ta.append("மழை எச்சரிக்கை: நீர்ப்பாசனம் செய்வதை தவிர்க்கவும் மற்றும் வயலில் தண்ணீர் தேங்காமல் வடிகால் அமைக்கவும்.")
        weather_alert_en = "Rainfall in forecast: Do not apply foliar spray or urea today to prevent nutrient leaching."
        weather_alert_ta = "மழை வாய்ப்பு உள்ளது: உரம் அல்லது பூச்சிக்கொல்லி தெளிப்பதை தற்காலிகமாக ஒத்திவைக்கவும்."
    elif temp > 36.0:
        today_actions_en.append(f"High heat alert ({temp}°C): Irrigate during early morning or evening hours to minimize evaporation.")
        today_actions_ta.append(f"அதிக வெப்பநிலை ({temp}°C): ஆவியாதலைத் தடுக்க அதிகாலை அல்லது மாலை வேளையில் பாசனம் செய்யவும்.")
        weather_alert_en = "High temperature warning: Ensure optimal soil moisture to protect flowering/pod setting."
        weather_alert_ta = "வெப்ப அலை எச்சரிக்கை: பூக்கள் உதிர்வதை தடுக்க நிலத்தில் போதுமான ஈரப்பதம் இருப்பதை உறுதி செய்யவும்."

    # Next milestone
    next_action_en = f"Apply recommended micronutrient foliar spray ({crop.name_en} Special) within the next 7-10 days."
    next_action_ta = f"அடுத்த 7-10 நாட்களுக்குள் பரிந்துரைக்கப்பட்ட நுண்ணூட்டக் கலவையை இலைவழியாக தெளிக்கவும்."

    return {
        "crop_name_en": crop.name_en,
        "crop_name_ta": crop.name_ta,
        "current_stage_en": "Vegetative Growth & Root Establishment",
        "current_stage_ta": "பயிர் வளர்ச்சி & வேர் ஊன்றும் பருவம்",
        "days_to_harvest": crop.duration_days,
        "today_actions_en": today_actions_en,
        "today_actions_ta": today_actions_ta,
        "next_milestone_en": next_action_en,
        "next_milestone_ta": next_action_ta,
        "weather_alert_en": weather_alert_en,
        "weather_alert_ta": weather_alert_ta,
        "timestamp": datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    }
