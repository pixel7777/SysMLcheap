# ADR-010: Auto-Generated Tables and GitHub Actions

**Date:** 2026-02-13
**Status:** Accepted

## Context

The YAML model is the source of truth, but humans need readable views — tables of actors, use cases, requirements, etc. Manually maintaining both YAML and documentation leads to drift.

## Decision

- **Auto-generate markdown tables** from the YAML model (actors, use cases, blocks, etc.) that render natively in GitHub
- **GitHub Action** runs `validate.py` on every push to catch model errors early
- **Auto-generate README** with PlantUML diagram links (using PlantUML server URLs)

## Rationale

- Single source of truth (YAML) with generated views eliminates documentation drift
- GitHub Actions provide continuous validation without manual steps
- Markdown tables render in GitHub without any tooling on the reader's side
- PlantUML server URLs mean diagrams render without local installation

## Consequences

- Generated files must be clearly marked as auto-generated (don't edit manually)
- CI pipeline must be maintained alongside the model tooling
- PlantUML server dependency for diagram rendering (can self-host if needed)
- Build step required before documentation is current
