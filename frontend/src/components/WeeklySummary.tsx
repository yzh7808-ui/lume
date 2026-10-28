import { useEffect, useState } from 'react';
import axios from 'axios';
import { API_BASE_URL } from '../api/client';

type Insight = {
  user_id: string;
  summary: string;
  themes: string[];
  questions: string[];
};

export function WeeklySummary() {
  const [data, setData] = useState<Insight | null>(null);

  useEffect(() => {
    axios
      .get(`${API_BASE_URL}/insights/weekly`, {
        params: { user_id: 'u_001' },
      })
      .then((res) => setData(res.data))
      .catch(() => setData({
        user_id: 'u_001',
        summary: 'No weekly summary yet. Start journaling and your insights will appear here.',
        themes: ['Growth', 'Work', 'Life'],
        questions: ['What keeps repeating?', 'What deserves more attention?'],
      }));
  }, []);

  if (!data) return null;

  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900 p-5 shadow-xl shadow-slate-950/30">
      <h2 className="mb-3 text-lg font-semibold text-white">Weekly reflection</h2>
      <p className="mb-4 text-sm text-slate-300">{data.summary}</p>

      <div className="mb-4 flex flex-wrap gap-2">
        {data.themes.map((theme) => (
          <span key={theme} className="rounded-full bg-indigo-500/15 px-3 py-1 text-xs font-medium text-indigo-200">
            {theme}
          </span>
        ))}
      </div>

      <ul className="space-y-2 text-sm text-slate-300">
        {data.questions.map((question) => (
          <li key={question}>• {question}</li>
        ))}
      </ul>
    </div>
  );
}
