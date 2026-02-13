# UC Review — Access Application (MVP Single-User)

Purpose: make control logic, guards, loops, and signal connectivity reviewable (activity-like) without Cameo.

## 1) Control-Flow Contract (review view)

```mermaid
flowchart TD
  A[AcceptEvent: App Entry Request\n(sig_app_entry_request)] --> B[CallOp: requestApplicationEntry]
  B --> C[CallOp: evaluateAccessGateRequirement]
  C --> D{Decision: gate required?}

  D -- No --> E[CallOp: establishLearnerSession\n(no-credential path)]
  D -- Yes --> F[AcceptEvent: Local Access Credential\n(sig_local_access_credential)]
  F --> G[CallOp: validateLocalAccessCredential]
  G --> H{Decision: credential valid?}
  H -- No --> F
  H -- Yes --> E

  E --> I[CallOp: loadMvpStaticConfiguration]
  E --> J[CallOp: loadCurrentStories]
  E --> K[CallOp: loadLearnerProgressSummary]

  I --> L[CallOp: renderLearnerHomeView]
  J --> L
  K --> L

  L --> M[SendSignal: Learner Home View Model\n(sig_learner_home_view_model)]
  M --> N((Final))
```

## 2) Node Catalog (type + ownership)

- `AcceptEvent` `app_entry_request` (external input)
- `CallOperation` `requestApplicationEntry`
- `CallOperation` `evaluateAccessGateRequirement`
- `Decision` `gate required?`
- `AcceptEvent` `local_access_credential` (external input)
- `CallOperation` `validateLocalAccessCredential`
- `Decision` `credential valid?`
- `CallOperation` `establishLearnerSession`
- `CallOperation` `loadMvpStaticConfiguration`
- `CallOperation` `loadCurrentStories`
- `CallOperation` `loadLearnerProgressSummary`
- `CallOperation` `renderLearnerHomeView`
- `SendSignal` `learner_home_view_model`

## 3) Object-Flow Connectivity Ledger

| Signal | Producer | Consumer(s) | Origin | Status |
|---|---|---|---|---|
| `sig_app_entry_request` | Learning User External | `requestApplicationEntry`, `evaluateAccessGateRequirement` | external | connected |
| `sig_app_entry_response` | `requestApplicationEntry` | Learning User External | system | terminal-to-external |
| `sig_access_gate_decision` | `evaluateAccessGateRequirement` | decision `gate required?` | system | connected |
| `sig_local_access_credential` | Learning User External | `validateLocalAccessCredential` | external | connected |
| `sig_credential_validation_result` | `validateLocalAccessCredential` | decision `credential valid?`, `establishLearnerSession` (valid path) | system | connected |
| `sig_learner_session` | `establishLearnerSession` | `loadMvpStaticConfiguration`, `loadCurrentStories`, `loadLearnerProgressSummary` | system | connected |
| `sig_mvp_configuration_snapshot` | `loadMvpStaticConfiguration` | `renderLearnerHomeView` | system | connected |
| `sig_current_story_summary` | `loadCurrentStories` | `renderLearnerHomeView` | system | connected |
| `sig_learner_progress_summary` | `loadLearnerProgressSummary` | `renderLearnerHomeView` | system | connected |
| `sig_learner_home_view_model` | `renderLearnerHomeView` | Learning User External | system | terminal-to-external |

## 4) Quick Correctness Checks

- Guarded branch exists for gate-required vs no-gate path. ✅
- Retry loop exists for invalid credential. ✅
- External-origin events are explicit (`AcceptEvent`). ✅
- Produced signals are either consumed internally or intentionally terminal to external UI. ✅

## 5) Open decisions

- Keep both `requestApplicationEntry` and `evaluateAccessGateRequirement` as separate operations, or merge into one operation with structured response?
- Should no-gate path produce an explicit synthetic pass signal (for stricter uniformity), or keep direct decision-to-session establishment path?
