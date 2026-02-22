import http from 'node:http';
import { URL } from 'node:url';
import { createSession, getCodex, getMessages, getSession, listSessions, saveTurn } from './storyStore.js';
import { generateMockDmTurn } from './mockDm.js';

const port = Number(process.env.PORT || 3000);

function sendJson(res, status, payload) {
  res.writeHead(status, { 'content-type': 'application/json; charset=utf-8' });
  res.end(JSON.stringify(payload, null, 2));
}

function notFound(res) {
  sendJson(res, 404, { error: 'Not found' });
}

function parseBody(req) {
  return new Promise((resolve, reject) => {
    let data = '';
    req.on('data', (chunk) => {
      data += chunk;
      if (data.length > 1_000_000) {
        reject(new Error('Request body too large'));
      }
    });
    req.on('end', () => {
      try {
        resolve(data ? JSON.parse(data) : {});
      } catch {
        reject(new Error('Invalid JSON'));
      }
    });
    req.on('error', reject);
  });
}

function renderAppShell() {
  return `<!doctype html>
<html>
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>Croatian App — RP Vertical Slice</title>
<style>
  :root { color-scheme: dark; }
  body { margin: 0; font-family: Inter, system-ui, sans-serif; background: #0f1115; color: #e9eef5; }
  .top { display:flex; gap:12px; align-items:center; padding:12px 16px; border-bottom:1px solid #262b35; }
  .top input,.top select,.top button, textarea { background:#161b23; border:1px solid #303848; color:#e9eef5; border-radius:8px; padding:8px; }
  .top button { cursor:pointer; }
  .layout { display:grid; grid-template-columns: 1fr 1fr; height: calc(100vh - 62px); }
  .pane { padding:12px; overflow:auto; }
  .pane + .pane { border-left:1px solid #262b35; }
  .entry { border:1px solid #2f3847; border-radius:10px; padding:10px; margin-bottom:10px; background:#141922; }
  .msg { margin-bottom:10px; padding:10px; border-radius:8px; }
  .msg.user { background:#1f2d1f; }
  .msg.assistant { background:#1a2232; }
  .chatInput { position: sticky; bottom:0; background:#0f1115; padding-top:10px; }
  textarea { width:100%; min-height:84px; }
  .muted { color:#9fb0c7; font-size:12px; }
</style>
</head>
<body>
  <div class="top">
    <strong>RP Prototype</strong>
    <label>Session: <select id="sessionSelect"></select></label>
    <input id="newStoryTitle" placeholder="new story title" />
    <button id="newStoryBtn">New Story</button>
    <button id="refreshBtn">Refresh</button>
    <span class="muted">Login/Logout placeholder (top bar reserved)</span>
  </div>
  <div class="layout">
    <section class="pane" id="codexPane"><h2>Codex</h2><div id="codexEntries"></div></section>
    <section class="pane" id="chatPane">
      <h2>Chat</h2>
      <div id="messages"></div>
      <div class="chatInput">
        <textarea id="userInput" placeholder="Try: I ask the guard for a deal."></textarea>
        <button id="sendBtn">Send</button>
      </div>
    </section>
  </div>
<script>
async function api(path, options = {}) {
  const res = await fetch(path, { headers: { 'content-type': 'application/json' }, ...options });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

let currentSessionId = null;

function renderMessages(messages) {
  const box = document.getElementById('messages');
  box.innerHTML = messages.map((m) => {
    const safeText = m.text.replaceAll('<', '&lt;');
    return '<div class="msg ' + m.role + '"><strong>' + m.role + '</strong><div>' + safeText + '</div><div class="muted">' + m.createdAt + '</div></div>';
  }).join('');
}

function renderCodex(entries) {
  const box = document.getElementById('codexEntries');
  if (!entries.length) {
    box.innerHTML = '<p class="muted">No codex entries yet. Story facts appear here as canon is accepted.</p>';
    return;
  }
  box.innerHTML = entries.map((e) => {
    const safeBody = e.body.replaceAll('<', '&lt;');
    return '<article class="entry"><h3>' + e.title + '</h3><pre style="white-space:pre-wrap">' + safeBody + '</pre><div class="muted">updated ' + e.updatedAt + '</div></article>';
  }).join('');
}

async function loadSession(sessionId) {
  currentSessionId = sessionId;
  const [messages, codex] = await Promise.all([
    api('/api/sessions/' + sessionId + '/chat'),
    api('/api/sessions/' + sessionId + '/codex')
  ]);
  renderMessages(messages.messages);
  renderCodex(codex.codex);
}

async function refreshSessions() {
  const { sessions } = await api('/api/sessions');
  const sel = document.getElementById('sessionSelect');
  sel.innerHTML = sessions.map((s) => '<option value="' + s.id + '">' + s.title + ' (' + s.id + ')</option>').join('');
  if (!sessions.length) {
    const created = await api('/api/sessions', { method:'POST', body: JSON.stringify({ title: 'Demo Story' }) });
    return refreshSessions(created.session.id);
  }
  if (!currentSessionId || !sessions.find(s => s.id === currentSessionId)) currentSessionId = sessions[0].id;
  sel.value = currentSessionId;
  await loadSession(currentSessionId);
}

document.getElementById('sessionSelect').addEventListener('change', async (e) => {
  await loadSession(e.target.value);
});

document.getElementById('newStoryBtn').addEventListener('click', async () => {
  const title = document.getElementById('newStoryTitle').value || 'New Story';
  const { session } = await api('/api/sessions', { method:'POST', body: JSON.stringify({ title }) });
  currentSessionId = session.id;
  await refreshSessions();
});

document.getElementById('refreshBtn').addEventListener('click', refreshSessions);

document.getElementById('sendBtn').addEventListener('click', async () => {
  const text = document.getElementById('userInput').value.trim();
  if (!text || !currentSessionId) return;
  document.getElementById('userInput').value = '';
  await api('/api/sessions/' + currentSessionId + '/turn', { method:'POST', body: JSON.stringify({ userText: text }) });
  await loadSession(currentSessionId);
});

refreshSessions();
</script>
</body>
</html>`;
}

const server = http.createServer(async (req, res) => {
  const url = new URL(req.url, `http://${req.headers.host}`);

  if (req.method === 'GET' && url.pathname === '/') {
    res.writeHead(200, { 'content-type': 'text/html; charset=utf-8' });
    res.end(renderAppShell());
    return;
  }

  if (req.method === 'GET' && url.pathname === '/api/sessions') {
    sendJson(res, 200, { sessions: listSessions() });
    return;
  }

  if (req.method === 'POST' && url.pathname === '/api/sessions') {
    try {
      const body = await parseBody(req);
      const session = createSession({ title: body.title || 'New Story' });
      sendJson(res, 201, { session });
    } catch (error) {
      sendJson(res, 400, { error: error.message });
    }
    return;
  }

  const sessionCodex = url.pathname.match(/^\/api\/sessions\/([^/]+)\/codex$/);
  if (req.method === 'GET' && sessionCodex) {
    const sessionId = sessionCodex[1];
    const session = getSession(sessionId);
    if (!session) return notFound(res);
    sendJson(res, 200, { session, codex: getCodex(sessionId) });
    return;
  }

  const sessionChat = url.pathname.match(/^\/api\/sessions\/([^/]+)\/chat$/);
  if (req.method === 'GET' && sessionChat) {
    const sessionId = sessionChat[1];
    const session = getSession(sessionId);
    if (!session) return notFound(res);
    sendJson(res, 200, { session, messages: getMessages(sessionId) });
    return;
  }

  const sessionTurn = url.pathname.match(/^\/api\/sessions\/([^/]+)\/turn$/);
  if (req.method === 'POST' && sessionTurn) {
    const sessionId = sessionTurn[1];
    const session = getSession(sessionId);
    if (!session) return notFound(res);

    try {
      const body = await parseBody(req);
      const userText = body.userText?.trim();
      if (!userText) return sendJson(res, 400, { error: 'userText is required' });

      const recentMessages = getMessages(sessionId).slice(-12);
      const codexEntries = getCodex(sessionId);
      const promptSummary = {
        recentMessages: recentMessages.length,
        codexEntries: codexEntries.length,
        mode: 'mock'
      };

      const dmResult = generateMockDmTurn({ session, userText, codexEntries, recentMessages });
      const result = saveTurn({ sessionId, userText, dmResult, promptSummary });

      sendJson(res, 200, {
        sessionId,
        assistantText: dmResult.assistantText,
        codex: result.codex,
        acceptedCanon: result.acceptedCanon
      });
    } catch (error) {
      sendJson(res, 400, { error: error.message });
    }

    return;
  }

  notFound(res);
});

server.listen(port, () => {
  console.log(`RP prototype listening on http://localhost:${port}`);
});
