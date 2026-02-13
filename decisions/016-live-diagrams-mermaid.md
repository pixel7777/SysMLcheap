# ADR-016: Live YAML-Rendered Diagrams via Mermaid

**Date:** 2026-02-13  
**Status:** Accepted

## Context

PlantUML diagram generation has been unstable in practice and introduces maintenance friction when diagrams are generated as files. We already adopted a successful live-table pattern where YAML is fetched directly from GitHub and rendered in-browser, removing build-step drift.

We need the same property for diagrams:

- YAML remains source of truth
- Views auto-update with YAML changes
- No manual “regenerate diagrams” prompt needed
- No drift between model and visual artifacts

## Decision

Adopt **live diagram rendering in GitHub Pages** using Mermaid:

- Add `docs/diagrams.html` that fetches YAML from `raw.githubusercontent.com`
- Transform YAML into Mermaid definitions client-side
- Render diagrams in-browser on page load (and refresh button)
- Keep generated PlantUML files optional/legacy; not required for current diagrams page

Initial live views:

1. Use Case Overview (actors/use cases/include/extend)
2. Logical Context (context block + top-level decomposition)
3. Requirement ↔ Use Case trace graph

## Rationale

- Eliminates artifact drift by design
- Removes dependency on PlantUML stability for day-to-day visualization
- Matches existing live table workflow and maintenance style
- Keeps architecture model auditable and text-first (MBSE-friendly)

## Consequences

- Mermaid syntax expressiveness differs from full SysML notation
- Very large graphs may need filtered/segmented views
- Browser-side rendering depends on Mermaid + js-yaml CDN availability (can be vendored later if needed)

## Follow-on

- Add diagram view filters (status, architecture slice, actor subset)
- Add deterministic layout hints and view templates
- Add CI validation for diagram transform integrity
