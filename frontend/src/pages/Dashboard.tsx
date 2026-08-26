import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { useAuth } from '../context/AuthContext';
import api from '../services/api';
import { WeatherData } from '../types';
import {
  Sprout,
  CloudSun,
  FlaskConical,
  Bot,
  History,
  TrendingUp,
  ArrowRight,
  Sparkles,
  Calendar,
  AlertCircle,
  Thermometer,
  Droplets,
  Wind
} from 'lucide-react';

export const Dashboard: React.FC = () => {
  const { t, i18n } = useTranslation();
  const lang = i18n.language || 'ta';
  const { user } = useAuth();

  const [weather, setWeather] = useState<WeatherData | null>(null);
  const [recentPredictions, setRecentPredictions] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const loadDashboardData = async () => {
      try {
        // Fetch recent predictions
        const predsRes = await api.get('/predictions');
        setRecentPredictions(predsRes.data.slice(0, 3));

        // Fetch live weather for farmer's default district/taluk or Coimbatore baseline
        const distId = user?.district_id || 4; // Coimbatore / Erode
        const tlkId = user?.taluk_id || 1;
        const weatherRes = await api.get(`/weather/${distId}/${tlkId}`);
        setWeather(weatherRes.data);
      } catch (err) {
        console.error('Error loading dashboard data:', err);
      } finally {
        setIsLoading(false);
      }
    };

    loadDashboardData();
  }, [user]);

  const latest = recentPredictions[0];

  return (
    <div className="space-y-6">
      {/* Welcome Banner */}
      <div className="glass-panel rounded-3xl p-6 sm:p-8 relative overflow-hidden border border-emerald-500/20 bg-gradient-to-r from-slate-900/90 via-slate-900/60 to-emerald-950/40">
        <div className="max-w-2xl space-y-2">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 text-emerald-400 text-xs font-semibold border border-emerald-500/20">
            <Sparkles className="w-3.5 h-3.5" />
            <span>AI Powered Smart Farming</span>
          </div>
          <h1 className="text-2xl sm:text-4xl font-extrabold text-white">
            {t('dashboard.greeting')}, {user?.full_name || 'Farmer'}!
          </h1>
          <p className="text-xs sm:text-sm text-slate-300">
            {user?.district_name
              ? `${user.district_name} • ${user.taluk_name || ''}`
              : 'Tamil Nadu Agriculture Decision Support'}
          </p>
        </div>

        <div className="mt-6 flex flex-wrap gap-3">
          <Link
            to="/predict"
            className="px-6 py-3 rounded-xl bg-gradient-to-r from-emerald-500 to-green-600 hover:from-emerald-400 hover:to-green-500 text-slate-950 font-bold text-sm shadow-lg shadow-emerald-500/20 flex items-center gap-2 transition-all transform hover:-translate-y-0.5"
          >
            <Sprout className="w-4 h-4" />
            <span>{t('dashboard.quick_predict')}</span>
            <ArrowRight className="w-4 h-4 ml-1" />
          </Link>
          <Link
            to="/chat"
            className="px-5 py-3 rounded-xl glass-card hover:bg-slate-800 text-white font-semibold text-sm flex items-center gap-2 border border-slate-700 transition-colors"
          >
            <Bot className="w-4 h-4 text-emerald-400" />
            <span>{t('dashboard.ask_ai')}</span>
          </Link>
        </div>
      </div>

      {/* Top 3 Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
        {/* Card 1: Live Weather */}
        <div className="glass-panel glass-card-hover rounded-2xl p-5 space-y-4 border border-emerald-500/20">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2 text-sm font-bold text-slate-200">
              <CloudSun className="w-5 h-5 text-amber-400" />
              <span>{t('dashboard.live_weather')}</span>
            </div>
            <Link to="/weather" className="text-xs text-emerald-400 hover:underline">
              {t('common.next')} →
            </Link>
          </div>

          {weather ? (
            <div className="space-y-3">
              <div className="flex items-baseline justify-between">
                <span className="text-3xl font-extrabold text-white">
                  {weather.temperature}°C
                </span>
                <span className="text-xs font-semibold px-2.5 py-1 rounded-lg bg-slate-800 text-emerald-300">
                  {lang === 'ta' ? weather.condition_ta : weather.condition_en}
                </span>
              </div>
              <div className="grid grid-cols-3 gap-2 pt-1 text-center text-xs">
                <div className="p-2 rounded-lg bg-slate-900/60 border border-slate-800">
                  <Droplets className="w-3.5 h-3.5 mx-auto text-blue-400 mb-1" />
                  <span className="text-slate-400 text-[10px] block">{t('dashboard.humidity')}</span>
                  <span className="font-bold text-white">{weather.humidity}%</span>
                </div>
                <div className="p-2 rounded-lg bg-slate-900/60 border border-slate-800">
                  <CloudSun className="w-3.5 h-3.5 mx-auto text-amber-400 mb-1" />
                  <span className="text-slate-400 text-[10px] block">{t('dashboard.rainfall')}</span>
                  <span className="font-bold text-white">{weather.rainfall_mm} mm</span>
                </div>
                <div className="p-2 rounded-lg bg-slate-900/60 border border-slate-800">
                  <Wind className="w-3.5 h-3.5 mx-auto text-teal-400 mb-1" />
                  <span className="text-slate-400 text-[10px] block">{t('dashboard.wind')}</span>
                  <span className="font-bold text-white">{weather.wind_speed_kmh} km/h</span>
                </div>
              </div>
            </div>
          ) : (
            <div className="text-xs text-slate-400 py-4">{t('common.loading')}</div>
          )}
        </div>

        {/* Card 2: Latest Prediction */}
        <div className="glass-panel glass-card-hover rounded-2xl p-5 space-y-4 border border-emerald-500/20">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2 text-sm font-bold text-slate-200">
              <TrendingUp className="w-5 h-5 text-emerald-400" />
              <span>Latest Prediction</span>
            </div>
            <Link to="/predictions" className="text-xs text-emerald-400 hover:underline">
              History →
            </Link>
          </div>

          {latest ? (
            <div className="space-y-3">
              <div>
                <div className="text-lg font-bold text-white">
                  {lang === 'ta' ? latest.crop_name_ta : latest.crop_name_en}
                </div>
                <div className="text-xs text-slate-400">
                  {latest.pattam} • {latest.land_area_acres} {t('common.acres')}
                </div>
              </div>
              <div className="p-3 rounded-xl bg-slate-900/70 border border-slate-800 flex items-center justify-between">
                <div>
                  <span className="text-[10px] uppercase text-slate-400 block font-semibold">
                    Yield / Acre
                  </span>
                  <span className="text-lg font-extrabold text-emerald-400">
                    {latest.predicted_yield_per_acre.toLocaleString()} kg
                  </span>
                </div>
                <div className="text-right">
                  <span className="text-[10px] uppercase text-slate-400 block font-semibold">
                    Total Production
                  </span>
                  <span className="text-lg font-extrabold text-amber-300">
                    {latest.total_production_kg.toLocaleString()} kg
                  </span>
                </div>
              </div>
            </div>
          ) : (
            <div className="space-y-2 py-3 text-center">
              <p className="text-xs text-slate-400">{t('dashboard.no_predictions_yet')}</p>
              <Link
                to="/predict"
                className="inline-block text-xs font-bold text-emerald-400 hover:underline"
              >
                + {t('dashboard.start_first_prediction')}
              </Link>
            </div>
          )}
        </div>

        {/* Card 3: Quick AI Assistant */}
        <div className="glass-panel glass-card-hover rounded-2xl p-5 space-y-4 border border-emerald-500/20 flex flex-col justify-between">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2 text-sm font-bold text-slate-200">
              <Bot className="w-5 h-5 text-emerald-400" />
              <span>{t('dashboard.ask_ai')}</span>
            </div>
            <span className="text-[10px] px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 font-bold">
              24/7 AI
            </span>
          </div>

          <div className="space-y-2">
            <p className="text-xs text-slate-300">
              Ask any question about Tamil Nadu crops, fertilizers, pest control, or season calendars.
            </p>
            <div className="p-2.5 rounded-xl bg-slate-900/60 border border-slate-800 text-xs text-emerald-300/90 italic">
              "நெல் பயிருக்கு எப்போது உரம் போட வேண்டும்?"
            </div>
          </div>

          <Link
            to="/chat"
            className="w-full py-2.5 rounded-xl bg-emerald-500/20 hover:bg-emerald-500/30 border border-emerald-500/30 text-emerald-300 text-xs font-bold flex items-center justify-center gap-2 transition-colors"
          >
            <span>Start Chatting</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </Link>
        </div>
      </div>

      {/* Quick Action Navigation Grid */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <Link
          to="/predict"
          className="glass-panel glass-card-hover p-4 rounded-2xl flex items-center gap-3 border border-slate-800"
        >
          <div className="w-10 h-10 rounded-xl bg-emerald-500/20 flex items-center justify-center text-emerald-400">
            <Sprout className="w-5 h-5" />
          </div>
          <div>
            <span className="text-xs font-bold text-white block">{t('nav.predict_yield')}</span>
            <span className="text-[10px] text-slate-400">AI Calculation</span>
          </div>
        </Link>

        <Link
          to="/soil"
          className="glass-panel glass-card-hover p-4 rounded-2xl flex items-center gap-3 border border-slate-800"
        >
          <div className="w-10 h-10 rounded-xl bg-blue-500/20 flex items-center justify-center text-blue-400">
            <FlaskConical className="w-5 h-5" />
          </div>
          <div>
            <span className="text-xs font-bold text-white block">{t('nav.soil_health')}</span>
            <span className="text-[10px] text-slate-400">Upload & OCR</span>
          </div>
        </Link>

        <Link
          to="/crops"
          className="glass-panel glass-card-hover p-4 rounded-2xl flex items-center gap-3 border border-slate-800"
        >
          <div className="w-10 h-10 rounded-xl bg-amber-500/20 flex items-center justify-center text-amber-400">
            <Calendar className="w-5 h-5" />
          </div>
          <div>
            <span className="text-xs font-bold text-white block">{t('nav.crops_catalog')}</span>
            <span className="text-[10px] text-slate-400">50+ TN Crops</span>
          </div>
        </Link>

        <Link
          to="/predictions"
          className="glass-panel glass-card-hover p-4 rounded-2xl flex items-center gap-3 border border-slate-800"
        >
          <div className="w-10 h-10 rounded-xl bg-purple-500/20 flex items-center justify-center text-purple-400">
            <History className="w-5 h-5" />
          </div>
          <div>
            <span className="text-xs font-bold text-white block">{t('nav.my_predictions')}</span>
            <span className="text-[10px] text-slate-400">Past Reports</span>
          </div>
        </Link>
      </div>
    </div>
  );
};
