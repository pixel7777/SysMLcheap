# RP Vertical Slice (English-Only) — Implementation Plan

**Date:** 2026-02-22  
**Owner:** Gale + Heidi

## Objective

Build a deployable, testable RP-first slice that proves:
1. session-based DM interaction works,
2. world facts can be accumulated into a codex,
3. the same canon can be reused for subsequent turns.

## In Scope

- Web UI (single page):
  - Top: auth/session controls placeholders
  - Left: codex pane (live updates)
  - Right: chat pane
- Backend endpoints:
  - `POST /api/sessions`
  - `GET /api/sessions`
  - `GET /api/sessions/:id/chat`
  - `GET /api/sessions/:id/codex`
  - `POST /api/sessions/:id/turn`
- Persistent local store (`src/data/story-db.json`)
- Mock DM turn generator with structured output
- Turn logs capturing prompt context summary + canon handling

## Out of Scope (for this phase)

- Croatian language adaptation
- Character sheet/game mechanics integration
- Rich codex taxonomy
- Multi-model orchestration

## Turn Processing Contract (v0)

Input:
- `sessionId`
- `userText`
- recent messages (max 12)
- current codex entries

Generator output:
- `assistantText`
- `canonCandidates[]`
- `openThreads[]`
- `model`
- `latencyMs`

Persistence:
- save user+assistant messages
- upsert codex entries from accepted canon candidates
- append turn log

## Ready-for-API-Key Checklist

- [x] UI supports side-by-side codex + chat
- [x] Session create/select works
- [x] Turn endpoint and pipeline work with mock generator
- [x] Canon candidates persist into codex
- [x] Tests cover message+codex persistence path
- [ ] Provider adapter (`LLM_PROVIDER=openrouter`) and key wiring
- [ ] Prompt templates and JSON-schema enforcement for live model
- [ ] Failure fallback path (malformed model output)

## Test Notes

Current automated tests validate that one turn writes:
- user + assistant messages,
- codex entries (including guard-deal signal),
- accepted canon references.

Manual demo script:
1. Create session ("Guard Negotiation Demo")
2. Send: "I ask the guard for a deal."
3. Confirm codex shows location/thread/NPC updates
4. Send follow-up and verify continuity in chat + codex updates
