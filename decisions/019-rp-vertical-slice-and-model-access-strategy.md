# ADR-019: RP-First Vertical Slice and API-First Model Access

**Date:** 2026-02-22
**Status:** Accepted

## Context

We need to de-risk the interaction core before adding Croatian pedagogy and game mechanics layers.

The immediate question is whether to:
- prototype with local open-source models,
- rely on a subscription chat UI, or
- use backend API model access.

## Decision

1. Implement an English-only RP vertical slice first.
2. Scope includes:
   - side-by-side chat + codex UI,
   - persistent story sessions,
   - canon extraction and codex updates,
   - text-only interaction.
3. Exclude for this slice:
   - language-learning adaptation,
   - formal game engine mechanics,
   - final codex schema design.
4. Use API-first model integration in backend (provider-agnostic), with mock-DM mode enabled until API key is configured.
5. Recommended initial low-cost model target: DeepSeek V3-class model via OpenRouter, with Mistral Small-class fallback.

## Rationale

- Vertical slice tests core unknowns (coherent DM loop + persistent canon) with minimum complexity.
- API-first architecture preserves backend control, observability, and model portability.
- Mock mode allows implementation and testing before key provisioning.

## Consequences

- Frontend and backend contracts are now established for turn processing and codex updates.
- Model provider can be swapped without frontend redesign.
- Additional ADRs will be needed for canon schema, contradiction handling, and language-layer insertion.
