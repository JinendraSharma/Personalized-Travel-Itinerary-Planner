# Phase 5 — Project Development

## Implemented application

The application is split into a React/Vite frontend and a Python/FastAPI backend. The source also contains Docker packaging and platform configuration. The top-level `server/src/config/schema.sql` is an additional schema copy; the backend setup instructions point to `backend/schema.sql`, which should be treated as the operational schema unless the duplicate is deliberately reconciled.

## Technology stack

| Layer | Technologies |
|---|---|
| Frontend | React 18, Vite 5, React Router, Framer Motion, Lucide React, CSS |
| Backend | Python, FastAPI, Pydantic, Uvicorn, Gunicorn |
| Data | Supabase Postgres; in-memory service fallback for local development |
| AI | Groq chat completions or Ollama HTTP endpoint; local curated/procedural fallback |
| Authentication | Password hashing and signed HS256 bearer tokens |
| Deployment | Docker Compose, Render backend configuration, Vercel frontend configuration |

## Source map

```text
frontend/src/
  App.jsx                 Route map and authenticated navigation
  pages/                  Home, CreateTrip, SavedTrips, TripView, Account
  components/             TripForm and ItineraryDisplay
  services/api.js         HTTP client, session handling, trip cache

backend/app/
  main.py                 FastAPI app, CORS, runtime routes
  routers/auth.py         Authentication endpoints
  routes/trips.py         Trip generation and CRUD endpoints
  schemas/schemas.py      Request and response contracts
  services/               AI, trip, auth, history, and Supabase services
  prompts/                Itinerary prompt construction
  db/                     Database client setup
backend/schema.sql        Supabase tables, indexes, and RLS setup
```

## Setup for local development

Prerequisites: Node.js/npm, Python, and (for persistent storage) a Supabase project.

### Backend

1. In `backend/`, create and activate a Python virtual environment.
2. Install `requirements.txt`.
3. Copy `backend/.env.example` to `backend/.env` and set a unique `SECRET_KEY`.
4. For persistent storage, configure Supabase URL and server-side keys, then apply `backend/schema.sql` in the Supabase SQL editor.
5. Select `AI_PROVIDER=groq` and provide `GROQ_API_KEY`, select `AI_PROVIDER=ollama` and configure Ollama, or use the local development provider.
6. Start with `uvicorn app.main:app --reload` from `backend/`.

### Frontend

1. In `frontend/`, run `npm install`.
2. Configure `VITE_API_BASE_URL` when the API is not at the development default.
3. Run `npm run dev` and open the Vite URL shown in the terminal.

Exact environment names and production checks are described in the root [README](../README.md). Never place server-only secrets in frontend environment variables.

## Persistence behavior

When Supabase credentials are configured, backend services use Supabase for accounts, trips, itinerary days, and history. Without a database client, development services keep records in process memory; those records are lost when the backend process restarts. The frontend also caches saved trips in per-user local storage and may use that cache when selected network operations fail. That browser cache does not make server-side account or trip data durable.

## Deployment configuration

- `docker-compose.yml` builds the backend and frontend containers and exposes the configured web port through the frontend container/reverse-proxy setup.
- `render.yaml` describes a Python service built from `backend/` with a health check.
- `frontend/vercel.json` supports direct navigation to frontend routes.
- The README documents setting the backend's allowed frontend origin and the frontend API base URL.

## Development status

This document records the observed source structure and setup. It does not imply a production deployment is live or that deployment credentials/configuration have been verified. Hugging Face configuration fields may exist, but a Hugging Face provider adapter is not implemented in the inspected AI service.

## Phase deliverables

- [Code-Layout, Readability and Reusability - Personalized Travel Itinerary Planner](Code-Layout%2C%20Readability%20and%20Reusability%20-%20Personalized%20Travel%20Itinerary%20Planner.pdf)
- [Coding & Solution - Personalized Travel Itinerary Planner](Coding%20%26%20Solution%20-%20Personalized%20Travel%20Itinerary%20Planner.pdf)
- [No. of Functional Features Included in the Solution - Personalized Travel Itinerary Planner](No.%20of%20Functional%20Features%20Included%20in%20the%20Solution%20-%20Personalized%20Travel%20Itinerary%20Planner.pdf)
