import { useEffect, useRef, useState } from 'react'
import { useAuth0 } from '@auth0/auth0-react'
import { sendChatMessage } from '../api/chat.js'

function ParkingChat() {
  const { getAccessTokenSilently } = useAuth0()
  const [input, setInput] = useState('')
  const [messages, setMessages] = useState([])
  const [isSending, setIsSending] = useState(false)
  const [error, setError] = useState(null)
  const requestRef = useRef(null)
  const conversationRef = useRef(null)
  const inputRef = useRef(null)

  useEffect(() => () => requestRef.current?.abort(), [])

  useEffect(() => {
    const conversation = conversationRef.current
    conversation.scrollTop = conversation.scrollHeight
  }, [messages, isSending])

  async function handleSend(event) {
    event.preventDefault()
    const message = input.trim()
    if (!message || requestRef.current) return

    const controller = new AbortController()
    requestRef.current = controller
    setIsSending(true)
    setError(null)
    setMessages((previous) => [...previous, { role: 'user', text: message }])

    try {
      const accessToken = await getAccessTokenSilently()
      if (controller.signal.aborted) return

      const reply = await sendChatMessage(message, {
        accessToken,
        signal: controller.signal,
      })
      if (controller.signal.aborted) return

      setMessages((previous) => [...previous, { role: 'assistant', text: reply }])
      setInput('')
    } catch {
      if (!controller.signal.aborted) {
        setMessages((previous) => previous.slice(0, -1))
        setError('Could not send your message. Please try again.')
      }
    } finally {
      if (!controller.signal.aborted) {
        requestRef.current = null
        setIsSending(false)
        inputRef.current?.focus({ preventScroll: true })
      }
    }
  }

  return (
    <section className="data-card parking-chat" aria-labelledby="parking-chat-title">
      <div className="data-card__header">
        <div>
          <h2 id="parking-chat-title">Parking assistant</h2>
          <p>Ask about parking lots, levels, and available spaces.</p>
        </div>
      </div>

      <div
        className="parking-chat__conversation"
        ref={conversationRef}
        role="log"
        aria-label="Parking assistant conversation"
        tabIndex={0}
      >
        {messages.length === 0 && (
          <p className="parking-chat__empty">
            Where would you like to park? Try asking “How many spaces are free in Main Parking Lot?”
          </p>
        )}
        {messages.map((message, index) => (
          <div
            className={`parking-chat__message parking-chat__message--${message.role}`}
            key={index}
          >
            <span className="parking-chat__sender">
              {message.role === 'user' ? 'You' : 'Parking assistant'}
            </span>
            <p>{message.text}</p>
          </div>
        ))}
        {isSending && (
          <div className="parking-chat__thinking">
            <span className="spinner" aria-hidden="true" />
            Finding an answer...
          </div>
        )}
      </div>

      <form className="parking-chat__form" onSubmit={handleSend}>
        <label htmlFor="parking-chat-message">Your message</label>
        <div className="parking-chat__composer">
          <input
            id="parking-chat-message"
            name="message"
            ref={inputRef}
            type="text"
            value={input}
            onChange={(event) => setInput(event.target.value)}
            placeholder="Ask a parking question..."
            maxLength={4000}
            readOnly={isSending}
            autoComplete="off"
            required
          />
          <button
            className="auth-button auth-button--primary"
            type="submit"
            disabled={isSending || !input.trim()}
          >
            {isSending ? 'Sending...' : 'Send'}
          </button>
        </div>
        {error && <p className="parking-chat__error" role="alert">{error}</p>}
      </form>
    </section>
  )
}

export default ParkingChat
