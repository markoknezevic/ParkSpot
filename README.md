# ParkSpot

## Backend

Install the dependencies and start the API with
[uv](https://docs.astral.sh/uv/):

```bash
cd backend
uv sync
uv run uvicorn app.main:app --reload
```

Open <http://127.0.0.1:8000/> to receive:

```json
{"message": "Hello World"}
```
