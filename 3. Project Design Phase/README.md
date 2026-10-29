# Phase 3 — Project Design

## Architecture

```text
Traveler's browser
  └─ React 18 + Vite + React Router
       ├─ pages and reusable components
       └─ frontend/src/services/api.js
            └─ JSON HTTP requests + bearer access token
                 └─ FastAPI application
                      ├─ /auth routes → authentication service
                      ├─ /trips routes → trip and itinerary services
                      ├─ AI orchestrator → Groq, Ollama, or local generator
                      └─ Supabase service-role client when configured
                           └─ Supabase Postgres
```

The backend also has process-memory fallbacks for development when Supabase is not configured. The frontend maintains a per-user local-storage cache of saved trips to support quicker rendering and offline fallbacks in selected operations. The browser cache is not the authoritative persistent database.

## Main components

| Component | Responsibility |
|---|---|
| `frontend/src/App.jsx` | Route selection, authentication gating, and transient generated-itinerary state. |
| `frontend/src/pages/` | Home, create-trip, saved-trip list, trip detail, and account screens. |
| `frontend/src/components/` | Trip form and itinerary display. |
| `frontend/src/services/api.js` | API requests, bearer headers, session storage, and saved-trip cache. |
| `backend/app/main.py` | FastAPI setup, runtime configuration, CORS, routers, root and health endpoints. |
| `backend/app/routers/` and `backend/app/routes/` | Authentication router and trip endpoint implementation (the trip router module re-exports route handlers). |
| `backend/app/schemas/` | Pydantic request and response models. |
| `backend/app/services/` | Authentication, trip persistence, itinerary persistence, AI generation, and history logging. |
| `backend/app/db/` and `backend/schema.sql` | Supabase clients and database schema. |

## Key data entities

- **User:** UUID, normalized email, name, password hash, timestamps.
- **Trip:** UUID, owning user UUID, destination, dates, preference JSON, timestamps.
- **Itinerary day:** trip UUID, day number, title, activities JSON, notes, timestamps.
- **Preference:** user UUID and default style, interests, budget, currency, pace, and dietary requirements (schema exists; a complete preferences API is not currently wired into the frontend flow).
- **History:** user UUID, optional trip UUID, action, JSON details, timestamp.
- **Saved place:** table exists in SQL; a saved-place application flow is not currently present in the frontend/API.

The database schema enables row-level security and removes permissive public policies. The application accesses Supabase through a backend-only service-role client and enforces user ownership in application services; the service-role key must remain secret.

## API design

| Method | Path | Purpose | Auth |
|---|---|---|---|
| `GET` | `/` | Basic API-running response. | No |
| `GET` | `/health` | Health-check response. | No |
| `POST` | `/auth/register` | Create account and issue access token. | No |
| `POST` | `/auth/login` | Verify credentials and issue access token. | No |
| `GET` | `/auth/me` | Return the current user's profile. | Yes |
| `POST` | `/trips/plan` | Generate an itinerary without persisting it. | Yes |
| `POST` | `/trips/create` | Save supplied itinerary or generate and save a trip. | Yes |
| `GET` | `/trips` | List current user's trips. | Yes |
| `GET` | `/trips/{trip_id}` | Return a trip and its itinerary days. | Yes |
| `PATCH` | `/trips/{trip_id}` | Update trip fields and optionally itinerary. | Yes |
| `DELETE` | `/trips/{trip_id}` | Delete a trip. | Yes |
| `POST` | `/trips/regenerate-day` | Return a replacement day based on preferences and feedback. | Yes |

API docs are available at `/docs` outside production; production configuration disables docs and OpenAPI routes.

## Itinerary generation design

The AI service builds a prompt from trip inputs. It can call Groq or an explicitly configured Ollama endpoint and parses the response into Pydantic models. If remote generation fails, the orchestrator uses local curated destination data and procedural activity generation. The local day-regeneration method currently returns a structured template based on the supplied style, feedback, and budget; it should not be described as guaranteed to call an LLM.

## Design decisions and constraints

- Use JSON HTTP APIs between frontend and backend.
- Use HS256 signed access tokens, with expiration configured by environment.
- Store trip preferences as JSONB for flexible trip-specific inputs.
- Keep provider credentials and Supabase service-role access server-side.
- Treat share URLs as navigable trip-detail URLs that still require authentication; they are not anonymous public links.
