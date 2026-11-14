import { Link, useLocation, useParams } from 'react-router-dom'

import { useEffect, useState } from 'react'
import { useAuth0 } from '@auth0/auth0-react'
import { getParkingLot } from '../api/parkingLots.js'
import ParkingSpotTable from '../components/ParkingSpotTable.jsx'

function ParkingLotDetailsPage() {
  const { parkingLotId } = useParams()
  const { state } = useLocation()
  return <ParkingLotDetails key={parkingLotId} parkingLotId={parkingLotId} summary={state?.parkingLot} />
}

function ParkingLotDetails({ parkingLotId, summary }) {
  const { getAccessTokenSilently } = useAuth0()
  const [details, setDetails] = useState(null)
  const [failed, setFailed] = useState(false)

  useEffect(() => {
    const controller = new AbortController()
    async function loadDetails() {
      try {
        const accessToken = await getAccessTokenSilently()
        const lot = await getParkingLot(parkingLotId, { accessToken, signal: controller.signal })
        if (!controller.signal.aborted) setDetails(lot)
      } catch {
        if (!controller.signal.aborted) setFailed(true)
      }
    }
    loadDetails()
    return () => controller.abort()
  }, [parkingLotId, getAccessTokenSilently])

  const parkingLot = details ?? summary
  const parkingLotName = parkingLot?.name ?? `Parking lot #${parkingLotId}`

  return (
    <main className="main-content">
      <div className="container">
        <Link className="back-link" to="/">
          <span aria-hidden="true">←</span>
          Back to parking lots
        </Link>

        <section className="details-intro" aria-labelledby="details-title">
          <p className="eyebrow">Location #{parkingLotId}</p>
          <h1 id="details-title">{parkingLotName}</h1>
        </section>

        <section className="data-card" aria-labelledby="spots-title">
          <div className="data-card__header">
            <h2 id="spots-title">Parking spots</h2>
          </div>
          {failed ? (
            <p className="message-state" role="alert">Could not load parking spots.</p>
          ) : details ? (
            <ParkingSpotTable spots={details.parkingSpots} />
          ) : (
            <p className="message-state" role="status">Loading parking spots…</p>
          )}
        </section>
      </div>
    </main>
  )
}

export default ParkingLotDetailsPage
