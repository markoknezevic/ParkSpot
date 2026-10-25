import { useState } from 'react'
import { useAuth0 } from '@auth0/auth0-react'
import { Link, NavLink, Route, Routes } from 'react-router-dom'
import ParkingLotsPage from './pages/ParkingLotsPage.jsx'
import ParkingLotDetailsPage from './pages/ParkingLotDetailsPage.jsx'

function App() {
  const { isLoading, isAuthenticated, error, loginWithRedirect, logout, user } = useAuth0()
  const [actionError, setActionError] = useState(null)
  const [isRedirecting, setIsRedirecting] = useState(false)

  async function handleAuthAction(action) {
    setActionError(null)
    setIsRedirecting(true)
    try {
      await action()
    } catch (authError) {
      setActionError(authError.message || 'Unable to connect to sign-in. Please try again.')
    } finally {
      setIsRedirecting(false)
    }
  }

  const authError = actionError || error?.message

  return (
    <div className="app-shell">
      <header className="site-header">
        <div className="container site-header__content">
          <Link className="brand" to="/" aria-label="ParkSpot home">
            <span className="brand__mark" aria-hidden="true">
              P
            </span>
            <span>ParkSpot</span>
          </Link>

          {isAuthenticated && <nav aria-label="Main navigation">
            <NavLink
              className={({ isActive }) =>
                `nav-link${isActive ? ' nav-link--active' : ''}`
              }
              to="/"
              end
            >
              Parking lots
            </NavLink>
          </nav>}

          {!isLoading && isAuthenticated && (
            <div className="auth-actions">
              <span className="auth-user">{user?.email || user?.name || 'Signed in'}</span>
              <button
                className="auth-button"
                disabled={isRedirecting}
                onClick={() => handleAuthAction(() => logout({
                  logoutParams: { returnTo: window.location.origin },
                }))}
              >
                Log out
              </button>
            </div>
          )}
        </div>
      </header>

      {authError && (
        <div className="container auth-error" role="alert">
          Authentication error: {authError}
        </div>
      )}

      {isLoading ? (
        <main className="main-content">
          <div className="message-state" role="status">
            <span className="spinner" aria-hidden="true" />
            <p>Checking your session...</p>
          </div>
        </main>
      ) : isAuthenticated ? <Routes>
        <Route path="/" element={<ParkingLotsPage />} />
        <Route
          path="/parking-lots/:parkingLotId"
          element={<ParkingLotDetailsPage />}
        />
      </Routes> : (
        <main className="main-content">
          <section className="container" aria-labelledby="welcome-title">
            <p className="eyebrow">Welcome to ParkSpot</p>
            <h1 id="welcome-title">Your parking, in one place.</h1>
            <p className="page-intro__description">
              Log in or create an account to view parking locations.
            </p>
            <div className="auth-actions auth-actions--welcome">
              <button
                className="auth-button auth-button--primary"
                disabled={isRedirecting}
                onClick={() => handleAuthAction(() => loginWithRedirect())}
              >
                Log in
              </button>
              <button
                className="auth-button"
                disabled={isRedirecting}
                onClick={() => handleAuthAction(() => loginWithRedirect({
                  authorizationParams: { screen_hint: 'signup' },
                }))}
              >
                Sign up
              </button>
              {isRedirecting && <span role="status">Redirecting...</span>}
            </div>
          </section>
        </main>
      )}

      <footer className="site-footer">
        <div className="container site-footer__content">
          <span>© {new Date().getFullYear()} ParkSpot</span>
          <span>Parking made simple.</span>
        </div>
      </footer>
    </div>
  )
}

export default App
