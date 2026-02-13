# UC Review — Access Application (MVP Single-User)

This artifact is a human-review companion to `model/logical.yaml`.
It makes operation order, signal consumption/production, and sanity checks explicit.

## 1) Intent (Need, not solution)

Heidi can open the app URL from mobile/desktop browser and reach a learner home view initialized with:
- MVP static configuration
- current stories
- learner progress summary

A minimal local access gate may be applied in MVP.
Federated/multi-user auth remains future scope.

## 2) Ordered Execution Flow (System-Level)

1. `requestApplicationEntry`
   - consumes: `sig_app_entry_request`
   - produces: `sig_app_entry_response`

2. `evaluateAccessGateRequirement`
   - consumes: `sig_app_entry_request`
   - produces: `sig_access_gate_decision`

3. `validateLocalAccessCredential` (conditional)
   - consumes: `sig_local_access_credential`
   - produces: `sig_credential_validation_result`

4. `establishLearnerSession`
   - consumes: `sig_credential_validation_result` (or equivalent pass condition if gate not required)
   - produces: `sig_learner_session`

5. `loadMvpStaticConfiguration`
   - consumes: `sig_learner_session`
   - produces: `sig_mvp_configuration_snapshot`

6. `loadCurrentStories`
   - consumes: `sig_learner_session`
   - produces: `sig_current_story_summary`

7. `loadLearnerProgressSummary`
   - consumes: `sig_learner_session`
   - produces: `sig_learner_progress_summary`

8. `renderLearnerHomeView`
   - consumes: `sig_mvp_configuration_snapshot`, `sig_current_story_summary`, `sig_learner_progress_summary`
   - produces: `sig_learner_home_view_model`

## 3) Signal Ledger (Who Produces / Who Consumes)

- `sig_app_entry_request`
  - produced by: Learning User External (via Learning UI)
  - consumed by: `requestApplicationEntry`, `evaluateAccessGateRequirement`

- `sig_app_entry_response`
  - produced by: `requestApplicationEntry`
  - consumed by: Learning User External (via Learning UI)

- `sig_access_gate_decision`
  - produced by: `evaluateAccessGateRequirement`
  - consumed by: access control path logic (system-level control decision)

- `sig_local_access_credential`
  - produced by: Learning User External (via Learning UI)
  - consumed by: `validateLocalAccessCredential`

- `sig_credential_validation_result`
  - produced by: `validateLocalAccessCredential`
  - consumed by: `establishLearnerSession`

- `sig_learner_session`
  - produced by: `establishLearnerSession`
  - consumed by: `loadMvpStaticConfiguration`, `loadCurrentStories`, `loadLearnerProgressSummary`

- `sig_mvp_configuration_snapshot`
  - produced by: `loadMvpStaticConfiguration`
  - consumed by: `renderLearnerHomeView`

- `sig_current_story_summary`
  - produced by: `loadCurrentStories`
  - consumed by: `renderLearnerHomeView`

- `sig_learner_progress_summary`
  - produced by: `loadLearnerProgressSummary`
  - consumed by: `renderLearnerHomeView`

- `sig_learner_home_view_model`
  - produced by: `renderLearnerHomeView`
  - consumed by: Learning User External (via Learning UI)

## 4) Alternate/Exception Paths to Confirm

- Invalid local credential
  - expected: no learner session established, retry/error response allowed.

- Config unavailable/corrupt
  - expected: safe defaults + warning status path.

- Story/progress retrieval failure
  - expected: partial home view + degraded status path.

## 5) Best-Practice Checkpoints (Community-aligned)

For app-entry use cases, common good practice is:
- Separate entry handling from credential validation.
- Treat session establishment as an explicit function boundary.
- Load independent home-view data in parallelizable functions.
- Compose final UI model from validated sub-results.
- Define degraded-mode behavior explicitly (partial data, safe defaults).

This UC currently follows those patterns.

## 6) Open Modeling Decisions

- Should `establishLearnerSession` accept a generalized gate result instead of only credential result (for no-gate path clarity)?
- Should `sig_app_entry_response` include explicit challenge metadata for the local gate?
- Do we want explicit operation(s) for degraded-mode composition (instead of implicit behavior in `renderLearnerHomeView`)?
