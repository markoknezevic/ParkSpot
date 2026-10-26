export async function getParkingLots({ signal, accessToken } = {}) {
  if (!accessToken) throw new Error('An access token is required')
  const response = await fetch('/api/parking-lots', {
    signal,
    headers: { Authorization: `Bearer ${accessToken}` },
  })

  if (!response.ok) {
    throw new Error(`Request failed with status ${response.status}`)
  }

  return response.json()
}
