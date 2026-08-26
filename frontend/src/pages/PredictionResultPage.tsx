import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import api from '../services/api';
import { PredictionResult, ActionPlan } from '../types';
import { YieldGauge } from '../components/YieldGauge';
import { FactorChart } from '../components/FactorChart';
import {
  Sprout,
  Calendar,
  Layers,
  Sparkles,
  Bot,
  Send,
  CheckCircle2,
  AlertCircle,
  HelpCircle,
  Clock,
  ArrowRight,
  TrendingUp,
  MapPin
} from 'lucide-react';

export const PredictionResultPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const { t, i18n } = useTranslation();
  const lang = i18n.language || 'ta';

  const [prediction, setPrediction] = useState<PredictionResult | null>(null);
  const [actionPlan, setActionPlan] = useState<ActionPlan | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');

  // Post-prediction Chatbot State
  const [chatMessages, setChatMessages] = useState<Array<{ sender: string; message: string }>>([
    {
      sender: 'ai',
      message:
        lang === 'ta'
          ? 'வணக்கம்! உங்கள் பண்ணை மகசூல் கணிப்பு மற்றும் சாகுபடி அட்டவணை தயார். உரம், நீர் பாசனம் அல்லது மகசூலை அதிகரிப்பது பற்றி என்னிடம் கேள்வி கேட்கலாம்.'
          : 'Welcome! Your crop yield prediction and cultivation action plan are ready. Feel free to ask me anything about fertilizers, pest management, or boosting your yield.',
    },
  ]);
  const [inputMessage, setInputMessage] = useState('');
  const [isChatSending, setIsChatSending] = useState(false);

  useEffect(() => {
    if (!id) return;
    setIsLoading(true);

    Promise.all([
      api.get(`/predictions/${id}`),
      api.get(`/recommendations/${id}`),
    ])
      .then(([predRes, recRes]) => {
        setPrediction(predRes.data);
        setActionPlan(recRes.data);
      })
      .catch((err) => {
        console.error('Error fetching prediction report:', err);
        setError('Unable to load prediction record. Please try again.');
      })
      .finally(() => setIsLoading(false));
  }, [id]);

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputMessage.trim() || !id || isChatSending) return;

    const userText = inputMessage.trim();
    setInputMessage('');
    setChatMessages((prev) => [...prev, { sender: 'user', message: userText }]);
    setIsChatSending(true);

    try {
      const res = await api.post('/chat/prediction', {
        prediction_id: parseInt(id),
        message: userText,
      });

      setChatMessages((prev) => [
        ...prev,
        { sender: 'ai', message: res.data.message },
      ]);
    } catch (err: any) {
      setChatMessages((prev) => [
        ...prev,
        {
          sender: 'ai',
          message:
            lang === 'ta'
              ? 'மன்னிக்கவும். தகவல் பெறுவதில் சிக்கல் ஏற்பட்டது. மீண்டும் முயற்சிக்கவும்.'
              : 'Sorry, there was an issue processing your request. Please try again.',
        },
      ]);
    } finally {
      setIsChatSending(false);
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-[60vh] flex flex-col items-center justify-center space-y-3">
        <div className="w-12 h-12 rounded-full border-4 border-emerald-500 border-t-transparent animate-spin" />
        <span className="text-sm font-semibold text-slate-300">{t('common.loading')}</span>
      </div>
    );
  }

  if (error || !prediction) {
    return (
      <div className="p-8 text-center glass-panel rounded-3xl max-w-lg mx-auto space-y-4">
        <AlertCircle className="w-12 h-12 text-red-400 mx-auto" />
        <h2 className="text-xl font-bold text-white">Prediction Record Not Found</h2>
        <p className="text-xs text-slate-300">{error || 'Please make a new prediction.'}</p>
        <Link to="/predict" className="inline-block px-6 py-2.5 rounded-xl bg-emerald-500 text-slate-950 font-bold text-xs">
          Make Prediction
        </Link>
      </div>
    );
  }

  const cropName = lang === 'ta' ? prediction.crop_name_ta : prediction.crop_name_en;
  const districtName = lang === 'ta' ? prediction.district_name_ta : prediction.district_name_en;
  const talukName = lang === 'ta' ? prediction.taluk_name_ta : prediction.taluk_name_en;
  const explanation = lang === 'ta' ? prediction.explanation_ta : prediction.explanation_en;
  const whatNow = actionPlan?.what_should_i_do_now;

  return (
    <div className="max-w-5xl mx-auto space-y-6 pb-16">
      {/* Header Info */}
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 text-xs font-semibold text-emerald-400">
            <MapPin className="w-4 h-4" />
            <span>{districtName} • {talukName} • {prediction.pattam}</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-white mt-1">
            {cropName} {t('result.estimated_yield')}
          </h1>
        </div>

        <div className="flex items-center gap-3">
          <Link
            to="/predict"
            className="px-4 py-2 rounded-xl glass-card text-xs font-semibold text-slate-200 hover:text-white border border-slate-700"
          >
            + New Prediction
          </Link>
        </div>
      </div>

      {/* Main Yield Gauge Dial Card */}
      <YieldGauge
        predictedYield={prediction.predicted_yield_per_acre}
        totalProduction={prediction.total_production_kg}
        landArea={prediction.land_area_acres}
        cropName={cropName}
        typicalMin={prediction.typical_yield_min_acre}
        typicalMax={prediction.typical_yield_max_acre}
        confidenceScore={prediction.confidence_score}
      />

      {/* AI Explanation Callout */}
      <div className="glass-panel rounded-2xl p-5 sm:p-6 border border-emerald-500/20 space-y-2">
        <div className="flex items-center gap-2 text-sm font-bold text-emerald-300">
          <Sparkles className="w-4 h-4 text-emerald-400" />
          <span>AI Agronomic Analysis</span>
        </div>
        <p className="text-xs sm:text-sm text-slate-200 whitespace-pre-line leading-relaxed">
          {explanation}
        </p>
      </div>

      {/* Explainable AI Factors */}
      {prediction.factors && prediction.factors.length > 0 && (
        <FactorChart factors={prediction.factors} />
      )}

      {/* "What Should I Do Now?" Priority Action Box */}
      {whatNow && (
        <div className="glass-panel rounded-2xl p-6 border border-amber-500/30 bg-gradient-to-br from-slate-900/90 to-amber-950/20 space-y-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2 text-base font-bold text-amber-300">
              <Clock className="w-5 h-5 text-amber-400" />
              <span>{t('result.what_to_do_now_title')}</span>
            </div>
            <span className="text-xs font-semibold px-2.5 py-0.5 rounded-full bg-amber-500/20 text-amber-300 border border-amber-500/30">
              {lang === 'ta' ? whatNow.current_stage_ta : whatNow.current_stage_en}
            </span>
          </div>

          <div className="space-y-2">
            <span className="text-xs font-bold text-slate-400 uppercase tracking-wider block">
              {t('result.today_task')}
            </span>
            <ul className="space-y-1.5 text-xs sm:text-sm text-slate-200">
              {(lang === 'ta' ? whatNow.today_actions_ta : whatNow.today_actions_en).map((act, i) => (
                <li key={i} className="flex items-start gap-2">
                  <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
                  <span>{act}</span>
                </li>
              ))}
            </ul>
          </div>

          {(whatNow.weather_alert_en || whatNow.weather_alert_ta) && (
            <div className="p-3 rounded-xl bg-slate-900/90 border border-amber-500/40 text-xs text-amber-200 flex items-center gap-2">
              <AlertCircle className="w-4 h-4 text-amber-400 shrink-0" />
              <span>{lang === 'ta' ? whatNow.weather_alert_ta : whatNow.weather_alert_en}</span>
            </div>
          )}
        </div>
      )}

      {/* Stage-by-stage Cultivation Timeline */}
      {actionPlan?.timeline_stages && actionPlan.timeline_stages.length > 0 && (
        <div className="glass-panel rounded-2xl p-6 space-y-5">
          <h3 className="text-base font-bold text-slate-100 flex items-center gap-2">
            <Calendar className="w-5 h-5 text-emerald-400" />
            <span>{t('result.action_plan_title')}</span>
          </h3>

          <div className="space-y-4 relative before:absolute before:inset-0 before:left-3.5 before:w-0.5 before:bg-slate-800">
            {actionPlan.timeline_stages.map((stage) => {
              const title = lang === 'ta' ? stage.title_ta : stage.title_en;
              const tasks = lang === 'ta' ? stage.tasks_ta : stage.tasks_en;

              return (
                <div key={stage.stage_number} className="relative pl-9 space-y-2">
                  <div className="absolute left-1.5 top-1 w-4 h-4 rounded-full bg-emerald-500 border-4 border-slate-950 flex items-center justify-center" />
                  <div className="flex flex-wrap items-center justify-between gap-2">
                    <span className="text-sm font-bold text-white">{title}</span>
                    <span className="text-[11px] font-semibold text-emerald-400 px-2 py-0.5 rounded-md bg-emerald-950/60 border border-emerald-800/40">
                      {stage.timeline_days}
                    </span>
                  </div>
                  <ul className="space-y-1 text-xs text-slate-300">
                    {tasks.map((tsk, idx) => (
                      <li key={idx} className="flex items-start gap-2">
                        <span className="text-emerald-400">•</span>
                        <span>{tsk}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Integrated Post-Prediction AI Farmer Chatbot */}
      <div className="glass-panel rounded-3xl p-6 sm:p-8 space-y-4 border border-emerald-500/30">
        <div className="flex items-center gap-3 pb-3 border-b border-slate-800">
          <div className="w-10 h-10 rounded-xl bg-emerald-500/20 flex items-center justify-center text-emerald-400">
            <Bot className="w-6 h-6" />
          </div>
          <div>
            <h3 className="text-base font-bold text-white">{t('result.post_chat_title')}</h3>
            <p className="text-xs text-slate-400">{t('result.post_chat_desc')}</p>
          </div>
        </div>

        {/* Chat message bubbles */}
        <div className="space-y-3 max-h-72 overflow-y-auto pr-2 py-2">
          {chatMessages.map((msg, i) => (
            <div
              key={i}
              className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-[85%] p-3.5 rounded-2xl text-xs sm:text-sm leading-relaxed whitespace-pre-line ${
                  msg.sender === 'user'
                    ? 'bg-emerald-600 text-slate-950 font-medium rounded-tr-none'
                    : 'bg-slate-900/90 text-slate-100 border border-slate-800 rounded-tl-none'
                }`}
              >
                {msg.message}
              </div>
            </div>
          ))}
          {isChatSending && (
            <div className="flex justify-start">
              <div className="p-3 rounded-2xl bg-slate-900 border border-slate-800 text-xs text-emerald-400 flex items-center gap-2">
                <span className="w-2 h-2 rounded-full bg-emerald-400 animate-ping" />
                <span>AI is formulating agronomy advice...</span>
              </div>
            </div>
          )}
        </div>

        {/* Input box */}
        <form onSubmit={handleSendMessage} className="flex gap-2 pt-2">
          <input
            type="text"
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            placeholder={t('result.chat_placeholder')}
            className="flex-1 bg-slate-900 border border-slate-700/80 focus:border-emerald-500 rounded-xl px-4 py-2.5 text-xs sm:text-sm text-white focus:outline-none focus:ring-1 focus:ring-emerald-500"
          />
          <button
            type="submit"
            disabled={isChatSending || !inputMessage.trim()}
            className="px-5 py-2.5 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold text-xs flex items-center gap-1.5 disabled:opacity-40 transition-all"
          >
            <span>{t('chatbot.send')}</span>
            <Send className="w-3.5 h-3.5" />
          </button>
        </form>
      </div>
    </div>
  );
};
