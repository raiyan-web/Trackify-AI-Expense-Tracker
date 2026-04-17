export default function ExpenseTable({ expenses }) {
  if (!expenses?.length) {
    return (
      <div className="rounded-3xl bg-white p-8 shadow-sm">
        <p className="text-slate-500">No expenses found yet. Upload a receipt or add an expense manually.</p>
      </div>
    )
  }

  return (
    <div className="overflow-hidden rounded-3xl bg-white shadow-sm">
      <table className="min-w-full divide-y divide-slate-200">
        <thead className="bg-slate-50">
          <tr>
            <th className="px-6 py-4 text-left text-sm font-semibold text-slate-700">Merchant</th>
            <th className="px-6 py-4 text-left text-sm font-semibold text-slate-700">Category</th>
            <th className="px-6 py-4 text-left text-sm font-semibold text-slate-700">Date</th>
            <th className="px-6 py-4 text-right text-sm font-semibold text-slate-700">Total</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-200 bg-white">
          {expenses.map((expense) => (
            <tr key={expense.id}>
              <td className="px-6 py-4 text-sm text-slate-700">{expense.merchant}</td>
              <td className="px-6 py-4 text-sm text-slate-700">{expense.category}</td>
              <td className="px-6 py-4 text-sm text-slate-700">{expense.date}</td>
              <td className="px-6 py-4 text-right text-sm font-semibold text-slate-900">${expense.total}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
