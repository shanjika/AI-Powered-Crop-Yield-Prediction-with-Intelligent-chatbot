import React from 'react';
import { NavLink } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import {
  LayoutDashboard,
  Sprout,
  CloudSun,
  FlaskConical,
  BookOpen,
  History,
  Bot,
  User,
  Settings
} from 'lucide-react';

export const Sidebar: React.FC = () => {
  const { t } = useTranslation();

  const navItems = [
    { to: '/dashboard', label: t('nav.dashboard'), icon: LayoutDashboard },
    { to: '/predict', label: t('nav.predict_yield'), icon: Sprout, highlight: true },
    { to: '/weather', label: t('nav.weather'), icon: CloudSun },
    { to: '/soil', label: t('nav.soil_health'), icon: FlaskConical },
    { to: '/crops', label: t('nav.crops_catalog'), icon: BookOpen },
    { to: '/predictions', label: t('nav.my_predictions'), icon: History },
    { to: '/chat', label: t('nav.ai_assistant'), icon: Bot, isChat: true },
    { to: '/profile', label: t('nav.profile'), icon: User },
    { to: '/settings', label: t('nav.settings'), icon: Settings },
  ];

  return (
    <>
      {/* Desktop Left Sidebar */}
      <aside className="hidden lg:flex flex-col w-64 glass-panel border-r border-emerald-950/40 p-4 space-y-2 shrink-0 min-h-[calc(100vh-4rem)]">
        <div className="text-[11px] font-bold text-emerald-400/70 tracking-wider px-3 py-1 uppercase">
          {t('dashboard.summary_title')}
        </div>
        <nav className="flex-1 space-y-1.5">
          {navItems.map((item) => {
            const Icon = item.icon;
            return (
              <NavLink
                key={item.to}
                to={item.to}
                className={({ isActive }) =>
                  `flex items-center gap-3 px-3.5 py-2.5 rounded-xl text-sm font-medium transition-all ${
                    isActive
                      ? 'bg-emerald-600/30 text-emerald-300 border border-emerald-500/30 shadow-md shadow-emerald-950/50'
                      : item.highlight
                      ? 'bg-emerald-500/10 text-emerald-300 hover:bg-emerald-500/20 border border-emerald-500/20 font-semibold'
                      : 'text-slate-300 hover:bg-slate-800/60 hover:text-white'
                  }`
                }
              >
                <Icon className={`w-4 h-4 ${item.highlight ? 'text-emerald-400' : ''}`} />
                <span>{item.label}</span>
                {item.isChat && (
                  <span className="ml-auto text-[10px] px-1.5 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 font-bold border border-emerald-500/30">
                    AI
                  </span>
                )}
              </NavLink>
            );
          })}
        </nav>
      </aside>

      {/* Mobile Bottom Navigation Bar */}
      <div className="lg:hidden fixed bottom-0 left-0 right-0 z-50 glass-panel border-t border-slate-700/50 px-2 py-1.5 flex justify-around items-center">
        {navItems.slice(0, 5).map((item) => {
          const Icon = item.icon;
          return (
            <NavLink
              key={item.to}
              to={item.to}
              className={({ isActive }) =>
                `flex flex-col items-center gap-1 p-2 rounded-lg text-[10px] font-medium transition-colors ${
                  isActive ? 'text-emerald-400 font-bold' : 'text-slate-400 hover:text-slate-200'
                }`
              }
            >
              <Icon className="w-5 h-5" />
              <span className="truncate max-w-[60px] text-center">{item.label}</span>
            </NavLink>
          );
        })}
        <NavLink
          to="/chat"
          className={({ isActive }) =>
            `flex flex-col items-center gap-1 p-2 rounded-lg text-[10px] font-medium transition-colors ${
              isActive ? 'text-emerald-400 font-bold' : 'text-slate-400 hover:text-slate-200'
            }`
          }
        >
          <Bot className="w-5 h-5 text-emerald-400" />
          <span>AI</span>
        </NavLink>
      </div>
    </>
  );
};
