# Personalized Travel Itinerary Planner

A SkillWallet capstone project that helps users plan a trip and generate a simple personalized itinerary.

**Stack:** React (frontend), FastAPI with Python (backend), Supabase (database).

## Eight-phase project documentation

The project documentation is organized into eight phases, from ideation and requirements through development, testing, and demonstration. Start with the [documentation index](7.%20Project%20Documentation/README.md), or open a phase directly:

1. [Brainstorming and Ideation](1.%20Brainstorming%20and%20Ideation/README.md)
2. [Requirement Analysis](2.%20Requirement%20Analysis/README.md)
3. [Project Design](3.%20Project%20Design%20Phase/README.md)
4. [Project Planning](4.%20Project%20Planning%20Phase/README.md)
5. [Project Development](5.%20Project%20Development%20Phase/README.md)
6. [Project Testing](6.%20Project%20Testing/README.md)
7. [Project Documentation](7.%20Project%20Documentation/README.md)
8. [Project Demonstration](8.%20Project%20Demonstration/README.md)

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

## Deploy the backend to Render

The root-level `render.yaml` configures a Python web service that builds from `backend/`, installs `backend/requirements.txt`, starts FastAPI with Gunicorn and Uvicorn workers, and checks `/health`. In Render, create a Blueprint from this GitHub repository and select `render.yaml` (or create a Python web service with the same settings). The service deploys from `main` when automatic deploys are enabled.

Add these values in the Render service's **Environment** settings. Keep secret values in Render; do not paste a real `.env` file into Git or a public issue.

| Variable | Value |
| --- | --- |
| `ENVIRONMENT` | `production` |
| `DEBUG` | `false` |
| `AI_PROVIDER` | `groq` |
| `SUPABASE_URL` | Your Supabase project URL |
| `SUPABASE_SERVICE_ROLE_KEY` | Your Supabase service-role key |
| `SUPABASE_KEY` | Your Supabase anon/public key, if used |
| `SECRET_KEY` | A unique random secret, at least 32 characters |
| `GROQ_API_KEY` | Your Groq API key when using the Groq provider |
| `FRONTEND_URL` | The deployed frontend's HTTPS origin, such as `https://your-site.example` |

Render supplies `PORT` automatically. Do not set it manually. `FRONTEND_URL` must be updated to the actual frontend origin before the service can start in production. Apply `backend/schema.sql` to the Supabase project before using account and trip storage. After deployment, verify the service's `/health` endpoint returns `{"status":"ok"}` and configure the frontend's `VITE_API_BASE_URL` to the Render service URL.

## Deploy the frontend to Vercel

Import this GitHub repository as a Vercel project, set the **Root Directory** to `frontend`, and use the Vite framework preset. The build command is `npm run build`, the output directory is `dist`, and the install command is `npm install` (Vercel can also detect these from `frontend/package.json`).

Set `VITE_API_BASE_URL` in the Vercel project's environment variables to the Render backend's base URL, for example `https://your-service.onrender.com`. Do not append `/api`: the frontend calls `/trips` and `/auth` directly, and the backend does not mount those routes under an `/api` prefix. Redeploy the Vercel project after changing build environment variables.

After Vercel assigns the production domain, set Render's `FRONTEND_URL` to that HTTPS origin (for example, `https://your-project.vercel.app`, without a path). This enables browser requests through the backend's CORS policy. If you use additional Vercel domains, list their origins comma-separated. Then redeploy the backend. The `frontend/vercel.json` rewrite serves the React app for direct navigation to routes such as `/trips/123`.

## Notes

- Copy `backend/.env.example` to `backend/.env`. Never commit real keys.
- `.env`, `node_modules`, and Python `venv` are listed in `.gitignore`.
- Without Supabase credentials, trip storage falls back to process memory for development and is cleared when the backend restarts.
- Open **My Trips** in the app to view, update trip details, and delete saved trips. Each saved trip has a rendered detail page with shareable summaries, a copied link, a readable Markdown download, and day regeneration.
- Authentication uses signed, expiring HS256 tokens. All user-scoped API requests require a signed-in account. Without Supabase configured, development accounts and trips are kept in process memory and reset when the backend restarts.

## Conclusion

The Personalized Travel Itinerary Planner demonstrates how generative AI can work with a modern full-stack application to create tailored travel experiences. Its React interface gathers trip preferences, while the FastAPI backend uses structured prompts to generate day-by-day itineraries shaped by destination, dates, budget, travel style, and interests.

The application extends beyond itinerary generation with account authentication, trip saving and management, shareable summaries, and export options. Supabase provides persistent storage when configured, and the modular backend, environment-based configuration, automated checks, and Render and Vercel deployment setup prepare the project for cloud hosting and future development. Potential next steps include real-time collaboration, richer recommendations, and additional AI providers.
