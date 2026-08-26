import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import api from '../services/api';
import { Bot, Send, Sparkles, AlertCircle, HelpCircle, RotateCcw } from 'lucide-react';

export const GeneralChatPage: React.FC = () => {
  const { t, i18n } = useTranslation();
  const lang = i18n.language || 'ta';

  const initialMessage = {
    sender: 'ai',
    message:
      lang === 'ta'
        ? 'வணக்கம்! நான் உங்கள் AI வேளாண்மை உதவியாளர். தமிழ்நாடு பயிர்கள், உரம், விதைப்பு காலம், பூச்சி மேலாண்மை அல்லது வானிலை குறித்து என்னிடம் கேளுங்கள்.'
        : 'Vanakkam! I am your AI Agricultural Assistant. Ask me anything about Tamil Nadu crops, fertilizers, sowing seasons (Pattams), pest management, or irrigation.',
  };

  const [messages, setMessages] = useState<Array<{ sender: string; message: string; isRefusal?: boolean }>>([
    initialMessage,
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const suggestedQuestions = [
    t('chatbot.q1'),
    t('chatbot.q2'),
    t('chatbot.q3'),
    t('chatbot.q4'),
  ];

  const handleSend = async (queryText?: string) => {
    const textToSend = queryText || input.trim();
    if (!textToSend || isLoading) return;

    setInput('');
    setMessages((prev) => [...prev, { sender: 'user', message: textToSend }]);
    setIsLoading(true);

    try {
      const res = await api.post('/chat/general', {
        message: textToSend,
      });

      setMessages((prev) => [
        ...prev,
        {
          sender: 'ai',
          message: res.data.message,
          isRefusal: res.data.is_refusal,
        },
      ]);
    } catch (err: any) {
      setMessages((prev) => [
        ...prev,
        {
          sender: 'ai',
          message:
            lang === 'ta'
              ? 'மன்னிக்கவும். சேவையகத்துடன் இணைக்க முடியவில்லை. மீண்டும் முயற்சிக்கவும்.'
              : 'Sorry, unable to connect to the agricultural intelligence service. Please try again.',
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-4 pb-12">
      {/* Header */}
      <div className="glass-panel rounded-3xl p-6 border border-emerald-500/20 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-12 h-12 rounded-2xl bg-gradient-to-tr from-emerald-600 to-green-400 flex items-center justify-center text-slate-950 shadow-lg shadow-emerald-500/20 font-bold">
            <Bot className="w-7 h-7" />
          </div>
          <div>
            <h1 className="text-xl sm:text-2xl font-extrabold text-white">{t('chatbot.title')}</h1>
            <p className="text-xs text-slate-300">{t('chatbot.subtitle')}</p>
          </div>
        </div>

        <button
          onClick={() => setMessages([initialMessage])}
          className="p-2.5 rounded-xl glass-card hover:bg-slate-800 text-slate-300 text-xs flex items-center gap-1.5 border border-slate-700 transition-colors"
          title={t('chatbot.clear')}
        >
          <RotateCcw className="w-3.5 h-3.5" />
          <span className="hidden sm:inline">{t('chatbot.clear')}</span>
        </button>
      </div>

      {/* Suggested Prompts */}
      <div className="space-y-1.5">
        <span className="text-[11px] font-bold text-slate-400 flex items-center gap-1.5 px-1">
          <Sparkles className="w-3.5 h-3.5 text-emerald-400" />
          <span>{t('chatbot.suggested_title')}</span>
        </span>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
          {suggestedQuestions.map((q, idx) => (
            <button
              key={idx}
              onClick={() => handleSend(q)}
              className="p-2.5 rounded-xl bg-slate-900/60 hover:bg-slate-850 border border-slate-800 hover:border-emerald-500/40 text-left text-xs text-slate-300 hover:text-emerald-300 transition-all flex items-center justify-between"
            >
              <span className="truncate pr-2">"{q}"</span>
              <span className="text-emerald-400 text-xs">→</span>
            </button>
          ))}
        </div>
      </div>

      {/* Chat Area */}
      <div className="glass-panel rounded-3xl p-5 sm:p-6 min-h-[420px] max-h-[550px] flex flex-col justify-between border border-slate-800">
        {/* Messages list */}
        <div className="flex-1 space-y-3.5 overflow-y-auto pr-2">
          {messages.map((m, idx) => (
            <div
              key={idx}
              className={`flex ${m.sender === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-[85%] p-4 rounded-2xl text-xs sm:text-sm leading-relaxed whitespace-pre-line ${
                  m.sender === 'user'
                    ? 'bg-emerald-600 text-slate-950 font-medium rounded-tr-none shadow-md'
                    : m.isRefusal
                    ? 'bg-amber-950/40 border border-amber-500/30 text-amber-200 rounded-tl-none'
                    : 'bg-slate-900/90 text-slate-100 border border-slate-800 rounded-tl-none shadow-inner'
                }`}
              >
                {m.message}
              </div>
            </div>
          ))}

          {isLoading && (
            <div className="flex justify-start">
              <div className="p-3.5 rounded-2xl bg-slate-900 border border-slate-800 text-xs text-emerald-400 flex items-center gap-2">
                <span className="w-2 h-2 rounded-full bg-emerald-400 animate-ping" />
                <span>AI is formulating answer...</span>
              </div>
            </div>
          )}
        </div>

        {/* Input Bar */}
        <form
          onSubmit={(e) => {
            e.preventDefault();
            handleSend();
          }}
          className="mt-4 pt-3 border-t border-slate-800 flex gap-2"
        >
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder={t('chatbot.input_placeholder')}
            className="flex-1 bg-slate-900/90 border border-slate-700/80 focus:border-emerald-500 rounded-xl px-4 py-3 text-xs sm:text-sm text-white focus:outline-none focus:ring-1 focus:ring-emerald-500"
          />
          <button
            type="submit"
            disabled={isLoading || !input.trim()}
            className="px-6 py-3 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold text-sm shadow-md shadow-emerald-500/20 flex items-center gap-2 disabled:opacity-40 transition-all"
          >
            <span>{t('chatbot.send')}</span>
            <Send className="w-4 h-4" />
          </button>
        </form>
      </div>

      <div className="text-center text-[11px] text-slate-400">
        🛡️ {t('chatbot.scope_notice')}
      </div>
    </div>
  );
};
