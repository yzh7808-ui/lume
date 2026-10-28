import { NoteInput } from '../components/NoteInput';
import { NoteList } from '../components/NoteList';
import { WeeklySummary } from '../components/WeeklySummary';
import { useState } from 'react';

export function HomePage() {
  const [refreshKey, setRefreshKey] = useState(0);

  return (
    <div className="space-y-6">
      <section className="grid gap-6 xl:grid-cols-[1.1fr,0.9fr]">
        <NoteInput onCreated={() => setRefreshKey((k) => k + 1)} />
        <WeeklySummary />
      </section>

      <section>
        <NoteList key={refreshKey} />
      </section>
    </div>
  );
}
