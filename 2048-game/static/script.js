/* ── State ─────────────────────────────────────────────────────── */
let board = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]];
let score = 0;
let highScore = 0;
let gameOver = false;
let autoplay = false;
let autoplayTimer = null;

/* ── DOM refs ─────────────────────────────────────────────────── */
const boardEl = document.getElementById('board');
const scoreEl = document.getElementById('score');
const highScoreEl = document.getElementById('high-score');
const finalScoreEl = document.getElementById('final-score');
const gameOverOverlay = document.getElementById('game-over-overlay');
const aiStatusEl = document.getElementById('ai-status');
const depthSlider = document.getElementById('depth-slider');
const depthValue  = document.getElementById('depth-value');
const aiMoveBtn   = document.getElementById('ai-move-btn');
const aiAutoplayBtn = document.getElementById('ai-autoplay-btn');
const resetBtn    = document.getElementById('restart-btn');

/* ── Render ───────────────────────────────────────────────────── */
const TILE_COLORS = {
  0: 'tile-0', 2: 'tile-2', 4: 'tile-4', 8: 'tile-8',
  16: 'tile-16', 32: 'tile-32', 64: 'tile-64', 128: 'tile-128',
  256: 'tile-256', 512: 'tile-512', 1024: 'tile-1024', 2048: 'tile-2048',
};

function tileClass(value) {
  return TILE_COLORS[value] || 'tile-super';
}

function render() {
  boardEl.innerHTML = '';
  for (let i = 0; i < 4; i++) {
    for (let j = 0; j < 4; j++) {
      const val = board[i][j];
      const div = document.createElement('div');
      div.className = `tile ${tileClass(val)}`;
      if (val) div.textContent = val;
      boardEl.appendChild(div);
    }
  }
  scoreEl.textContent = score;
  highScoreEl.textContent = highScore;
  if (gameOver) {
    finalScoreEl.textContent = score;
    gameOverOverlay.classList.remove('hidden');
  } else {
    gameOverOverlay.classList.add('hidden');
  }
}

/* ── API helpers ──────────────────────────────────────────────── */
async function fetchState() {
  const res = await fetch('/api/state');
  const data = await res.json();
  board = data.board;
  score = data.score;
  highScore = data.highScore;
  gameOver = data.gameOver;
  render();
}

async function move(direction) {
  const res = await fetch('/api/move', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ direction }),
  });
  const data = await res.json();
  if (data.error) { console.error(data.error); return; }
  board = data.board;
  score = data.score;
  highScore = data.highScore;
  gameOver = data.gameOver;
  render();
  return data;
}

async function aiMove(depth) {
  aiStatusEl.textContent = '🤖 AI thinking…';
  aiMoveBtn.disabled = true;
  const res = await fetch('/api/ai-move', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ depth }),
  });
  const data = await res.json();
  aiMoveBtn.disabled = false;
  if (data.error) { aiStatusEl.textContent = `Error: ${data.error}`; return data; }
  board = data.board;
  score = data.score;
  highScore = data.highScore;
  gameOver = data.gameOver;
  render();
  if (data.aiMove) {
    aiStatusEl.textContent = `🤖 AI played: ${data.aiMove}  (heuristic score: ${Math.round(data.aiScore)})`;
  } else if (gameOver) {
    aiStatusEl.textContent = '🤖 Game over — no moves left.';
  }
  return data;
}

async function resetGame() {
  if (autoplay) stopAutoplay();
  const res = await fetch('/api/reset', { method: 'POST' });
  const data = await res.json();
  board = data.board;
  score = data.score;
  highScore = data.highScore;
  gameOver = data.gameOver;
  aiStatusEl.textContent = '';
  render();
}

/* ── Autoplay ─────────────────────────────────────────────────── */
function startAutoplay() {
  if (autoplay) return;
  autoplay = true;
  aiAutoplayBtn.textContent = '⏹ Stop AI';
  aiAutoplayBtn.classList.add('running');
  aiMoveBtn.disabled = true;
  tickAutoplay();
}

function stopAutoplay() {
  autoplay = false;
  clearTimeout(autoplayTimer);
  aiAutoplayBtn.textContent = '▶ AI Autoplay';
  aiAutoplayBtn.classList.remove('running');
  aiMoveBtn.disabled = false;
}

async function tickAutoplay() {
  if (!autoplay || gameOver) {
    if (gameOver) stopAutoplay();
    return;
  }
  const depth = parseInt(depthSlider.value, 10);
  const data = await aiMove(depth);
  if (data && data.gameOver) {
    stopAutoplay();
    return;
  }
  if (autoplay) {
    autoplayTimer = setTimeout(tickAutoplay, 200);
  }
}

/* ── Keyboard ─────────────────────────────────────────────────── */
document.addEventListener('keydown', (e) => {
  const keyMap = {
    ArrowUp: 'UP', ArrowDown: 'DOWN', ArrowLeft: 'LEFT', ArrowRight: 'RIGHT',
    w: 'UP', s: 'DOWN', a: 'LEFT', d: 'RIGHT',
    W: 'UP', S: 'DOWN', A: 'LEFT', D: 'RIGHT',
  };
  const dir = keyMap[e.key];
  if (dir) {
    e.preventDefault();
    if (gameOver) return;
    if (autoplay) stopAutoplay();
    move(dir);
  }
  if (e.key === 'Enter' && gameOver) resetGame();
});

/* ── Touch / swipe ────────────────────────────────────────────── */
let touchStartX = 0, touchStartY = 0;
document.addEventListener('touchstart', (e) => {
  touchStartX = e.touches[0].clientX;
  touchStartY = e.touches[0].clientY;
}, { passive: true });

document.addEventListener('touchend', (e) => {
  const dx = e.changedTouches[0].clientX - touchStartX;
  const dy = e.changedTouches[0].clientY - touchStartY;
  const absDx = Math.abs(dx), absDy = Math.abs(dy);
  if (Math.max(absDx, absDy) < 30) return; // too short
  if (gameOver) return;
  if (autoplay) stopAutoplay();
  if (absDx > absDy) {
    move(dx > 0 ? 'RIGHT' : 'LEFT');
  } else {
    move(dy > 0 ? 'DOWN' : 'UP');
  }
}, { passive: true });

/* ── Button events ────────────────────────────────────────────── */
aiMoveBtn.addEventListener('click', () => {
  if (gameOver) { resetGame(); return; }
  if (autoplay) stopAutoplay();
  const depth = parseInt(depthSlider.value, 10);
  aiMove(depth);
});

aiAutoplayBtn.addEventListener('click', () => {
  if (autoplay) { stopAutoplay(); return; }
  if (gameOver) { resetGame(); setTimeout(startAutoplay, 100); return; }
  startAutoplay();
});

resetBtn.addEventListener('click', resetGame);
document.getElementById('reset-btn')?.addEventListener('click', resetGame);

depthSlider.addEventListener('input', () => {
  depthValue.textContent = depthSlider.value;
});

/* ── Init ─────────────────────────────────────────────────────── */
fetchState();