# ADR-011: GitHub Issues for Work Management

**Date:** 2026-02-13
**Status:** Accepted

## Context

We need a lightweight work management system that integrates with the model-driven development approach. External tools (Jira, etc.) add complexity and cost for a small team.

## Decision

- Use **GitHub Issues + Project board** for Kanban-style work management
- **Generate issues directly** from model elements (e.g., one issue per MVP use case)
- Add a **status field** on model blocks (`planned` / `in-progress` / `implemented` / `tested`) reported by the validator

## Rationale

- GitHub Issues are free and already where the code lives
- Model-driven issue generation ensures traceability from requirements to tasks
- Kanban board provides visual workflow without heavyweight process
- Validator can report implementation status alongside model completeness

## Consequences

- Need a script to generate/sync GitHub Issues from YAML model
- Status field adds another dimension to the model schema
- Must avoid issue sprawl (generate only actionable items, not every model element)
- Two-way sync between model status and issue status needs a convention
