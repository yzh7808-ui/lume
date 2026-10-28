import { Link, Route, Routes } from 'react-router-dom';
import { HomePage } from './pages/HomePage';
import { SearchPage } from './pages/SearchPage';
import { WeeklyReflectionPage } from './pages/WeeklyReflectionPage';

export default function App() {
  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      <header className="border-b border-slate-800 bg-slate-950/80 backdrop-blur-sm">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
          <Link to="/" className="text-xl font-semibold tracking-tight text-white">
            Lume
          </Link>
          <nav className="flex gap-4 text-sm text-slate-300">
            <Link to="/" className="hover:text-white">Home</Link>
            <Link to="/notes" className="hover:text-white">Notes</Link>
            <Link to="/search" className="hover:text-white">Search</Link>
            <Link to="/reflection" className="hover:text-white">Reflection</Link>
          </nav>
        </div>
      </header>

      <main className="mx-auto max-w-6xl px-6 py-8">
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
