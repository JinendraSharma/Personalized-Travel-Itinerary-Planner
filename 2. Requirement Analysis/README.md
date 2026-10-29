# Phase 2 — Requirement Analysis

## Product goal

Let an authenticated traveler create a personalized multi-day itinerary and manage that itinerary as a saved trip.

## Scope

### In scope

- Account registration, login, profile lookup, and logout.
- Itinerary requests containing destination, dates, travel style, number of travelers, daily budget, currency, interests, pace, and dietary needs.
- Structured itinerary output organized by day and activity.
- Saving, listing, viewing, updating, and deleting trips.
- Regenerating an individual day with optional feedback.
- Copying a trip URL or summary, using native browser sharing where available, and downloading a Markdown summary.
- Supabase-backed persistence when configured, with process-memory backend fallback and browser-side trip cache behavior in the frontend.

### Out of scope in the current implementation

- Booking, payments, reservations, or verified availability.
- Live maps, routing, weather, flight, or transit integrations.
- Collaborative trip editing or public access controls for shared trip URLs.
- A user preference management API, despite preference-related database schema and data fields.
- Email verification, password reset, or refresh-token flow.

## Functional requirements

| ID | Requirement | Current implementation evidence |
|---|---|---|
| FR-01 | A visitor can register with name, email, and a password of at least eight characters. | `/auth/register`; Pydantic validation and password hashing. |
| FR-02 | A registered user can sign in and receive a signed access token. | `/auth/login`; frontend stores the bearer token in local storage. |
| FR-03 | An authenticated user can request an itinerary using trip preferences. | `POST /trips/plan`; structured request and response schemas. |
| FR-04 | A user can save a generated itinerary as a trip. | `POST /trips/create`; accepts supplied itinerary or generates one when omitted. |
| FR-05 | A user can list, retrieve, edit, and delete their saved trips. | `GET /trips`, `GET /trips/{id}`, `PATCH /trips/{id}`, `DELETE /trips/{id}`. |
| FR-06 | A user can request a replacement itinerary day with feedback. | `POST /trips/regenerate-day`; the detail page saves the returned day to the trip. |
| FR-07 | A user can share or export a readable itinerary summary. | Detail page copies summary/link, invokes Web Share when available, and downloads Markdown. |
| FR-08 | The application can generate a plan without a remote AI provider. | Local curated/procedural fallback in the AI orchestrator. |

## Non-functional requirements

- **Security:** protect user-scoped routes with signed bearer tokens; hash passwords; keep Supabase service-role credentials on the backend; configure CORS by environment.
- **Reliability:** validate request/response structures and provide a local itinerary-generation fallback when remote generation fails.
- **Maintainability:** separate UI pages, API client, routers, schemas, and services.
- **Deployability:** support local development and provide Docker Compose, Render, and Vercel deployment configuration.
- **Usability:** show account, planning, saved-trip, and itinerary-detail flows with loading and error feedback.

## User journey

1. A new traveler creates an account or an existing traveler signs in.
2. The traveler opens the trip builder and enters preferences.
3. The frontend sends a bearer-authenticated request to generate the itinerary.
4. The traveler reviews the generated plan and saves it.
5. The traveler opens **My Trips**, views the itinerary, edits trip fields, or regenerates a day.
6. The traveler copies/shares the trip link or summary, or downloads a Markdown copy.

## Data and validation notes

Trip and activity shapes are defined in `backend/app/schemas/schemas.py`. The trip form includes dates as strings, traveler count is constrained to 1–50, destination length is constrained, and budget cannot be negative. The fallback generator caps its itinerary length at 30 days. Date ordering is not guaranteed by the schema alone and should be validated if stricter date rules are required.

## Acceptance criteria for the main flow

- A valid trip request produces a response containing trip details and day objects with activity lists.
- An authenticated user can save and retrieve their trip and itinerary.
- A user cannot use another account's trip through the user-scoped trip service.
- Invalid credentials do not return a successful session.
- If remote generation is unavailable, the configured local path can still produce a structured itinerary.
- The saved-trip detail page can update the stored itinerary after regenerating a day.

## Requirements traceability

The API and screens listed here describe current source behavior. They are not a claim that every acceptance criterion has been independently executed in this documentation pass; see [Phase 6 — Project Testing](../6.%20Project%20Testing/README.md).
