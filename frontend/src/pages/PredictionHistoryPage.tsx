import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import api from '../services/api';
import { History, ArrowRight, TrendingUp, Calendar, MapPin, Sprout } from 'lucide-react';
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid } from 'recharts';

export const PredictionHistoryPage: React.FC = () => {
  const { t, i18n } = useTranslation();
  const lang = i18n.language || 'ta';

  const [predictions, setPredictions] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    api.get('/predictions')
      .then((res) => setPredictions(res.data))
      .catch((err) => console.error('Error fetching prediction history:', err))
      .finally(() => setIsLoading(false));
  }, []);

  const chartData = predictions.slice(0, 6).reverse().map((p) => ({
    name: lang === 'ta' ? p.crop_name_ta : p.crop_name_en,
    yieldPerAcre: p.predicted_yield_per_acre,
  }));

  return (
    <div className="max-w-5xl mx-auto space-y-6 pb-12">
      {/* Header */}
      <div className="glass-panel rounded-3xl p-6 sm:p-8 space-y-2 border border-emerald-500/20 flex flex-wrap items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <div className="w-12 h-12 rounded-2xl bg-purple-500/20 flex items-center justify-center text-purple-400 font-bold shadow-lg shadow-purple-500/10">
            <History className="w-7 h-7" />
          </div>
          <div>
            <h1 className="text-xl sm:text-2xl font-extrabold text-white">{t('history.title')}</h1>
            <p className="text-xs text-slate-300">{t('history.subtitle')}</p>
          </div>
        </div>

        <Link
          to="/predict"
          className="px-5 py-2.5 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold text-xs shadow-md shadow-emerald-500/20 flex items-center gap-1.5 transition-all"
        >
          <Sprout className="w-4 h-4" />
          <span>New Prediction</span>
        </Link>
      </div>

      {isLoading ? (
        <div className="py-16 text-center space-y-2">
          <div className="w-10 h-10 rounded-full border-4 border-emerald-500 border-t-transparent animate-spin mx-auto" />
          <span className="text-xs text-slate-400">{t('common.loading')}</span>
        </div>
      ) : predictions.length > 0 ? (
        <>
          {/* Comparison Bar Chart */}
          <div className="glass-panel rounded-3xl p-6 sm:p-8 space-y-4">
            <h3 className="text-sm font-bold text-slate-100 flex items-center gap-2">
              <TrendingUp className="w-4 h-4 text-emerald-400" />
              <span>Yield Comparison (kg / acre)</span>
            </h3>

            <div className="h-60 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={chartData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                  <XAxis dataKey="name" stroke="#94a3b8" fontSize={11} />
                  <YAxis stroke="#94a3b8" fontSize={11} />
                  <Tooltip
                    contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '12px' }}
                    labelStyle={{ color: '#22c55e', fontWeight: 'bold' }}
                  />
                  <Bar dataKey="yieldPerAcre" fill="#22c55e" radius={[8, 8, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Table / List */}
          <div className="glass-panel rounded-3xl p-6 space-y-4">
            <div className="space-y-3">
              {predictions.map((p) => (
                <div
                  key={p.id}
                  className="p-4 sm:p-5 rounded-2xl bg-slate-900/60 border border-slate-800 flex flex-wrap items-center justify-between gap-4 hover:border-slate-700 transition-colors"
                >
                  <div className="space-y-1">
                    <div className="flex items-center gap-2">
                      <span className="text-base font-extrabold text-white">
                        {lang === 'ta' ? p.crop_name_ta : p.crop_name_en}
                      </span>
                      <span className="text-xs text-slate-400">({p.land_area_acres} {t('common.acres')})</span>
                    </div>
                    <div className="flex items-center gap-3 text-xs text-slate-400">
                      <span className="flex items-center gap-1">
                        <MapPin className="w-3.5 h-3.5 text-emerald-400" /> {p.district_name_en}
                      </span>
                      <span className="flex items-center gap-1">
                        <Calendar className="w-3.5 h-3.5 text-amber-400" /> {p.pattam}
                      </span>
                      <span>{p.created_at}</span>
                    </div>
                  </div>

                  <div className="flex items-center gap-6">
                    <div className="text-right">
                      <span className="text-[10px] text-slate-400 uppercase block font-semibold">
                        Yield / Acre
                      </span>
                      <span className="text-base font-bold text-emerald-400">
                        {p.predicted_yield_per_acre.toLocaleString()} kg
                      </span>
                    </div>

                    <div className="text-right">
                      <span className="text-[10px] text-slate-400 uppercase block font-semibold">
                        Total Production
                      </span>
                      <span className="text-base font-bold text-amber-300">
                        {p.total_production_kg.toLocaleString()} kg
                      </span>
                    </div>

                    <Link
                      to={`/predictions/${p.id}`}
                      className="p-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-emerald-400 font-bold text-xs flex items-center gap-1 border border-slate-700"
                    >
                      <span>{t('history.view_analysis')}</span>
                      <ArrowRight className="w-3.5 h-3.5" />
                    </Link>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </>
      ) : (
        <div className="glass-panel rounded-3xl p-12 text-center space-y-4 max-w-md mx-auto">
          <History className="w-12 h-12 text-slate-600 mx-auto" />
          <h2 className="text-base font-bold text-white">{t('dashboard.no_predictions_yet')}</h2>
          <Link
            to="/predict"
            className="inline-block px-6 py-3 rounded-xl bg-emerald-500 text-slate-950 font-bold text-xs shadow-lg shadow-emerald-500/20"
          >
            {t('dashboard.start_first_prediction')}
          </Link>
        </div>
      )}
    </div>
  );
};
