import http from 'node:http';
import { URL } from 'node:url';
import { decideEntry } from './entryDecision.js';

const port = Number(process.env.PORT || 3000);

function page(title, body) {
  return `<!doctype html><html><head><meta charset="utf-8"/><title>${title}</title></head><body style="font-family:system-ui;padding:24px"><h1>${title}</h1>${body}</body></html>`;
}

function renderInApp(decision) {
  const actions = {
    resume_checkpoint: '<a href="/resume">Continue from checkpoint</a>',
    start_onboarding: '<a href="/onboarding">Start onboarding</a>',
    degraded_mode_fallback: '<a href="/app">Open safe fallback home</a>'
  };

  return page('Language Questing System — In App', `
    <p><strong>Entry decision:</strong> ${decision.entryDecision}</p>
    ${decision.banner ? `<p style="color:#9a6700"><strong>Notice:</strong> ${decision.banner}</p>` : ''}
    <p><strong>First action:</strong> ${decision.firstAction}</p>
    <p>${actions[decision.entryDecision] || '<a href="/app">Open app home</a>'}</p>
  `);
}

const server = http.createServer((req, res) => {
  const url = new URL(req.url, `http://${req.headers.host}`);

  if (url.pathname === '/') {
    const learnerId = url.searchParams.get('learner') || 'heidi';
    const degraded = url.searchParams.get('degraded') === '1';
    const decision = decideEntry({ learnerId, degraded });

    res.writeHead(302, {
      Location: `/app?learner=${encodeURIComponent(learnerId)}&decision=${decision.entryDecision}${decision.checkpointId ? `&checkpoint=${decision.checkpointId}` : ''}${degraded ? '&degraded=1' : ''}`
    });
    res.end();
    return;
  }

  if (url.pathname === '/app') {
    const learnerId = url.searchParams.get('learner') || 'heidi';
    const degraded = url.searchParams.get('degraded') === '1';
    const decision = decideEntry({ learnerId, degraded });

    res.writeHead(200, { 'content-type': 'text/html; charset=utf-8' });
    res.end(renderInApp(decision));
    return;
  }

  if (url.pathname === '/resume') {
    res.writeHead(200, { 'content-type': 'text/html; charset=utf-8' });
    res.end(page('Resume Checkpoint', '<p>Placeholder resume screen.</p>'));
    return;
  }

  if (url.pathname === '/onboarding') {
    res.writeHead(200, { 'content-type': 'text/html; charset=utf-8' });
    res.end(page('Onboarding Start', '<p>Placeholder onboarding screen.</p>'));
    return;
  }

  res.writeHead(404, { 'content-type': 'text/plain; charset=utf-8' });
  res.end('Not found');
});

server.listen(port, () => {
  console.log(`LQS MVP server listening on http://localhost:${port}`);
});
