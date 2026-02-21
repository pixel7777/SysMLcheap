import fs from 'node:fs';
import path from 'node:path';

const DB_PATH = path.resolve(process.cwd(), 'src/data/dev-db.json');

export function loadDevDb() {
  const raw = fs.readFileSync(DB_PATH, 'utf8');
  return JSON.parse(raw);
}

export function decideEntry({ learnerId = 'heidi' }) {
  const db = loadDevDb();
  const checkpoint = db.progressCheckpoints.find((x) => x.learnerId === learnerId && x.active === true);

  if (checkpoint) {
    return {
      entryDecision: 'resume_checkpoint',
      checkpointId: checkpoint.id,
      firstAction: 'continue_checkpoint'
    };
  }

  return {
    entryDecision: 'start_onboarding',
    firstAction: 'start_onboarding'
  };
}
