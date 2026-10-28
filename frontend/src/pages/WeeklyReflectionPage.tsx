import { useEffect, useMemo, useState } from 'react';
import axios from 'axios';
import { API_BASE_URL } from '../api/client';

type Note = {
  id: number;
  title: string | null;
  content: string;
  summary?: string | null;
  category: string;
  mood?: string | null;
  tags: string[];
  created_at: string;
};

export function WeeklyReflectionPage() {
  const [notes, setNotes] = useState<Note[]>([]);

  useEffect(() => {
    axios
      .get(`${API_BASE_URL}/notes`, { params: { user_id: 'u_001' } })
      .then((res) => setNotes(res.data))
      .catch(() => setNotes([]));
  }, []);

  const summary = useMemo(() => {
    if (notes.length === 0) {
      return 'No notes yet. Start journaling to unlock weekly reflections.';
    }

    const tagCounts = new Map<string, number>();
    for (const note of notes) {
      for (const tag of note.tags || []) {
        tagCounts.set(tag, (tagCounts.get(tag) || 0) + 1);
      }
    }

    const themes = [...tagCounts.entries()]
      .sort((a, b) => b[1] - a[1])
      .slice(0, 4)
      .map(([tag]) => tag);

    return `Your recent notes keep circling around ${themes.join(', ') || 'your core themes'}. This suggests a recurring pattern worth paying attention to.`;
  }, [notes]);

  const questions = useMemo(
    () => [
      'What keeps recurring across this week?',
      'What deserves more attention than it currently gets?',
      'Which thought pattern is creating friction?',
    ],
    [],
  );

  return (
    <div className="space-y-6">
      <div className="rounded-2xl border border-slate-800 bg-slate-900 p-5 shadow-xl shadow-slate-950/30">
        <h1 className="mb-2 text-2xl font-semibold text-white">Weekly reflection</h1>
        <p className="text-slate-300">{summary}</p>
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <div className="rounded-2xl border border-slate-800 bg-slate-900 p-5">
          <h2 className="mb-4 text-lg font-semibold text-white">Core themes</h2>
          <div className="flex flex-wrap gap-2">
            {notes.length === 0 ? (
              <span className="text-slate-400">No themes available yet.</span>
            ) : (
              [...new Set(notes.flatMap((note) => note.tags || []))].slice(0, 8).map((tag) => (
                <span key={tag} className="rounded-full bg-indigo-500/15 px-3 py-1 text-xs font-medium text-indigo-200">
                  #{tag}
                </span>
              ))
            )}
          </div>
        </div>

        <div className="rounded-2xl border border-slate-800 bg-slate-900 p-5">
          <h2 className="mb-4 text-lg font-semibold text-white">Reflection prompts</h2>
          <ul className="space-y-2 text-sm text-slate-300">
            {questions.map((question) => (
              <li key={question}>• {question}</li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}
