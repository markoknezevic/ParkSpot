# ParkSpot

ParkSpot is a web application for viewing parking lots, their levels, and individual parking spots. It tracks spot availability using the latest recorded status, helping users find free spaces.

The project includes an LLM chatbot integration that interprets natural-language parking questions, queries counts of free, taken and pending spots by parking lot and level, and uses those results to generate an answer.

## Technologies

- **React, Vite, and React Router** — frontend interface and navigation.
- **Python and FastAPI** — backend API.
- **OpenAI API** — LLM chatbot integration with function calling.
- **PostgreSQL** — storage for parking lots, spots, status history, and users.
- **SQLAlchemy and Alembic** — database access and schema migrations.
- **Pydantic** — request and response validation.
- **Celery and Redis** — background task processing, with Redis as the message broker.
- **Auth0** — user authentication.
- **Docker Compose** — local backend services and infrastructure.
- **uv** — Python dependency management.
