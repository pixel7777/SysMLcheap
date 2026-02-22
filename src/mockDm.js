function inferScene(userText, codexEntries) {
  const lc = userText.toLowerCase();

  if (lc.includes('guard')) return 'City Gate';
  if (lc.includes('tavern') || lc.includes('inn')) return 'Broken Compass Tavern';
  if (lc.includes('market')) return 'Riverside Market';

  const sceneEntry = codexEntries.find((entry) => entry.title.startsWith('Location:'));
  if (sceneEntry) return sceneEntry.title.replace('Location: ', '');
  return 'Old Road';
}

export function generateMockDmTurn({ session, userText, codexEntries, recentMessages }) {
  const start = Date.now();
  const scene = inferScene(userText, codexEntries);
  const previousAssistant = [...recentMessages].reverse().find((m) => m.role === 'assistant');
  const continuity = previousAssistant ? 'building on your previous move' : 'opening a fresh beat';

  const assistantText = `You are in ${scene}. ${continuity}, the world reacts to your action: "${userText}".\n\nA nearby NPC studies you for a moment, then answers in clear terms, giving you one concrete next choice and one risky alternative.`;

  const canonCandidates = [
    {
      entityType: 'Location',
      entityName: scene,
      fact: `Current focal scene includes the player's latest action: ${userText}`
    },
    {
      entityType: 'Thread',
      entityName: 'Immediate Choice',
      fact: `Player created a decision point in ${scene} by attempting: ${userText}`
    }
  ];

  if (userText.toLowerCase().includes('deal')) {
    canonCandidates.push({
      entityType: 'NPC',
      entityName: 'Gate Guard',
      fact: 'Guard is willing to negotiate if trust or leverage is established.'
    });
  }

  return {
    model: 'mock-dm-v0',
    assistantText,
    canonCandidates,
    openThreads: ['Resolve the immediate choice', 'Escalate or defuse local tension'],
    latencyMs: Date.now() - start
  };
}
