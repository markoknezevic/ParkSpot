import { useEffect, useState } from 'react'
import { useAuth0 } from '@auth0/auth0-react'
import { requestProfile } from '../api/profile.js'

function namesFrom(profile) {
  return { firstName: profile.firstName ?? '', lastName: profile.lastName ?? '' }
}

export default function ProfilePage() {
  const { getAccessTokenSilently } = useAuth0()
  const [original, setOriginal] = useState(null)
  const [names, setNames] = useState(null)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState('')
  const [saved, setSaved] = useState(false)

  useEffect(() => {
    const controller = new AbortController()
    async function load() {
      try {
        const token = await getAccessTokenSilently()
        const profile = await requestProfile(token, { signal: controller.signal })
        if (controller.signal.aborted) return
        const values = namesFrom(profile)
        setOriginal(values)
        setNames(values)
      } catch {
        if (!controller.signal.aborted) setError('Could not load your profile. Refresh to try again.')
      }
    }
    load()
    return () => controller.abort()
  }, [getAccessTokenSilently])

  const changes = {}
  for (const field of Object.keys(names ?? {})) {
    if (names[field] !== original[field]) changes[field] = names[field] || null
  }

  async function save(event) {
    event.preventDefault()
    if (saving || !Object.keys(changes).length) return
    setSaving(true)
    setError('')
    try {
      const token = await getAccessTokenSilently()
      const values = namesFrom(await requestProfile(token, { changes }))
      setNames(values)
      setOriginal(values)
      setSaved(true)
    } catch {
      setError('Could not save your changes. Please try again.')
    } finally {
      setSaving(false)
    }
  }

  function edit(event) {
    setNames({ ...names, [event.target.name]: event.target.value })
    setSaved(false)
    setError('')
  }

  return (
    <main className="main-content">
      <div className="container">
        <h1>My profile</h1>
        {error && <p className="auth-error" role="alert">{error}</p>}
        {!names && !error && <p role="status">Loading your profile...</p>}
        {names && (
          <form className="data-card profile-form" onSubmit={save}>
            <label>First name
              <input name="firstName" autoComplete="given-name" value={names.firstName}
                onChange={edit} disabled={saving} maxLength={120} />
            </label>
            <label>Last name
              <input name="lastName" autoComplete="family-name" value={names.lastName}
                onChange={edit} disabled={saving} maxLength={120} />
            </label>
            <button className="auth-button auth-button--primary" type="submit"
              disabled={saving || !Object.keys(changes).length}>
              {saving ? 'Saving...' : 'Save changes'}
            </button>
            {saved && <span role="status">Changes saved.</span>}
          </form>
        )}
      </div>
    </main>
  )
}
