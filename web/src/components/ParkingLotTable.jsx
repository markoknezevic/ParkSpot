function ParkingLotTable({ parkingLots }) {
  return (
    <div className="table-wrapper">
      <table>
        <caption>All parking lots</caption>
        <thead>
          <tr>
            <th scope="col">Parking lot</th>
            <th scope="col">Location ID</th>
          </tr>
        </thead>
        <tbody>
          {parkingLots.map((parkingLot) => (
            <tr key={parkingLot.id}>
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
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export default ParkingLotTable
