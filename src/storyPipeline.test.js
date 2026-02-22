import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { createSession, getCodex, getMessages, saveTurn } from './storyStore.js';
import { generateMockDmTurn } from './mockDm.js';

const dbPath = path.resolve('src/data/story-db.json');

test('story turn persists messages and codex canon', () => {
  if (fs.existsSync(dbPath)) fs.unlinkSync(dbPath);

  const session = createSession({ title: 'Guard Negotiation' });
  const dm = generateMockDmTurn({
    session,
    userText: 'I try to make a deal with the guard.',
    codexEntries: [],
    recentMessages: []
  });

  const result = saveTurn({
    sessionId: session.id,
    userText: 'I try to make a deal with the guard.',
    dmResult: dm,
    promptSummary: { mode: 'mock' }
  });

  const messages = getMessages(session.id);
  const codex = getCodex(session.id);

  assert.equal(messages.length, 2);
  assert.equal(messages[0].role, 'user');
  assert.equal(messages[1].role, 'assistant');
  assert.ok(codex.length >= 2);
  assert.ok(codex.some((entry) => entry.title.includes('Gate Guard')));
  assert.ok(result.acceptedCanon.length >= 2);
});
