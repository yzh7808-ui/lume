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
    <div className="mx-auto max-w-5xl space-y-6">
      <section className="rounded-[26px] border border-[#e7e2db] bg-[#fffdfb] p-6 shadow-[0_10px_24px_rgba(32,33,37,0.06)]">
        <h1 className="text-3xl font-bold tracking-[-0.05em] text-[#1f2937]">Weekly reflection</h1>
        <p className="mt-3 max-w-3xl text-[17px] leading-8 text-[#4b5563]">{summary}</p>
      </section>

      <div className="grid gap-6 lg:grid-cols-2">
        <section className="rounded-[24px] border border-[#e7e2db] bg-[#fffdfb] p-6 shadow-[0_10px_24px_rgba(32,33,37,0.06)]">
          <h2 className="mb-5 text-2xl font-semibold tracking-[-0.04em] text-[#1f2937]">Core themes</h2>
          <div className="flex flex-wrap gap-2">
            {notes.length === 0 ? (
              <span className="text-[#6b7280]">No themes available yet.</span>
            ) : (
              [...new Set(notes.flatMap((note) => note.tags || []))].slice(0, 8).map((tag) => (
                <span key={tag} className="rounded-full bg-[#eef1ff] px-3 py-1.5 text-xs font-bold text-[#586fe7]">
                  #{tag}
                </span>
              ))
            )}
          </div>
        </section>

        <section className="rounded-[24px] border border-[#e7e2db] bg-[#fffdfb] p-6 shadow-[0_10px_24px_rgba(32,33,37,0.06)]">
          <h2 className="mb-5 text-2xl font-semibold tracking-[-0.04em] text-[#1f2937]">Reflection prompts</h2>
          <ul className="space-y-3 text-[15px] leading-7 text-[#4b5563]">
            {questions.map((question) => (
              <li key={question} className="rounded-2xl border border-[#e7e2db] bg-[#f3efe9] px-4 py-3">
                • {question}
              </li>
            ))}
          </ul>
        </section>
      </div>
    </div>
  );
}
