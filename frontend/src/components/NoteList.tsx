import { useEffect, useState } from 'react';
import axios from 'axios';
import { API_BASE_URL } from '../api/client';
import { Note } from '../types/note';

export function NoteList() {
  const [notes, setNotes] = useState<Note[]>([]);
  const [loading, setLoading] = useState(true);

  async function fetchNotes() {
    setLoading(true);
    try {
      const res = await axios.get(`${API_BASE_URL}/notes`, {
        params: { user_id: 'u_001' },
      });
      setNotes(res.data);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    fetchNotes();
  }, []);

  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900 p-5 shadow-xl shadow-slate-950/30">
      <div className="mb-4 flex items-center justify-between">
        <h2 className="text-lg font-semibold text-white">Recent thoughts</h2>
        <button
          onClick={fetchNotes}
          className="rounded-lg border border-slate-700 bg-slate-800 px-3 py-1.5 text-sm text-slate-200 hover:bg-slate-700"
        >
          Refresh
        </button>
      </div>

      {loading ? (
        <div className="text-slate-400">Loading...</div>
      ) : notes.length === 0 ? (
        <div className="text-slate-400">No notes yet.</div>
      ) : (
        <div className="space-y-4">
          {notes.map((note) => (
            <article key={note.id} className="rounded-xl border border-slate-800 bg-slate-950 p-4">
              <div className="mb-2 flex items-center justify-between gap-4">
                <h3 className="font-medium text-white">{note.title || 'Untitled thought'}</h3>
                <span className="text-xs uppercase tracking-wide text-indigo-300">{note.category}</span>
              </div>
              <p className="text-sm leading-6 text-slate-300">{note.content}</p>
              <div className="mt-3 flex flex-wrap gap-2">
                {note.tags.map((tag) => (
                  <span key={tag} className="rounded-full border border-slate-700 bg-slate-800 px-2 py-1 text-xs text-slate-300">
                    #{tag}
                  </span>
                ))}
              </div>
              <p className="mt-3 text-xs text-slate-500">
                {new Date(note.created_at).toLocaleString()}
              </p>
            </article>
          ))}
        </div>
      )}
    </div>
  );
}
