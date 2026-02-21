import test from 'node:test';
import assert from 'node:assert/strict';
import { decideEntry } from './entryDecision.js';

test('returning learner with checkpoint routes to resume', () => {
  const result = decideEntry({ learnerId: 'heidi', degraded: false });
  assert.equal(result.entryDecision, 'resume_checkpoint');
  assert.equal(result.firstAction, 'continue_checkpoint');
});

test('first-time learner routes to onboarding', () => {
  const result = decideEntry({ learnerId: 'new-learner', degraded: false });
  assert.equal(result.entryDecision, 'start_onboarding');
  assert.equal(result.firstAction, 'start_onboarding');
});

test('AI degraded state does not change entry routing decision', () => {
  const normal = decideEntry({ learnerId: 'heidi' });
  const withDegradedFlag = decideEntry({ learnerId: 'heidi', degraded: true });
  assert.equal(normal.entryDecision, 'resume_checkpoint');
  assert.equal(withDegradedFlag.entryDecision, 'resume_checkpoint');
});
