# Personalized Travel Itinerary Planner

A SkillWallet capstone project that helps users plan a trip and generate a simple personalized itinerary.

**Stack:** React (frontend), FastAPI with Python (backend), Supabase (database).

## Project structure

```
frontend/   # Website the user sees (React + Vite)
backend/    # API that talks to Supabase (FastAPI)
```

- `frontend/src/components/` — reusable UI pieces (buttons, cards, forms)
- `frontend/src/pages/` — full screens (Home, Planner, Saved Itinerary)
- `frontend/src/services/` — functions that call the FastAPI backend
- `backend/app/routers/` — API endpoints such as `/trips`
- `backend/app/models/` — request and response shapes
- `backend/app/services/` — logic that talks to Supabase
- `backend/app/db/` — shared Supabase public and service-role clients

## Setup

You will need Node.js, Python 3, and a free [Supabase](https://supabase.com) project.

### Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

Set `SUPABASE_URL`, `SUPABASE_KEY`, and `SUPABASE_SERVICE_ROLE_KEY` in `backend/.env`. The service-role key is used only by the backend after it verifies the user's signed token and ownership. Never put it in a frontend variable or commit it. Run `backend/schema.sql` in the Supabase SQL Editor to create tables and remove permissive public policies.

Generate a development JWT secret with `python -c "import secrets; print(secrets.token_urlsafe(32))"` and set it as `SECRET_KEY`. Configure `AI_PROVIDER=groq` with `GROQ_API_KEY`, or `AI_PROVIDER=ollama` with an available Ollama host and `OLLAMA_MODEL`. Hugging Face credentials can be stored in configuration, but a Hugging Face provider adapter is not implemented yet.

```bash
uvicorn app.main:app --reload
```

The API runs at `http://127.0.0.1:8000`. Docs: `http://127.0.0.1:8000/docs`.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

The website runs at `http://localhost:5173`.

## Reliability checks

Run the backend's offline scenario and security checks from `backend/`:

```bash
python -m unittest discover -s tests -v
```

Create a production frontend bundle from `frontend/` with `npm run build`.

## Production container deployment

Copy `backend/.env.example` to `backend/.env`, replace every placeholder with newly generated credentials, set `ENVIRONMENT=production`, `DEBUG=False`, `FRONTEND_URL` to the deployed HTTPS origin, and choose a supported AI provider. Apply the SQL schema to Supabase, then run `docker compose up --build -d` from the project root. The app is served on port 8080 by default; set `WEB_PORT` to change it. Put a TLS-enabled reverse proxy in front of the published port for public hosting. The backend is only reachable inside the Compose network.

Production startup rejects the development JWT secret, debug mode, missing Supabase service-role credentials, and localhost CORS origins. API docs are disabled in production. Keep `.env` values in the deployment platform's secret store when deploying outside Docker Compose.

## Notes

- Copy `backend/.env.example` to `backend/.env`. Never commit real keys.
- `.env`, `node_modules`, and Python `venv` are listed in `.gitignore`.
- Without Supabase credentials, trip storage falls back to process memory for development and is cleared when the backend restarts.
- Open **My Trips** in the app to view, edit, and delete saved trips. Each saved trip has a detail page with shareable summaries, a copied link, Markdown and JSON downloads, and day regeneration.
- Authentication uses signed, expiring HS256 tokens. The demo identity is available only in development; production requires registration or sign-in.
