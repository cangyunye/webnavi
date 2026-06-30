/* ---- Search: pure functions ---- */
const PUBLIC_CAT_IDS = { 1:'学习', 4:'AI', 5:'测试', 6:'软件资源', 8:'工具' };

function filterResources(resources, query) {
  if (!query) return resources;
  const q = query.toLowerCase();
  return resources.filter(r =>
    (r.name && r.name.toLowerCase().includes(q)) ||
    (r.url && r.url.toLowerCase().includes(q)) ||
    (r.description && r.description.toLowerCase().includes(q))
  );
}

function setCachedData(data) {
  try {
    localStorage.setItem('rn_cache', JSON.stringify(data));
    localStorage.setItem('rn_cache_ts', String(Date.now()));
  } catch {}
}

function getCachedData() {
  try {
    const raw = localStorage.getItem('rn_cache');
    const ts = localStorage.getItem('rn_cache_ts');
    if (!raw || !ts) return null;
    if (Date.now() - Number(ts) > 2 * 60 * 60 * 1000) {
      clearCache();
      return null;
    }
    return JSON.parse(raw);
  } catch { return null; }
}

function clearCache() {
  localStorage.removeItem('rn_cache');
  localStorage.removeItem('rn_cache_ts');
}

function filterByPermission(resources, user) {
  if (!user || user.role === 'admin' || user.role === 'ops_expert') return resources;
  return resources.filter(r => PUBLIC_CAT_IDS[r.category_id]);
}

function filterUsers(users, query, roleFilter) {
  let filtered = users;
  if (query) {
    const q = query.toLowerCase();
    filtered = filtered.filter(u =>
      (u.username && u.username.toLowerCase().includes(q)) ||
      (u.email && u.email.toLowerCase().includes(q))
    );
  }
  if (roleFilter) {
    filtered = filtered.filter(u => u.role === roleFilter);
  }
  return filtered;
}
