import { useNavigate } from 'react-router-dom'

function ParkingLotTable({ parkingLots }) {
  const navigate = useNavigate()

  function viewParkingLot(parkingLot) {
    navigate(`/parking-lots/${parkingLot.id}`, {
      state: { parkingLot },
    })
  }

  return (
    <div className="table-wrapper">
      <table>
        <caption>All parking lots</caption>
        <thead>
          <tr>
            <th scope="col">Parking lot</th>
            <th scope="col">Location ID</th>
            <th className="action-heading" scope="col">
              Action
            </th>
          </tr>
        </thead>
        <tbody>
          {parkingLots.map((parkingLot) => (
            <tr
              className="clickable-row"
              key={parkingLot.id}
              onClick={() => viewParkingLot(parkingLot)}
              onKeyDown={(event) => {
                if (
                  event.target === event.currentTarget &&
                  (event.key === 'Enter' || event.key === ' ')
                ) {
                  event.preventDefault()
                  viewParkingLot(parkingLot)
                }
              }}
              tabIndex="0"
            >
              <td>
                <div className="parking-lot-name">
                  <span className="parking-lot-name__icon" aria-hidden="true">
                    P
                  </span>
                  <span>
                    <strong>{parkingLot.name}</strong>
                    <small>ParkSpot location</small>
                  </span>
                </div>
              </td>
              <td>
                <span className="location-id">#{parkingLot.id}</span>
              </td>
              <td className="action-cell">
                <button
                  className="details-button"
                  type="button"
                  aria-label={`View ${parkingLot.name}`}
                  onClick={(event) => {
                    event.stopPropagation()
                    viewParkingLot(parkingLot)
                  }}
                >
                  View details
                  <span aria-hidden="true">→</span>
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export default ParkingLotTable
