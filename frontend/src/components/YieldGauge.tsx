import React from 'react';
import { useTranslation } from 'react-i18next';
import { TrendingUp, Award, Sparkles } from 'lucide-react';

interface YieldGaugeProps {
  predictedYield: number;
  totalProduction: number;
  landArea: number;
  cropName: string;
  typicalMin: number;
  typicalMax: number;
  confidenceScore: number;
}

export const YieldGauge: React.FC<YieldGaugeProps> = ({
  predictedYield,
  totalProduction,
  landArea,
  cropName,
  typicalMin,
  typicalMax,
  confidenceScore,
}) => {
  const { t } = useTranslation();
  const benchmarkAvg = (typicalMin + typicalMax) / 2.0;
  const percentage = Math.min(100, Math.max(10, (predictedYield / (typicalMax * 1.25)) * 100));
  const diffPct = (((predictedYield - benchmarkAvg) / benchmarkAvg) * 100).toFixed(1);
  const isPositive = predictedYield >= benchmarkAvg;

  return (
    <div className="glass-panel rounded-2xl p-6 relative overflow-hidden border border-emerald-500/30">
      {/* Background ambient glow */}
      <div className="absolute top-0 right-0 w-64 h-64 bg-emerald-500/10 rounded-full blur-3xl -z-10 pointer-events-none" />

      <div className="flex flex-col md:flex-row md:items-center justify-between gap-6">
        {/* Left Side: Yield & Production stats */}
        <div className="space-y-4">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/20 text-emerald-300 text-xs font-bold border border-emerald-500/30">
            <Sparkles className="w-3.5 h-3.5" />
            <span>{t('result.estimated_yield')}</span>
          </div>

          <div>
            <div className="flex items-baseline gap-2">
              <span className="text-4xl sm:text-5xl font-extrabold text-white tracking-tight">
                {predictedYield.toLocaleString()}
              </span>
              <span className="text-lg font-semibold text-emerald-400">
                {t('result.per_acre')}
              </span>
            </div>
            <p className="text-xs text-slate-400 mt-1">
              {cropName} • {typicalMin.toLocaleString()} - {typicalMax.toLocaleString()} {t('result.per_acre')} (TN Baseline)
            </p>
          </div>

          <div className="p-4 rounded-xl bg-slate-900/80 border border-slate-700/60 max-w-md">
            <div className="text-xs font-medium text-slate-400">
              {t('result.total_production')} ({t('result.for_your_farm', { acres: landArea })})
            </div>
            <div className="text-2xl font-bold text-amber-300 mt-0.5">
              {totalProduction.toLocaleString()} {t('common.kg')}
            </div>
          </div>
        </div>

        {/* Right Side: Visual Progress Ring / Benchmark comparison */}
        <div className="flex flex-col items-center md:items-end justify-center min-w-[200px] text-center md:text-right space-y-3">
          <div className="w-32 h-32 rounded-full border-8 border-slate-800 flex flex-col items-center justify-center relative shadow-inner bg-slate-950/60">
            <svg className="w-full h-full absolute -rotate-90" viewBox="0 0 100 100">
              <circle
                cx="50"
                cy="50"
                r="40"
                className="stroke-slate-800"
                strokeWidth="8"
                fill="transparent"
              />
              <circle
                cx="50"
                cy="50"
                r="40"
                className="stroke-emerald-500 transition-all duration-1000 ease-out"
                strokeWidth="8"
                strokeDasharray={`${(percentage * 251) / 100} 251`}
                strokeLinecap="round"
                fill="transparent"
              />
            </svg>
            <span className="text-xl font-black text-white relative z-10">
              {Math.round(confidenceScore * 100)}%
            </span>
            <span className="text-[10px] text-slate-400 uppercase font-semibold relative z-10">
              AI Confidence
            </span>
          </div>

          <div className="flex items-center gap-1.5 text-xs font-semibold">
            <TrendingUp className={`w-4 h-4 ${isPositive ? 'text-emerald-400' : 'text-amber-400'}`} />
            <span className={isPositive ? 'text-emerald-300' : 'text-amber-300'}>
              {isPositive ? `+${diffPct}%` : `${diffPct}%`} {t('result.typical_benchmark')}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};
