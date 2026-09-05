import { Link, NavLink, Route, Routes } from 'react-router-dom'
import ParkingLotsPage from './pages/ParkingLotsPage.jsx'
import ParkingLotDetailsPage from './pages/ParkingLotDetailsPage.jsx'

function App() {
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

          <nav aria-label="Main navigation">
            <NavLink
              className={({ isActive }) =>
                `nav-link${isActive ? ' nav-link--active' : ''}`
              }
              to="/"
              end
            >
              Parking lots
            </NavLink>
          </nav>
        </div>
      </header>

      <Routes>
        <Route path="/" element={<ParkingLotsPage />} />
        <Route
          path="/parking-lots/:parkingLotId"
          element={<ParkingLotDetailsPage />}
        />
      </Routes>

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
