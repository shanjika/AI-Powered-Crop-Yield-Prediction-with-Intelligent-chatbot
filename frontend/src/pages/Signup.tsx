import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { useAuth } from '../context/AuthContext';
import api from '../services/api';
import { District, Taluk } from '../types';
import { Sprout, Lock, Phone, User, Mail, MapPin, AlertCircle, ArrowRight } from 'lucide-react';

export const Signup: React.FC = () => {
  const { t, i18n } = useTranslation();
  const lang = i18n.language || 'ta';
  const { login } = useAuth();
  const navigate = useNavigate();

  const [districts, setDistricts] = useState<District[]>([]);
  const [taluks, setTaluks] = useState<Taluk[]>([]);

  const [formData, setFormData] = useState({
    fullName: '',
    mobileNumber: '',
    email: '',
    password: '',
    confirmPassword: '',
    districtId: '',
    talukId: '',
    preferredLanguage: lang,
  });

  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    // Load all districts
    api.get('/districts')
      .then((res) => setDistricts(res.data))
      .catch((err) => console.error('Error fetching districts:', err));
  }, []);

  useEffect(() => {
    if (formData.districtId) {
      api.get(`/taluks/${formData.districtId}`)
        .then((res) => setTaluks(res.data))
        .catch((err) => console.error('Error fetching taluks:', err));
    } else {
      setTaluks([]);
    }
  }, [formData.districtId]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    if (formData.password !== formData.confirmPassword) {
      setError(t('auth.password_mismatch'));
      return;
    }

    if (formData.mobileNumber.length < 10) {
      setError(t('auth.invalid_phone'));
      return;
    }

    setIsLoading(true);
    try {
      const payload = {
        full_name: formData.fullName.trim(),
        mobile_number: formData.mobileNumber.trim(),
        email: formData.email.trim() || undefined,
        password: formData.password,
        preferred_language: formData.preferredLanguage,
        district_id: formData.districtId ? parseInt(formData.districtId) : undefined,
        taluk_id: formData.talukId ? parseInt(formData.talukId) : undefined,
      };

      const res = await api.post('/auth/signup', payload);
      login(res.data.access_token, res.data.user);
      navigate('/dashboard');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Error registering farmer account. Please check your inputs.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-[85vh] flex items-center justify-center px-4 py-8">
      <div className="glass-panel rounded-3xl p-6 sm:p-10 w-full max-w-lg border border-emerald-500/20 shadow-2xl">
        <div className="text-center space-y-2 mb-6">
          <div className="w-12 h-12 mx-auto rounded-2xl bg-gradient-to-tr from-emerald-600 to-green-400 flex items-center justify-center shadow-lg shadow-emerald-500/20 mb-2">
            <Sprout className="w-6 h-6 text-slate-950 font-bold" />
          </div>
          <h2 className="text-2xl font-bold text-white">{t('auth.signup_title')}</h2>
          <p className="text-xs text-slate-300">{t('auth.signup_sub')}</p>
        </div>

        {error && (
          <div className="p-3 mb-5 rounded-xl bg-red-950/40 border border-red-500/30 text-red-200 text-xs flex items-center gap-2">
            <AlertCircle className="w-4 h-4 shrink-0 text-red-400" />
            <span>{error}</span>
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1">
              {t('auth.full_name')} *
            </label>
            <div className="relative">
              <User className="w-4 h-4 absolute left-3.5 top-3.5 text-slate-400" />
              <input
                type="text"
                required
                value={formData.fullName}
                onChange={(e) => setFormData({ ...formData, fullName: e.target.value })}
                placeholder="e.g. Murugan / முருகன்"
                className="w-full bg-slate-900/80 border border-slate-700/80 focus:border-emerald-500 rounded-xl pl-10 pr-4 py-2 text-sm text-white placeholder-slate-500 focus:outline-none focus:ring-1 focus:ring-emerald-500"
              />
            </div>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">
                {t('auth.mobile_number')} *
              </label>
              <div className="relative">
                <Phone className="w-4 h-4 absolute left-3.5 top-3.5 text-slate-400" />
                <input
                  type="tel"
                  required
                  value={formData.mobileNumber}
                  onChange={(e) => setFormData({ ...formData, mobileNumber: e.target.value })}
                  placeholder="9876543210"
                  className="w-full bg-slate-900/80 border border-slate-700/80 focus:border-emerald-500 rounded-xl pl-10 pr-4 py-2 text-sm text-white placeholder-slate-500 focus:outline-none focus:ring-1 focus:ring-emerald-500"
                />
              </div>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">
                {t('auth.email_optional')}
              </label>
              <div className="relative">
                <Mail className="w-4 h-4 absolute left-3.5 top-3.5 text-slate-400" />
                <input
                  type="email"
                  value={formData.email}
                  onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                  placeholder="farmer@example.com"
                  className="w-full bg-slate-900/80 border border-slate-700/80 focus:border-emerald-500 rounded-xl pl-10 pr-4 py-2 text-sm text-white placeholder-slate-500 focus:outline-none focus:ring-1 focus:ring-emerald-500"
                />
              </div>
            </div>
          </div>

          {/* District and Taluk Dropdowns */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">
                {t('auth.select_district')}
              </label>
              <select
                value={formData.districtId}
                onChange={(e) => setFormData({ ...formData, districtId: e.target.value, talukId: '' })}
                className="w-full bg-slate-900/80 border border-slate-700/80 focus:border-emerald-500 rounded-xl px-3 py-2 text-sm text-white focus:outline-none focus:ring-1 focus:ring-emerald-500"
              >
                <option value="">{t('wizard.select_district_placeholder')}</option>
                {districts.map((d) => (
                  <option key={d.id} value={d.id}>
                    {lang === 'ta' ? `${d.name_ta} (${d.name_en})` : d.name_en}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">
                {t('auth.select_taluk')}
              </label>
              <select
                value={formData.talukId}
                disabled={!formData.districtId}
                onChange={(e) => setFormData({ ...formData, talukId: e.target.value })}
                className="w-full bg-slate-900/80 border border-slate-700/80 focus:border-emerald-500 rounded-xl px-3 py-2 text-sm text-white focus:outline-none focus:ring-1 focus:ring-emerald-500 disabled:opacity-40"
              >
                <option value="">{t('wizard.select_taluk_placeholder')}</option>
                {taluks.map((t) => (
                  <option key={t.id} value={t.id}>
                    {lang === 'ta' ? `${t.name_ta} (${t.name_en})` : t.name_en}
                  </option>
                ))}
              </select>
            </div>
          </div>

          {/* Password fields */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">
                {t('auth.password')} *
              </label>
              <div className="relative">
                <Lock className="w-4 h-4 absolute left-3.5 top-3.5 text-slate-400" />
                <input
                  type="password"
                  required
                  value={formData.password}
                  onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                  placeholder="••••••••"
                  className="w-full bg-slate-900/80 border border-slate-700/80 focus:border-emerald-500 rounded-xl pl-10 pr-4 py-2 text-sm text-white placeholder-slate-500 focus:outline-none focus:ring-1 focus:ring-emerald-500"
                />
              </div>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">
                {t('auth.confirm_password')} *
              </label>
              <div className="relative">
                <Lock className="w-4 h-4 absolute left-3.5 top-3.5 text-slate-400" />
                <input
                  type="password"
                  required
                  value={formData.confirmPassword}
                  onChange={(e) => setFormData({ ...formData, confirmPassword: e.target.value })}
                  placeholder="••••••••"
                  className="w-full bg-slate-900/80 border border-slate-700/80 focus:border-emerald-500 rounded-xl pl-10 pr-4 py-2 text-sm text-white placeholder-slate-500 focus:outline-none focus:ring-1 focus:ring-emerald-500"
                />
              </div>
            </div>
          </div>

          <button
            type="submit"
            disabled={isLoading}
            className="w-full mt-2 py-3 px-4 rounded-xl bg-gradient-to-r from-emerald-500 to-green-600 hover:from-emerald-400 hover:to-green-500 text-slate-950 font-bold text-sm shadow-lg shadow-emerald-500/20 flex items-center justify-center gap-2 transition-all disabled:opacity-50"
          >
            {isLoading ? <span>{t('common.loading')}</span> : (
              <>
                <span>{t('auth.register_btn')}</span>
                <ArrowRight className="w-4 h-4" />
              </>
            )}
          </button>
        </form>

        <div className="mt-6 text-center text-xs text-slate-400">
          {t('auth.already_have_account')}{' '}
          <Link to="/login" className="text-emerald-400 hover:underline font-bold">
            {t('auth.login_here')}
          </Link>
        </div>
      </div>
    </div>
  );
};
