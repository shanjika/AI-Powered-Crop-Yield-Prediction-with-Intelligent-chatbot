export interface User {
  id: number;
  full_name: string;
  mobile_number: string;
  email?: string;
  preferred_language: string;
  district_id?: number;
  taluk_id?: number;
  district_name?: string;
  taluk_name?: string;
}

export interface District {
  id: number;
  name_en: string;
  name_ta: string;
  latitude: number;
  longitude: number;
  taluk_count: number;
}

export interface Taluk {
  id: number;
  district_id: number;
  name_en: string;
  name_ta: string;
  latitude: number;
  longitude: number;
}

export interface Crop {
  id: number;
  name_en: string;
  name_ta: string;
  category: string;
  duration_days: number;
  ideal_soil: string;
  ideal_soil_ta: string;
  min_temp: number;
  max_temp: number;
  min_rainfall: number;
  max_rainfall: number;
  water_req_level: string;
  water_req_level_ta: string;
  typical_yield_min_acre: number;
  typical_yield_max_acre: number;
  n_req?: number;
  p_req?: number;
  k_req?: number;
  ideal_ph_min?: number;
  ideal_ph_max?: number;
  harvest_indicators_en?: string;
  harvest_indicators_ta?: string;
  major_pests_en?: string;
  major_pests_ta?: string;
  major_diseases_en?: string;
  major_diseases_ta?: string;
}

export interface Pattam {
  id: number;
  name_en: string;
  name_ta: string;
  months_en: string;
  months_ta: string;
  description_en: string;
  description_ta: string;
  recommended_crops_en: string;
  recommended_crops_ta: string;
}

export interface WeatherForecastDay {
  date: string;
  temp_max: number;
  temp_min: number;
  precipitation_mm: number;
  rain_probability_pct: number;
  condition_en: string;
  condition_ta: string;
  icon: string;
}

export interface WeatherData {
  temperature: number;
  humidity: number;
  rainfall_mm: number;
  wind_speed_kmh: number;
  pressure_hpa: number;
  condition_en: string;
  condition_ta: string;
  icon: string;
  location_name: string;
  district_name_en?: string;
  district_name_ta?: string;
  taluk_name_en?: string;
  taluk_name_ta?: string;
  forecast: WeatherForecastDay[];
  warnings: Array<{ type: string; en: string; ta: string }>;
  timestamp: string;
}

export interface FactorDetail {
  name_en: string;
  name_ta: string;
  impact: 'positive' | 'negative' | 'neutral';
  score: number;
  detail_en: string;
  detail_ta: string;
}

export interface PredictionResult {
  id: number;
  crop_id: number;
  crop_name_en: string;
  crop_name_ta: string;
  district_name_en: string;
  district_name_ta: string;
  taluk_name_en: string;
  taluk_name_ta: string;
  pattam: string;
  land_area_acres: number;
  soil_type: string;
  temperature: number;
  humidity: number;
  rainfall_mm: number;
  weather_condition: string;
  soil_ph: number;
  soil_n: number;
  soil_p: number;
  soil_k: number;
  predicted_yield_per_acre: number;
  total_production_kg: number;
  confidence_score: number;
  typical_yield_min_acre: number;
  typical_yield_max_acre: number;
  benchmark_diff_pct: number;
  factors: FactorDetail[];
  explanation_en: string;
  explanation_ta: string;
  created_at: string;
}

export interface TimelineStage {
  stage_number: number;
  title_en: string;
  title_ta: string;
  timeline_days: string;
  is_current: boolean;
  status: string;
  tasks_en: string[];
  tasks_ta: string[];
}

export interface ActionPlan {
  prediction_id: number;
  crop_name_en: string;
  crop_name_ta: string;
  duration_days: number;
  pattam: string;
  district: string;
  what_should_i_do_now: {
    crop_name_en: string;
    crop_name_ta: string;
    current_stage_en: string;
    current_stage_ta: string;
    days_to_harvest: number;
    today_actions_en: string[];
    today_actions_ta: string[];
    next_milestone_en: string;
    next_milestone_ta: string;
    weather_alert_en?: string;
    weather_alert_ta?: string;
  };
  timeline_stages: TimelineStage[];
  fertilizer_guide_en: Record<string, string>;
  fertilizer_guide_ta: Record<string, string>;
}
