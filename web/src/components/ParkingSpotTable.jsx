export default function ParkingSpotTable({ spots }) {
  return (
    <div className="table-wrapper">
      <table>
        <caption>Parking spots</caption>
        <thead>
          <tr>
            <th scope="col">Number</th>
            <th scope="col">Level</th>
            <th scope="col">Status</th>
          </tr>
        </thead>
        <tbody>
          {spots.map((spot) => (
            <tr key={spot.id}>
              <td>{spot.number}</td>
              <td>{spot.level ?? 'Unknown'}</td>
              <td>
                <span className="spot-status" data-status={spot.lastStatus?.slug}>
                  {spot.lastStatus?.name ?? 'Unknown'}
                </span>
              </td>
            </tr>
          ))}
          {spots.length === 0 && (
            <tr><td colSpan={3}>No parking spots found.</td></tr>
          )}
        </tbody>
      </table>
    </div>
  )
}
