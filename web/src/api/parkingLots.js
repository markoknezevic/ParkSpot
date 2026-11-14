async function fetchParkingLots(path, { signal, accessToken } = {}) {
  if (!accessToken) throw new Error('An access token is required')
  const response = await fetch(path, {
    signal,
    headers: { Authorization: `Bearer ${accessToken}` },
  })

  if (!response.ok) {
    throw new Error(`Request failed with status ${response.status}`)
  }

  return response.json()
}

export function getParkingLots(options) {
  return fetchParkingLots('/api/parking-lots', options)
}

export function getParkingLot(id, options) {
  return fetchParkingLots(`/api/parking-lots/${encodeURIComponent(id)}`, options)
}
