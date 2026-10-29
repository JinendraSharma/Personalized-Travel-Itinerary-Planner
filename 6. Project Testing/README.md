# Phase 6 — Project Testing

## Testing approach

Testing should cover request validation, authentication and ownership, AI-provider fallback, trip persistence, frontend workflows, and production configuration. The repository includes a backend offline reliability/security test module at `backend/tests/test_reliability.py`. This documentation pass did not execute tests or a production build.

## Existing automated coverage

The test module sets its own environment before importing application modules so local `.env` credentials are not loaded during the test scenarios. Its stated scope is offline reliability checks for production configuration and core trip scenarios. Inspect the test file for the exact cases and current assertions before using it as a release gate; this report does not claim a passing result.

The frontend package currently defines a Vite development server, production build, and preview scripts. No dedicated frontend test script or frontend test suite was found in `frontend/package.json` and the inspected project file list.

## Recommended verification matrix

| Area | Scenario | Expected result |
|---|---|---|
| Registration | Submit valid name, email, and password. | Account is created and a bearer token is returned. |
| Registration | Reuse an email or submit a short password. | Duplicate/invalid request is rejected with a useful response. |
| Login | Use valid and invalid credentials. | Valid credentials return a token; invalid credentials are rejected. |
| Authorization | Call a protected endpoint without a token or with an invalid token. | Request is rejected. |
| Ownership | User A attempts to read/update/delete User B's trip. | No cross-account trip data is returned or changed. |
| Planning | Generate a trip with representative preferences. | Response includes dates, trip fields, days, and activity objects. |
| Provider fallback | Make the selected remote provider unavailable. | The local generation path returns a structured plan. |
| Trip lifecycle | Save, list, fetch, update, and delete a trip. | Each operation reflects the latest persisted state. |
| Day refinement | Regenerate one day and save the returned itinerary. | The selected day is replaced while other days remain. |
| Frontend routes | Load `/trips/:tripId` directly after deployment. | Vercel rewrite serves the React app and the page loads trip data. |
| Production config | Start with unsafe/missing production settings. | Backend rejects invalid production configuration. |
| Build | Build the frontend for production. | Vite produces the `dist` bundle without errors. |

## Manual acceptance walkthrough

1. Create a test account and sign in.
2. Generate a multi-day trip using a known destination and varied preferences.
3. Save it, refresh the browser, and confirm it remains available when using Supabase.
4. Edit the trip dates or budget and confirm the detail page reflects the update.
5. Regenerate one day with a clear feedback instruction and confirm the updated day is saved.
6. Download the Markdown itinerary and verify that trip dates, days, activities, and link are readable.
7. Sign out and confirm protected pages return to the sign-in flow.

## Known validation gaps to consider

- Add frontend component and API-client tests.
- Add end-to-end coverage for registration through saved-trip editing.
- Validate date parsing and ensure the end date is not earlier than the start date.
- Test Supabase RLS and backend ownership behavior against a non-production project.
- Verify fallback behavior for malformed model JSON, timeouts, and provider credential errors.
- Add regression tests for local-storage corruption and browser offline behavior.

## Reporting results

For a release report, record the date, environment, exact command, pass/fail counts, and any skipped scenarios. Do not describe a test as passed until it has actually been run and its output reviewed.

## Phase deliverables

- [Performance Testing - Personalized Travel Itinerary Planner](Performance%20Testing%20-%20Personalized%20Travel%20Itinerary%20Planner.pdf)
