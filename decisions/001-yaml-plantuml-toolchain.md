# ADR-001: YAML+PlantUML as Modeling Toolchain

**Date:** 2026-02-12
**Status:** Accepted

## Context

We need a modeling approach that supports MBSE rigor (typed elements, relationships, validation, traceability) without requiring expensive commercial tools like Cameo. Heidi has 15 years of Cameo/SysML experience and wants to bring that discipline to this project.

## Options Considered

1. **Cameo/MagicDraw** — Gold standard but expensive ($$$), heavyweight, not collaborative-friendly for a two-person team
2. **Text-only design docs** — Easy but loses structure, no validation, no traceability
3. **PlantUML alone** — Good diagrams but no semantic model underneath (just pictures)
4. **YAML as semantic model + PlantUML as visualization layer** — Structured data with validation + human-readable diagrams
5. **SysML v2 textual notation** — Ideal in theory but tooling is immature

## Decision

Use YAML files as the semantic model (source of truth) with Python scripts that:
- Validate completeness and consistency (inspired by SAIC DE Validation Rules v27)
- Generate PlantUML diagrams for visualization
- Generate markdown tables and reports

## Rationale

- YAML is human-readable and editable in any text editor
- Git-friendly (diffable, mergeable)
- Validation rules can be adapted from Heidi's SAIC DE profile
- PlantUML covers the diagram types we need (use case, BDD, activity, sequence, state machine)
- Zero cost, no vendor lock-in
- Can be extended incrementally as needs grow

## Consequences

- We own the toolchain — maintenance is on us
- PlantUML has limits (IBDs are awkward, no native SysML notation)
- Schema design is critical — bad schema = pain later
- Learning curve for YAML editing (mitigated by Discord-based workflow with AI assistance)
