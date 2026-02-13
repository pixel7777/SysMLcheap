# ADR-005: Language Stats Persist Across Stories

**Date:** 2026-02-13
**Status:** Accepted

## Context

Players may want to play multiple stories (different genres, restart with new characters, etc.). We need to decide whether language learning progress is tied to a story or to the player.

## Decision

- **Language stats** (vocabulary mastery, grammar level, SRS data) persist across all stories as player-level data
- **Character sheets** (name, class, inventory, story-specific attributes) are story-specific
- Multiple stories share a unified language progress profile

## Rationale

- Language learning is cumulative — a word learned in a fantasy story is still known in a sci-fi story
- Restarting a story shouldn't reset months of vocabulary progress
- Character sheets are narrative constructs; language stats are learning constructs
- Allows experimentation with different story types without penalty

## Consequences

- Need clear separation between player profile (language) and character profile (story)
- Story difficulty must reference the shared language profile, not story-local data
- Data model must support one-to-many relationship: one player, many stories
