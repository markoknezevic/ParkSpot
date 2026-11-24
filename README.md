# ParkSpot

ParkSpot is a full-stack parking application that brings together parking availability, a conversational assistant, and semantic search over parking rules. It demonstrates modular backend development, relational and vector data storage, authentication, and AI integration in a single project.

## What it does

- **Parking overview:** Browse parking lots, levels, and individual spaces, with availability based on each space’s latest recorded status.
- **Conversational parking assistant:** Ask questions about availability in natural language. The assistant selects a backend function, retrieves parking counts from the database, and uses those results to compose its answer.
- **Searchable parking knowledge:** Store general parking rules and find relevant documents by meaning, including when a question uses different wording from the original text.
- **User accounts:** Sign in through Auth0 and manage a user profile.

## Technologies and their roles

| Technology | How ParkSpot uses it |
| --- | --- |
| **React** | Builds the parking views, user profile, and chat interface with reusable components. |
| **Vite and React Router** | Provide frontend development tooling, production builds, and navigation between pages. |
| **Python and FastAPI** | Implement the backend, with dependency injection connecting routes, business logic, and database access. |
| **Pydantic** | Validates incoming data and defines structured response schemas. |
| **PostgreSQL** | Stores parking lots, spaces, status history, users, and parking documentation. |
| **SQLAlchemy** | Maps database records to Python models and builds queries, including availability counts based on the latest status of each space. |
| **Alembic** | Manages database schema changes through versioned migrations. |
| **pgvector** | Stores document embeddings alongside their text and supports similarity searches within PostgreSQL. |
| **FastEmbed and ONNX Runtime** | Run the English `BAAI/bge-small-en-v1.5` embedding model locally on CPU, generating vectors for documents and search questions. |
| **OpenAI API** | Powers the conversational assistant’s function selection and responses grounded in retrieved parking availability data. |
| **Auth0** | Handles frontend sign-in and backend access-token validation, with identities linked to local user records. |
| **Celery and Redis** | Provide background task infrastructure, currently demonstrated through a scheduled logging task. Redis acts as the message broker. |
| **Docker and Docker Compose** | Package the backend and coordinate PostgreSQL, Redis, the API, and the background worker. The API image includes the local embedding model. |
| **uv** | Manages Python dependencies and the lockfile used to build the backend environment. |

## Architecture

The backend is organized into domain modules for parking, users, LLM integration, parking knowledge, and background jobs. Each feature uses separate layers for HTTP handling, business logic, and persistence, making responsibilities explicit and allowing modules to evolve independently.

The parking assistant uses function calling to obtain structured availability data before generating a response. This connects natural-language questions to application logic while keeping database queries in the backend.

The knowledge module generates a 384-dimensional vector from each document’s title and content, then saves the vector and text together. Search questions are embedded with the same local model, and PostgreSQL ranks matching documents by cosine similarity. After the model is downloaded during setup, embedding generation runs locally without external inference calls.

## Current scope

The conversational assistant answers availability questions using recorded parking data. The knowledge module provides document storage and semantic retrieval as the foundation for RAG; connecting those documents to chatbot-generated answers is a future step.

Availability represents the latest recorded database state. Reservations and guaranteed space availability are outside the current scope.
