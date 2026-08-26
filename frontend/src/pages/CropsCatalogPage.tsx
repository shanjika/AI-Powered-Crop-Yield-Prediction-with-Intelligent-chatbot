import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import api from '../services/api';
import { Crop } from '../types';
import { BookOpen, Search, Filter, Droplets, Thermometer, CloudRain, Clock, AlertTriangle, ShieldCheck, X } from 'lucide-react';

export const CropsCatalogPage: React.FC = () => {
  const { t, i18n } = useTranslation();
  const lang = i18n.language || 'ta';

  const [crops, setCrops] = useState<Crop[]>([]);
  const [selectedCrop, setSelectedCrop] = useState<Crop | null>(null);
  const [search, setSearch] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('All');
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    api.get('/crops')
      .then((res) => setCrops(res.data))
      .catch((err) => console.error('Error fetching crops:', err))
      .finally(() => setIsLoading(false));
  }, []);

  const categories = ['All', 'Cereals', 'Millets', 'Pulses', 'Oilseeds', 'Commercial', 'Fruits', 'Vegetables', 'Spices'];

  const filteredCrops = crops.filter((c) => {
    const matchesSearch =
      c.name_en.toLowerCase().includes(search.toLowerCase()) ||
      c.name_ta.toLowerCase().includes(search.toLowerCase());
    const matchesCategory = selectedCategory === 'All' || c.category === selectedCategory;
    return matchesSearch && matchesCategory;
  });

  const handleOpenDetail = (cropId: number) => {
    api.get(`/crops/${cropId}`)
      .then((res) => setSelectedCrop(res.data))
      .catch((err) => console.error('Error fetching crop details:', err));
  };

  return (
    <div className="max-w-6xl mx-auto space-y-6 pb-12">
      {/* Header */}
      <div className="glass-panel rounded-3xl p-6 sm:p-8 space-y-4 border border-emerald-500/20">
        <div className="flex items-center gap-3">
          <div className="w-12 h-12 rounded-2xl bg-amber-500/20 flex items-center justify-center text-amber-400 font-bold shadow-lg shadow-amber-500/10">
            <BookOpen className="w-7 h-7" />
          </div>
          <div>
            <h1 className="text-xl sm:text-2xl font-extrabold text-white">{t('crops.title')}</h1>
            <p className="text-xs text-slate-300">{t('crops.subtitle')}</p>
          </div>
        </div>

        {/* Search & Category Filter Pills */}
        <div className="space-y-3 pt-2">
          <div className="relative">
            <Search className="w-4 h-4 absolute left-3.5 top-3.5 text-slate-400" />
            <input
              type="text"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder={t('crops.search')}
              className="w-full bg-slate-900/90 border border-slate-700/80 focus:border-emerald-500 rounded-xl pl-10 pr-4 py-2.5 text-xs sm:text-sm text-white focus:outline-none focus:ring-1 focus:ring-emerald-500"
            />
          </div>

          <div className="flex flex-wrap gap-1.5">
            {categories.map((cat) => (
              <button
                key={cat}
                onClick={() => setSelectedCategory(cat)}
                className={`px-3 py-1.5 rounded-xl text-xs font-semibold transition-all ${
                  selectedCategory === cat
                    ? 'bg-emerald-500 text-slate-950 font-bold shadow-md shadow-emerald-500/20'
                    : 'bg-slate-900/60 text-slate-300 hover:bg-slate-800'
                }`}
              >
                {cat}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Crops Cards Grid */}
      {isLoading ? (
        <div className="py-16 text-center space-y-2">
          <div className="w-10 h-10 rounded-full border-4 border-emerald-500 border-t-transparent animate-spin mx-auto" />
          <span className="text-xs text-slate-400">{t('common.loading')}</span>
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
          {filteredCrops.map((crop) => (
            <div
              key={crop.id}
              onClick={() => handleOpenDetail(crop.id)}
              className="glass-panel glass-card-hover rounded-2xl p-5 space-y-3 cursor-pointer border border-slate-800 hover:border-emerald-500/40"
            >
              <div className="flex items-start justify-between">
                <div>
                  <h3 className="text-base font-bold text-white group-hover:text-emerald-300">
                    {lang === 'ta' ? crop.name_ta : crop.name_en}
                  </h3>
                  <p className="text-[11px] text-slate-400">
                    {lang === 'ta' ? crop.name_en : crop.name_ta}
                  </p>
                </div>
                <span className="text-[10px] px-2 py-0.5 rounded-full bg-emerald-950/60 border border-emerald-800/50 text-emerald-300 font-semibold">
                  {crop.category}
                </span>
              </div>

              <div className="space-y-1.5 text-xs text-slate-300 pt-2 border-t border-slate-800/80">
                <div className="flex items-center justify-between">
                  <span className="text-slate-400 flex items-center gap-1">
                    <Clock className="w-3.5 h-3.5 text-amber-400" /> Duration:
                  </span>
                  <span className="font-bold text-white">{crop.duration_days} days</span>
                </div>

                <div className="flex items-center justify-between">
                  <span className="text-slate-400 flex items-center gap-1">
                    <Droplets className="w-3.5 h-3.5 text-blue-400" /> Water:
                  </span>
                  <span className="font-semibold text-white">
                    {lang === 'ta' ? crop.water_req_level_ta : crop.water_req_level}
                  </span>
                </div>

                <div className="flex items-center justify-between">
                  <span className="text-slate-400">Avg Yield:</span>
                  <span className="font-bold text-emerald-400">
                    {crop.typical_yield_min_acre.toLocaleString()} - {crop.typical_yield_max_acre.toLocaleString()} kg/ac
                  </span>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Detail Modal */}
      {selectedCrop && (
        <div className="fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-md flex items-center justify-center p-4">
          <div className="glass-panel rounded-3xl p-6 sm:p-8 max-w-2xl w-full max-h-[90vh] overflow-y-auto space-y-5 border border-emerald-500/30 relative">
            <button
              onClick={() => setSelectedCrop(null)}
              className="absolute top-5 right-5 p-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300"
            >
              <X className="w-5 h-5" />
            </button>

            <div className="space-y-1">
              <span className="text-xs font-bold text-emerald-400 uppercase tracking-wide">
                {selectedCrop.category}
              </span>
              <h2 className="text-2xl font-black text-white">
                {lang === 'ta' ? selectedCrop.name_ta : selectedCrop.name_en}
                <span className="text-sm font-normal text-slate-400 ml-2">
                  ({lang === 'ta' ? selectedCrop.name_en : selectedCrop.name_ta})
                </span>
              </h2>
            </div>

            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-center text-xs">
              <div className="p-3 rounded-xl bg-slate-900/80 border border-slate-800">
                <span className="text-slate-400 block text-[10px]">Duration</span>
                <span className="font-bold text-white text-sm">{selectedCrop.duration_days} days</span>
              </div>
              <div className="p-3 rounded-xl bg-slate-900/80 border border-slate-800">
                <span className="text-slate-400 block text-[10px]">Temperature</span>
                <span className="font-bold text-white text-sm">{selectedCrop.min_temp}°C - {selectedCrop.max_temp}°C</span>
              </div>
              <div className="p-3 rounded-xl bg-slate-900/80 border border-slate-800">
                <span className="text-slate-400 block text-[10px]">Rainfall</span>
                <span className="font-bold text-white text-sm">{selectedCrop.min_rainfall} - {selectedCrop.max_rainfall} mm</span>
              </div>
              <div className="p-3 rounded-xl bg-slate-900/80 border border-slate-800">
                <span className="text-slate-400 block text-[10px]">N-P-K Baseline</span>
                <span className="font-bold text-emerald-400 text-sm">{selectedCrop.n_req}-{selectedCrop.p_req}-{selectedCrop.k_req}</span>
              </div>
            </div>

            <div className="space-y-3 text-xs sm:text-sm">
              <div>
                <span className="font-bold text-slate-300 block mb-1">Ideal Soil Type:</span>
                <p className="text-slate-200">{lang === 'ta' ? selectedCrop.ideal_soil_ta : selectedCrop.ideal_soil}</p>
              </div>

              <div>
                <span className="font-bold text-amber-300 block mb-1">Major Pests (பூச்சிகள்):</span>
                <p className="text-slate-200">{lang === 'ta' ? selectedCrop.major_pests_ta : selectedCrop.major_pests_en}</p>
              </div>

              <div>
                <span className="font-bold text-red-300 block mb-1">Major Diseases (நோய்கள்):</span>
                <p className="text-slate-200">{lang === 'ta' ? selectedCrop.major_diseases_ta : selectedCrop.major_diseases_en}</p>
              </div>

              <div>
                <span className="font-bold text-emerald-300 block mb-1">Harvest Indicators (அறுவடை அறிகுறிகள்):</span>
                <p className="text-slate-200">{lang === 'ta' ? selectedCrop.harvest_indicators_ta : selectedCrop.harvest_indicators_en}</p>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
