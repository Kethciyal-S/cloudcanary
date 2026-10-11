import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom';
import Overview from './pages/Overview';
import Events from './pages/Events';

function NavLink({ to, children }) {
  const location = useLocation();
  const isActive = location.pathname === to;
  return (
    <Link
      to={to}
      className={`px-4 py-2 rounded transition ${
        isActive ? 'bg-emerald-500 text-white' : 'text-slate-400 hover:text-white'
      }`}
    >
      {children}
    </Link>
  );
}

function Header() {
  return (
    <header className="border-b border-slate-800 bg-slate-950 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <span className="text-2xl">🐤</span>
          <span className="text-xl font-bold">CloudCanary</span>
        </div>
        <nav className="flex gap-2">
          <NavLink to="/">Overview</NavLink>
          <NavLink to="/events">Events</NavLink>
        </nav>
      </div>
    </header>
  );
}

export default function App() {
  return (
    <Router>
      <div className="min-h-screen bg-slate-950">
        <Header />
        <main className="max-w-7xl mx-auto">
          <Routes>
            <Route path="/" element={<Overview />} />
            <Route path="/events" element={<Events />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}
