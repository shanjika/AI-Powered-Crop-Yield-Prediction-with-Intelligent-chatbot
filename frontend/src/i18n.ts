import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';

import enCommon from './locales/en/common.json';
import taCommon from './locales/ta/common.json';

const savedLanguage = localStorage.getItem('agri_app_lang') || 'ta';

i18n
  .use(initReactI18next)
  .init({
    resources: {
      en: {
        translation: enCommon,
      },
      ta: {
        translation: taCommon,
      },
    },
    lng: savedLanguage,
    fallbackLng: 'en',
    interpolation: {
      escapeValue: false,
    },
  });

export const changeAppLanguage = (lang: string) => {
  i18n.changeLanguage(lang);
  localStorage.setItem('agri_app_lang', lang);
};

export default i18n;
