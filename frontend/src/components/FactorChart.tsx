import React from 'react';
import { useTranslation } from 'react-i18next';
import { FactorDetail } from '../types';
import { CheckCircle2, AlertTriangle, Info } from 'lucide-react';

interface FactorChartProps {
  factors: FactorDetail[];
}

export const FactorChart: React.FC<FactorChartProps> = ({ factors }) => {
  const { i18n, t } = useTranslation();
  const lang = i18n.language || 'ta';

  return (
    <div className="glass-panel rounded-2xl p-5 sm:p-6 space-y-4">
      <div className="flex items-center justify-between">
        <h3 className="text-base font-bold text-slate-100 flex items-center gap-2">
          <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
          {t('result.factors_title')}
        </h3>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-3 sm:gap-4">
        {factors.map((factor, idx) => {
          const isPos = factor.impact === 'positive';
          const isNeg = factor.impact === 'negative';
          const name = lang === 'ta' ? factor.name_ta : factor.name_en;
          const detail = lang === 'ta' ? factor.detail_ta : factor.detail_en;

          return (
            <div
              key={idx}
              className={`p-3.5 rounded-xl border transition-all ${
                isPos
                  ? 'bg-emerald-950/20 border-emerald-500/30'
                  : isNeg
                  ? 'bg-amber-950/20 border-amber-500/30'
                  : 'bg-slate-900/40 border-slate-700/50'
              }`}
            >
              <div className="flex items-start justify-between gap-2">
                <div className="flex items-center gap-2">
                  {isPos ? (
                    <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
                  ) : isNeg ? (
                    <AlertTriangle className="w-4 h-4 text-amber-400 shrink-0" />
                  ) : (
                    <Info className="w-4 h-4 text-blue-400 shrink-0" />
                  )}
                  <span className="text-sm font-semibold text-white">{name}</span>
                </div>
                <span
                  className={`text-[11px] font-bold px-2 py-0.5 rounded-full ${
                    isPos
                      ? 'bg-emerald-500/20 text-emerald-300'
                      : isNeg
                      ? 'bg-amber-500/20 text-amber-300'
                      : 'bg-slate-700/50 text-slate-300'
                  }`}
                >
                  {isPos ? t('result.positive_factor') : isNeg ? t('result.limiting_factor') : 'Optimal'}
                </span>
              </div>

              {/* Progress Bar */}
              <div className="mt-2 w-full bg-slate-800 rounded-full h-1.5 overflow-hidden">
                <div
                  className={`h-full rounded-full transition-all duration-700 ${
                    isPos ? 'bg-emerald-500' : isNeg ? 'bg-amber-500' : 'bg-blue-500'
                  }`}
                  style={{ width: `${factor.score}%` }}
                />
              </div>

              <p className="text-xs text-slate-300 mt-2 leading-relaxed">{detail}</p>
            </div>
          );
        })}
      </div>
    </div>
  );
};
