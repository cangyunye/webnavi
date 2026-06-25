const API_BASE = '/api';

function getToken() {
  return localStorage.getItem('rn_token');
}

function getUser() {
  try {
    const u = localStorage.getItem('rn_user');
    return u ? JSON.parse(u) : null;
  } catch { return null; }
}

function setAuth(token, user) {
  if (token) localStorage.setItem('rn_token', token);
  if (user) localStorage.setItem('rn_user', JSON.stringify(user));
}

function clearAuth() {
  localStorage.removeItem('rn_token');
  localStorage.removeItem('rn_user');
}

function logout() {
  clearAuth();
  location.href = 'index.html';
}

/* ---- Theme ---- */
function themeIcon() { return document.documentElement.classList.contains('dark-theme') ? '☀️' : '🌙'; }

function initTheme() {
  const saved = localStorage.getItem('rn_theme');
  if (saved === 'dark') document.documentElement.classList.add('dark-theme');
  document.querySelectorAll('.theme-toggle').forEach(el => el.textContent = saved === 'dark' ? '☀️' : '🌙');
}

function toggleTheme() {
  document.documentElement.classList.toggle('dark-theme');
  const isDark = document.documentElement.classList.contains('dark-theme');
  localStorage.setItem('rn_theme', isDark ? 'dark' : 'light');
  // Update all toggle buttons on the page
  document.querySelectorAll('.theme-toggle').forEach(el => el.textContent = isDark ? '☀️' : '🌙');
}

async function apiRequest(url, options = {}) {
  const token = getToken();
  const headers = { ...options.headers };
  if (token) headers['Authorization'] = `Bearer ${token}`;
  if (options.body && !(options.body instanceof FormData)) {
    headers['Content-Type'] = 'application/json';
  }
  const res = await fetch(API_BASE + url, { ...options, headers });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: '请求失败' }));
    throw new Error(err.detail || `HTTP ${res.status}`);
  }
  const ct = res.headers.get('content-type') || '';
  if (ct.includes('application/json')) return res.json();
  return res.text();
}
