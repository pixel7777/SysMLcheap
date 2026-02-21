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
- `src/server.js` — HTTP app with placeholder screens/routes
- `src/entryDecision.js` — entry decision logic
- `src/data/dev-db.json` — dev stub data
- `src/entryDecision.test.js` — acceptance-aligned logic tests
- `specs/physical/UC-ACCESS-APPLICATION.physical.md` — physical architecture intent + decisions
- `docs/architecture/UC-ACCESS-APPLICATION-implementation-plan.md` — plain-English implementation plan
