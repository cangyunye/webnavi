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

function go(url) {
  const base = window.location.origin;
  if (location.href === base + '/' + url || location.href === base + '/frontend/' + url) {
    location.reload();
  } else {
    location.href = url;
  }
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

let _themeOptionsCache = null;

async function getThemeOptions() {
  if (_themeOptionsCache) return _themeOptionsCache;
  try {
    const opts = await apiRequest('/enum-items/resource_theme/options-full');
    _themeOptionsCache = {};
    opts.forEach(o => { _themeOptionsCache[o.value] = o; });
    return _themeOptionsCache;
  } catch {
    return {};
  }
}

function getAvatarInitial(name) {
  if (!name) return '?';
  const ch = name[0];
  return /[a-zA-Z]/.test(ch) ? ch.toUpperCase() : ch;
}

function applyThemeToCard(el, themeKey, themeOptions) {
  const theme = themeOptions[themeKey];
  if (theme && themeKey !== 'default') {
    const color = theme.color;
    const r = parseInt(color.slice(1,3), 16);
    const g = parseInt(color.slice(3,5), 16);
    const b = parseInt(color.slice(5,7), 16);
    el.style.setProperty('--card-accent', color);
    el.style.setProperty('--card-glow-soft', `rgba(${r},${g},${b},0.08)`);
    el.style.setProperty('--card-glow-strong', `rgba(${r},${g},${b},0.2)`);
    el.style.setProperty('--avatar-text', '#fff');
  } else {
    el.style.removeProperty('--card-accent');
    el.style.removeProperty('--card-glow-soft');
    el.style.removeProperty('--card-glow-strong');
    el.style.removeProperty('--avatar-text');
  }
}

function openThemeSelector(anchorEl, resourceId, currentThemeKey, themeOptions, onUpdated) {
  closeThemeSelector();
  const rect = anchorEl.getBoundingClientRect();
  const sel = document.createElement('div');
  sel.className = 'theme-selector';
  sel.id = 'activeThemeSelector';
  sel.style.position = 'fixed';
  sel.style.left = rect.left + 'px';
  sel.style.top = (rect.bottom + 4) + 'px';
  sel.style.zIndex = 9999;

  const keys = ['default', 'red', 'blue', 'green', 'yellow', 'purple', 'orange', 'teal', 'pink', 'gray'];
  keys.forEach(key => {
    const opt = themeOptions[key];
    if (!opt) return;
    const item = document.createElement('div');
    item.className = 'theme-selector-item' + (key === (currentThemeKey || 'default') ? ' active' : '');
    const dot = document.createElement('span');
    dot.className = 'theme-selector-dot' + (key === 'default' ? ' default' : '');
    if (key !== 'default') dot.style.background = opt.color;
    const label = document.createElement('span');
    label.className = 'theme-selector-label';
    label.textContent = opt.label;
    item.appendChild(dot);
    item.appendChild(label);
    if (key === (currentThemeKey || 'default')) {
      const check = document.createElement('span');
      check.className = 'theme-selector-check';
      check.textContent = '✓';
      item.appendChild(check);
    }
    item.addEventListener('click', async (e) => {
      e.preventDefault();
      e.stopPropagation();
      try {
        await apiRequest(`/resource-themes/${resourceId}`, {
          method: 'PUT',
          body: JSON.stringify({ theme_key: key })
        });
        closeThemeSelector();
        if (onUpdated) onUpdated(resourceId, key);
      } catch (err) { alert(err.message); }
    });
    sel.appendChild(item);
  });

  document.body.appendChild(sel);

  setTimeout(() => {
    document.addEventListener('click', _closeThemeSelectorOnClick);
  }, 0);
}

function _closeThemeSelectorOnClick(e) {
  const sel = document.getElementById('activeThemeSelector');
  if (sel && !sel.contains(e.target)) closeThemeSelector();
}

function closeThemeSelector() {
  const sel = document.getElementById('activeThemeSelector');
  if (sel) sel.remove();
  document.removeEventListener('click', _closeThemeSelectorOnClick);
}
