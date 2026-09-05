export async function getParkingLots({ signal } = {}) {
  const response = await fetch('/api/parking-lots', { signal })

  if (!response.ok) {
    throw new Error(`Request failed with status ${response.status}`)
  }

  return response.json()
}
