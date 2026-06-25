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
