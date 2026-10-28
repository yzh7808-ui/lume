import { Link, Route, Routes } from 'react-router-dom';
import { HomePage } from './pages/HomePage';
import { SearchPage } from './pages/SearchPage';
import { WeeklyReflectionPage } from './pages/WeeklyReflectionPage';

export default function App() {
  return (
    <div className="min-h-screen bg-[#f6f3ee] text-[#1f2937]">
      <header className="sticky top-0 z-10 border-b border-[#e7e2db] bg-white/70 backdrop-blur-md">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
          <Link to="/" className="text-3xl font-bold tracking-[-0.06em] text-[#1f2937]">
            Lume
          </Link>

          <nav className="flex items-center gap-5 text-sm font-semibold text-[#4b5563]">
            <Link to="/" className="transition-colors hover:text-[#1f2937]">Home</Link>
            <Link to="/notes" className="transition-colors hover:text-[#1f2937]">Notes</Link>
            <Link to="/search" className="transition-colors hover:text-[#1f2937]">Search</Link>
            <Link to="/reflection" className="transition-colors hover:text-[#1f2937]">Reflection</Link>
          </nav>
        </div>
      </header>

      <main className="mx-auto max-w-6xl px-6 pb-12 pt-8">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/notes" element={<HomePage />} />
          <Route path="/search" element={<SearchPage />} />
          <Route path="/reflection" element={<WeeklyReflectionPage />} />
        </Routes>
      </main>
    </div>
  );
}
