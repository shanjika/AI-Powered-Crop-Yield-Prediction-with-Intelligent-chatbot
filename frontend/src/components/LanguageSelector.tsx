import React from 'react';
import { useTranslation } from 'react-i18next';
import { changeAppLanguage } from '../i18n';
import { Globe } from 'lucide-react';

export const LanguageSelector: React.FC = () => {
  const { i18n } = useTranslation();
  const currentLang = i18n.language || 'ta';

  const handleToggle = (lang: string) => {
    changeAppLanguage(lang);
  };

  return (
    <div className="flex items-center bg-slate-900/80 border border-slate-700/60 rounded-full p-1 shadow-inner">
      <Globe className="w-4 h-4 text-emerald-400 ml-2 mr-1" />
      <button
        onClick={() => handleToggle('en')}
        className={`px-3 py-1 text-xs font-semibold rounded-full transition-all ${
          currentLang === 'en'
            ? 'bg-emerald-500 text-slate-950 shadow-md font-bold'
            : 'text-slate-300 hover:text-white'
        }`}
      >
        English
      </button>
      <button
        onClick={() => handleToggle('ta')}
        className={`px-3 py-1 text-xs font-semibold rounded-full transition-all ${
          currentLang === 'ta'
            ? 'bg-emerald-500 text-slate-950 shadow-md font-bold'
            : 'text-slate-300 hover:text-white'
        }`}
      >
        தமிழ்
      </button>
    </div>
  );
};
