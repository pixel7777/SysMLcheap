import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';

const dataDir = path.resolve('src/data');
const dbPath = path.join(dataDir, 'story-db.json');

function nowIso() {
  return new Date().toISOString();
}

function createEmptyDb() {
  return {
    sessions: [],
    messages: [],
    codexEntries: [],
    turnLogs: []
  };
}

function readDb() {
  if (!fs.existsSync(dbPath)) {
    fs.mkdirSync(dataDir, { recursive: true });
    const empty = createEmptyDb();
    fs.writeFileSync(dbPath, JSON.stringify(empty, null, 2));
    return empty;
  }

  return JSON.parse(fs.readFileSync(dbPath, 'utf-8'));
}

function writeDb(db) {
  fs.writeFileSync(dbPath, JSON.stringify(db, null, 2));
}

function id(prefix) {
  return `${prefix}-${crypto.randomUUID().slice(0, 8)}`;
}

export function createSession({ title = 'New Story' } = {}) {
  const db = readDb();
  const session = {
    id: id('session'),
    title,
    createdAt: nowIso(),
    updatedAt: nowIso(),
    status: 'active'
  };

  db.sessions.push(session);
  writeDb(db);
  return session;
}

export function listSessions() {
  return readDb().sessions;
}

export function getSession(sessionId) {
  const db = readDb();
  return db.sessions.find((s) => s.id === sessionId) || null;
}

export function getMessages(sessionId) {
  const db = readDb();
  return db.messages.filter((m) => m.sessionId === sessionId);
}

export function getCodex(sessionId) {
  const db = readDb();
  return db.codexEntries
    .filter((entry) => entry.sessionId === sessionId)
    .sort((a, b) => a.title.localeCompare(b.title));
}

function upsertCodexEntries(db, sessionId, canonCandidates) {
  const accepted = [];

  for (const candidate of canonCandidates || []) {
    const title = `${candidate.entityType || 'Note'}: ${candidate.entityName || 'Unknown'}`;
    const body = candidate.fact || '';
    if (!body.trim()) continue;

    const existing = db.codexEntries.find(
      (e) => e.sessionId === sessionId && e.title.toLowerCase() === title.toLowerCase()
    );

    if (existing) {
      if (!existing.body.includes(body)) {
        existing.body = `${existing.body}\n- ${body}`;
        existing.updatedAt = nowIso();
      }
      accepted.push(existing);
    } else {
      const entry = {
        id: id('codex'),
        sessionId,
        title,
        body: `- ${body}`,
        updatedAt: nowIso()
      };
      db.codexEntries.push(entry);
      accepted.push(entry);
    }
  }

  return accepted;
}

export function saveTurn({ sessionId, userText, dmResult, promptSummary }) {
  const db = readDb();
  const timestamp = nowIso();

  db.messages.push(
    { id: id('msg'), sessionId, role: 'user', text: userText, createdAt: timestamp },
    {
      id: id('msg'),
      sessionId,
      role: 'assistant',
      text: dmResult.assistantText,
      createdAt: timestamp
    }
  );

  const acceptedCanon = upsertCodexEntries(db, sessionId, dmResult.canonCandidates);

  db.turnLogs.push({
    id: id('turn'),
    sessionId,
    createdAt: timestamp,
    model: dmResult.model,
    latencyMs: dmResult.latencyMs,
    promptSummary,
    openThreads: dmResult.openThreads,
    canonCandidates: dmResult.canonCandidates,
    acceptedCanonIds: acceptedCanon.map((e) => e.id)
  });

  const session = db.sessions.find((s) => s.id === sessionId);
  if (session) session.updatedAt = timestamp;

  writeDb(db);

  return {
    acceptedCanon,
    messages: db.messages.filter((m) => m.sessionId === sessionId),
    codex: db.codexEntries.filter((entry) => entry.sessionId === sessionId)
  };
}
