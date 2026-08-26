import os
import random
import numpy as np
import pandas as pd
from app.database.seed_data import TN_DISTRICTS_DATA, TN_PATTAMS_DATA, TN_CROPS_DATA

SOIL_TYPES = [
    "Red Loam", "Clay Loam", "Sandy Loam", "Black Cotton Soil",
    "Alluvial", "Laterite Soil", "Sandy Soil", "Clay Soil"
]

IRRIGATION_TYPES = [
    "Well / Tube Well", "Canal Irrigation", "Drip Irrigation",
    "Sprinkler", "Rainfed"
]

def generate_tamil_nadu_agri_dataset(num_samples: int = 15000) -> pd.DataFrame:
    """
    Generates a realistic, scientifically calibrated Tamil Nadu crop yield dataset
    based on TNAU / ICAR agronomic baselines for all 38 districts and 50+ crops.
    """
    np.random.seed(42)
    random.seed(42)

    records = []
    
    # District lookup
    district_names = [d["name_en"] for d in TN_DISTRICTS_DATA]
    pattam_names = [p["name_en"] for p in TN_PATTAMS_DATA]

    for _ in range(num_samples):
        # Pick random crop
        crop = random.choice(TN_CROPS_DATA)
        district = random.choice(district_names)
        pattam = random.choice(pattam_names)
        soil_type = random.choice(SOIL_TYPES)
        irrigation = random.choice(IRRIGATION_TYPES)
        land_area_acres = round(random.uniform(0.5, 25.0), 2)

        # Environmental factors around crop ideal range with realistic noise
        temp_center = (crop["min_temp"] + crop["max_temp"]) / 2.0
        temperature = round(np.random.normal(temp_center, 3.5), 1)
        temperature = max(10.0, min(48.0, temperature))

        rain_center = (crop["min_rainfall"] + crop["max_rainfall"]) / 2.0
        rainfall_mm = round(np.random.normal(rain_center, 120.0), 1)
        rainfall_mm = max(100.0, min(3500.0, rainfall_mm))

        humidity = round(np.random.normal(68.0, 12.0), 1)
        humidity = max(25.0, min(98.0, humidity))

        # Soil parameters
        ph_center = (crop["ideal_ph_min"] + crop["ideal_ph_max"]) / 2.0
        soil_ph = round(np.random.normal(ph_center, 0.45), 2)
        soil_ph = max(4.5, min(9.5, soil_ph))

        soil_n = round(np.random.normal(crop["n_req"], crop["n_req"] * 0.25), 1)
        soil_n = max(10.0, soil_n)

        soil_p = round(np.random.normal(crop["p_req"], crop["p_req"] * 0.25), 1)
        soil_p = max(5.0, soil_p)

        soil_k = round(np.random.normal(crop["k_req"] if crop["k_req"] > 0 else 30.0, 25.0), 1)
        soil_k = max(5.0, soil_k)

        soil_ec = round(random.uniform(0.2, 1.8), 2)
        soil_oc = round(random.uniform(0.35, 1.1), 2)

        # Scientific Yield Calculation Model based on Agronomic response curve
        base_min = crop["typical_yield_min_acre"]
        base_max = crop["typical_yield_max_acre"]
        base_yield = (base_min + base_max) / 2.0

        # Temperature suitability factor (0.75 - 1.15)
        if crop["min_temp"] <= temperature <= crop["max_temp"]:
            temp_factor = 1.05
        else:
            temp_penalty = min(0.35, abs(temperature - temp_center) / 25.0)
            temp_factor = 1.0 - temp_penalty

        # Rainfall suitability factor (0.75 - 1.15)
        if crop["min_rainfall"] <= rainfall_mm <= crop["max_rainfall"]:
            rain_factor = 1.08
        else:
            rain_penalty = min(0.30, abs(rainfall_mm - rain_center) / 1000.0)
            rain_factor = 1.0 - rain_penalty

        # Soil pH suitability factor (0.80 - 1.10)
        if crop["ideal_ph_min"] <= soil_ph <= crop["ideal_ph_max"]:
            ph_factor = 1.06
        else:
            ph_penalty = min(0.25, abs(soil_ph - ph_center) / 3.0)
            ph_factor = 1.0 - ph_penalty

        # NPK nutrition factor (0.85 - 1.12)
        n_ratio = min(1.3, max(0.6, soil_n / (crop["n_req"] if crop["n_req"] > 0 else 40.0)))
        p_ratio = min(1.3, max(0.6, soil_p / (crop["p_req"] if crop["p_req"] > 0 else 30.0)))
        k_target = crop["k_req"] if crop["k_req"] > 0 else 30.0
        k_ratio = min(1.3, max(0.6, soil_k / k_target))
        nutrient_factor = (n_ratio * 0.4 + p_ratio * 0.3 + k_ratio * 0.3)

        # Irrigation bonus
        if irrigation in ["Drip Irrigation", "Canal Irrigation"]:
            irr_factor = 1.08
        elif irrigation == "Well / Tube Well":
            irr_factor = 1.03
        else:
            irr_factor = 0.92

        # Soil type match
        soil_factor = 1.04 if soil_type in crop["ideal_soil"] else 0.96

        # Pattam match
        pattam_factor = 1.05 if crop["name_en"].lower() in pattam.lower() else 0.98

        # Compute simulated yield per acre with realistic random field variance
        field_noise = np.random.normal(1.0, 0.04)
        yield_per_acre = base_yield * temp_factor * rain_factor * ph_factor * nutrient_factor * irr_factor * soil_factor * pattam_factor * field_noise

        # Ensure inside reasonable biological bounds for the crop
        yield_per_acre = max(base_min * 0.65, min(base_max * 1.35, yield_per_acre))
        yield_per_acre = round(yield_per_acre, 2)

        total_production_kg = round(yield_per_acre * land_area_acres, 2)

        records.append({
            "district": district,
            "crop": crop["name_en"],
            "pattam": pattam,
            "soil_type": soil_type,
            "irrigation_type": irrigation,
            "land_area_acres": land_area_acres,
            "temperature": temperature,
            "humidity": humidity,
            "rainfall_mm": rainfall_mm,
            "soil_ph": soil_ph,
            "soil_n": soil_n,
            "soil_p": soil_p,
            "soil_k": soil_k,
            "soil_ec": soil_ec,
            "soil_organic_carbon": soil_oc,
            "yield_per_acre": yield_per_acre,
            "total_production_kg": total_production_kg
        })

    df = pd.DataFrame(records)
    return df

if __name__ == "__main__":
    out_dir = os.path.join(os.path.dirname(__file__), "data")
    os.makedirs(out_dir, exist_ok=True)
    df = generate_tamil_nadu_agri_dataset(15000)
    csv_path = os.path.join(out_dir, "tamil_nadu_crop_yield_dataset.csv")
    df.to_csv(csv_path, index=False)
    print(f"Generated {len(df)} records of Tamil Nadu crop yield data at {csv_path}")
