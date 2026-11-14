export async function requestProfile(accessToken, { changes, signal } = {}) {
  const headers = { Authorization: `Bearer ${accessToken}` }
  if (changes) headers['Content-Type'] = 'application/json'

  const response = await fetch('/api/users/me', {
    method: changes ? 'PATCH' : 'GET',
    headers,
    signal,
    body: changes ? JSON.stringify(changes) : undefined,
  })
  if (!response.ok) throw new Error(`Profile request failed (${response.status})`)
  return response.json()
}
