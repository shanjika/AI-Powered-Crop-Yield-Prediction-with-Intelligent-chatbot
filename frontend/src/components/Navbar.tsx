import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { useAuth } from '../context/AuthContext';
import { LanguageSelector } from './LanguageSelector';
import { Sprout, LogOut, User as UserIcon, Bell } from 'lucide-react';

export const Navbar: React.FC = () => {
  const { t } = useTranslation();
  const { user, isAuthenticated, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <header className="sticky top-0 z-40 w-full glass-panel border-b border-emerald-900/30">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        {/* Logo */}
        <Link to={isAuthenticated ? "/dashboard" : "/"} className="flex items-center gap-3 group">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-emerald-600 to-green-400 flex items-center justify-center shadow-lg shadow-emerald-500/20 group-hover:scale-105 transition-transform">
            <Sprout className="w-6 h-6 text-slate-950 font-bold" />
          </div>
          <div>
            <span className="text-lg font-bold bg-gradient-to-r from-emerald-300 via-green-200 to-amber-200 bg-clip-text text-transparent">
              {t('app_name')}
            </span>
            <p className="text-[10px] text-emerald-400/80 font-medium tracking-wide">
              TAMIL NADU AGRI AI
            </p>
          </div>
        </Link>

        {/* Right Section */}
        <div className="flex items-center gap-3 sm:gap-4">
          <LanguageSelector />

          {isAuthenticated ? (
            <div className="flex items-center gap-2 sm:gap-3">
              <Link
                to="/profile"
                className="hidden sm:flex items-center gap-2 px-3 py-1.5 rounded-lg bg-slate-800/80 hover:bg-slate-750 border border-slate-700/50 text-xs text-slate-200 transition-colors"
              >
                <UserIcon className="w-4 h-4 text-emerald-400" />
                <span className="font-semibold">{user?.full_name || 'Farmer'}</span>
              </Link>

              <button
                onClick={handleLogout}
                className="p-2 rounded-lg bg-red-950/40 hover:bg-red-900/50 border border-red-800/40 text-red-300 transition-colors"
                title={t('nav.logout')}
              >
                <LogOut className="w-4 h-4" />
              </button>
            </div>
          ) : (
            <div className="flex items-center gap-2">
              <Link
                to="/login"
                className="px-3 sm:px-4 py-1.5 text-xs sm:text-sm font-semibold rounded-lg text-slate-300 hover:text-white transition-colors"
              >
                {t('nav.login')}
              </Link>
              <Link
                to="/signup"
                className="px-3 sm:px-4 py-1.5 text-xs sm:text-sm font-semibold rounded-lg bg-emerald-500 text-slate-950 hover:bg-emerald-400 shadow-md shadow-emerald-500/20 transition-all"
              >
                {t('nav.signup')}
              </Link>
            </div>
          )}
        </div>
      </div>
    </header>
  );
};
