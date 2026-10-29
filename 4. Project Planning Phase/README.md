# Phase 4 — Project Planning

## Delivery objective

Deliver a usable full-stack itinerary planner with account access, itinerary generation, saved-trip management, and a deployable configuration.

## Work breakdown

| Workstream | Planned outcome | Repository evidence |
|---|---|---|
| Product definition | Define traveler inputs, primary workflow, and feature boundary. | README, trip schemas, and UI flow. |
| Requirements and data | Specify API payloads, ownership, and persistence entities. | Pydantic schemas and `backend/schema.sql`. |
| UX and frontend | Build planner, account, trip list, and trip detail pages. | `frontend/src/pages/` and `components/`. |
| Backend API | Implement authentication, planning, and trip CRUD routes. | `backend/app/routers/`, `routes/`, and services. |
| AI integration | Add provider abstraction and local generation fallback. | `backend/app/services/ai.py`, prompts, and destination data. |
| Reliability/security | Add configuration checks and offline scenario checks. | `backend/tests/test_reliability.py`, auth utilities, runtime config. |
| Deployment | Provide container, Render, and Vercel deployment configuration. | Dockerfiles, `docker-compose.yml`, `render.yaml`, `frontend/vercel.json`. |
| Documentation/demo | Explain setup, system behavior, and a reproducible demonstration. | This eight-phase documentation set and root README. |

## Suggested implementation sequence

1. Confirm problem, user flow, and trip inputs.
2. Define schemas, database tables, and authenticated API boundaries.
3. Implement backend persistence and account flows.
4. Implement generation provider and local fallback.
5. Build frontend routes and connect them to the API.
6. Validate core scenarios and production configuration.
7. Configure and document deployment.
8. Prepare a demonstration using a test account and representative itinerary.

This sequence is a sensible project plan inferred from the current architecture, not a record of historical sprint dates. No dates, effort estimates, or completed sprint history were present in the local source inspected for these documents.

## Backlog

### Delivered in current source

- Registration, login, signed-token authentication, and profile lookup.
- Itinerary generation with Groq/Ollama selection and local fallback.
- Supabase persistence with in-memory development behavior.
- Saved-trip list, detail, editing, deletion, and day regeneration.
- Copy/share/Markdown export controls on itinerary details.
- Local, Docker Compose, Render, and Vercel setup configuration.

### Recommended future backlog

- Add strict date parsing and start/end ordering validation.
- Add automated frontend component/API tests and end-to-end coverage.
- Add observability around provider latency, fallback rate, and persistence errors.
- Add a clear shared-trip authorization model before making links public.
- Add verified map/routing, opening-hour, weather, and price sources if product scope requires them.
- Add account lifecycle capabilities such as password reset and email verification.

## Risks and mitigations

| Risk | Mitigation or current constraint |
|---|---|
| AI output may be incomplete or unsuitable for a real trip. | Validate structured output and use local fallback; make clear that suggestions require traveler verification. |
| Provider/network outage. | Local itinerary generation keeps a planning path available. |
| In-memory fallback loses data on restart. | Use configured Supabase for persistent deployments; clearly treat memory mode as development-only. |
| Service-role key exposure would grant broad database access. | Keep credentials in backend/deployment secrets and never in `VITE_` frontend variables. |
| Share URL may be mistaken for a public itinerary. | Authentication protects trip routes; explain that recipients need an authenticated account with access. |
| Feature expectations exceed source behavior. | Separate implemented functionality from future ideas in project reports and demos. |

## Completion checklist

- Core flow is usable from account creation through saved itinerary detail.
- Backend and frontend configuration examples are documented without real secrets.
- Supabase schema and deployment settings match the deployed environment.
- Reliability checks and production build are run by the project owner before release.
- Demo scenarios and known limitations are stated accurately.
