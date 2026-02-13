# ADR-008: NovelCrafter-Style Context Management

**Date:** 2026-02-13
**Status:** Accepted

## Context

AI language models have limited context windows and charge per token. A long-running TTRPG story accumulates significant lore: NPCs, locations, inventory, plot threads, timeline. Sending everything every turn is wasteful and eventually impossible.

## Decision

Implement a NovelCrafter-inspired wiki/context management system:
- **Codex entries** for world lore, locations, rules
- **Timeline** tracking story events in order
- **Inventory** for character possessions
- **NPC registry** with relationship status and last interaction
- Only **relevant entries** are sent as AI context each turn (token efficiency)

## Rationale

- NovelCrafter has proven this pattern works for long-form AI-assisted narrative
- Selective context injection keeps AI responses consistent without sending everything
- Structured data (not just raw conversation history) enables smarter retrieval
- Supports stories that run for months without context window degradation

## Consequences

- Need a relevance algorithm to select which context entries matter for the current scene
- Entries must be maintained (auto-updated from AI responses + manual corrections)
- Adds complexity to the prompt engineering pipeline
- Storage and retrieval system becomes a core architectural component
