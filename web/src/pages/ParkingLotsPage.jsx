import { useEffect, useState } from 'react'
import { useAuth0 } from '@auth0/auth0-react'
import { getParkingLots } from '../api/parkingLots.js'
import ParkingLotTable from '../components/ParkingLotTable.jsx'
import ParkingChat from '../components/ParkingChat.jsx'

function ParkingLotsPage() {
  const { getAccessTokenSilently } = useAuth0()
  const [parkingLots, setParkingLots] = useState([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    const controller = new AbortController()

    async function loadParkingLots() {
      try {
        const accessToken = await getAccessTokenSilently()
        if (controller.signal.aborted) return
        const data = await getParkingLots({ signal: controller.signal, accessToken })
        setParkingLots(data)
      } catch (requestError) {
        if (requestError.name !== 'AbortError') {
          setError('Could not load parking lots.')
        }
      } finally {
        if (!controller.signal.aborted) {
          setIsLoading(false)
        }
      }
    }

    loadParkingLots()

    return () => controller.abort()
  }, [getAccessTokenSilently])

  const locationLabel = `${parkingLots.length} ${
    parkingLots.length === 1 ? 'location' : 'locations'
  }`

  return (
    <main className="main-content">
      <div className="container">
        <section className="page-intro" aria-labelledby="page-title">
          <div>
            <p className="eyebrow">Parking overview</p>
            <h1 id="page-title">Parking lots</h1>
            <p className="page-intro__description">
              See every parking location connected to ParkSpot in one place.
            </p>
          </div>

          <div className="location-count" aria-live="polite">
            <span className="location-count__dot" aria-hidden="true" />
            {isLoading ? 'Loading locations' : locationLabel}
          </div>
        </section>

        <section className="data-card" aria-labelledby="locations-title">
          <div className="data-card__header">
            <div>
              <h2 id="locations-title">All locations</h2>
            </div>
            <span className="api-badge">
              <span aria-hidden="true" />
              Live API
            </span>
          </div>

          <div className="data-card__body">
            {isLoading && (
              <div className="message-state" role="status">
                <span className="spinner" aria-hidden="true" />
                <p>Loading parking lots...</p>
              </div>
            )}

            {error && (
              <div className="message-state message-state--error" role="alert">
                <span className="message-state__icon" aria-hidden="true">
                  !
                </span>
                <div>
                  <strong>Unable to load parking lots</strong>
                  <p>{error} Check that the API is running and try again.</p>
                </div>
              </div>
            )}

            {!isLoading && !error && parkingLots.length === 0 && (
              <div className="message-state">
                <span className="message-state__icon" aria-hidden="true">
                  P
                </span>
                <div>
                  <strong>No parking lots found</strong>
                  <p>New locations will appear here when they are added.</p>
                </div>
              </div>
            )}

            {!isLoading && !error && parkingLots.length > 0 && (
              <ParkingLotTable parkingLots={parkingLots} />
            )}
          </div>
        </section>
        <ParkingChat />
      </div>
    </main>
  )
}

export default ParkingLotsPage
