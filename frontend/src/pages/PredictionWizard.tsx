import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { useAuth } from '../context/AuthContext';
import api from '../services/api';
import { District, Taluk, Crop, Pattam, WeatherData } from '../types';
import {
  Sprout,
  MapPin,
  Calendar,
  Layers,
  FlaskConical,
  CloudSun,
  Upload,
  CheckCircle2,
  AlertTriangle,
  ArrowRight,
  ArrowLeft,
  Sparkles,
  Search
} from 'lucide-react';

const SOIL_TYPES = [
  "Red Loam", "Clay Loam", "Sandy Loam", "Black Cotton Soil",
  "Alluvial", "Laterite Soil", "Sandy Soil", "Clay Soil"
];

const IRRIGATION_TYPES = [
  "Well / Tube Well", "Canal Irrigation", "Drip Irrigation",
  "Sprinkler", "Rainfed"
];

export const PredictionWizard: React.FC = () => {
  const { t, i18n } = useTranslation();
  const lang = i18n.language || 'ta';
  const { user } = useAuth();
  const navigate = useNavigate();

  // Wizard Step (1 to 6)
  const [currentStep, setCurrentStep] = useState(1);

  // Reference Data
  const [districts, setDistricts] = useState<District[]>([]);
  const [taluks, setTaluks] = useState<Taluk[]>([]);
  const [crops, setCrops] = useState<Crop[]>([]);
  const [pattams, setPattams] = useState<Pattam[]>([]);

  // Search Filter for crops
  const [cropSearch, setCropSearch] = useState('');
  const [selectedCropObj, setSelectedCropObj] = useState<Crop | null>(null);

  // Form State
  const [formData, setFormData] = useState({
    districtId: user?.district_id ? String(user.district_id) : '',
    talukId: user?.taluk_id ? String(user.taluk_id) : '',
    cropId: '',
    pattam: 'Aadi Pattam (Monsoon Sowing)',
    landAreaAcres: '2.5',
    soilType: 'Red Loam',
    irrigationType: 'Well / Tube Well',
    // Soil Parameters
    soilPh: 6.8,
    soilN: 250.0,
    soilP: 18.0,
    soilK: 210.0,
    soilEc: 0.45,
    soilOc: 0.65,
    soilReportId: null as number | null,
  });

  // Weather state
  const [weatherData, setWeatherData] = useState<WeatherData | null>(null);
  const [weatherLoading, setWeatherLoading] = useState(false);

  // Soil file upload
  const [soilFile, setSoilFile] = useState<File | null>(null);
  const [soilUploading, setSoilUploading] = useState(false);
  const [soilSuccessMsg, setSoilSuccessMsg] = useState('');

  // Prediction loading state
  const [isPredicting, setIsPredicting] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');

  // 1. Fetch initial datasets
  useEffect(() => {
    Promise.all([
      api.get('/districts'),
      api.get('/crops'),
      api.get('/pattams'),
    ])
      .then(([distRes, cropRes, patRes]) => {
        setDistricts(distRes.data);
        setCrops(cropRes.data);
        setPattams(patRes.data);
        if (cropRes.data.length > 0) {
          setFormData((prev) => ({ ...prev, cropId: String(cropRes.data[0].id) }));
          setSelectedCropObj(cropRes.data[0]);
        }
      })
      .catch((err) => console.error('Error fetching wizard base data:', err));
  }, []);

  // 2. Fetch taluks on district change
  useEffect(() => {
    if (formData.districtId) {
      api.get(`/taluks/${formData.districtId}`)
        .then((res) => {
          setTaluks(res.data);
          if (res.data.length > 0 && !formData.talukId) {
            setFormData((prev) => ({ ...prev, talukId: String(res.data[0].id) }));
          }
        })
        .catch((err) => console.error('Error fetching taluks:', err));
    }
  }, [formData.districtId]);

  // 3. Fetch weather when district and taluk are selected
  useEffect(() => {
    if (formData.districtId && formData.talukId) {
      setWeatherLoading(true);
      api.get(`/weather/${formData.districtId}/${formData.talukId}`)
        .then((res) => setWeatherData(res.data))
        .catch((err) => console.error('Error fetching live weather:', err))
        .finally(() => setWeatherLoading(false));
    }
  }, [formData.districtId, formData.talukId]);

  // Handle Crop Selection
  const handleSelectCrop = (crop: Crop) => {
    setFormData({ ...formData, cropId: String(crop.id) });
    setSelectedCropObj(crop);
  };

  // Handle Soil Report Upload & OCR
  const handleSoilUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!e.target.files || e.target.files.length === 0) return;
    const file = e.target.files[0];
    setSoilFile(file);
    setSoilUploading(true);
    setErrorMessage('');

    const form = new FormData();
    form.append('file', file);

    try {
      const res = await api.post('/soil/upload', form, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });

      const extracted = res.data.extracted_parameters;
      setFormData((prev) => ({
        ...prev,
        soilPh: extracted.ph || 6.8,
        soilN: extracted.nitrogen || 250.0,
        soilP: extracted.phosphorus || 18.0,
        soilK: extracted.potassium || 210.0,
        soilEc: extracted.ec || 0.45,
        soilOc: extracted.organic_carbon || 0.65,
        soilType: extracted.soil_type || prev.soilType,
        soilReportId: res.data.report_id,
      }));

      setSoilSuccessMsg(lang === 'ta' ? res.data.message_ta : res.data.message_en);
    } catch (err: any) {
      setErrorMessage(err.response?.data?.detail || 'Error processing soil report file.');
    } finally {
      setSoilUploading(false);
    }
  };

  // Submit Final Prediction
  const handleRunPrediction = async () => {
    setErrorMessage('');
    const acres = parseFloat(formData.landAreaAcres);
    if (isNaN(acres) || acres <= 0) {
      setErrorMessage('Please enter a valid land area greater than 0 acres.');
      return;
    }

    setIsPredicting(true);
    try {
      const payload = {
        district_id: parseInt(formData.districtId),
        taluk_id: parseInt(formData.talukId),
        crop_id: parseInt(formData.cropId),
        pattam: formData.pattam,
        land_area_acres: acres,
        soil_type: formData.soilType,
        irrigation_type: formData.irrigationType,
        soil_ph: formData.soilPh,
        soil_n: formData.soilN,
        soil_p: formData.soilP,
        soil_k: formData.soilK,
        soil_ec: formData.soilEc,
        soil_organic_carbon: formData.soilOc,
        soil_report_id: formData.soilReportId,
      };

      const res = await api.post('/predict', payload);
      // Navigate to prediction result page with returned ID
      navigate(`/predictions/${res.data.id}`);
    } catch (err: any) {
      setErrorMessage(err.response?.data?.detail || 'Prediction failed. Please check inputs and try again.');
      setIsPredicting(false);
    }
  };

  // Filter crops by search query
  const filteredCrops = crops.filter(
    (c) =>
      c.name_en.toLowerCase().includes(cropSearch.toLowerCase()) ||
      c.name_ta.toLowerCase().includes(cropSearch.toLowerCase())
  );

  return (
    <div className="max-w-4xl mx-auto space-y-6 pb-12">
      {/* Wizard Header */}
      <div className="glass-panel rounded-3xl p-6 sm:p-8 border border-emerald-500/20">
        <div className="flex items-center gap-3">
          <div className="w-12 h-12 rounded-2xl bg-gradient-to-tr from-emerald-600 to-green-400 flex items-center justify-center text-slate-950 font-bold shadow-lg shadow-emerald-500/20">
            <Sprout className="w-6 h-6" />
          </div>
          <div>
            <h1 className="text-xl sm:text-2xl font-extrabold text-white">{t('wizard.title')}</h1>
            <p className="text-xs sm:text-sm text-slate-300">{t('wizard.subtitle')}</p>
          </div>
        </div>

        {/* Step Indicator Tabs */}
        <div className="grid grid-cols-3 sm:grid-cols-6 gap-2 mt-6 pt-6 border-t border-slate-800">
          {[
            { step: 1, label: t('wizard.step1_location') },
            { step: 2, label: t('wizard.step2_crop') },
            { step: 3, label: t('wizard.step3_land') },
            { step: 4, label: t('wizard.step4_soil_report') },
            { step: 5, label: t('wizard.step5_weather') },
            { step: 6, label: t('wizard.step6_predict') },
          ].map((item) => (
            <button
              key={item.step}
              onClick={() => setCurrentStep(item.step)}
              className={`p-2 rounded-xl text-left transition-all ${
                currentStep === item.step
                  ? 'bg-emerald-500 text-slate-950 font-bold shadow-md shadow-emerald-500/20'
                  : currentStep > item.step
                  ? 'bg-slate-800/80 text-emerald-400 font-semibold'
                  : 'bg-slate-900/60 text-slate-400'
              }`}
            >
              <div className="text-[10px] uppercase tracking-wider">{item.label}</div>
            </button>
          ))}
        </div>
      </div>

      {/* Error Alert */}
      {errorMessage && (
        <div className="p-4 rounded-2xl bg-red-950/40 border border-red-500/30 text-red-200 text-xs flex items-center gap-3">
          <AlertTriangle className="w-5 h-5 text-red-400 shrink-0" />
          <span>{errorMessage}</span>
        </div>
      )}

      {/* STEP 1: Location */}
      {currentStep === 1 && (
        <div className="glass-panel rounded-3xl p-6 sm:p-8 space-y-6 animate-fadeIn">
          <div className="flex items-center gap-2 text-lg font-bold text-white">
            <MapPin className="w-5 h-5 text-emerald-400" />
            <span>{t('wizard.step1_location')}</span>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-5">
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-2">
                {t('wizard.district_label')} *
              </label>
              <select
                value={formData.districtId}
                onChange={(e) => setFormData({ ...formData, districtId: e.target.value, talukId: '' })}
                className="w-full bg-slate-900/90 border border-slate-700/80 focus:border-emerald-500 rounded-xl px-4 py-3 text-sm text-white focus:outline-none focus:ring-1 focus:ring-emerald-500"
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
              <label className="block text-xs font-semibold text-slate-300 mb-2">
                {t('wizard.taluk_label')} *
              </label>
              <select
                value={formData.talukId}
                disabled={!formData.districtId}
                onChange={(e) => setFormData({ ...formData, talukId: e.target.value })}
                className="w-full bg-slate-900/90 border border-slate-700/80 focus:border-emerald-500 rounded-xl px-4 py-3 text-sm text-white focus:outline-none focus:ring-1 focus:ring-emerald-500 disabled:opacity-40"
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

          <div className="flex justify-end pt-4">
            <button
              onClick={() => setCurrentStep(2)}
              disabled={!formData.districtId || !formData.talukId}
              className="px-6 py-3 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold text-sm shadow-md shadow-emerald-500/20 flex items-center gap-2 disabled:opacity-40 transition-all"
            >
              <span>{t('common.next')}</span>
              <ArrowRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      )}

      {/* STEP 2: Crop & Pattam Selection */}
      {currentStep === 2 && (
        <div className="glass-panel rounded-3xl p-6 sm:p-8 space-y-6 animate-fadeIn">
          <div className="flex items-center gap-2 text-lg font-bold text-white">
            <Calendar className="w-5 h-5 text-emerald-400" />
            <span>{t('wizard.step2_crop')}</span>
          </div>

          {/* Pattam Dropdown */}
          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-2">
              {t('wizard.pattam_label')} *
            </label>
            <select
              value={formData.pattam}
              onChange={(e) => setFormData({ ...formData, pattam: e.target.value })}
              className="w-full bg-slate-900/90 border border-slate-700/80 focus:border-emerald-500 rounded-xl px-4 py-3 text-sm text-white focus:outline-none focus:ring-1 focus:ring-emerald-500"
            >
              {pattams.map((p) => (
                <option key={p.id} value={p.name_en}>
                  {lang === 'ta' ? `${p.name_ta} - ${p.months_ta}` : `${p.name_en} (${p.months_en})`}
                </option>
              ))}
            </select>
          </div>

          {/* 50+ Crops Search & Grid */}
          <div className="space-y-3">
            <label className="block text-xs font-semibold text-slate-300">
              {t('wizard.crop_label')} *
            </label>
            <div className="relative">
              <Search className="w-4 h-4 absolute left-3.5 top-3.5 text-slate-400" />
              <input
                type="text"
                value={cropSearch}
                onChange={(e) => setCropSearch(e.target.value)}
                placeholder={t('wizard.search_crops')}
                className="w-full bg-slate-900/90 border border-slate-700/80 focus:border-emerald-500 rounded-xl pl-10 pr-4 py-2.5 text-sm text-white focus:outline-none focus:ring-1 focus:ring-emerald-500"
              />
            </div>

            <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-2.5 max-h-64 overflow-y-auto pr-1">
              {filteredCrops.map((crop) => {
                const isSelected = String(crop.id) === formData.cropId;
                return (
                  <button
                    key={crop.id}
                    type="button"
                    onClick={() => handleSelectCrop(crop)}
                    className={`p-3 rounded-xl text-left border transition-all ${
                      isSelected
                        ? 'bg-emerald-500/20 border-emerald-500 text-emerald-300 font-bold shadow-md shadow-emerald-500/10'
                        : 'bg-slate-900/60 border-slate-800 text-slate-300 hover:border-slate-600'
                    }`}
                  >
                    <span className="text-xs block truncate">{crop.name_ta}</span>
                    <span className="text-[11px] text-slate-400 block truncate">{crop.name_en}</span>
                  </button>
                );
              })}
            </div>
          </div>

          <div className="flex justify-between pt-4">
            <button
              onClick={() => setCurrentStep(1)}
              className="px-5 py-2.5 rounded-xl glass-card text-slate-300 hover:text-white text-xs font-semibold flex items-center gap-2"
            >
              <ArrowLeft className="w-4 h-4" />
              <span>{t('common.back')}</span>
            </button>
            <button
              onClick={() => setCurrentStep(3)}
              disabled={!formData.cropId}
              className="px-6 py-3 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold text-sm shadow-md shadow-emerald-500/20 flex items-center gap-2 transition-all"
            >
              <span>{t('common.next')}</span>
              <ArrowRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      )}

      {/* STEP 3: Land & Soil Options */}
      {currentStep === 3 && (
        <div className="glass-panel rounded-3xl p-6 sm:p-8 space-y-6 animate-fadeIn">
          <div className="flex items-center gap-2 text-lg font-bold text-white">
            <Layers className="w-5 h-5 text-emerald-400" />
            <span>{t('wizard.step3_land')}</span>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-5">
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-2">
                {t('wizard.land_area_label')} *
              </label>
              <input
                type="number"
                step="0.1"
                min="0.1"
                required
                value={formData.landAreaAcres}
                onChange={(e) => setFormData({ ...formData, landAreaAcres: e.target.value })}
                placeholder="e.g. 3.0"
                className="w-full bg-slate-900/90 border border-slate-700/80 focus:border-emerald-500 rounded-xl px-4 py-3 text-sm text-white focus:outline-none focus:ring-1 focus:ring-emerald-500 font-bold"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-2">
                {t('wizard.soil_type_label')}
              </label>
              <select
                value={formData.soilType}
                onChange={(e) => setFormData({ ...formData, soilType: e.target.value })}
                className="w-full bg-slate-900/90 border border-slate-700/80 focus:border-emerald-500 rounded-xl px-4 py-3 text-sm text-white focus:outline-none focus:ring-1 focus:ring-emerald-500"
              >
                {SOIL_TYPES.map((st) => (
                  <option key={st} value={st}>
                    {st}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-2">
                {t('wizard.irrigation_label')}
              </label>
              <select
                value={formData.irrigationType}
                onChange={(e) => setFormData({ ...formData, irrigationType: e.target.value })}
                className="w-full bg-slate-900/90 border border-slate-700/80 focus:border-emerald-500 rounded-xl px-4 py-3 text-sm text-white focus:outline-none focus:ring-1 focus:ring-emerald-500"
              >
                {IRRIGATION_TYPES.map((it) => (
                  <option key={it} value={it}>
                    {it}
                  </option>
                ))}
              </select>
            </div>
          </div>

          <div className="flex justify-between pt-4">
            <button
              onClick={() => setCurrentStep(2)}
              className="px-5 py-2.5 rounded-xl glass-card text-slate-300 hover:text-white text-xs font-semibold flex items-center gap-2"
            >
              <ArrowLeft className="w-4 h-4" />
              <span>{t('common.back')}</span>
            </button>
            <button
              onClick={() => setCurrentStep(4)}
              className="px-6 py-3 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold text-sm shadow-md shadow-emerald-500/20 flex items-center gap-2 transition-all"
            >
              <span>{t('common.next')}</span>
              <ArrowRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      )}

      {/* STEP 4: Soil Report Upload (OCR) & Manual Verification */}
      {currentStep === 4 && (
        <div className="glass-panel rounded-3xl p-6 sm:p-8 space-y-6 animate-fadeIn">
          <div className="flex items-center gap-2 text-lg font-bold text-white">
            <FlaskConical className="w-5 h-5 text-emerald-400" />
            <span>{t('wizard.step4_soil_report')}</span>
          </div>

          {/* Upload Dropzone */}
          <div className="p-6 rounded-2xl border-2 border-dashed border-slate-700/80 hover:border-emerald-500/60 bg-slate-900/40 text-center space-y-3 transition-colors">
            <Upload className="w-8 h-8 text-emerald-400 mx-auto" />
            <div>
              <span className="text-sm font-bold text-white block">
                {t('wizard.soil_upload_title')}
              </span>
              <span className="text-xs text-slate-400 max-w-sm block mx-auto">
                {t('wizard.soil_upload_desc')}
              </span>
            </div>
            <label className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-emerald-500/20 hover:bg-emerald-500/30 border border-emerald-500/30 text-emerald-300 text-xs font-bold cursor-pointer transition-colors">
              <span>{soilUploading ? t('common.loading') : t('wizard.upload_btn')}</span>
              <input
                type="file"
                accept=".pdf,.jpg,.jpeg,.png,.webp"
                onChange={handleSoilUpload}
                className="hidden"
              />
            </label>
          </div>

          {soilSuccessMsg && (
            <div className="p-3 rounded-xl bg-emerald-950/40 border border-emerald-500/30 text-emerald-300 text-xs flex items-center gap-2">
              <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
              <span>{soilSuccessMsg}</span>
            </div>
          )}

          {/* Editable Soil Nutrient Fields */}
          <div className="space-y-3">
            <span className="text-xs font-bold text-slate-300 block">
              {t('wizard.manual_soil_title')}
            </span>
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
              <div>
                <label className="block text-[11px] font-semibold text-slate-400 mb-1">
                  {t('wizard.soil_ph')}
                </label>
                <input
                  type="number"
                  step="0.1"
                  value={formData.soilPh}
                  onChange={(e) => setFormData({ ...formData, soilPh: parseFloat(e.target.value) || 6.5 })}
                  className="w-full bg-slate-900 border border-slate-700 focus:border-emerald-500 rounded-xl px-3 py-2 text-xs text-white"
                />
              </div>

              <div>
                <label className="block text-[11px] font-semibold text-slate-400 mb-1">
                  {t('wizard.soil_n')}
                </label>
                <input
                  type="number"
                  step="1"
                  value={formData.soilN}
                  onChange={(e) => setFormData({ ...formData, soilN: parseFloat(e.target.value) || 250.0 })}
                  className="w-full bg-slate-900 border border-slate-700 focus:border-emerald-500 rounded-xl px-3 py-2 text-xs text-white"
                />
              </div>

              <div>
                <label className="block text-[11px] font-semibold text-slate-400 mb-1">
                  {t('wizard.soil_p')}
                </label>
                <input
                  type="number"
                  step="1"
                  value={formData.soilP}
                  onChange={(e) => setFormData({ ...formData, soilP: parseFloat(e.target.value) || 18.0 })}
                  className="w-full bg-slate-900 border border-slate-700 focus:border-emerald-500 rounded-xl px-3 py-2 text-xs text-white"
                />
              </div>

              <div>
                <label className="block text-[11px] font-semibold text-slate-400 mb-1">
                  {t('wizard.soil_k')}
                </label>
                <input
                  type="number"
                  step="1"
                  value={formData.soilK}
                  onChange={(e) => setFormData({ ...formData, soilK: parseFloat(e.target.value) || 200.0 })}
                  className="w-full bg-slate-900 border border-slate-700 focus:border-emerald-500 rounded-xl px-3 py-2 text-xs text-white"
                />
              </div>
            </div>
          </div>

          <div className="flex justify-between pt-4">
            <button
              onClick={() => setCurrentStep(3)}
              className="px-5 py-2.5 rounded-xl glass-card text-slate-300 hover:text-white text-xs font-semibold flex items-center gap-2"
            >
              <ArrowLeft className="w-4 h-4" />
              <span>{t('common.back')}</span>
            </button>
            <button
              onClick={() => setCurrentStep(5)}
              className="px-6 py-3 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold text-sm shadow-md shadow-emerald-500/20 flex items-center gap-2 transition-all"
            >
              <span>{t('common.next')}</span>
              <ArrowRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      )}

      {/* STEP 5: Live Weather Preview */}
      {currentStep === 5 && (
        <div className="glass-panel rounded-3xl p-6 sm:p-8 space-y-6 animate-fadeIn">
          <div className="flex items-center gap-2 text-lg font-bold text-white">
            <CloudSun className="w-5 h-5 text-amber-400" />
            <span>{t('wizard.step5_weather')}</span>
          </div>

          {weatherLoading ? (
            <div className="py-8 text-center text-xs text-slate-400">
              {t('wizard.fetching_weather')}
            </div>
          ) : weatherData ? (
            <div className="space-y-4">
              <div className="p-4 rounded-2xl bg-slate-900/70 border border-slate-800 flex items-center justify-between">
                <div>
                  <span className="text-xs text-emerald-400 font-semibold block">
                    {weatherData.location_name}
                  </span>
                  <span className="text-3xl font-extrabold text-white">
                    {weatherData.temperature}°C
                  </span>
                  <span className="text-xs text-slate-400 ml-2">
                    ({lang === 'ta' ? weatherData.condition_ta : weatherData.condition_en})
                  </span>
                </div>
                <div className="text-right text-xs space-y-1">
                  <div className="text-slate-300">Humidity: <span className="text-white font-bold">{weatherData.humidity}%</span></div>
                  <div className="text-slate-300">Rainfall: <span className="text-white font-bold">{weatherData.rainfall_mm} mm</span></div>
                  <div className="text-slate-300">Wind: <span className="text-white font-bold">{weatherData.wind_speed_kmh} km/h</span></div>
                </div>
              </div>

              {/* 3-day preview cards */}
              <div className="grid grid-cols-3 gap-3">
                {weatherData.forecast.slice(0, 3).map((f, idx) => (
                  <div key={idx} className="p-3 rounded-xl bg-slate-900/50 border border-slate-800 text-center">
                    <span className="text-[11px] font-semibold text-slate-400 block">{f.date}</span>
                    <span className="text-base font-bold text-white block my-0.5">{f.temp_max}°C</span>
                    <span className="text-[10px] text-emerald-300 block">{f.precipitation_mm}mm rain</span>
                  </div>
                ))}
              </div>
            </div>
          ) : (
            <div className="p-4 rounded-xl bg-slate-900/50 border border-slate-800 text-xs text-slate-400">
              Live weather synchronized.
            </div>
          )}

          <div className="flex justify-between pt-4">
            <button
              onClick={() => setCurrentStep(4)}
              className="px-5 py-2.5 rounded-xl glass-card text-slate-300 hover:text-white text-xs font-semibold flex items-center gap-2"
            >
              <ArrowLeft className="w-4 h-4" />
              <span>{t('common.back')}</span>
            </button>
            <button
              onClick={() => setCurrentStep(6)}
              className="px-6 py-3 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold text-sm shadow-md shadow-emerald-500/20 flex items-center gap-2 transition-all"
            >
              <span>{t('common.next')}</span>
              <ArrowRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      )}

      {/* STEP 6: Run Prediction Confirmation */}
      {currentStep === 6 && (
        <div className="glass-panel rounded-3xl p-6 sm:p-8 space-y-6 animate-fadeIn">
          <div className="flex items-center gap-2 text-lg font-bold text-white">
            <Sparkles className="w-5 h-5 text-emerald-400" />
            <span>{t('wizard.step6_predict')}</span>
          </div>

          <div className="p-5 rounded-2xl bg-slate-900/80 border border-slate-800 space-y-3">
            <h3 className="text-sm font-bold text-emerald-300">Review Farm Configuration</h3>
            <div className="grid grid-cols-2 sm:grid-cols-3 gap-3 text-xs">
              <div>
                <span className="text-slate-400 block">Crop:</span>
                <span className="font-bold text-white">{selectedCropObj ? (lang === 'ta' ? selectedCropObj.name_ta : selectedCropObj.name_en) : 'Paddy'}</span>
              </div>
              <div>
                <span className="text-slate-400 block">Land Area:</span>
                <span className="font-bold text-amber-300">{formData.landAreaAcres} Acres</span>
              </div>
              <div>
                <span className="text-slate-400 block">Season / Pattam:</span>
                <span className="font-bold text-white">{formData.pattam}</span>
              </div>
              <div>
                <span className="text-slate-400 block">Soil Type & pH:</span>
                <span className="font-bold text-white">{formData.soilType} (pH {formData.soilPh})</span>
              </div>
              <div>
                <span className="text-slate-400 block">Available N-P-K:</span>
                <span className="font-bold text-white">{formData.soilN}-{formData.soilP}-{formData.soilK} kg/ha</span>
              </div>
              <div>
                <span className="text-slate-400 block">Irrigation:</span>
                <span className="font-bold text-white">{formData.irrigationType}</span>
              </div>
            </div>
          </div>

          {isPredicting ? (
            <div className="p-8 rounded-2xl bg-emerald-950/30 border border-emerald-500/30 text-center space-y-3">
              <div className="w-12 h-12 rounded-full border-4 border-emerald-500 border-t-transparent animate-spin mx-auto" />
              <div className="text-base font-bold text-white">{t('wizard.analyzing_message')}</div>
              <p className="text-xs text-slate-400">{t('wizard.please_wait')}</p>
            </div>
          ) : (
            <div className="flex justify-between pt-4">
              <button
                onClick={() => setCurrentStep(5)}
                className="px-5 py-2.5 rounded-xl glass-card text-slate-300 hover:text-white text-xs font-semibold flex items-center gap-2"
              >
                <ArrowLeft className="w-4 h-4" />
                <span>{t('common.back')}</span>
              </button>
              <button
                onClick={handleRunPrediction}
                className="px-8 py-4 rounded-2xl bg-gradient-to-r from-emerald-500 to-green-600 hover:from-emerald-400 hover:to-green-500 text-slate-950 font-extrabold text-base shadow-xl shadow-emerald-500/25 flex items-center gap-2 transition-all transform hover:-translate-y-0.5"
              >
                <span>{t('wizard.predict_now_btn')}</span>
                <ArrowRight className="w-5 h-5" />
              </button>
            </div>
          )}
        </div>
      )}
    </div>
  );
};
