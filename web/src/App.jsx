import ParkingLotsPage from './pages/ParkingLotsPage.jsx'

function App() {
  return (
    <div className="app-shell">
      <header className="site-header">
        <div className="container site-header__content">
          <a className="brand" href="/" aria-label="ParkSpot home">
            <span className="brand__mark" aria-hidden="true">
              P
            </span>
            <span>ParkSpot</span>
          </a>

          <nav aria-label="Main navigation">
            <a className="nav-link nav-link--active" href="/">
              Parking lots
            </a>
          </nav>
        </div>
      </header>

      <ParkingLotsPage />

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
