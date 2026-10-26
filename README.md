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
export AUTH0_DOMAIN=dev-xra3gs5hmyhr87je.us.auth0.com
export AUTH0_AUDIENCE=https://parkspot-api
uv run alembic upgrade head
uv run uvicorn app.core.main:app --reload
```

Use `GET /parking-lots` to retrieve all parking lots with only their IDs and
names. Use `GET /parking-lots/{parking_lot_id}` to retrieve a parking lot with
its parking spots and their latest statuses.

Both endpoints require an Auth0 user access token in `Authorization: Bearer ...`.
In Auth0, register an API with identifier `https://parkspot-api` and RS256 signing,
or set `AUTH0_AUDIENCE` to your existing API identifier. The frontend's
`VITE_AUTH0_AUDIENCE` must match. Docker Compose uses these same environment
variables with the defaults shown above. Restart the frontend after env changes.

`require_registered_user` validates the token and finds or creates a local user
by issuer and subject. It does not link existing accounts by email or grant roles.
Profile fields remain empty until collected separately. The profile migration's
downgrade requires filling missing profile fields first.

Run backend authentication tests without Auth0 or PostgreSQL:

```bash
cd backend
.venv/bin/python -m unittest discover -s tests -v
```

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
