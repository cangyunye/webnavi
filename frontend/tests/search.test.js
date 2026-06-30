const assert = require('assert');

// Polyfill localStorage for Node.js
global.localStorage = { _d: {}, getItem(k) { return this._d[k] ?? null; }, setItem(k, v) { this._d[k] = String(v); }, removeItem(k) { delete this._d[k]; } };

// Load search module (evaluate in Node context)
const fs = require('fs');
const vm = require('vm');
const code = fs.readFileSync(__dirname + '/../js/search.js', 'utf8');
vm.createContext({ PUBLIC_CAT_IDS: { 1:'学习',4:'AI',5:'测试',6:'软件资源',8:'工具' }, localStorage: global.localStorage });
vm.runInNewContext(code, global);

// ---- Test data ----
const MOCK_RESOURCES = [
  { id:1, category_id:1, name:'GitHub', url:'https://github.com', description:'代码托管平台' },
  { id:2, category_id:1, name:'MDN', url:'https://developer.mozilla.org', description:'Web技术文档' },
  { id:3, category_id:8, name:'wttr.in', url:'https://wttr.in', description:'天气预报' },
  { id:4, category_id:4, name:'OpenAI', url:'https://openai.com', description:'人工智能研究' },
  { id:5, category_id:7, name:'Grafana', url:'https://grafana.com', description:'监控可视化' },
  { id:6, category_id:6, name:'VS Code', url:'https://code.visualstudio.com', description:'代码编辑器' },
  { id:7, category_id:4, name:'Hugging Face', url:'https://huggingface.co', description:'AI模型社区' },
  { id:8, category_id:5, name:'Postman', url:'https://postman.com', description:'API测试工具' },
];

const USERS = [
  { id:1, username:'admin', email:'admin@example.com', role:'admin' },
  { id:2, username:'zhangsan', email:'zhang@example.com', role:'registered' },
  { id:3, username:'mentor', email:'mentor@example.com', role:'learning_mentor' },
  { id:4, username:'expert', email:'expert@example.com', role:'ops_expert' },
];

// ===== filterResources =====
// #1
assert.equal(filterResources(MOCK_RESOURCES, '').length, 8, '#1 empty query returns all');

// #2
const gitResult = filterResources(MOCK_RESOURCES, 'git');
assert.equal(gitResult.length, 1, '#2 name match');
assert.equal(gitResult[0].name, 'GitHub', '#2 match GitHub');

// #3
const urlResult = filterResources(MOCK_RESOURCES, 'openai.com');
assert.equal(urlResult.length, 1, '#3 url match');
assert.equal(urlResult[0].name, 'OpenAI', '#3 match OpenAI');

// #4
const descResult = filterResources(MOCK_RESOURCES, '监控');
assert.equal(descResult.length, 1, '#4 description match');
assert.equal(descResult[0].name, 'Grafana', '#4 match Grafana');

// #5
const caseResult = filterResources(MOCK_RESOURCES, 'GITHUB');
assert.equal(caseResult.length, 1, '#5 case insensitive');

// #6
const partialResult = filterResources(MOCK_RESOURCES, '.com');
assert.ok(partialResult.length >= 5, '#6 partial match .com');

// #7
assert.equal(filterResources(MOCK_RESOURCES, 'zzznotexist').length, 0, '#7 no match');

// #8
const codeResult = filterResources(MOCK_RESOURCES, 'code');
assert.equal(codeResult.length, 1, '#8 code matches VS Code only');
assert.equal(codeResult[0].name, 'VS Code', '#8 vs code');

// ===== Cache =====
// #9
const testData = [{ id:1, name:'test' }];
localStorage.removeItem('rn_cache');
localStorage.removeItem('rn_cache_ts');
setCachedData(testData);
assert.deepEqual(getCachedData(), testData, '#9 set then get');

// #10
localStorage.setItem('rn_cache_ts', String(Date.now() - 60 * 60 * 1000)); // 1h ago
assert.deepEqual(getCachedData(), testData, '#10 cache not expired');

// #11
localStorage.setItem('rn_cache_ts', String(Date.now() - 3 * 60 * 60 * 1000)); // 3h ago
assert.equal(getCachedData(), null, '#11 expired cache returns null');

// #12
localStorage.removeItem('rn_cache');
localStorage.removeItem('rn_cache_ts');
assert.equal(getCachedData(), null, '#12 no cache returns null');

// #13
localStorage.setItem('rn_cache', 'not-json');
localStorage.setItem('rn_cache_ts', String(Date.now()));
assert.equal(getCachedData(), null, '#13 corrupted data returns null');

// ===== filterByPermission =====
// #14 guest
assert.equal(filterByPermission(MOCK_RESOURCES, { role:'guest' }).length, 7, '#14 guest excludes 运维');

// #15 learning_mentor — only PUBLIC
const lmResult = filterByPermission(MOCK_RESOURCES, { role:'learning_mentor' });
const lmCatIds = lmResult.map(r => r.category_id);
assert.ok(!lmCatIds.includes(7), '#15 learning_mentor excludes 运维');
assert.equal(lmResult.length, 7, '#15 learning_mentor sees 7 public resources');

// #16 admin — all
assert.equal(filterByPermission(MOCK_RESOURCES, { role:'admin' }).length, 8, '#16 admin sees all');

// #17 registered — same as guest
assert.equal(filterByPermission(MOCK_RESOURCES, { role:'registered' }).length, 7, '#17 registered excludes 运维');

// #18 guest sees public tools
const guestResult = filterByPermission(MOCK_RESOURCES, { role:'guest' });
const tool = guestResult.find(r => r.name === 'wttr.in');
assert.ok(tool, '#18 guest sees public category');

// #19 ops_expert — all
assert.equal(filterByPermission(MOCK_RESOURCES, { role:'ops_expert' }).length, 8, '#19 ops_expert sees all');

// ===== filterUsers =====
// #20
assert.equal(filterUsers(USERS, 'admin').length, 1, '#20 username search');
assert.equal(filterUsers(USERS, 'ADMIN').length, 1, '#20 username case insensitive');

// #21
const emailResult = filterUsers(USERS, '@example.com');
assert.equal(emailResult.length, 4, '#21 email partial match');

// #22
assert.equal(filterUsers(USERS, '').length, 4, '#22 empty query returns all');

// #23 role filter
assert.equal(filterUsers(USERS, '', 'admin').length, 1, '#23 role filter admin');
assert.equal(filterUsers(USERS, '', 'registered').length, 1, '#23 role filter registered');

// #24 combined
assert.equal(filterUsers(USERS, 'mentor', 'learning_mentor').length, 1, '#24 combined query + role');
assert.equal(filterUsers(USERS, 'mentor', 'admin').length, 0, '#24 combined mismatch');

console.log('All', 24, 'tests passed');
