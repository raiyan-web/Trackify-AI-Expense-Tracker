import { useState } from 'react'
import Charts from '../components/Charts'

export default function Reports() {
  const [month, setMonth] = useState('1')
  const [year, setYear] = useState('2025')
  const [report, setReport] = useState(null)
  const [error, setError] = useState('')

  const handleFetch = async () => {
    try {
      setError('')
      const response = await fetch(`http://localhost:8000/reports/monthly?month=${month}&year=${year}`)
      if (!response.ok) throw new Error('Unable to fetch report')
      setReport(await response.json())
    } catch (err) {
      setError(err.message)
    }
  }

  return (
    <div className="space-y-6">
      <div className="rounded-3xl bg-white p-8 shadow-sm">
        <h2 className="text-2xl font-semibold">Monthly report</h2>
        <p className="mt-2 text-slate-600">Generate spending summaries and category breakdowns.</p>
        <div className="mt-6 flex flex-wrap gap-4">
          <select value={month} onChange={(e) => setMonth(e.target.value)} className="rounded-3xl border border-slate-200 bg-slate-50 px-4 py-3">
            {Array.from({ length: 12 }, (_, i) => i + 1).map((value) => (
              <option key={value} value={value}>{value}</option>
            ))}
          </select>
          <input
            type="number"
            min="2024"
            value={year}
            onChange={(e) => setYear(e.target.value)}
            className="rounded-3xl border border-slate-200 bg-slate-50 px-4 py-3"
          />
          <button onClick={handleFetch} className="rounded-3xl bg-sky-600 px-5 py-3 text-white shadow-sm hover:bg-sky-700">
            Fetch report
          </button>
        </div>
      </div>
      {error && <div className="rounded-3xl bg-rose-50 p-6 text-rose-700 shadow-sm">{error}</div>}
      {report && (
        <div className="rounded-3xl bg-white p-8 shadow-sm">
          <div className="flex items-center justify-between gap-4">
            <div>
              <h3 className="text-xl font-semibold">{report.month}/{report.year}</h3>
              <p className="mt-1 text-slate-500">Total spent: ${report.total_spent.toFixed(2)}</p>
            </div>
          </div>
          <div className="mt-6">
            <Charts data={report.by_category} />
          </div>
        </div>
      )}
    </div>
  )
}
