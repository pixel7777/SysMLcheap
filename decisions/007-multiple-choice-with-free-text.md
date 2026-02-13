# ADR-007: Multiple Choice Croatian with Free Text Option

**Date:** 2026-02-13
**Status:** Accepted

## Context

Player input is the core interaction loop. Pure free text in Croatian is intimidating for beginners. Pure multiple choice limits expression and feels like a quiz, not a game.

## Decision

- **Multiple choice options** are always presented in Croatian, with click-for-definition help available
- An **always-available free text option** lets players type their own Croatian response
- **Free text earns more points** than selecting a pre-written option, rewarding risk-taking

## Rationale

- Multiple choice provides scaffolding for beginners (they see correct Croatian forms)
- Click-for-definition reduces frustration without breaking flow
- Free text option rewards learners who are ready to produce language, not just recognize it
- Point differential incentivizes graduation from recognition to production (a key language learning milestone)

## Consequences

- AI must generate plausible, grammatically correct multiple choice options at the right level
- Free text responses need NLP evaluation (grammar checking, intent parsing)
- Scoring system must balance encouragement with accuracy feedback
- UI must make the free text option visible but not overwhelming for beginners
