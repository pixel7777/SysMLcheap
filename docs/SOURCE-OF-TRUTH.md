# Source of Truth and Guardrails

This project uses a layered source-of-truth model to prevent drift.

## Authority Hierarchy

1. **Behavioral truth**: `model/behavioral.yaml`
   - Canonical actors/use cases and IDs.
2. **Delivery truth (per use case)**: `specs/use-cases/*.lds.yaml`
   - Canonical intended outcomes, rules, responsibilities, quality targets, acceptance tests.
3. **Physical truth (per use case)**: `specs/physical/*.physical.md`
   - Canonical physical architecture intent and post-implementation reality notes.
4. **Implementation truth**: code + tests in repo.
5. **Views only (non-authoritative)**: `docs/index.html`, table layouts, any display formatting.

## Required ID Anchor

`useCaseRef` is the primary anchor across artifacts.

- Behavioral use case IDs live in `model/behavioral.yaml`.
- LDS files must reference one behavioral use case via `useCaseRef`.
- Physical specs must declare `**Use Case Ref:**` in the header.
- Physical index must include all use cases that have LDS and/or physical specs.

## Guardrail Automation

Script: `tools/check_guardrails.py`

Checks:
- LDS `useCaseRef` values map to behavioral use case IDs
- Physical spec `Use Case Ref` values map to behavioral use case IDs
- `docs/architecture/physical-index.md` includes all refs present in LDS/physical specs

Run locally:

```bash
python3 tools/check_guardrails.py
```

## PR Discipline Rule

A use-case change is not complete unless these are in sync (same PR where possible):
- behavioral model entry
- LDS file
- physical spec
- code/tests
- physical index row
