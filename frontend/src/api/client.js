const BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

export async function apiRequest(path, options = {}) {
  const response = await fetch(`${BASE_URL}${path}`, {
    headers: {
      'Accept': 'application/json',
      ...options.headers,
    },
    ...options,
  })
  if (!response.ok) {
    const error = await response.json().catch(() => ({}))
    throw new Error(error.detail || response.statusText)
  }
  return response.json()
}

export async function uploadReceipt(file) {
  const formData = new FormData()
  formData.append('file', file)
  return apiRequest('/receipts/upload', {
    method: 'POST',
    body: formData,
  })
}
