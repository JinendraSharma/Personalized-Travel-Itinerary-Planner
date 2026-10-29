# Phase 1 — Brainstorming and Ideation

## Project

**Personalized Travel Itinerary Planner** is a web application for turning a traveler's destination, dates, budget, group size, pace, travel style, interests, and dietary needs into a day-by-day itinerary. The project combines a React/Vite frontend with a FastAPI backend, optional language-model generation, and Supabase persistence.

## Problem statement

Planning a multi-day trip often means collecting preferences, researching activities, and arranging them into a workable schedule across several sources. This project explores a single workflow where a traveler can describe the trip once, review a structured plan, save it, and revise it later.

## Intended users

- **Independent travelers** who want a starting itinerary shaped by their interests and budget.
- **Friends or families** who need the plan to account for group size and different trip preferences.
- **Travelers revising a plan** who want to regenerate one day or update saved trip details without rebuilding everything.

These are project personas inferred from the implemented inputs and screens; they are not the result of formal user interviews.

## Opportunity areas considered

1. Personalized day-by-day itinerary generation.
2. A persistent library of trips linked to a user account.
3. Editable trip details and regeneration of an individual day.
4. Clear presentation and portable sharing of a saved itinerary.
5. A locally generated plan when a configured AI service is unavailable.

## Prioritization

| Priority | Idea | Reason |
|---|---|---|
| Core | Collect trip preferences and generate a structured itinerary | Defines the central user outcome and is implemented by the trip planner. |
| Core | Register, sign in, and scope saved trips to the account | Supports saved-trip workflows and is implemented by the authentication and trip APIs. |
| Core | View, edit, delete, and regenerate saved trip content | Makes the plan useful after the first generation. |
| Supporting | Copy/share a trip summary and download Markdown | Available on the saved trip detail page. |
| Supporting | Use Supabase when configured and local in-memory behavior for development | Gives the backend a hosted persistence path and a development fallback. |
| Future | Live travel data, collaborative editing, maps, booking, and notifications | Not represented as implemented functionality in the current source. |

## Product concept

The user signs in, enters trip preferences, requests a plan, reviews the itinerary, and saves it to **My Trips**. From a saved trip, the user can open its detail page, update trip information, regenerate a day with feedback, copy a link or summary, share through the browser, or download a Markdown file.

## Ideation outcome

The selected concept is a focused itinerary planning and management app. The feature boundary is intentionally centered on planning and editing; it does not claim to book transport or accommodation, verify real-time opening hours, or guarantee live availability or prices.

## Evidence and assumptions

- The input fields, screens, and actions above were checked against the current frontend and backend source.
- The user groups and planning pain points are reasonable product assumptions, not validated research findings.
- Generated activity and cost suggestions are planning content, not confirmed reservations or live quotes.

## Phase deliverables

- [Brainstorming & Idea Prioritization - Personalized Travel Itinerary Planner](Brainstorming%20%26%20Idea%20Prioritization%20-%20Personalized%20Travel%20Itinerary%20Planner.pdf)
- [Define Problem Statements - Personalized Travel Itinerary Planner](Define%20Problem%20Statements%20-%20Personalized%20Travel%20Itinerary%20Planner.pdf)
- [Empathy Map - Personalized Travel Itinerary Planner](Empathy%20Map%20-%20Personalized%20Travel%20Itinerary%20Planner.pdf)
