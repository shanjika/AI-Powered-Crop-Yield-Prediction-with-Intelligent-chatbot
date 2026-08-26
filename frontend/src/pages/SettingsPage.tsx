import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { useAuth } from '../context/AuthContext';
import { useTheme } from '../context/ThemeContext';
import api from '../services/api';
import { District, Taluk } from '../types';
import {
  Settings as SettingsIcon,
  User,
  Sun,
  Moon,
  Monitor,
  Phone,
  Mail,
  MapPin,
  CheckCircle2,
  Save,
  ChevronRight,
  Palette
} from 'lucide-react';

export const SettingsPage: React.FC = () => {
  const { t, i18n } = useTranslation();
  const lang = i18n.language || 'ta';
  const { user, updateUser } = useAuth();
  const { theme, setTheme } = useTheme();

  // Profile form state
  const [fullName, setFullName] = useState(user?.full_name || '');
  const [email, setEmail] = useState(user?.email || '');
  const [districtId, setDistrictId] = useState(user?.district_id ? String(user.district_id) : '');
  const [talukId, setTalukId] = useState(user?.taluk_id ? String(user.taluk_id) : '');
  const [preferredLanguage, setPreferredLanguage] = useState(user?.preferred_language || 'ta');

  // Reference data
  const [districts, setDistricts] = useState<District[]>([]);
  const [taluks, setTaluks] = useState<Taluk[]>([]);

  // Save state
  const [isSaving, setIsSaving] = useState(false);
  const [savedSuccess, setSavedSuccess] = useState(false);
  const [saveError, setSaveError] = useState('');

  // Active section for accordion style
  const [activeSection, setActiveSection] = useState<'theme' | 'profile' | null>('theme');

  useEffect(() => {
    api.get('/districts').then((res) => setDistricts(res.data)).catch(console.error);
  }, []);

  useEffect(() => {
    if (districtId) {
      api.get(`/taluks/${districtId}`)
        .then((res) => {
          setTaluks(res.data);
        })
        .catch(console.error);
    } else {
      setTaluks([]);
    }
  }, [districtId]);

  const handleSaveProfile = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSaving(true);
    setSavedSuccess(false);
    setSaveError('');

    try {
      const params = new URLSearchParams();
      if (fullName) params.append('full_name', fullName);
      if (preferredLanguage) params.append('preferred_language', preferredLanguage);
      if (districtId) params.append('district_id', districtId);
      if (talukId) params.append('taluk_id', talukId);

      const res = await api.put(`/auth/profile?${params.toString()}`);
      updateUser(res.data);
      setSavedSuccess(true);
      setTimeout(() => setSavedSuccess(false), 3000);
    } catch (err: any) {
      setSaveError(err.response?.data?.detail || 'Failed to save profile. Please try again.');
    } finally {
      setIsSaving(false);
    }
  };

  const themeOptions = [
    {
      id: 'dark' as const,
      label: 'Dark Mode',
      labelTa: 'இருண்ட தோற்றம்',
      desc: 'Easy on eyes, ideal for night use',
      descTa: 'இரவு நேர பயன்பாட்டிற்கு ஏற்றது',
      icon: Moon,
      gradient: 'from-slate-800 to-slate-900',
      border: 'border-slate-600',
      selectedBorder: 'border-emerald-500',
      iconColor: 'text-indigo-400',
    },
    {
      id: 'light' as const,
      label: 'Light Mode',
      labelTa: 'வெளிர் தோற்றம்',
      desc: 'Bright and clear, ideal for daytime',
      descTa: 'பகல் நேர பயன்பாட்டிற்கு சிறந்தது',
      icon: Sun,
      gradient: 'from-amber-50 to-white',
      border: 'border-amber-200',
      selectedBorder: 'border-amber-500',
      iconColor: 'text-amber-500',
    },
  ];

  const toggle = (section: 'theme' | 'profile') => {
    setActiveSection((prev) => (prev === section ? null : section));
  };

  return (
    <div className="max-w-2xl mx-auto space-y-4 pb-12">
      {/* Page Header */}
      <div className="glass-panel rounded-3xl p-6 sm:p-8 border border-emerald-500/20 flex items-center gap-4">
        <div className="w-12 h-12 rounded-2xl bg-emerald-500/20 flex items-center justify-center text-emerald-400 shadow-lg shadow-emerald-500/10">
          <SettingsIcon className="w-7 h-7" />
        </div>
        <div>
          <h1 className="text-xl sm:text-2xl font-extrabold text-white">
            {lang === 'ta' ? 'அமைப்புகள்' : 'Settings'}
          </h1>
          <p className="text-xs text-slate-400 mt-0.5">
            {lang === 'ta'
              ? 'உங்கள் சுயவிவரம், தோற்றம் மற்றும் மொழி விருப்பங்களை மாற்றவும்'
              : 'Update your profile details, theme, and language preferences'}
          </p>
        </div>
      </div>

      {/* ────────────────────────────────────────── */}
      {/* SECTION 1: Theme / Appearance             */}
      {/* ────────────────────────────────────────── */}
      <div className="glass-panel rounded-2xl border border-slate-800 overflow-hidden">
        {/* Section Header — clickable accordion */}
        <button
          onClick={() => toggle('theme')}
          className="w-full flex items-center justify-between px-6 py-4 hover:bg-slate-800/40 transition-colors"
        >
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-xl bg-purple-500/20 flex items-center justify-center text-purple-400">
              <Palette className="w-5 h-5" />
            </div>
            <div className="text-left">
              <span className="text-sm font-bold text-white block">
                {lang === 'ta' ? 'தோற்ற அமைப்பு' : 'Appearance & Theme'}
              </span>
              <span className="text-[11px] text-slate-400">
                {lang === 'ta'
                  ? `தற்போது: ${theme === 'dark' ? 'இருண்ட தோற்றம்' : 'வெளிர் தோற்றம்'}`
                  : `Currently: ${theme === 'dark' ? 'Dark Mode' : 'Light Mode'}`}
              </span>
            </div>
          </div>
          <ChevronRight
            className={`w-4 h-4 text-slate-400 transition-transform ${activeSection === 'theme' ? 'rotate-90' : ''}`}
          />
        </button>

        {activeSection === 'theme' && (
          <div className="px-6 pb-6 pt-2 space-y-3 border-t border-slate-800/80">
            <p className="text-xs text-slate-400 mb-4">
              {lang === 'ta'
                ? 'உங்களுக்கு விரும்பிய தோற்றத்தை தேர்வு செய்யுங்கள்'
                : 'Choose your preferred display theme'}
            </p>

            <div className="grid grid-cols-2 gap-3">
              {themeOptions.map((opt) => {
                const Icon = opt.icon;
                const isSelected = theme === opt.id;
                return (
                  <button
                    key={opt.id}
                    onClick={() => setTheme(opt.id)}
                    className={`relative p-4 rounded-2xl border-2 text-left transition-all duration-200 ${
                      isSelected
                        ? `${opt.selectedBorder} shadow-lg`
                        : `${opt.border} hover:border-slate-600`
                    } ${opt.id === 'light' ? 'bg-gradient-to-br from-slate-100/10 to-slate-50/5' : 'bg-gradient-to-br from-slate-900 to-slate-950'}`}
                  >
                    {/* Selected badge */}
                    {isSelected && (
                      <div className="absolute top-2.5 right-2.5 w-5 h-5 rounded-full bg-emerald-500 flex items-center justify-center">
                        <CheckCircle2 className="w-3.5 h-3.5 text-white" />
                      </div>
                    )}

                    <Icon className={`w-7 h-7 mb-2 ${opt.iconColor}`} />
                    <span className="text-sm font-bold text-white block">
                      {lang === 'ta' ? opt.labelTa : opt.label}
                    </span>
                    <span className="text-[11px] text-slate-400 block mt-0.5">
                      {lang === 'ta' ? opt.descTa : opt.desc}
                    </span>
                  </button>
                );
              })}
            </div>
          </div>
        )}
      </div>

      {/* ────────────────────────────────────────── */}
      {/* SECTION 2: Profile Details                */}
      {/* ────────────────────────────────────────── */}
      <div className="glass-panel rounded-2xl border border-slate-800 overflow-hidden">
        {/* Section Header */}
        <button
          onClick={() => toggle('profile')}
          className="w-full flex items-center justify-between px-6 py-4 hover:bg-slate-800/40 transition-colors"
        >
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-xl bg-emerald-500/20 flex items-center justify-center text-emerald-400">
              <User className="w-5 h-5" />
            </div>
            <div className="text-left">
              <span className="text-sm font-bold text-white block">
                {lang === 'ta' ? 'சுயவிவர விபரங்கள்' : 'Profile Details'}
              </span>
              <span className="text-[11px] text-slate-400">
                {user?.full_name || ''} • {user?.mobile_number || ''}
              </span>
            </div>
          </div>
          <ChevronRight
            className={`w-4 h-4 text-slate-400 transition-transform ${activeSection === 'profile' ? 'rotate-90' : ''}`}
          />
        </button>

        {activeSection === 'profile' && (
          <div className="px-6 pb-6 pt-2 border-t border-slate-800/80">
            {/* Read-only identity info bar */}
            <div className="flex flex-wrap gap-3 mb-5 mt-3">
              <div className="flex items-center gap-2 px-3 py-1.5 rounded-xl bg-slate-900 border border-slate-800 text-xs text-slate-300">
                <Phone className="w-3.5 h-3.5 text-emerald-400" />
                <span>{user?.mobile_number || '—'}</span>
              </div>
              {user?.email && (
                <div className="flex items-center gap-2 px-3 py-1.5 rounded-xl bg-slate-900 border border-slate-800 text-xs text-slate-300">
                  <Mail className="w-3.5 h-3.5 text-emerald-400" />
                  <span>{user.email}</span>
                </div>
              )}
            </div>

            {/* Success / Error messages */}
            {savedSuccess && (
              <div className="mb-4 p-3 rounded-xl bg-emerald-950/40 border border-emerald-500/30 text-emerald-300 text-xs flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
                <span>
                  {lang === 'ta'
                    ? 'சுயவிவரம் வெற்றிகரமாக புதுப்பிக்கப்பட்டது!'
                    : 'Profile updated successfully!'}
                </span>
              </div>
            )}

            {saveError && (
              <div className="mb-4 p-3 rounded-xl bg-red-950/40 border border-red-500/30 text-red-300 text-xs">
                {saveError}
              </div>
            )}

            <form onSubmit={handleSaveProfile} className="space-y-4">
              {/* Full Name */}
              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1.5">
                  {lang === 'ta' ? 'முழு பெயர்' : 'Full Name'} *
                </label>
                <input
                  type="text"
                  value={fullName}
                  onChange={(e) => setFullName(e.target.value)}
                  placeholder={lang === 'ta' ? 'உங்கள் பெயர்' : 'Your name'}
                  className="w-full bg-slate-900/90 border border-slate-700 focus:border-emerald-500 rounded-xl px-4 py-2.5 text-sm text-white placeholder-slate-500 focus:outline-none focus:ring-1 focus:ring-emerald-500"
                />
              </div>

              {/* Preferred Language */}
              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1.5">
                  {lang === 'ta' ? 'விருப்ப மொழி' : 'Preferred Language'}
                </label>
                <div className="flex gap-2">
                  <button
                    type="button"
                    onClick={() => setPreferredLanguage('ta')}
                    className={`flex-1 py-2.5 rounded-xl text-xs font-bold border transition-all ${
                      preferredLanguage === 'ta'
                        ? 'bg-emerald-500 border-emerald-500 text-slate-950'
                        : 'bg-slate-900 border-slate-700 text-slate-300 hover:border-slate-500'
                    }`}
                  >
                    தமிழ்
                  </button>
                  <button
                    type="button"
                    onClick={() => setPreferredLanguage('en')}
                    className={`flex-1 py-2.5 rounded-xl text-xs font-bold border transition-all ${
                      preferredLanguage === 'en'
                        ? 'bg-emerald-500 border-emerald-500 text-slate-950'
                        : 'bg-slate-900 border-slate-700 text-slate-300 hover:border-slate-500'
                    }`}
                  >
                    English
                  </button>
                </div>
              </div>

              {/* District & Taluk */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-semibold text-slate-300 mb-1.5">
                    {lang === 'ta' ? 'மாவட்டம்' : 'District'}
                  </label>
                  <select
                    value={districtId}
                    onChange={(e) => {
                      setDistrictId(e.target.value);
                      setTalukId('');
                    }}
                    className="w-full bg-slate-900 border border-slate-700 focus:border-emerald-500 rounded-xl px-3 py-2.5 text-sm text-white focus:outline-none focus:ring-1 focus:ring-emerald-500"
                  >
                    <option value="">
                      {lang === 'ta' ? '-- மாவட்டத்தை தேர்க --' : '-- Choose District --'}
                    </option>
                    {districts.map((d) => (
                      <option key={d.id} value={d.id}>
                        {lang === 'ta' ? `${d.name_ta} (${d.name_en})` : d.name_en}
                      </option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="block text-xs font-semibold text-slate-300 mb-1.5">
                    {lang === 'ta' ? 'வட்டம் (தாலுகா)' : 'Taluk'}
                  </label>
                  <select
                    value={talukId}
                    disabled={!districtId}
                    onChange={(e) => setTalukId(e.target.value)}
                    className="w-full bg-slate-900 border border-slate-700 focus:border-emerald-500 rounded-xl px-3 py-2.5 text-sm text-white focus:outline-none focus:ring-1 focus:ring-emerald-500 disabled:opacity-40"
                  >
                    <option value="">
                      {lang === 'ta' ? '-- வட்டத்தை தேர்க --' : '-- Choose Taluk --'}
                    </option>
                    {taluks.map((tk) => (
                      <option key={tk.id} value={tk.id}>
                        {lang === 'ta' ? `${tk.name_ta} (${tk.name_en})` : tk.name_en}
                      </option>
                    ))}
                  </select>
                </div>
              </div>

              {/* Save Button */}
              <div className="pt-2">
                <button
                  type="submit"
                  disabled={isSaving || !fullName.trim()}
                  className="w-full py-3 rounded-xl bg-gradient-to-r from-emerald-500 to-green-600 hover:from-emerald-400 hover:to-green-500 text-slate-950 font-bold text-sm shadow-lg shadow-emerald-500/20 flex items-center justify-center gap-2 transition-all disabled:opacity-50"
                >
                  <Save className="w-4 h-4" />
                  <span>
                    {isSaving
                      ? lang === 'ta' ? 'சேமிக்கப்படுகிறது...' : 'Saving...'
                      : lang === 'ta' ? 'சுயவிவரத்தை சேமி' : 'Save Profile'}
                  </span>
                </button>
              </div>
            </form>
          </div>
        )}
      </div>

      {/* Current profile summary card */}
      <div className="glass-panel rounded-2xl p-5 border border-slate-800/60">
        <div className="flex items-center gap-3">
          <div className="w-12 h-12 rounded-full bg-gradient-to-tr from-emerald-600 to-green-400 flex items-center justify-center font-black text-slate-950 text-lg shadow-lg shadow-emerald-500/20">
            {(user?.full_name || 'F')[0].toUpperCase()}
          </div>
          <div>
            <p className="text-sm font-bold text-white">{user?.full_name || 'Farmer'}</p>
            <p className="text-xs text-slate-400">{user?.mobile_number || ''}</p>
            {user?.district_name && (
              <p className="text-xs text-emerald-400 flex items-center gap-1 mt-0.5">
                <MapPin className="w-3 h-3" />
                <span>{user.district_name} {user.taluk_name ? `• ${user.taluk_name}` : ''}</span>
              </p>
            )}
          </div>
          <div className="ml-auto flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-slate-800 border border-slate-700 text-[11px] text-slate-300 font-medium">
            {theme === 'dark' ? <Moon className="w-3 h-3 text-indigo-400" /> : <Sun className="w-3 h-3 text-amber-400" />}
            <span>{theme === 'dark' ? 'Dark' : 'Light'}</span>
          </div>
        </div>
      </div>
    </div>
  );
};
