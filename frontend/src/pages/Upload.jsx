import { useState } from 'react'
import { uploadReceipt } from '../api/client'

export default function Upload() {
  const [result, setResult] = useState(null)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleUpload = async (event) => {
    setError('')
    setResult(null)
    const file = event.target.files?.[0]
    if (!file) return

    setLoading(true)
    try {
      const data = await uploadReceipt(file)
      setResult(data.data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-6">
      <div className="rounded-3xl bg-white p-8 shadow-sm">
        <h2 className="text-2xl font-semibold">Upload receipt</h2>
        <p className="mt-2 text-slate-600">Drop a receipt image and let Claude extract merchant, date, total, and line items.</p>
        <div className="mt-6">
          <input
            type="file"
            accept="image/*"
            onChange={handleUpload}
            className="block w-full cursor-pointer rounded-3xl border border-slate-200 bg-slate-50 p-3 text-sm"
          />
        </div>
      </div>

      {loading && <div className="rounded-3xl bg-white p-6 shadow-sm">Processing receipt...</div>}
      {error && <div className="rounded-3xl bg-rose-50 p-6 text-rose-700 shadow-sm">{error}</div>}

      {result && (
        <div className="rounded-3xl bg-white p-8 shadow-sm">
          <h3 className="text-xl font-semibold">Extracted receipt</h3>
          <div className="mt-4 grid gap-4 sm:grid-cols-2">
            <div>
              <p className="text-sm text-slate-500">Merchant</p>
              <p className="mt-1 text-lg font-medium">{result.merchant}</p>
            </div>
            <div>
              <p className="text-sm text-slate-500">Category</p>
              <p className="mt-1 text-lg font-medium">{result.category}</p>
            </div>
            <div>
              <p className="text-sm text-slate-500">Total</p>
              <p className="mt-1 text-lg font-medium">${result.total}</p>
            </div>
            <div>
              <p className="text-sm text-slate-500">Date</p>
              <p className="mt-1 text-lg font-medium">{result.date}</p>
            </div>
          </div>

          <div className="mt-6">
            <h4 className="text-lg font-semibold">Items</h4>
            {result.items?.length ? (
              <ul className="mt-3 space-y-2">
                {result.items.map((item, index) => (
                  <li key={index} className="rounded-2xl border border-slate-200 p-4">
                    <div className="flex justify-between gap-4">
                      <span>{item.name || 'Item'}</span>
                      <strong>${item.price ?? '0.00'}</strong>
                    </div>
                  </li>
                ))}
              </ul>
            ) : (
              <p className="mt-3 text-sm text-slate-500">No items were extracted from this receipt.</p>
            )}
          </div>
        </div>
      )}
    </div>
  )
}
