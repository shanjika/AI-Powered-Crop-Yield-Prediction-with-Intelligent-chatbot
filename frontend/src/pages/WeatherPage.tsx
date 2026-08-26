import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { useAuth } from '../context/AuthContext';
import api from '../services/api';
import { District, Taluk, WeatherData } from '../types';
import {
  CloudSun,
  MapPin,
  Droplets,
  Wind,
  Gauge,
  Thermometer,
  AlertTriangle,
  Calendar,
  CloudRain,
  Sun
} from 'lucide-react';

export const WeatherPage: React.FC = () => {
  const { t, i18n } = useTranslation();
  const lang = i18n.language || 'ta';
  const { user } = useAuth();

  const [districts, setDistricts] = useState<District[]>([]);
  const [taluks, setTaluks] = useState<Taluk[]>([]);
  const [selectedDistrict, setSelectedDistrict] = useState(user?.district_id ? String(user.district_id) : '8'); // Erode default
  const [selectedTaluk, setSelectedTaluk] = useState(user?.taluk_id ? String(user.taluk_id) : '1');

  const [weather, setWeather] = useState<WeatherData | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  // Load districts
  useEffect(() => {
    api.get('/districts').then((res) => {
      setDistricts(res.data);
      if (!selectedDistrict && res.data.length > 0) {
        setSelectedDistrict(String(res.data[0].id));
      }
    });
  }, []);

  // Load taluks
  useEffect(() => {
    if (selectedDistrict) {
      api.get(`/taluks/${selectedDistrict}`).then((res) => {
        setTaluks(res.data);
        if (res.data.length > 0) {
          setSelectedTaluk(String(res.data[0].id));
        }
      });
    }
  }, [selectedDistrict]);

  // Load weather data
  useEffect(() => {
    if (selectedDistrict && selectedTaluk) {
      setIsLoading(true);
      api.get(`/weather/${selectedDistrict}/${selectedTaluk}`)
        .then((res) => setWeather(res.data))
        .catch((err) => console.error('Error loading weather:', err))
        .finally(() => setIsLoading(false));
    }
  }, [selectedDistrict, selectedTaluk]);

  return (
    <div className="max-w-5xl mx-auto space-y-6 pb-12">
      {/* Header & Location Switcher */}
      <div className="glass-panel rounded-3xl p-6 sm:p-8 space-y-4 border border-emerald-500/20">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="w-12 h-12 rounded-2xl bg-amber-500/20 flex items-center justify-center text-amber-400 font-bold shadow-lg shadow-amber-500/10">
              <CloudSun className="w-7 h-7" />
            </div>
            <div>
              <h1 className="text-xl sm:text-2xl font-extrabold text-white">{t('nav.weather')}</h1>
              <p className="text-xs text-slate-300">Live agro-meteorological station tracking for Tamil Nadu</p>
            </div>
          </div>

          {/* District & Taluk Selector */}
          <div className="flex flex-wrap items-center gap-2">
            <select
              value={selectedDistrict}
              onChange={(e) => setSelectedDistrict(e.target.value)}
              className="bg-slate-900 border border-slate-700 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-emerald-500"
            >
              {districts.map((d) => (
                <option key={d.id} value={d.id}>
                  {lang === 'ta' ? d.name_ta : d.name_en}
                </option>
              ))}
            </select>

            <select
              value={selectedTaluk}
              onChange={(e) => setSelectedTaluk(e.target.value)}
              className="bg-slate-900 border border-slate-700 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-emerald-500"
            >
              {taluks.map((t) => (
                <option key={t.id} value={t.id}>
                  {lang === 'ta' ? t.name_ta : t.name_en}
                </option>
              ))}
            </select>
          </div>
        </div>
      </div>

      {isLoading ? (
        <div className="py-16 text-center space-y-2">
          <div className="w-10 h-10 rounded-full border-4 border-emerald-500 border-t-transparent animate-spin mx-auto" />
          <span className="text-xs text-slate-400">{t('common.loading')}</span>
        </div>
      ) : weather ? (
        <div className="space-y-6">
          {/* Main Current Weather Showcase */}
          <div className="glass-panel rounded-3xl p-6 sm:p-8 bg-gradient-to-br from-slate-900/90 via-slate-900/70 to-emerald-950/30 border border-emerald-500/20">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-6">
              <div className="space-y-2">
                <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-emerald-500/10 text-emerald-300 text-xs font-semibold">
                  <MapPin className="w-3.5 h-3.5" />
                  <span>{weather.location_name}</span>
                </div>
                <div className="flex items-baseline gap-3">
                  <span className="text-5xl sm:text-6xl font-black text-white">
                    {weather.temperature}°C
                  </span>
                  <span className="text-base sm:text-lg font-bold text-amber-300">
                    {lang === 'ta' ? weather.condition_ta : weather.condition_en}
                  </span>
                </div>
                <p className="text-xs text-slate-400">Updated at: {weather.timestamp}</p>
              </div>

              {/* Meteorological Indicators Grid */}
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
                <div className="p-3.5 rounded-2xl bg-slate-900/80 border border-slate-800 text-center">
                  <Droplets className="w-5 h-5 text-blue-400 mx-auto mb-1" />
                  <span className="text-[10px] text-slate-400 block font-semibold">{t('dashboard.humidity')}</span>
                  <span className="text-lg font-bold text-white">{weather.humidity}%</span>
                </div>

                <div className="p-3.5 rounded-2xl bg-slate-900/80 border border-slate-800 text-center">
                  <CloudRain className="w-5 h-5 text-teal-400 mx-auto mb-1" />
                  <span className="text-[10px] text-slate-400 block font-semibold">{t('dashboard.rainfall')}</span>
                  <span className="text-lg font-bold text-white">{weather.rainfall_mm} mm</span>
                </div>

                <div className="p-3.5 rounded-2xl bg-slate-900/80 border border-slate-800 text-center">
                  <Wind className="w-5 h-5 text-indigo-400 mx-auto mb-1" />
                  <span className="text-[10px] text-slate-400 block font-semibold">{t('dashboard.wind')}</span>
                  <span className="text-lg font-bold text-white">{weather.wind_speed_kmh} km/h</span>
                </div>

                <div className="p-3.5 rounded-2xl bg-slate-900/80 border border-slate-800 text-center">
                  <Gauge className="w-5 h-5 text-emerald-400 mx-auto mb-1" />
                  <span className="text-[10px] text-slate-400 block font-semibold">Pressure</span>
                  <span className="text-lg font-bold text-white">{weather.pressure_hpa} hPa</span>
                </div>
              </div>
            </div>
          </div>

          {/* Agricultural Weather Warnings */}
          {weather.warnings && weather.warnings.length > 0 && (
            <div className="space-y-2">
              {weather.warnings.map((w, idx) => (
                <div
                  key={idx}
                  className="p-4 rounded-2xl bg-amber-950/40 border border-amber-500/40 text-amber-200 text-xs flex items-center gap-3"
                >
                  <AlertTriangle className="w-5 h-5 text-amber-400 shrink-0" />
                  <span>{lang === 'ta' ? w.ta : w.en}</span>
                </div>
              ))}
            </div>
          )}

          {/* 7-Day Agricultural Forecast Cards */}
          <div className="glass-panel rounded-3xl p-6 sm:p-8 space-y-4">
            <h2 className="text-base font-bold text-white flex items-center gap-2">
              <Calendar className="w-5 h-5 text-emerald-400" />
              <span>7-Day Agricultural Forecast</span>
            </h2>

            <div className="grid grid-cols-2 sm:grid-cols-4 md:grid-cols-7 gap-3">
              {weather.forecast.map((f, i) => (
                <div
                  key={i}
                  className="p-3.5 rounded-2xl bg-slate-900/60 border border-slate-800 text-center space-y-1.5"
                >
                  <span className="text-[11px] font-bold text-slate-400 block">{f.date}</span>
                  <div className="text-base font-extrabold text-white">{f.temp_max}°C</div>
                  <div className="text-[10px] text-slate-400">Min: {f.temp_min}°C</div>
                  <div className="text-[10px] text-emerald-300 font-semibold pt-1 border-t border-slate-800/80">
                    {f.precipitation_mm} mm ({f.rain_probability_pct}%)
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      ) : null}
    </div>
  );
};
