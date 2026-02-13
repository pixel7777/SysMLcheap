# ADR-004: App Concept - AI-DM Croatian TTRPG Learning App

**Date:** 2026-02-13
**Status:** Accepted

## Context

We need a compelling mechanism to motivate sustained Croatian language learning. Traditional flashcard apps (Anki, Duolingo) are effective but suffer from motivation decay. Tabletop RPGs provide intrinsic narrative motivation — players want to know what happens next.

## Decision

Build an AI-powered Dungeon Master that generates ongoing story content in Croatian, calibrated to the learner's vocabulary and grammar levels. The app combines:
- **Spaced Repetition (SRS)** for vocabulary retention
- **Progressive grammar introduction** matched to learner level
- **Narrative motivation** — learn by playing a character in your own story

## Rationale

- Story context makes vocabulary memorable (episodic memory > rote memory)
- AI can dynamically adjust language difficulty based on learner performance
- TTRPG mechanics provide natural scaffolding for interaction (choices, consequences, progression)
- Combines proven language learning techniques with an engagement model that players voluntarily spend hours on

## Consequences

- AI content generation must be carefully calibrated — too hard loses learners, too easy bores them
- Need robust language modeling to track what the learner knows
- Story quality depends heavily on prompt engineering and context management
- Novel concept with no direct competitors to benchmark against
