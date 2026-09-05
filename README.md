# ParkSpot

## Backend

### Run with Docker

Start the FastAPI application, PostgreSQL, Redis, and the Celery worker. The API
container applies all Alembic migrations before starting:

```bash
docker compose up --build
```

The API documentation is available at <http://127.0.0.1:8000/docs> and PostgreSQL
at `localhost:5434` (database/user/password: `parkspot`). Database data is kept
in the `postgres_data` Docker volume.

To run only PostgreSQL for local backend development:

```bash
docker compose up -d db
```

### Run locally

Install the dependencies and start the API with
[uv](https://docs.astral.sh/uv/):

```bash
cd backend
uv sync
uv run alembic upgrade head
uv run uvicorn app.core.main:app --reload
```

Use `GET /parking-lots` to retrieve all parking lots with only their IDs and
names. Use `GET /parking-lots/{parking_lot_id}` to retrieve a parking lot with
its parking spots and their latest statuses.

Create future schema migrations from model changes with:

```bash
cd backend
uv run alembic revision --autogenerate -m "describe the change"
uv run alembic upgrade head
```

Seed the default statuses and a 10-slot parking lot after applying migrations:

```bash
psql postgresql://parkspot:parkspot@localhost:5434/parkspot -f backend/seed.sql
```
