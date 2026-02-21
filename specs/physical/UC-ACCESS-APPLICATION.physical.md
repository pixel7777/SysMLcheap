# Physical Architecture Intent Spec — UC-ACCESS-APPLICATION

**Use Case Ref:** `uc_access_application`  
**LDS Ref:** `specs/use-cases/UC-ACCESS-APPLICATION.lds.yaml`  
**Status:** Baseline approved (2026-02-21)  
**Last Updated:** 2026-02-21

## 1) Scope and Outcome

Initial functionality target:

> Learner can enter the app reliably, resume where they left off, and reach the next actionable learning step quickly.

This spec defines physical intent before implementation and becomes the place we reflect implemented reality after code changes.

## 2) Physical Containers (Intent)

### C1. Learner Browser Client (Heidi)
- Runs web UI
- Initiates app entry request
- Displays one of: Resume, Onboarding, Home/Placeholder, Degraded mode

### C2. Language Questing Web App/API
- Handles entry orchestration
- Resolves learner context and route decision
- Applies security and degraded-mode policies

### C3. Data Store
- Stores learner profile, session metadata, and progress checkpoint
- Supports fast lookup on app entry

### C4. Host Platform (TBD)
- Deploys Web App/API
- Provides runtime, networking, logs, and environment config
- Candidate examples: Vercel / Fly.io / Railway / Render

### C5. External Dependencies (placeholder)
- Authentication provider (future/externalized option)
- AI provider health signal (for degraded mode decisioning)

## 3) Runtime Interaction (Intent Sequence)

1. Learner opens app URL on host platform.
2. Client calls entry endpoint (`/api/entry`).
3. Web App/API validates/recovers learner session.
4. Web App/API resolves context (checkpoint exists? first-time learner?).
5. Web App/API checks dependency availability state (AI health snapshot).
6. Web App/API returns entry decision:
   - `resume_checkpoint`
   - `start_onboarding`
   - `show_home_placeholder`
   - `degraded_mode_fallback`
7. Client routes to destination and renders first actionable screen.

## 4) Physical Interface Sketch (Intent)

## Endpoint: `POST /api/entry`

Request (minimal intent):
- session token/cookie (if present)
- client metadata (optional)

Response (intent shape):

```json
{
  "entryDecision": "resume_checkpoint | start_onboarding | show_home_placeholder | degraded_mode_fallback",
  "checkpointId": "optional",
  "banner": "optional text",
  "firstAction": "string"
}
```

## Endpoint: `POST /api/auth/login` (if local auth path used)
- Generic failure responses (no account enumeration)
- Audit event on failed attempt

## Endpoint: `GET /api/health/dependencies` (internal or service-only)
- Returns cached dependency availability for entry orchestration

## 5) Quality Budgets and Constraints

- **Performance:** p95 app open to first actionable screen < 2.5s (normal mode)
- **Reliability:** 99.5% successful entry orchestration when core dependencies are healthy
- **Security:** auth failure messaging does not disclose account existence
- **Operability:** entry path emits telemetry for outcome + latency + error reason code

## 6) Trade Decisions (To Resolve)

| Topic | Options | Proposed for MVP | Reasoning | Final Decision |
|---|---|---|---|---|
| Session model | JWT vs server session | Server session | Simpler revocation + less token complexity for MVP | Server-session style behavior in single-user dev baseline |
| Context lookup | DB-only vs cache-first | DB-only first | Simpler consistency model early | DB-first baseline (no cache layer yet) |
| Entry routing location | Edge middleware vs app service layer | App service layer | Easier debugging, fewer platform-specific constraints | App service layer |
| Dependency health check | Live synchronous vs cached heartbeat | Cached heartbeat | Lower entry latency + graceful degradation | Degraded-mode flag for MVP stub; evolve to cached health snapshot |
| Host platform | Vercel/Fly/Railway/Render | Evaluate against criteria below | Need concrete deploy constraints | Existing free AWS EC2 + GitHub |

## 7) Host Platform Evaluation Criteria

Use this checklist before selecting C4 host platform:

- Cold start behavior and latency profile
- DB/network integration simplicity
- Secrets management ergonomics
- Logging/observability quality
- Cost predictability for low/medium traffic
- CI/CD and rollback support

## 8) Placeholder UX Definition (MVP)

Until full home/resume UI is built, app must show a clear “in app” placeholder screen containing:

- learner identity/session state (basic)
- selected entry decision
- next actionable button (continue / start onboarding)
- degraded-mode banner when applicable

This placeholder is an explicit physical deliverable, not throwaway ambiguity.

## 9) Code Reflection Plan (Post-Implementation Update)

When code is created/changed for this use case, update this spec with:

- actual deployed host platform and runtime
- implemented module structure and paths
- endpoint contracts as implemented
- deviations from intent and rationale
- verification evidence (test files, CI links, commit IDs)

## 10) Traceability

- Behavioral: `uc_access_application`
- Logical Delivery Spec: `lds-uc-access-application`
- Related requirements: `req-access-001`, `req-access-002`, `req-access-003`
- Related logical candidates:
  - `blk-identity-access-service`
  - `blk-learner-context-resolver`
  - `blk-entry-orchestrator`
  - `blk-availability-guard`
  - `blk-telemetry-logger`
