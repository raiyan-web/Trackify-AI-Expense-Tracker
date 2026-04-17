import { Routes, Route, NavLink } from 'react-router-dom'
import Dashboard from './pages/Dashboard'
import Upload from './pages/Upload'
import Expenses from './pages/Expenses'
import Reports from './pages/Reports'

const links = [
  { to: '/', label: 'Dashboard' },
  { to: '/upload', label: 'Upload' },
  { to: '/expenses', label: 'Expenses' },
  { to: '/reports', label: 'Reports' },
]

export default function App() {
  return (
    <div className="min-h-screen bg-slate-100 text-slate-900">
      <header className="bg-white shadow-sm border-b">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
          <div>
            <h1 className="text-xl font-semibold">Trackify</h1>
            <p className="text-sm text-slate-500">AI receipt & expense tracker</p>
          </div>
          <nav className="flex gap-4">
            {links.map((link) => (
              <NavLink
                key={link.to}
                to={link.to}
                className={({ isActive }) =>
                  `text-sm font-medium ${isActive ? 'text-sky-600' : 'text-slate-600 hover:text-slate-900'}`
                }
              >
                {link.label}
              </NavLink>
            ))}
          </nav>
        </div>
      </header>
      <main className="mx-auto max-w-6xl px-6 py-8">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/upload" element={<Upload />} />
          <Route path="/expenses" element={<Expenses />} />
          <Route path="/reports" element={<Reports />} />
        </Routes>
      </main>
    </div>
  )
}
