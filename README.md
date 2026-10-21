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

Open `.env` and paste your Supabase URL and key. Then start the API:

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

## Notes

- Copy `backend/.env.example` to `backend/.env`. Never commit real keys.
- `.env`, `node_modules`, and Python `venv` are listed in `.gitignore`.
