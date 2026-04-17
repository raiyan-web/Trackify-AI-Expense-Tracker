import Charts from '../components/Charts'

export default function Dashboard() {
  return (
    <div className="space-y-6">
      <section className="rounded-3xl bg-white p-8 shadow-sm">
        <div className="flex items-center justify-between gap-4">
          <div>
            <h2 className="text-2xl font-semibold">Welcome to Trackify</h2>
            <p className="mt-2 text-sm text-slate-600">
              Track receipts, categorize expenses, and get quick monthly reports.
            </p>
          </div>
          <div className="rounded-2xl bg-slate-100 px-4 py-3 text-sm text-slate-700">
            Ready to import receipts
          </div>
        </div>
      </section>

      <section className="grid gap-6 xl:grid-cols-3">
        <div className="rounded-3xl bg-white p-6 shadow-sm">
          <p className="text-sm uppercase tracking-[0.2em] text-slate-500">Total spend</p>
          <p className="mt-4 text-4xl font-semibold">$8,420</p>
          <p className="mt-2 text-sm text-slate-500">Based on last 30 days</p>
        </div>
        <div className="rounded-3xl bg-white p-6 shadow-sm">
          <p className="text-sm uppercase tracking-[0.2em] text-slate-500">Receipts processed</p>
          <p className="mt-4 text-4xl font-semibold">27</p>
          <p className="mt-2 text-sm text-slate-500">AI extraction completed</p>
        </div>
        <div className="rounded-3xl bg-white p-6 shadow-sm">
          <p className="text-sm uppercase tracking-[0.2em] text-slate-500">Active categories</p>
          <p className="mt-4 text-4xl font-semibold">5</p>
          <p className="mt-2 text-sm text-slate-500">Food, Travel, Shopping, Health</p>
        </div>
      </section>

      <section className="rounded-3xl bg-white p-6 shadow-sm">
        <div className="flex items-center justify-between">
          <h3 className="text-lg font-semibold">Spending overview</h3>
          <span className="text-sm text-slate-500">Last 30 days</span>
        </div>
        <div className="mt-6">
          <Charts />
        </div>
      </section>
    </div>
  )
}
