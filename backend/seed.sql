-- Seed the ParkSpot database with the default statuses and one parking lot.
-- Run this after applying the Alembic migrations.

BEGIN;

INSERT INTO spot_status (name, slug)
VALUES
    ('Free', 'free'),
    ('Pennding', 'pennding'),
    ('Taken', 'taken')
ON CONFLICT (name) DO UPDATE
SET
    slug = EXCLUDED.slug,
    updated_at = NOW();

WITH inserted_lot AS (
    INSERT INTO parking_lots (name)
    SELECT 'Main Parking Lot'
    WHERE NOT EXISTS (
        SELECT 1
        FROM parking_lots
        WHERE name = 'Main Parking Lot'
    )
    RETURNING id
), selected_lot AS (
    SELECT id
    FROM (
        SELECT id FROM inserted_lot
        UNION ALL
        SELECT id
        FROM parking_lots
        WHERE name = 'Main Parking Lot'
    ) AS matching_lots
    ORDER BY id
    LIMIT 1
)
INSERT INTO parking_spots (number, parking_lot_id)
SELECT slot_number, selected_lot.id
FROM selected_lot
CROSS JOIN generate_series(1, 10) AS slot_number
ON CONFLICT (parking_lot_id, number) DO NOTHING;

-- The newest history entry represents a parking spot's current status.
-- Add a Free entry only when Free is not already the current status.
WITH selected_lot AS (
    SELECT id
    FROM parking_lots
    WHERE name = 'Main Parking Lot'
    ORDER BY id
    LIMIT 1
), free_status AS (
    SELECT id
    FROM spot_status
    WHERE name = 'Free'
)
INSERT INTO parking_spot_status (parking_spot_id, spot_status_id)
SELECT parking_spots.id, free_status.id
FROM parking_spots
JOIN selected_lot
    ON selected_lot.id = parking_spots.parking_lot_id
CROSS JOIN free_status
WHERE parking_spots.number BETWEEN 1 AND 10
  AND COALESCE(
      (
          SELECT history.spot_status_id
          FROM parking_spot_status AS history
          WHERE history.parking_spot_id = parking_spots.id
          ORDER BY history.created_at DESC, history.id DESC
          LIMIT 1
      ),
      0
  ) <> free_status.id;

COMMIT;
