# Phase 8 — Project Demonstration

## Demonstration objective

Show the complete planning workflow: account access, preference entry, itinerary generation, saving, trip management, and itinerary export. Present generated activities as suggestions that need traveler verification.

## Pre-demo checklist

- Start the backend and frontend, or verify the deployed URLs are available.
- Confirm the backend `/health` endpoint responds successfully.
- Confirm the selected AI provider is configured, or choose the local provider for an offline demonstration.
- If demonstrating durable persistence, confirm the Supabase schema is applied and environment variables are present in the hosting platform.
- Use a dedicated demonstration account and non-sensitive sample inputs.
- Prepare a destination, dates, interests, budget, travel style, pace, and dietary requirement for the walkthrough.
- Keep provider keys and service-role keys out of browser views, screenshots, and recorded logs.

## Suggested 5–7 minute walkthrough

1. **Introduce the goal.** Explain that the app turns travel preferences into an editable day-by-day draft itinerary.
2. **Sign in or register.** Show the account flow and authenticated navigation.
3. **Enter trip preferences.** Use a realistic destination, dates, group size, budget, style, pace, interests, and dietary notes.
4. **Generate and review.** Point out the daily structure and activity details. Explain that generation can use Groq/Ollama or the local fallback, depending on configuration and provider availability.
5. **Save the plan.** Save the generated itinerary and open **My Trips**.
6. **Manage the trip.** Open its detail page, edit trip details, and regenerate one day with feedback.
7. **Share/export.** Copy a trip link or summary, use browser sharing if available, and download the Markdown itinerary.
8. **Close with architecture.** Briefly show the React frontend, FastAPI API, and Supabase persistence option.

## Example narration

“I enter the destination, dates, budget, travel style, pace, interests, and dietary needs. The backend returns a structured itinerary. I can save it to my trip library, revise the trip or one day, and download a Markdown summary. Supabase stores account and trip data when configured; local development can use an in-memory fallback.”

## Demo success criteria

- The presenter can explain the inputs and show a generated day-by-day itinerary.
- The generated itinerary can be saved and reopened from the trip list.
- At least one update or day regeneration is demonstrated.
- The presenter can explain the authentication, persistence, and AI fallback at a high level.
- Limitations are stated accurately: suggestions are not bookings, live prices, or verified opening-hour data; saved trip routes require authentication.

## Recovery plan

| Issue | Response |
|---|---|
| Remote AI provider is slow or unavailable | Use the configured local generation path and explain the fallback. |
| Backend cannot reach Supabase | Switch to a known local demo setup if available; explain that in-memory data is temporary and will reset on restart. |
| A saved trip fails to load | Retry once, confirm the backend is healthy and account is signed in, then use a prepared sample itinerary for the rest of the walkthrough. |
| Browser sharing is unavailable | Use the built-in copy-link/copy-summary controls or download Markdown. |
| Internet or deployment outage | Demonstrate the local frontend/backend setup if it was prepared in advance. |

## Future improvements to mention

Potential next steps include stronger date validation, automated frontend/end-to-end tests, a deliberate public-sharing permission model, and optional integrations for maps, transit, weather, or verified travel data. These are proposals, not claims about the current implementation.

## Phase deliverables

- [Communication - Personalized Travel Itinerary Planner](Communication%20-%20Personalized%20Travel%20Itinerary%20Planner.pdf)
- [Demonstration of Proposed Features - Personalized Travel Itinerary Planner](Demonstration%20of%20Proposed%20Features%20-%20Personalized%20Travel%20Itinerary%20Planner.pdf)
- [Project Demo Planning - Personalized Travel Itinerary Planner](Project%20Demo%20Planning%20-%20Personalized%20Travel%20Itinerary%20Planner.pdf)
- [Scalability & Future Plan - Personalized Travel Itinerary Planner](Scalability%20%26%20Future%20Plan%20-%20Personalized%20Travel%20Itinerary%20Planner.pdf)
- [Team Involvement in Demonstration - Personalized Travel Itinerary Planner](Team%20Involvement%20in%20Demonstration%20-%20Personalized%20Travel%20Itinerary%20Planner.pdf)
