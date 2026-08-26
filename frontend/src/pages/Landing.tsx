import React from 'react';
import { Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import {
  Sprout,
  TrendingUp,
  CloudSun,
  FlaskConical,
  Bot,
  MapPin,
  ShieldCheck,
  ArrowRight,
  CheckCircle2
} from 'lucide-react';

export const Landing: React.FC = () => {
  const { t } = useTranslation();

  const features = [
    {
      icon: Sprout,
      title: "AI Crop Yield Prediction",
      titleTa: "AI பயிர் மகசூல் கணிப்பு",
      desc: "Trained on ICAR & TNAU datasets to predict per-acre yield and total farm production with 97%+ model accuracy.",
      descTa: "தமிழ்நாடு வேளாண் பல்கலைக்கழக தரவுகளுடன் 97% துல்லியத்துடன் மகசூல் கணிக்கும் AI மாதிரி."
    },
    {
      icon: CloudSun,
      title: "Live Taluk-Level Weather",
      titleTa: "நேரடி வட்ட அளவிலான வானிலை",
      desc: "Real-time agro-meteorological synchronization, rainfall alerts, and 7-day agricultural forecasts across all 38 districts.",
      descTa: "38 மாவட்டங்களுக்கும் நேரடி மழை, வெப்பநிலை, ஈரப்பதம் மற்றும் 7 நாள் விவசாய வானிலை முன்னறிவிப்பு."
    },
    {
      icon: FlaskConical,
      title: "Soil Report OCR Extraction",
      titleTa: "மண் பரிசோதனை அறிக்கை ஆய்வு",
      desc: "Upload photo or PDF of Soil Health Cards to auto-extract pH, EC, N, P, K and Organic Carbon effortlessly.",
      descTa: "மண் அட்டை புகைப்படத்தை பதிவேற்றி pH, தழை, மணி, சாம்பல் சத்து அளவுகளை உடனடியாக பிரித்தெடுக்கும் வசதி."
    },
    {
      icon: Bot,
      title: "Dual Multilingual AI Assistants",
      titleTa: "இருமொழி AI வேளாண் உதவியாளர்",
      desc: "General farming Q&A and post-prediction contextual assistant in natural Tamil and English.",
      descTa: "பொது விவசாய கேள்விகள் மற்றும் உங்கள் பண்ணை மகசூல் குறித்த தனிப்பட்ட AI ஆலோசனை."
    }
  ];

  return (
    <div className="space-y-16 py-8 sm:py-12">
      {/* Hero Section */}
      <section className="text-center max-w-4xl mx-auto px-4 space-y-6">
        <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-emerald-500/10 text-emerald-300 border border-emerald-500/20 text-xs sm:text-sm font-semibold animate-pulse-slow">
          <Sprout className="w-4 h-4 text-emerald-400" />
          <span>{t('app_subtitle')}</span>
        </div>

        <h1 className="text-4xl sm:text-6xl font-black text-white tracking-tight leading-tight">
          {t('app_name')}
        </h1>

        <p className="text-base sm:text-xl text-slate-300 leading-relaxed max-w-2xl mx-auto">
          {t('tagline')}
        </p>

        <div className="flex flex-col sm:flex-row items-center justify-center gap-4 pt-4">
          <Link
            to="/signup"
            className="w-full sm:w-auto px-8 py-4 rounded-xl bg-gradient-to-r from-emerald-500 to-green-600 hover:from-emerald-400 hover:to-green-500 text-slate-950 font-bold text-base shadow-xl shadow-emerald-500/25 flex items-center justify-center gap-2 transition-all transform hover:-translate-y-0.5"
          >
            <span>{t('nav.signup')}</span>
            <ArrowRight className="w-5 h-5" />
          </Link>
          <Link
            to="/login"
            className="w-full sm:w-auto px-8 py-4 rounded-xl glass-card hover:bg-slate-800/80 text-white font-semibold text-base border border-slate-700 transition-colors"
          >
            {t('nav.login')}
          </Link>
        </div>

        {/* Quick Highlights Badge Bar */}
        <div className="pt-8 flex flex-wrap items-center justify-center gap-6 text-xs sm:text-sm text-slate-400 font-medium">
          <span className="flex items-center gap-1.5">
            <CheckCircle2 className="w-4 h-4 text-emerald-400" /> 38 Districts & All Taluks
          </span>
          <span className="flex items-center gap-1.5">
            <CheckCircle2 className="w-4 h-4 text-emerald-400" /> 50+ Tamil Nadu Crops
          </span>
          <span className="flex items-center gap-1.5">
            <CheckCircle2 className="w-4 h-4 text-emerald-400" /> Tamil & English Support
          </span>
          <span className="flex items-center gap-1.5">
            <CheckCircle2 className="w-4 h-4 text-emerald-400" /> Live Weather Sync
          </span>
        </div>
      </section>

      {/* Feature Cards Grid */}
      <section className="max-w-6xl mx-auto px-4">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {features.map((feat, idx) => {
            const Icon = feat.icon;
            return (
              <div
                key={idx}
                className="glass-panel glass-card-hover rounded-2xl p-6 sm:p-8 space-y-3 relative overflow-hidden"
              >
                <div className="w-12 h-12 rounded-xl bg-emerald-500/20 border border-emerald-500/30 flex items-center justify-center text-emerald-400 mb-4">
                  <Icon className="w-6 h-6" />
                </div>
                <h3 className="text-xl font-bold text-white">{feat.title}</h3>
                <p className="text-sm text-slate-300 leading-relaxed">{feat.desc}</p>
              </div>
            );
          })}
        </div>
      </section>

      {/* CTA Box */}
      <section className="max-w-4xl mx-auto px-4">
        <div className="glass-panel rounded-3xl p-8 sm:p-12 text-center relative overflow-hidden border border-emerald-500/30">
          <div className="space-y-4 max-w-xl mx-auto">
            <h2 className="text-2xl sm:text-3xl font-extrabold text-white">
              Ready to Maximize Your Farm's Harvest?
            </h2>
            <p className="text-sm sm:text-base text-slate-300">
              Get precision crop yield calculations, fertilizer plans, and immediate weather advisories for your specific land.
            </p>
            <div className="pt-2">
              <Link
                to="/signup"
                className="inline-flex items-center gap-2 px-8 py-3.5 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold shadow-lg shadow-emerald-500/20 transition-all"
              >
                <span>{t('auth.register_btn')}</span>
                <ArrowRight className="w-4 h-4" />
              </Link>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};
