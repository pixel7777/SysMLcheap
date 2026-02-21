import fs from 'node:fs';
import path from 'node:path';

const DB_PATH = path.resolve(process.cwd(), 'src/data/dev-db.json');

export function loadDevDb() {
  const raw = fs.readFileSync(DB_PATH, 'utf8');
  return JSON.parse(raw);
}

export function decideEntry({ learnerId = 'heidi', degraded = false }) {
  if (degraded) {
    return {
      entryDecision: 'degraded_mode_fallback',
      firstAction: 'show_home_placeholder',
      banner: 'AI services are currently degraded. You can still access safe fallback learning paths.'
    };
  }

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
