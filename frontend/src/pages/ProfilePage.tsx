import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { useAuth } from '../context/AuthContext';
import api from '../services/api';
import { District, Taluk } from '../types';
import { User as UserIcon, Phone, Mail, MapPin, CheckCircle2, Save } from 'lucide-react';

export const ProfilePage: React.FC = () => {
  const { t, i18n } = useTranslation();
  const lang = i18n.language || 'ta';
  const { user, updateUser } = useAuth();

  const [districts, setDistricts] = useState<District[]>([]);
  const [taluks, setTaluks] = useState<Taluk[]>([]);

  const [fullName, setFullName] = useState(user?.full_name || '');
  const [preferredLang, setPreferredLang] = useState(user?.preferred_language || 'ta');
  const [districtId, setDistrictId] = useState(user?.district_id ? String(user.district_id) : '');
  const [talukId, setTalukId] = useState(user?.taluk_id ? String(user.taluk_id) : '');

  const [savedSuccess, setSavedSuccess] = useState(false);
  const [isSaving, setIsSaving] = useState(false);

  useEffect(() => {
    api.get('/districts').then((res) => setDistricts(res.data));
  }, []);

  useEffect(() => {
    if (districtId) {
      api.get(`/taluks/${districtId}`).then((res) => setTaluks(res.data));
    }
  }, [districtId]);

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSaving(true);
    setSavedSuccess(false);

    try {
      const res = await api.put(`/auth/profile?full_name=${encodeURIComponent(fullName)}&preferred_language=${preferredLang}&district_id=${districtId || ''}&taluk_id=${talukId || ''}`);
      updateUser(res.data);
      setSavedSuccess(true);
    } catch (err) {
      console.error('Error updating profile:', err);
    } finally {
      setIsSaving(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto space-y-6 pb-12">
      <div className="glass-panel rounded-3xl p-6 sm:p-8 space-y-2 border border-emerald-500/20">
        <div className="flex items-center gap-3">
          <div className="w-12 h-12 rounded-2xl bg-emerald-500/20 flex items-center justify-center text-emerald-400 font-bold shadow-lg shadow-emerald-500/10">
            <UserIcon className="w-7 h-7" />
          </div>
          <div>
            <h1 className="text-xl sm:text-2xl font-extrabold text-white">{t('nav.profile')}</h1>
            <p className="text-xs text-slate-300">Manage your farm location, language preferences, and personal details</p>
          </div>
        </div>
      </div>

      <div className="glass-panel rounded-3xl p-6 sm:p-8 space-y-6">
        {savedSuccess && (
          <div className="p-3.5 rounded-xl bg-emerald-950/40 border border-emerald-500/30 text-emerald-300 text-xs flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4 text-emerald-400" />
            <span>Profile information updated successfully!</span>
          </div>
        )}

        <form onSubmit={handleSave} className="space-y-4">
          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1">Full Name</label>
            <input
              type="text"
              value={fullName}
              onChange={(e) => setFullName(e.target.value)}
              className="w-full bg-slate-900 border border-slate-700 focus:border-emerald-500 rounded-xl px-4 py-2.5 text-sm text-white"
            />
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">Mobile Number</label>
              <input
                type="text"
                disabled
                value={user?.mobile_number || ''}
                className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-sm text-slate-400 opacity-70 cursor-not-allowed"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">Email</label>
              <input
                type="text"
                disabled
                value={user?.email || 'N/A'}
                className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-sm text-slate-400 opacity-70 cursor-not-allowed"
              />
            </div>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">Primary District</label>
              <select
                value={districtId}
                onChange={(e) => {
                  setDistrictId(e.target.value);
                  setTalukId('');
                }}
                className="w-full bg-slate-900 border border-slate-700 focus:border-emerald-500 rounded-xl px-3 py-2.5 text-sm text-white"
              >
                <option value="">-- Choose District --</option>
                {districts.map((d) => (
                  <option key={d.id} value={d.id}>
                    {lang === 'ta' ? `${d.name_ta} (${d.name_en})` : d.name_en}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">Primary Taluk</label>
              <select
                value={talukId}
                disabled={!districtId}
                onChange={(e) => setTalukId(e.target.value)}
                className="w-full bg-slate-900 border border-slate-700 focus:border-emerald-500 rounded-xl px-3 py-2.5 text-sm text-white disabled:opacity-40"
              >
                <option value="">-- Choose Taluk --</option>
                {taluks.map((t) => (
                  <option key={t.id} value={t.id}>
                    {lang === 'ta' ? `${t.name_ta} (${t.name_en})` : t.name_en}
                  </option>
                ))}
              </select>
            </div>
          </div>

          <div className="pt-2">
            <button
              type="submit"
              disabled={isSaving}
              className="px-6 py-3 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold text-xs shadow-md shadow-emerald-500/20 flex items-center gap-2 transition-all disabled:opacity-50"
            >
              <Save className="w-4 h-4" />
              <span>{isSaving ? 'Saving...' : 'Save Profile Details'}</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};
