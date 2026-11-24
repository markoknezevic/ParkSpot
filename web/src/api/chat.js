export async function sendChatMessage(message, { accessToken, signal } = {}) {
  if (!accessToken) throw new Error('An access token is required')

  const response = await fetch('/api/chat/messages', {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${accessToken}`,
      'Content-Type': 'application/json',
    },
    signal,
    body: JSON.stringify({ message }),
  })

  if (!response.ok) {
    throw new Error(`Chat request failed with status ${response.status}`)
  }

  const data = await response.json()
  if (typeof data?.message !== 'string' || !data.message.trim()) {
    throw new Error('The chat response did not contain a message')
  }

  return data.message
}
