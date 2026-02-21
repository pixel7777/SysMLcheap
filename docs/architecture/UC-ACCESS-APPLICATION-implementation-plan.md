# UC-ACCESS-APPLICATION — Implementation Plan (Plain English)

## Goal
Build a working first slice where Heidi can open the app, get routed correctly (resume/onboarding/degraded), and see a clear in-app placeholder screen.

## Scope for this first build
1. Create one modular web app codebase (no microservices).
2. Implement entry decision logic.
3. Add placeholder screens for app, resume, onboarding.
4. Keep storage simple (DB-first mindset; current dev stub data for local execution).
5. Add automated tests for core routing scenarios.

## Build steps
- **Step 1:** App skeleton and routes (`/`, `/app`, `/resume`, `/onboarding`).
- **Step 2:** Entry decision service that returns one of:
  - `resume_checkpoint`
  - `start_onboarding`
  - `degraded_mode_fallback`
- **Step 3:** In-app placeholder screen displaying decision + next action.
- **Step 4:** Automated tests for returning learner, first-time learner, degraded mode.

## Review checklist (Heidi)
- Can I open `/` and reach a clear app screen?
- If learner has checkpoint, do I get resume behavior?
- If learner has no checkpoint, do I get onboarding behavior?
- If degraded flag is on, do I get fallback behavior and a banner?
- Are tests present and passing?

## Commands
- Run app: `npm start`
- Run tests: `npm test`

## Notes
This is intentionally lean so we can get to visible progress and iterate from a working baseline.
