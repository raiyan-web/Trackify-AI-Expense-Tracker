export default function ReceiptCard({ receipt }) {
  return (
    <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
      <div className="flex items-start justify-between gap-4">
        <div>
          <h4 className="text-lg font-semibold">{receipt.merchant}</h4>
          <p className="mt-1 text-sm text-slate-500">{receipt.category}</p>
        </div>
        <span className="text-lg font-semibold text-slate-900">${receipt.total}</span>
      </div>
      <div className="mt-4 text-sm text-slate-500">
        <p>Date: {receipt.date}</p>
        <p>Items: {receipt.items?.length ?? 0}</p>
      </div>
    </div>
  )
}
