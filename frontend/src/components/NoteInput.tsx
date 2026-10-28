import { useState } from 'react';
import axios from 'axios';
import { API_BASE_URL } from '../api/client';

type Props = {
  onCreated?: () => void;
};

export function NoteInput({ onCreated }: Props) {
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [tags, setTags] = useState('');
  const [loading, setLoading] = useState(false);

  async function handleSubmit() {
    if (!content.trim()) return;

    setLoading(true);
    try {
      await axios.post(`${API_BASE_URL}/notes`, {
        user_id: 'u_001',
        title: title || undefined,
        content,
        source: 'web',
        category: 'reflection',
        mood: 'neutral',
        importance: 0.7,
        tags: tags.split(',').map((tag) => tag.trim()).filter(Boolean),
      });

      setTitle('');
      setContent('');
      setTags('');
      onCreated?.();
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900 p-5 shadow-xl shadow-slate-950/30">
      <h2 className="mb-4 text-lg font-semibold text-white">New thought</h2>
      <div className="space-y-4">
        <input
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="Title"
          className="w-full rounded-xl border border-slate-700 bg-slate-950 px-3 py-2 text-white outline-none ring-0 placeholder:text-slate-500"
        />
        <textarea
          value={content}
          onChange={(e) => setContent(e.target.value)}
          placeholder="Write down your latest idea, reflection, or insight..."
          className="min-h-32 w-full rounded-xl border border-slate-700 bg-slate-950 px-3 py-2 text-white outline-none placeholder:text-slate-500"
        />
        <input
          value={tags}
          onChange={(e) => setTags(e.target.value)}
          placeholder="Tags (comma separated)"
          className="w-full rounded-xl border border-slate-700 bg-slate-950 px-3 py-2 text-white outline-none placeholder:text-slate-500"
        />
        <button
          onClick={handleSubmit}
          disabled={loading}
          className="rounded-xl bg-indigo-500 px-4 py-2 font-medium text-white transition hover:bg-indigo-400 disabled:cursor-not-allowed disabled:opacity-60"
        >
          {loading ? 'Saving...' : 'Save thought'}
        </button>
      </div>
    </div>
  );
}
