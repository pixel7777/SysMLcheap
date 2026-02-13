# ADR-010: Live Model Tables via GitHub Pages

**Date:** 2026-02-13
**Status:** Accepted (supersedes original ADR-010 build-step approach)
**Updated:** 2026-02-13

## Context

The YAML model is the source of truth, but humans need readable views — tables of actors, use cases, requirements, etc. The original approach (GitHub Actions generating markdown on push) introduced a build step and generated files that could drift if the action failed or was misconfigured.

## Decision

- **Render tables live in the browser** using a single HTML page hosted on GitHub Pages (`docs/index.html`)
- The page fetches raw YAML directly from the repository on every page load and renders tables client-side using `js-yaml`
- **No build step** — tables are always current with the latest pushed YAML
- All model tables support **per-column filtering** (text search or dropdown for enumerated fields) and **clickable column sorting** (ascending/descending toggle)
- New table types are added by appending entries to the `TABLES` configuration array in the HTML file
- GitHub Actions still runs `validate.py` on push for model validation (unchanged)

## Design Standards for Model Tables

All tables displaying model data on GitHub Pages must follow these conventions:

1. **Live fetch**: Read YAML from `raw.githubusercontent.com` at page load — never generate static files
2. **Column sorting**: Every text/scalar column is sortable (click header to toggle asc/desc)
3. **Column filtering**: Each column gets a filter control — `select` dropdown for enumerated fields (e.g., status, owner), free-text input for open fields
4. **Global search**: A top-level search bar filters across all columns simultaneously
5. **Clear filters**: A single button resets all filters, sorting, and search state
6. **Light theme**: White background, black text, muted grey (`#555` minimum) for secondary content — optimized for readability
7. **Status badges**: Color-coded pills for status fields (green=mvp, yellow=future, red=deprecated)
8. **Extensible**: Adding a new table = adding one object to the `TABLES` array with file path, YAML key, and column definitions

## Rationale

- Zero build step = zero drift. If it's in the YAML, it's in the table.
- Per-column filtering and sorting make large tables navigable without external tools
- Single HTML file is trivial to maintain — no framework, no dependencies beyond js-yaml CDN
- GitHub Pages hosting is free and automatic from `docs/`

## Consequences

- Requires GitHub Pages enabled (Settings → Pages → Deploy from branch, `/docs`)
- Depends on `raw.githubusercontent.com` availability (extremely reliable)
- CDN dependency for `js-yaml` (can vendor locally if needed)
- GitHub Actions pipeline remains for validation, separate from table rendering
