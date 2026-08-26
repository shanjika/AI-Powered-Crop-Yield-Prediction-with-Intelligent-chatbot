import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import api from '../services/api';
import { FlaskConical, Upload, CheckCircle2, AlertCircle, FileText, Sparkles } from 'lucide-react';

export const SoilReportPage: React.FC = () => {
  const { t, i18n } = useTranslation();
  const lang = i18n.language || 'ta';

  const [reports, setReports] = useState<any[]>([]);
  const [isUploading, setIsUploading] = useState(false);
  const [extractedData, setExtractedData] = useState<any | null>(null);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  const loadReports = () => {
    api.get('/soil/my-reports')
      .then((res) => setReports(res.data))
      .catch((err) => console.error('Error fetching soil reports:', err));
  };

  useEffect(() => {
    loadReports();
  }, []);

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!e.target.files || e.target.files.length === 0) return;
    const file = e.target.files[0];
    setIsUploading(true);
    setError('');
    setMessage('');

    const form = new FormData();
    form.append('file', file);

    try {
      const res = await api.post('/soil/upload', form, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      setExtractedData(res.data.extracted_parameters);
      setMessage(lang === 'ta' ? res.data.message_ta : res.data.message_en);
      loadReports();
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to analyze soil report.');
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6 pb-12">
      {/* Header */}
      <div className="glass-panel rounded-3xl p-6 sm:p-8 space-y-2 border border-emerald-500/20">
        <div className="flex items-center gap-3">
          <div className="w-12 h-12 rounded-2xl bg-blue-500/20 flex items-center justify-center text-blue-400 font-bold shadow-lg shadow-blue-500/10">
            <FlaskConical className="w-7 h-7" />
          </div>
          <div>
            <h1 className="text-xl sm:text-2xl font-extrabold text-white">{t('nav.soil_health')}</h1>
            <p className="text-xs text-slate-300">Soil Health Card OCR analyzer and fertility rating center</p>
          </div>
        </div>
      </div>

      {/* Upload Box */}
      <div className="glass-panel rounded-3xl p-6 sm:p-8 space-y-4">
        <div className="p-8 rounded-2xl border-2 border-dashed border-slate-700 hover:border-emerald-500/60 bg-slate-900/40 text-center space-y-3 transition-colors">
          <Upload className="w-10 h-10 text-emerald-400 mx-auto" />
          <div className="space-y-1">
            <span className="text-base font-bold text-white block">Upload Soil Test Card / Lab Report</span>
            <span className="text-xs text-slate-400 block max-w-sm mx-auto">
              Supports PDF documents, JPG, JPEG, and PNG soil testing laboratory reports.
            </span>
          </div>
          <label className="inline-flex items-center gap-2 px-6 py-3 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 text-xs font-bold cursor-pointer shadow-lg shadow-emerald-500/20 transition-all">
            <span>{isUploading ? t('common.loading') : 'Choose File to Analyze'}</span>
            <input
              type="file"
              accept=".pdf,.jpg,.jpeg,.png,.webp"
              onChange={handleFileUpload}
              className="hidden"
            />
          </label>
        </div>

        {message && (
          <div className="p-3.5 rounded-xl bg-emerald-950/40 border border-emerald-500/30 text-emerald-300 text-xs flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
            <span>{message}</span>
          </div>
        )}

        {error && (
          <div className="p-3.5 rounded-xl bg-red-950/40 border border-red-500/30 text-red-200 text-xs flex items-center gap-2">
            <AlertCircle className="w-4 h-4 text-red-400 shrink-0" />
            <span>{error}</span>
          </div>
        )}
      </div>

      {/* Extracted Parameters Card */}
      {extractedData && (
        <div className="glass-panel rounded-3xl p-6 sm:p-8 space-y-4 border border-emerald-500/30 animate-fadeIn">
          <div className="flex items-center gap-2 text-sm font-bold text-emerald-300">
            <Sparkles className="w-4 h-4" />
            <span>AI Soil Report OCR Analysis</span>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
            <div className="p-3.5 rounded-xl bg-slate-900/80 border border-slate-800 text-center">
              <span className="text-[11px] text-slate-400 block font-semibold">Soil pH</span>
              <span className="text-xl font-extrabold text-white">{extractedData.ph}</span>
              <span className="text-[10px] text-emerald-400 block mt-0.5">
                {extractedData.ratings?.ph?.rating_en}
              </span>
            </div>

            <div className="p-3.5 rounded-xl bg-slate-900/80 border border-slate-800 text-center">
              <span className="text-[11px] text-slate-400 block font-semibold">Nitrogen (N)</span>
              <span className="text-xl font-extrabold text-white">{extractedData.nitrogen}</span>
              <span className="text-[10px] text-emerald-400 block mt-0.5">
                {extractedData.ratings?.nitrogen?.rating_en}
              </span>
            </div>

            <div className="p-3.5 rounded-xl bg-slate-900/80 border border-slate-800 text-center">
              <span className="text-[11px] text-slate-400 block font-semibold">Phosphorus (P)</span>
              <span className="text-xl font-extrabold text-white">{extractedData.phosphorus}</span>
              <span className="text-[10px] text-emerald-400 block mt-0.5">
                {extractedData.ratings?.phosphorus?.rating_en}
              </span>
            </div>

            <div className="p-3.5 rounded-xl bg-slate-900/80 border border-slate-800 text-center">
              <span className="text-[11px] text-slate-400 block font-semibold">Potassium (K)</span>
              <span className="text-xl font-extrabold text-white">{extractedData.potassium}</span>
              <span className="text-[10px] text-emerald-400 block mt-0.5">
                {extractedData.ratings?.potassium?.rating_en}
              </span>
            </div>
          </div>
        </div>
      )}

      {/* Past Reports List */}
      <div className="glass-panel rounded-3xl p-6 sm:p-8 space-y-4">
        <h2 className="text-base font-bold text-white flex items-center gap-2">
          <FileText className="w-4 h-4 text-emerald-400" />
          <span>Previous Soil Health Reports</span>
        </h2>

        {reports.length > 0 ? (
          <div className="space-y-2.5">
            {reports.map((r) => (
              <div
                key={r.id}
                className="p-4 rounded-xl bg-slate-900/60 border border-slate-800 flex flex-wrap items-center justify-between gap-3 text-xs"
              >
                <div>
                  <span className="font-bold text-white block">{r.file_name}</span>
                  <span className="text-slate-400 text-[11px]">{r.soil_type} • {r.created_at}</span>
                </div>
                <div className="flex gap-4 text-right">
                  <div>
                    <span className="text-slate-400 block text-[10px]">pH</span>
                    <span className="font-bold text-emerald-400">{r.ph}</span>
                  </div>
                  <div>
                    <span className="text-slate-400 block text-[10px]">N-P-K (kg/ha)</span>
                    <span className="font-bold text-white">{r.nitrogen}-{r.phosphorus}-{r.potassium}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-xs text-slate-400 py-3 text-center">No previous soil reports uploaded yet.</p>
        )}
      </div>
    </div>
  );
};
