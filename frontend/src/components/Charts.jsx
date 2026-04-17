import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, PieChart, Pie, Cell, Legend } from 'recharts'

const COLORS = ['#0ea5e9', '#22c55e', '#eab308', '#f97316', '#6366f1']

export default function Charts({ data = [] }) {
  const barData = data.map((item) => ({ name: item.category, value: item.total }))

  return (
    <div className="grid gap-6 lg:grid-cols-[2fr_1fr]">
      <div className="rounded-3xl border border-slate-200 bg-white p-6">
        <h4 className="text-lg font-semibold">Category spend</h4>
        <div className="mt-4 h-80">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={barData} margin={{ top: 10, right: 20, left: 0, bottom: 0 }}>
              <XAxis dataKey="name" tick={{ fill: '#475569', fontSize: 12 }} />
              <YAxis tick={{ fill: '#475569', fontSize: 12 }} />
              <Tooltip />
              <Bar dataKey="value" fill="#0ea5e9" radius={[8, 8, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
      <div className="rounded-3xl border border-slate-200 bg-white p-6">
        <h4 className="text-lg font-semibold">Category breakdown</h4>
        <div className="mt-4 h-80">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie data={barData} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={90} fill="#0ea5e9" label>
                {barData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Legend verticalAlign="bottom" height={36} />
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  )
}
