import { useEffect, useState } from 'react'
import ExpenseTable from '../components/ExpenseTable'

export default function Expenses() {
  const [expenses, setExpenses] = useState([])
  const [error, setError] = useState('')

  useEffect(() => {
    async function fetchExpenses() {
      try {
        const response = await fetch('http://localhost:8000/expenses/', {
          credentials: 'include',
        })
        const data = await response.json()
        setExpenses(data)
      } catch (err) {
        setError('Unable to load expenses. Ensure the backend is running.')
      }
    }
    fetchExpenses()
  }, [])

  return (
    <div className="space-y-6">
      <div className="rounded-3xl bg-white p-8 shadow-sm">
        <h2 className="text-2xl font-semibold">Expenses</h2>
        <p className="mt-2 text-slate-600">A summary of your latest expense entries.</p>
      </div>
      {error && <div className="rounded-3xl bg-rose-50 p-6 text-rose-700 shadow-sm">{error}</div>}
      <ExpenseTable expenses={expenses} />
    </div>
  )
}
