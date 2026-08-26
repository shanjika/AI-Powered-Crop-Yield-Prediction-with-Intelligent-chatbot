import re
import httpx
from typing import Dict, Any, List, Optional
from app.config import settings

AGRI_KEYWORDS = [
    "crop", "yield", "paddy", "rice", "maize", "cotton", "sugarcane", "banana",
    "soil", "weather", "rain", "temperature", "pattam", "fertilizer", "urea", "potash",
    "pest", "disease", "irrigation", "water", "seed", "sowing", "harvest", "acre",
    "hectare", "farm", "farmer", "agriculture", "tnau", "icar", "organic", "neem",
    "panchagavya", "ph", "nitrogen", "phosphorus", "potassium", "groundnut", "millet",
    "துவரை", "உளுந்து", "பயறு", "நெல்", "விவசாயம்", "மண்", "வானிலை", "மழை", "பட்டம்",
    "உரம்", "பூச்சி", "நோய்", "பாசனம்", "நீர்", "விதை", "விதைப்பு", "அறுவடை", "ஏக்கர்",
    "மகசூல்", "செம்மண்", "கரிசல்", "கரும்பு", "வாழை", "மஞ்சள்", "பருத்தி", "தக்காளி",
    "வெங்காயம்", "மிளகாய்", "சாம்பல்", "தழைச்சத்து", "மணிச்சத்து", "சாம்பல்சத்து"
]

NON_AGRI_REFUSAL_EN = "Sorry, I can only help with agriculture, farming, crops, weather, soil, and crop yield prediction questions for Tamil Nadu farmers."
NON_AGRI_REFUSAL_TA = "மன்னிக்கவும். நான் விவசாயம், பயிர்கள், வானிலை, மண் வளம் மற்றும் மகசூல் கணிப்பு தொடர்பான கேள்விகளுக்கு மட்டுமே உதவ முடியும்."

def is_agriculture_query(query: str, has_farm_context: bool = False) -> bool:
    """Verifies if the user message is within the agricultural domain."""
    if has_farm_context:
        # In post-prediction chat, farmer is inquiring about the current farm context
        return True
    
    query_lower = query.lower()
    
    # Check off-topic flags
    off_topic_patterns = [
        r'\b(cricket|football|movie|actor|cinema|politics|election|bitcoin|crypto|song|dance|joke|story|recipe for cake)\b'
    ]
    for pattern in off_topic_patterns:
        if re.search(pattern, query_lower):
            return False

    # Check for presence of agriculture terms
    for kw in AGRI_KEYWORDS:
        if kw in query_lower:
            return True
            
    # If the text is in Tamil script or has farming tone
    if any(ord(char) >= 0x0B80 and ord(char) <= 0x0BFF for char in query):
        return True

    return False

def detect_language(text: str) -> str:
    """Detects whether user is writing in Tamil or English."""
    tamil_chars = sum(1 for c in text if 0x0B80 <= ord(c) <= 0x0BFF)
    if tamil_chars > 2:
        return "ta"
    return "en"

def get_expert_rule_response(query: str, lang: str, context: Optional[Dict[str, Any]] = None) -> str:
    """
    Expert rule-based Agronomy Engine providing scientifically verified TNAU recommendations.
    Used for instant fallback and high reliability.
    """
    q = query.lower()

    if context:
        crop = context.get("crop", "Paddy")
        crop_ta = context.get("crop_ta", "நெல்")
        district = context.get("district", "Tamil Nadu")
        predicted_yield = context.get("predicted_yield_per_acre", "2800")
        total_prod = context.get("total_production_kg", "8400")
        land_acres = context.get("land_area_acres", "3")
        soil_ph = context.get("soil_ph", "6.8")

        # Questions about why yield is low / how to improve
        if any(w in q for w in ["low", "increase", "improve", "boost", "குறைவு", "அதிகரிக்க", "உயர்த்த"]):
            if lang == "ta":
                return (
                    f"🌾 **உங்கள் {crop_ta} பயிர் மகசூலை ({predicted_yield} கி.கி/ஏக்கர்) உயர்த்துவதற்கான வழிகள்:**\n\n"
                    f"1. **மண் ஊட்டச்சத்து மேலாண்மை:** உங்கள் நிலத்தின் மண் pH {soil_ph} ஆக உள்ளது. அடி உரமாக 50% மணிச்சத்து மற்றும் தழைச்சத்து இடவும். காய்/தானியம் பிடிக்கும் தருணத்தில் பொட்டாஷ் (சாம்பல் சத்து) மேலுரம் இடுவது மகசூலை 15-20% அதிகரிக்கும்.\n"
                    f"2. **நுண்ணூட்டக் கலவை:** தமிழ்நாடு வேளாண் பல்கலை (TNAU) பரிந்துரைக்கும் நுண்ணூட்டக் கலவை அல்லது பஞ்சகவ்யா (1 லிட்டருக்கு 30 மி.லி) பூக்கும் பருவத்தில் இலைவழியாக தெளிக்கவும்.\n"
                    f"3. **பாசன இடைவெளி:** பூ பூக்கும் மற்றும் காய்/மணி திரளும் பருவத்தில் நீர் பற்றாக்குறை ஏற்படாமல் சீரான பாசனம் செய்யவும்.\n"
                    f"4. **பயிர் பாதுகாப்பு:** பூச்சி தாக்குதலை ஆரம்பத்திலேயே கண்காணிக்க வேப்பெண்ணெய் கரைசல் (3 மி.லி/லி) தெளிக்கவும்."
                )
            else:
                return (
                    f"🌾 **How to Maximize Your {crop} Yield ({predicted_yield} kg/acre) in {district}:**\n\n"
                    f"1. **Split Fertilizer Application:** Apply 50% Phosphorus and 25% Nitrogen as basal dose. Top-dress remaining Nitrogen with Potassium (MOP) during active vegetative and tillering/flowering stages.\n"
                    f"2. **Foliar Micronutrient Boost:** Spray 1% TNAU Micronutrient Mixture or 1% Pulse Wonder/Crop Booster at 30 & 45 days after sowing to minimize flower dropping.\n"
                    f"3. **Moisture Maintenance:** Ensure adequate soil moisture during the critical flowering and grain filling stages.\n"
                    f"4. **Prophylactic Pest Control:** Spray 3% Neem oil or 5% NSKE (Neem Seed Kernel Extract) at the first sighting of pests to avoid yield loss."
                )

        # Questions about fertilizer schedule
        if any(w in q for w in ["fertilizer", "urea", "potash", "உரம்", "யூரியா", "பொட்டாஷ்"]):
            if lang == "ta":
                return (
                    f"🧪 **{crop_ta} பயிருக்கான உரம் இடும் அட்டவணை ({land_acres} ஏக்கர்):**\n\n"
                    f"• **அடி உரம் (விதைப்புக்கு முன்):** ஏக்கருக்கு 5 டன் மக்கிய தொழுவுரம் + முழு அளவு சூப்பர் பாஸ்பேட் (மணிச்சத்து) + 25% யூரியா.\n"
                    f"• **முதல் மேலுரம் (20-25 நாட்கள்):** 40% யூரியா + களை எடுத்த பின் பாசனம்.\n"
                    f"• **இரண்டாம் மேலுரம் (45-50 நாட்கள் - பூக்கும் பருவம்):** 35% யூரியா + பொட்டாஷ் (சாம்பல் சத்து) இட்டு பாசனம் செய்யவும்.\n"
                    f"• **குறிப்பு:** மழைக்காலங்களில் யூரியா தெளிப்பதை தவிர்க்கவும்."
                )
            else:
                return (
                    f"🧪 **Fertilizer Schedule for your {land_acres} Acre {crop} Farm:**\n\n"
                    f"• **Basal Dose (At Sowing/Transplanting):** 5-10 tons FYM/compost + 100% Single Super Phosphate (SSP) + 25% Urea per acre.\n"
                    f"• **First Top Dressing (20-25 Days):** 40% Urea after weeding.\n"
                    f"• **Second Top Dressing (45-50 Days - Flowering Stage):** Remaining 35% Urea + Muriate of Potash (MOP) to boost grain quality.\n"
                    f"• **Tip:** Always apply fertilizer when soil has optimum moisture, never during heavy rain forecast."
                )

        # General post-prediction context response
        if lang == "ta":
            return (
                f"🌱 **உங்கள் பண்ணை விபரம் ({crop_ta} - {district}):**\n"
                f"• எதிர்பார்க்கப்படும் மகசூல்: **{predicted_yield} கிலோ / ஏக்கர்**\n"
                f"• மொத்த உற்பத்தி: **{total_prod} கிலோ** ({land_acres} ஏக்கர்)\n"
                f"• மண் pH: **{soil_ph}**\n\n"
                f"உங்கள் சாகுபடி, உரம், நீர் பாசனம் அல்லது பூச்சி மேலாண்மை பற்றி ஏதேனும் குறிப்பிட்ட கேள்வி கேட்கலாம்!"
            )
        else:
            return (
                f"🌱 **Your Farm Summary ({crop} - {district}):**\n"
                f"• Estimated Yield: **{predicted_yield} kg/acre**\n"
                f"• Total Expected Production: **{total_prod} kg** for your {land_acres} acre farm.\n"
                f"• Soil pH: **{soil_ph}**\n\n"
                f"Feel free to ask specific questions about fertilizer timing, pest management, irrigation schedules, or harvest signs for this crop!"
            )

    # General Chatbot Answers
    if any(w in q for w in ["pattam", "பட்டம்", "season"]):
        if lang == "ta":
            return (
                "📅 **தமிழகத்தின் முதன்மை விவசாய பட்டங்கள்:**\n\n"
                "1. **சித்திரை பட்டம் (ஏப்ரல் - மே):** எள், உளுந்து, தர்பூசணி, காய்கறிகள்.\n"
                "2. **ஆடி பட்டம் (ஜூலை - ஆகஸ்ட்):** 'ஆடி பட்டம் தேடி விதை' - நெல், மக்காச்சோளம், கம்பு, பருத்தி, நிலக்கடலை.\n"
                "3. **புரட்டாசி பட்டம் (செப் - அக்):** மானாவாரி சிறுதானியங்கள், பருத்தி, கொத்தமல்லி.\n"
                "4. **தை பட்டம் (ஜன - பிப்):** நிலக்கடலை, உளுந்து, கரும்பு, சூரியகாந்தி, காய்கறிகள்.\n"
                "5. **சம்பா பருவம் (ஆக - ஜன):** டெல்டா மற்றும் தமிழகத்தின் முதன்மை நெல் சாகுபடி பருவம்."
            )
        else:
            return (
                "📅 **Major Tamil Nadu Agricultural Seasons (Pattams):**\n\n"
                "1. **Chithirai Pattam (April - May):** Ideal for Sesame, Green Gram, Watermelon, and vegetables.\n"
                "2. **Aadi Pattam (July - August):** The primary monsoon sowing season for Paddy, Maize, Cotton, Groundnut, and Millets.\n"
                "3. **Purattasi Pattam (September - October):** Rainfed millets, cotton, Bengal gram, and coriander.\n"
                "4. **Thai Pattam (January - February):** Groundnut, sugarcane, pulses, and sunflower.\n"
                "5. **Samba / Thaladi (August - January):** The principal single/double crop rice season across Tamil Nadu."
            )

    if any(w in q for w in ["paddy", "rice", "நெல்"]):
        if lang == "ta":
            return (
                "🌾 **நெல் சாகுபடி முக்கிய குறிப்புகள்:**\n\n"
                "• **விதை நேர்த்தி:** 1 கிலோ விதைக்கு 10 கிராம் சூடோமோனாஸ் அல்லது 2 கிராம் கார்பென்டாசிம் கொண்டு விதை நேர்த்தி செய்யவும்.\n"
                "• **நாற்றங்கால்:** 20-25 நாள் வயதுடைய இளம் நாற்றுகளை நடவு செய்யவும்.\n"
                "• **உர மேலாண்மை:** ஏக்கருக்கு யூரியா 50 கி.கி, டிஏபி 50 கி.கி, பொட்டாஷ் 25 கி.கி 3 பிரிவுகளாக இடவும்.\n"
                "• **புகையான் & இலைச்சுருட்டு புழு:** வேப்பெண்ணெய் 3% அல்லது அசாடிராக்டின் 1% தெளிக்கவும்."
            )
        else:
            return (
                "🌾 **Key Recommendations for High Paddy Yield:**\n\n"
                "• **Seed Treatment:** Treat seeds with Pseudomonas fluorescens (10g/kg) before nursery sowing.\n"
                "• **Transplanting:** Transplant 20-25 day old seedlings at 2-3 seedlings per hill.\n"
                "• **Water Management:** Maintain 2-3 cm shallow standing water during early tillering; practice Alternate Wetting and Drying (AWD) to save water.\n"
                "• **Pest Vigilance:** Monitor for stem borer dead hearts and BPH (brown planthopper); maintain alleys (skip rows) every 2 meters for aeration."
            )

    # Generic farming response
    if lang == "ta":
        return (
            "🌱 **தமிழக விவசாயிகளுக்கான AI வேளாண் வழிகாட்டி:**\n\n"
            "உங்கள் மண் வகை, பயிர் ரகம், நடவு பருவம் அல்லது பூச்சி/நோய் மேலாண்மை குறித்த கேள்விகளை கேட்கலாம். "
            "எடுத்துக்காட்டாக: *'மக்காச்சோளத்திற்கு எந்த உரம் சிறந்தது?'*, *'பருத்தியில் பூ உதிர்வதை தடுப்பது எப்படி?'*, *'ஆடி பட்டத்தில் என்ன பயிர் செய்யலாம்?'*"
        )
    else:
        return (
            "🌱 **AI Farming Assistant for Tamil Nadu Farmers:**\n\n"
            "You can ask me questions about crop selection, fertilizer dosages, organic pest management, irrigation schedules, or Tamil Nadu agricultural seasons. "
            "For example: *'What fertilizer is best for Maize?'*, *'How to control pink bollworm in cotton?'*, *'Which crops are suitable for Aadi Pattam?'*"
        )

async def generate_chatbot_response(
    query: str,
    context: Optional[Dict[str, Any]] = None,
    chat_history: Optional[List[Dict[str, str]]] = None
) -> Dict[str, Any]:
    """
    Main chatbot handler with agricultural scope enforcement, language detection,
    and LLM API integration with robust expert agronomy fallback.
    """
    lang = detect_language(query)
    has_context = context is not None and len(context) > 0

    # 1. Agriculture Scope Enforcement Guardrail
    if not is_agriculture_query(query, has_farm_context=has_context):
        refusal_msg = NON_AGRI_REFUSAL_TA if lang == "ta" else NON_AGRI_REFUSAL_EN
        return {
            "response": refusal_msg,
            "language": lang,
            "is_refusal": True
        }

    # 2. If external LLM API key (Gemini / OpenAI) is configured, call it with structured agri prompt
    if settings.LLM_API_KEY and len(settings.LLM_API_KEY) > 10:
        try:
            # Build system prompt with agricultural guardrail and context
            system_prompt = (
                "You are an expert AI Agricultural Agronomist dedicated to Tamil Nadu farmers. "
                "You provide scientifically accurate, practical farming advice based on TNAU (Tamil Nadu Agricultural University) "
                "and ICAR standards. Only answer farming, crop, weather, fertilizer, pest, and soil questions. "
                "If the user asks something completely unrelated to agriculture, politely decline in their language. "
                f"Reply in the user's language: {'Tamil (தமிழ்)' if lang == 'ta' else 'English'}.\n"
            )
            if context:
                system_prompt += f"\nCURRENT FARM PREDICTION CONTEXT:\n{context}\n"

            # Gemini API call
            async with httpx.AsyncClient(timeout=12.0) as client:
                gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={settings.LLM_API_KEY}"
                payload = {
                    "contents": [
                        {"role": "user", "parts": [{"text": f"{system_prompt}\n\nFarmer Question: {query}"}]}
                    ]
                }
                res = await client.post(gemini_url, json=payload)
                if res.status_code == 200:
                    data = res.json()
                    answer = data["candidates"][0]["content"]["parts"][0]["text"]
                    return {
                        "response": answer,
                        "language": lang,
                        "is_refusal": False
                    }
        except Exception as e:
            print(f"LLM API Call exception, using expert agronomy engine: {e}")

    # 3. High-precision Expert Heuristic Agronomy Engine
    response_text = get_expert_rule_response(query, lang, context)
    return {
        "response": response_text,
        "language": lang,
        "is_refusal": False
    }
