# Croatian App MVP Scaffold

This repository contains MBSE artifacts and a lightweight implementation scaffold for `uc_access_application`.

## Run locally

```bash
npm start
```

Open `http://localhost:3000/`

Useful test URLs:
- Returning learner (default): `http://localhost:3000/`
- New learner: `http://localhost:3000/?learner=new-learner`
- Degraded mode: `http://localhost:3000/?degraded=1`

## Tests

```bash
npm test
```

## Key files
- `src/server.js` — RP prototype server (UI + API endpoints)
- `src/storyStore.js` — session/chat/codex persistence
- `src/mockDm.js` — mock DM generation for no-key development
- `src/storyPipeline.test.js` — turn persistence and codex tests
- `src/entryDecision.js` — legacy entry decision logic
- `specs/physical/UC-ACCESS-APPLICATION.physical.md` — physical architecture intent + decisions
- `docs/architecture/RP-VERTICAL-SLICE-IMPLEMENTATION-PLAN.md` — current RP slice implementation plan
