import { Link, useLocation, useParams } from 'react-router-dom'

function ParkingLotDetailsPage() {
  const { parkingLotId } = useParams()
  const { state } = useLocation()
  const parkingLot = state?.parkingLot
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
          <p className="page-intro__description">
            This page is ready for detailed parking-lot information.
          </p>
        </section>

        <section className="details-card">
          <span className="details-card__icon" aria-hidden="true">
            P
          </span>
          <div>
            <h2>Parking lot details</h2>
            <p>
              Parking spots, capacity, and availability can be added here next.
            </p>
          </div>
        </section>
      </div>
    </main>
  )
}

export default ParkingLotDetailsPage
