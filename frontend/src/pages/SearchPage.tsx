import { useState } from 'react';
import axios from 'axios';
import { API_BASE_URL } from '../api/client';

type SearchResult = {
  id: string | number;
  score?: number;
  payload?: {
    note_id?: number;
    title?: string | null;
    summary?: string | null;
    category?: string;
    mood?: string | null;
    source?: string;
    user_id?: string;
  };
};

export function SearchPage() {
  const [query, setQuery] = useState('成长');
  const [results, setResults] = useState<SearchResult[]>([]);
  const [loading, setLoading] = useState(false);

  async function handleSearch() {
    if (!query.trim()) return;

    setLoading(true);
    try {
      const res = await axios.get(`${API_BASE_URL}/notes/search`, {
        params: {
          user_id: 'u_001',
          query,
          limit: 5,
        },
      });
      setResults(res.data);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="mx-auto max-w-4xl space-y-6">
      <section className="rounded-[26px] border border-[#e7e2db] bg-[#fffdfb] p-6 shadow-[0_10px_24px_rgba(32,33,37,0.06)]">
        <h1 className="text-3xl font-bold tracking-[-0.05em] text-[#1f2937]">Search thoughts</h1>

        <div className="mt-5 flex gap-3">
          <input
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search for a theme, idea, or memory..."
            className="flex-1 rounded-2xl border border-[#e7e2db] bg-[#f3efe9] px-4 py-3 text-base text-[#1f2937] outline-none placeholder:text-[#6b7280]"
          />
          <button
            onClick={handleSearch}
            disabled={loading}
            className="rounded-2xl bg-[#7b8cff] px-5 py-3 font-semibold text-white shadow-[0_8px_18px_rgba(123,140,255,0.18)] transition hover:bg-[#687cf4] disabled:cursor-not-allowed disabled:opacity-60"
          >
            {loading ? 'Searching...' : 'Search'}
          </button>
        </div>
      </section>

      <section className="space-y-4">
        {results.length === 0 ? (
          <div className="rounded-[20px] border border-[#e7e2db] bg-[#fffdfb] p-5 text-[#6b7280] shadow-[0_8px_20px_rgba(15,23,42,0.04)]">
            No related notes yet. Try a different topic.
          </div>
        ) : (
          results.map((item, idx) => {
            const payload = item.payload || {};
            const title = payload.title || `Related thought ${idx + 1}`;
            const summary = payload.summary || 'No summary available.';
            const category = payload.category || 'reflection';

            return (
              <article
                key={String(item.id || idx)}
                className="rounded-[22px] border border-[#e7e2db] bg-[#fffdfb] p-5 shadow-[0_8px_20px_rgba(15,23,42,0.04)]"
              >
                <div className="mb-2 flex items-center justify-between gap-4">
                  <h3 className="text-xl font-semibold text-[#1f2937]">{title}</h3>
                  <span className="rounded-full bg-[#eef1ff] px-2.5 py-1 text-[10px] font-bold uppercase tracking-[0.08em] text-[#586fe7]">
                    {category}
                  </span>
                </div>
                <p className="leading-7 text-[#4b5563]">{summary}</p>
                {typeof item.score === 'number' && (
                  <p className="mt-3 text-xs text-[#6b7280]">
                    Relevance: {(item.score * 100).toFixed(1)}%
                  </p>
                )}
              </article>
            );
          })
        )}
      </section>
    </div>
  );
}
