const API_BASE = '/api';

const CATEGORY_ICONS = {
    '学习': '📚',
    '数据库': '🗄️',
    '研发机器': '🖥️',
    'AI': '🤖',
    '测试': '🧪',
    '软件资源': '💿',
    '运维': '⚙️',
    '工具': '🛠️'
};

const SITE_ICONS = {
    'GitHub': '🐙',
    'Stack Overflow': '🟨',
    'MDN Web Docs': '📘',
    '菜鸟教程': '📗',
    'LeetCode': '🔴',
    'Codecademy': '💚',
    'OpenAI': '🤖',
    'Hugging Face': '🤗',
    'Stable Diffusion': '🎨',
    'MidJourney': '✨',
    'Claude': '🔷',
    'Perplexity': '🔍',
    'VS Code': '💻',
    'Docker': '🐳',
    'Notion': '📝',
    'Figma': '🎯',
    'Chrome': '🌐',
    'wttr.in': '🌤️',
    'Public APIs': '🔌',
    'Papers With Code': '📄',
    'Hugging Face Datasets': '🤗',
    'DevDocs': '📖'
};

let categories = [];
let currentCategory = null;
let currentResources = [];
let currentUser = null;

async function apiRequest(url, options = {}) {
    const token = localStorage.getItem('token');
    if (token) {
        options.headers = {
            ...options.headers,
            'Authorization': `Bearer ${token}`
        };
    }
    if (options.body && !(options.body instanceof FormData)) {
        options.headers = {
            ...options.headers,
            'Content-Type': 'application/json'
        };
    }

    const response = await fetch(url, options);
    if (!response.ok) {
        const error = await response.json().catch(() => ({}));
        throw new Error(error.detail || '请求失败');
    }
    return response.json();
}

async function login(username, password) {
    const formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);

    const response = await fetch(`${API_BASE}/auth/login`, {
        method: 'POST',
        body: formData
    });

    if (!response.ok) {
        throw new Error('登录失败');
    }

    const data = await response.json();
    localStorage.setItem('token', data.access_token);
    currentUser = data.user;
    updateAuthUI();
    return data;
}

async function register(username, password, email) {
    const response = await fetch(`${API_BASE}/auth/register`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            username: username,
            password: password,
            email: email
        })
    });

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || '注册失败');
    }

    const data = await response.json();
    localStorage.setItem('token', data.access_token);
    currentUser = data.user;
    updateAuthUI();
    return data;
}

async function guestLogin() {
    const response = await fetch(`${API_BASE}/auth/guest`, {
        method: 'POST'
    });
    if (!response.ok) throw new Error('访客登录失败');
    const data = await response.json();
    localStorage.setItem('token', data.access_token);
    currentUser = data.user;
    updateAuthUI();
    return data;
}

function logout() {
    localStorage.removeItem('token');
    currentUser = null;
    updateAuthUI();
    renderHomePage();
}

function updateAuthUI() {
    const authContainer = document.getElementById('auth-container');
    if (!authContainer) return;

    if (currentUser) {
        authContainer.innerHTML = `
            <span class="user-info">
                <span class="user-role">${currentUser.role === 'admin' ? '管理员' : currentUser.role === 'registered' ? '注册用户' : '访客'}</span>
                <span class="user-name">${currentUser.username}</span>
            </span>
            <button class="btn-logout" onclick="logout()">退出</button>
        `;
    } else {
        authContainer.innerHTML = `
            <button class="btn-guest" onclick="showGuestLogin()">访客</button>
            <button class="btn-login" onclick="showLoginModal()">登录</button>
            <button class="btn-register" onclick="showRegisterModal()">注册</button>
        `;
    }
}

function showGuestLogin() {
    guestLogin().then(() => {
        fetchCategories();
    }).catch(error => {
        alert(error.message);
    });
}

function showLoginModal() {
    const modal = document.createElement('div');
    modal.className = 'modal-overlay';
    modal.id = 'login-modal';
    modal.innerHTML = `
        <div class="modal-content" onclick="event.stopPropagation()">
            <h2 class="modal-header">用户登录</h2>
            <div class="form-group">
                <label class="form-label">用户名</label>
                <input type="text" class="form-input" id="login-username" placeholder="请输入用户名">
            </div>
            <div class="form-group">
                <label class="form-label">密码</label>
                <input type="password" class="form-input" id="login-password" placeholder="请输入密码">
            </div>
            <div class="modal-actions">
                <button class="btn btn-cancel" onclick="closeLoginModal()">取消</button>
                <button class="btn btn-primary" onclick="handleLogin()">登录</button>
            </div>
            <p class="modal-footer">还没有账号？ <a href="#" onclick="closeLoginModal();showRegisterModal();">立即注册</a></p>
        </div>
    `;
    modal.addEventListener('click', () => closeLoginModal());
    document.body.appendChild(modal);
}

function closeLoginModal() {
    const modal = document.getElementById('login-modal');
    if (modal) modal.remove();
}

function handleLogin() {
    const username = document.getElementById('login-username').value;
    const password = document.getElementById('login-password').value;
    if (!username || !password) {
        alert('请填写用户名和密码');
        return;
    }

    login(username, password).then(() => {
        closeLoginModal();
        fetchCategories();
    }).catch(error => {
        alert(error.message);
    });
}

function showRegisterModal() {
    const modal = document.createElement('div');
    modal.className = 'modal-overlay';
    modal.id = 'register-modal';
    modal.innerHTML = `
        <div class="modal-content" onclick="event.stopPropagation()">
            <h2 class="modal-header">用户注册</h2>
            <div class="form-group">
                <label class="form-label">用户名</label>
                <input type="text" class="form-input" id="register-username" placeholder="请输入用户名">
            </div>
            <div class="form-group">
                <label class="form-label">邮箱 (可选)</label>
                <input type="email" class="form-input" id="register-email" placeholder="请输入邮箱">
            </div>
            <div class="form-group">
                <label class="form-label">密码</label>
                <input type="password" class="form-input" id="register-password" placeholder="至少6位密码">
            </div>
            <div class="form-group">
                <label class="form-label">确认密码</label>
                <input type="password" class="form-input" id="register-confirm" placeholder="再次输入密码">
            </div>
            <div class="modal-actions">
                <button class="btn btn-cancel" onclick="closeRegisterModal()">取消</button>
                <button class="btn btn-primary" onclick="handleRegister()">注册</button>
            </div>
        </div>
    `;
    modal.addEventListener('click', () => closeRegisterModal());
    document.body.appendChild(modal);
}

function closeRegisterModal() {
    const modal = document.getElementById('register-modal');
    if (modal) modal.remove();
}

function handleRegister() {
    const username = document.getElementById('register-username').value;
    const email = document.getElementById('register-email').value;
    const password = document.getElementById('register-password').value;
    const confirm = document.getElementById('register-confirm').value;

    if (!username || !password) {
        alert('请填写用户名和密码');
        return;
    }

    if (password !== confirm) {
        alert('两次输入的密码不一致');
        return;
    }

    register(username, password, email).then(() => {
        closeRegisterModal();
        fetchCategories();
    }).catch(error => {
        alert(error.message);
    });
}

function checkCategoryPermission(categoryName) {
    const guest_categories = ['学习', 'AI', '软件资源', '测试', '工具'];
    
    if (!currentUser || currentUser.role === 'guest') {
        return guest_categories.includes(categoryName);
    }
    
    if (currentUser.role === 'admin') {
        return true;
    }
    
    if (currentUser.role === 'registered') {
        if (!currentUser.permissions || currentUser.permissions.length === 0) {
            return true;
        }
        return currentUser.permissions.some(p => p.category_name === categoryName);
    }
    
    return false;
}

async function fetchCategories() {
    try {
        const response = await apiRequest(`${API_BASE}/categories`);
        categories = response;
        renderNavMenu();
        renderHomePage();
    } catch (error) {
        console.error('Error fetching categories:', error);
    }
}

function renderNavMenu() {
    const navMenu = document.getElementById('nav-menu');
    let menuHtml = categories.map(cat => {
        const hasPermission = checkCategoryPermission(cat.name);
        const disabledClass = !hasPermission ? 'nav-item-disabled' : '';
        return `
            <div class="nav-item ${disabledClass}" data-id="${cat.id}" data-name="${cat.name}"
                onclick="${hasPermission ? `selectCategory(this)` : `showLoginRequired()`}">
                <span class="nav-icon">${CATEGORY_ICONS[cat.name] || '📂'}</span>
                <span class="nav-text">${cat.name}</span>
            </div>
        `;
    }).join('');
    
    // 添加 API Key 管理菜单项（所有登录用户可见）
    if (currentUser && currentUser.role !== 'guest') {
        menuHtml += `
            <div class="nav-item" data-name="api_keys" onclick="showApiKeysPage()">
                <span class="nav-icon">🔐</span>
                <span class="nav-text">API Key 管理</span>
            </div>
        `;
    }
    
    // 添加管理菜单项（仅管理员可见）
    if (currentUser && currentUser.role === 'admin') {
        menuHtml += `
            <div class="nav-item" data-name="credentials" onclick="showCredentialsPage()">
                <span class="nav-icon">🔑</span>
                <span class="nav-text">凭据管理</span>
            </div>
            <div class="nav-item" data-name="users" onclick="showUserManagementPage()">
                <span class="nav-icon">👥</span>
                <span class="nav-text">用户管理</span>
            </div>
        `;
    }
    navMenu.innerHTML = menuHtml;
}

function showLoginRequired() {
    alert('此功能需要登录后才能访问，请先登录或注册');
    showLoginModal();
}

function renderHomePage() {
    currentCategory = null;
    document.querySelectorAll('.nav-item').forEach(i => i.classList.remove('active'));
    document.getElementById('page-title').textContent = '资源导航';
    document.getElementById('header-actions').innerHTML = '';
    const contentBody = document.getElementById('content-body');
    
    contentBody.innerHTML = `
        <div class="home-container">
            <div class="home-header">
                <h1 class="home-title">ResourceNav</h1>
                <p class="home-subtitle">选择一个分类开始探索</p>
            </div>
            <div class="card-grid">
                ${categories.map((cat) => {
                    const hasPermission = checkCategoryPermission(cat.name);
                    return `
                        <div class="category-card ${!hasPermission ? 'category-card-disabled' : ''}" data-id="${cat.id}" data-name="${cat.name}"
                            onclick="${hasPermission ? `handleCategoryCardClick(${cat.id},'${cat.name}')` : `showLoginRequired()`}">
                            <div class="card-image">${CATEGORY_ICONS[cat.name] || '📂'}</div>
                            <div class="card-content">
                                <h3 class="card-title">${cat.name}</h3>
                            </div>
                        </div>
                    `;
                }).join('')}
            </div>
        </div>
    `;
}

function handleCategoryCardClick(categoryId, categoryName) {
    const navItems = document.querySelectorAll('.nav-item');
    navItems.forEach(item => {
        if (item.dataset.id === String(categoryId)) {
            selectCategory(item);
        }
    });
}

function selectCategory(item) {
    document.querySelectorAll('.nav-item').forEach(i => i.classList.remove('active'));
    item.classList.add('active');

    const categoryId = item.dataset.id;
    const categoryName = item.dataset.name;
    currentCategory = { id: parseInt(categoryId), name: categoryName };

    document.getElementById('page-title').textContent = categoryName;
    loadCategoryData(categoryId, categoryName);
}

function goHome() {
    renderHomePage();
}

async function loadCategoryData(categoryId, categoryName) {
    const contentBody = document.getElementById('content-body');
    contentBody.innerHTML = '<div class="empty-state"><div class="empty-state-icon">⏳</div><p>加载中...</p></div>';

    try {
        if (categoryName === '研发机器') {
            await loadDevMachines();
        } else if (categoryName === '数据库') {
            await loadDbInstances();
        } else if (['学习', 'AI', '软件资源', '测试', '运维', '工具'].includes(categoryName)) {
            await loadResources(parseInt(categoryId));
        } else {
            contentBody.innerHTML = `
                <div class="welcome-panel">
                    <div class="welcome-icon">📂</div>
                    <h2>${categoryName}</h2>
                    <p>该分类内容正在建设中...</p>
                </div>
            `;
        }
    } catch (error) {
        console.error('Error loading category data:', error);
        contentBody.innerHTML = `
            <div class="empty-state">
                <div class="empty-state-icon">❌</div>
                <p>${error.message}</p>
            </div>
        `;
    }
}

async function loadResources(categoryId) {
    const resources = await apiRequest(`${API_BASE}/resources/${categoryId}`);
    currentResources = resources;
    renderResources(currentResources);
}

function renderResources(resources) {
    const contentBody = document.getElementById('content-body');
    document.getElementById('header-actions').innerHTML = '';

    const canEdit = currentUser && (currentUser.role === 'admin' || currentUser.can_edit);
    const canDelete = currentUser && (currentUser.role === 'admin' || currentUser.can_delete);

    const cardsHtml = resources.map((resource, index) => {
        return `
            <div class="resource-card" data-id="${resource.id}">
                ${canDelete ? `<button class="delete-btn" onclick="deleteResource(event,${resource.id})">×</button>` : ''}
                <a href="${resource.url}" target="_blank" class="resource-card-link">
                    <div class="resource-card-icon">${SITE_ICONS[resource.name] || '🔗'}</div>
                    <div class="resource-card-content">
                        <h3 class="resource-card-title">${resource.name}</h3>
                        <p class="resource-card-desc">${resource.description || ''}</p>
                    </div>
                </a>
            </div>
        `;
    }).join('');

    contentBody.innerHTML = `
        <div class="home-container">
            <div class="resource-card-grid">
                ${cardsHtml}
                ${canEdit ? `
                    <div class="add-card" onclick="openAddModal()">
                        <div class="add-card-icon">➕</div>
                        <div class="add-card-text">添加新资源</div>
                    </div>
                ` : ''}
            </div>
        </div>
    `;
}

function openAddModal() {
    const modal = document.createElement('div');
    modal.className = 'modal-overlay';
    modal.id = 'add-resource-modal';
    modal.innerHTML = `
        <div class="modal-content" onclick="event.stopPropagation()">
            <h2 class="modal-header">添加新资源</h2>
            <div class="form-group">
                <label class="form-label">名称</label>
                <input type="text" class="form-input" id="new-resource-name" placeholder="输入资源名称">
            </div>
            <div class="form-group">
                <label class="form-label">链接</label>
                <input type="url" class="form-input" id="new-resource-url" placeholder="https://example.com">
            </div>
            <div class="form-group">
                <label class="form-label">描述</label>
                <textarea class="form-input form-textarea" id="new-resource-desc" placeholder="输入资源描述"></textarea>
            </div>
            <div class="modal-actions">
                <button class="btn btn-cancel" onclick="closeAddModal()">取消</button>
                <button class="btn btn-primary" onclick="addResource()">添加</button>
            </div>
        </div>
    `;
    modal.addEventListener('click', () => closeAddModal());
    document.body.appendChild(modal);
}

function closeAddModal() {
    const modal = document.getElementById('add-resource-modal');
    if (modal) modal.remove();
}

async function addResource() {
    const name = document.getElementById('new-resource-name').value.trim();
    const url = document.getElementById('new-resource-url').value.trim();
    const description = document.getElementById('new-resource-desc').value.trim();

    if (!name || !url) {
        alert('请填写名称和链接');
        return;
    }

    try {
        await apiRequest(`${API_BASE}/resources`, {
            method: 'POST',
            body: JSON.stringify({
                category_id: currentCategory.id,
                name: name,
                url: url,
                description: description,
                status: 1
            })
        });

        closeAddModal();
        loadResources(currentCategory.id);
    } catch (error) {
        alert('添加失败: ' + error.message);
    }
}

async function deleteResource(event, resourceId) {
    event.stopPropagation();
    
    if (!confirm('确定要删除这个资源吗？')) {
        return;
    }

    try {
        await apiRequest(`${API_BASE}/resources/${resourceId}`, {
            method: 'DELETE'
        });
        
        loadResources(currentCategory.id);
    } catch (error) {
        alert('删除失败: ' + error.message);
    }
}

async function loadDevMachines() {
    const machines = await apiRequest(`${API_BASE}/dev-machines`);
    renderDevMachinesTable(machines);
}

function renderDevMachinesTable(machines) {
    const contentBody = document.getElementById('content-body');
    
    const canEdit = currentUser && (currentUser.role === 'admin' || currentUser.can_edit);
    const canDelete = currentUser && (currentUser.role === 'admin' || currentUser.can_delete);

    document.getElementById('header-actions').innerHTML = canEdit ? `
        <button class="btn btn-primary" onclick="openEditMachinePanel()">添加研发机器</button>
    ` : '';

    const tableHtml = `
        <div class="data-panel">
            <div class="filter-bar">
                <span class="filter-label">环境筛选:</span>
                <select class="filter-select" id="env-filter-bar" onchange="filterDevMachines()">
                    <option value="">全部</option>
                    <option value="dev">开发环境</option>
                    <option value="test">测试环境</option>
                    <option value="prod">生产环境</option>
                </select>
                <span class="filter-label">状态:</span>
                <select class="filter-select" id="status-filter" onchange="filterDevMachines()">
                    <option value="">全部</option>
                    <option value="1">在线</option>
                    <option value="0">离线</option>
                </select>
            </div>
            <div class="data-table-wrapper">
                <table class="data-table" id="machines-table">
                    <thead>
                        <tr>
                            <th>名称</th>
                            <th>IP地址</th>
                            <th>环境</th>
                            <th>状态</th>
                            <th>负责人</th>
                            <th>归属组织</th>
                            <th>CPU</th>
                            <th>内存</th>
                            <th>操作系统</th>
                            <th>操作</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${machines.map(m => `
                            <tr data-env="${m.environment}" data-status="${m.status}">
                                <td><strong>${m.name}</strong></td>
                                <td>${m.ip}:${m.port}</td>
                                <td><span class="env-badge ${m.environment}">${getEnvText(m.environment)}</span></td>
                                <td><span class="status-badge ${m.status === 1 ? 'online' : 'offline'}"><span class="status-dot"></span>${m.status === 1 ? '在线' : '离线'}</span></td>
                                <td>${m.owner_name || '-'}</td>
                                <td>${m.organization_name || '-'}</td>
                                <td>${m.cpu || '-'}</td>
                                <td>${m.memory || '-'}</td>
                                <td>${m.os || '-'}</td>
                                <td>
                                    ${canEdit ? `<button class="btn btn-primary btn-sm" style="margin-right:4px" onclick="openEditMachinePanel(${m.id})">修改</button>` : ''}
                                    ${canDelete ? `<button class="btn btn-danger btn-sm" onclick="deleteDevMachine(${m.id})">删除</button>` : ''}
                                </td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            </div>
        </div>
    `;
    contentBody.innerHTML = tableHtml;
}

function closeSidePanel() {
    const panel = document.getElementById('side-panel');
    if (panel) panel.classList.remove('active');
}

async function openEditMachinePanel(machineId = null) {
    const [organizations, owners] = await Promise.all([
        apiRequest(`${API_BASE}/organizations`),
        apiRequest(`${API_BASE}/owners`)
    ]);
    
    const titleEl = document.getElementById('side-panel-title');
    const bodyEl = document.getElementById('side-panel-body');
    
    const isEdit = machineId !== null;
    const machine = isEdit ? await apiRequest(`${API_BASE}/dev-machines/${machineId}`) : null;
    
    titleEl.textContent = isEdit ? '修改研发机器' : '添加研发机器';
    
    bodyEl.innerHTML = `
        ${isEdit ? `<input type="hidden" id="machine-id" value="${machineId}">` : ''}
        <div class="form-group">
            <label class="form-label">名称 *</label>
            <input type="text" class="form-input" id="machine-name" placeholder="研发机器名称" value="${isEdit ? machine.name : ''}">
        </div>
        <div class="form-group">
            <label class="form-label">IP地址 *</label>
            <input type="text" class="form-input" id="machine-ip" placeholder="IP地址" value="${isEdit ? machine.ip : ''}">
        </div>
        <div class="form-group">
            <label class="form-label">端口</label>
            <input type="number" class="form-input" id="machine-port" placeholder="端口" value="${isEdit ? machine.port : '22'}">
        </div>
        <div class="form-group">
            <label class="form-label">主机名</label>
            <input type="text" class="form-input" id="machine-hostname" placeholder="主机名" value="${isEdit ? machine.hostname || '' : ''}">
        </div>
        <div class="form-group">
            <label class="form-label">环境</label>
            <select class="form-input" id="machine-environment">
                <option value="dev" ${isEdit && machine.environment === 'dev' ? 'selected' : ''}>开发环境</option>
                <option value="test" ${isEdit && machine.environment === 'test' ? 'selected' : ''}>测试环境</option>
                <option value="prod" ${isEdit && machine.environment === 'prod' ? 'selected' : ''}>生产环境</option>
            </select>
        </div>
        <div class="form-group">
            <label class="form-label">CPU</label>
            <input type="text" class="form-input" id="machine-cpu" placeholder="CPU" value="${isEdit ? machine.cpu || '' : ''}">
        </div>
        <div class="form-group">
            <label class="form-label">内存</label>
            <input type="text" class="form-input" id="machine-memory" placeholder="内存" value="${isEdit ? machine.memory || '' : ''}">
        </div>
        <div class="form-group">
            <label class="form-label">操作系统</label>
            <input type="text" class="form-input" id="machine-os" placeholder="操作系统" value="${isEdit ? machine.os || '' : ''}">
        </div>
        <div class="form-group">
            <label class="form-label">负责人</label>
            <select class="form-input" id="machine-owner">
                <option value="">请选择</option>
                ${owners.map(o => `<option value="${o.id}" ${isEdit && machine.owner_id === o.id ? 'selected' : ''}>${o.username}</option>`).join('')}
            </select>
        </div>
        <div class="form-group">
            <label class="form-label">归属组织</label>
            <select class="form-input" id="machine-organization">
                <option value="">请选择</option>
                ${organizations.map(o => `<option value="${o.id}" ${isEdit && machine.organization_id === o.id ? 'selected' : ''}>${o.name}</option>`).join('')}
            </select>
        </div>
        <div class="form-group">
            <label class="form-label">描述</label>
            <textarea class="form-input form-textarea" id="machine-description" placeholder="描述">${isEdit ? machine.description || '' : ''}</textarea>
        </div>
        <div class="modal-actions">
            <button class="btn btn-cancel" onclick="closeSidePanel()">取消</button>
            <button class="btn btn-primary" onclick="${isEdit ? `updateDevMachine()` : `addDevMachine()`}">${isEdit ? '保存修改' : '添加'}</button>
        </div>
    `;
    
    document.getElementById('side-panel').classList.add('active');
}

async function addDevMachine() {
    const name = document.getElementById('machine-name').value.trim();
    const ip = document.getElementById('machine-ip').value.trim();
    const port = document.getElementById('machine-port').value || 22;
    const hostname = document.getElementById('machine-hostname').value.trim();
    const environment = document.getElementById('machine-environment').value;
    const cpu = document.getElementById('machine-cpu').value.trim();
    const memory = document.getElementById('machine-memory').value.trim();
    const os = document.getElementById('machine-os').value.trim();
    const ownerId = document.getElementById('machine-owner').value;
    const orgId = document.getElementById('machine-organization').value;
    const description = document.getElementById('machine-description').value.trim();
    
    if (!name || !ip) {
        alert('请填写名称和IP地址');
        return;
    }
    
    const data = {
        name,
        ip,
        port: parseInt(port),
        hostname: hostname || null,
        environment,
        cpu: cpu || null,
        memory: memory || null,
        os: os || null,
        owner_id: ownerId ? parseInt(ownerId) : null,
        organization_id: orgId ? parseInt(orgId) : null,
        description: description || null,
        status: 1
    };
    
    try {
        await apiRequest(`${API_BASE}/dev-machines`, {
            method: 'POST',
            body: JSON.stringify(data)
        });
        closeSidePanel();
        loadDevMachines();
    } catch (e) {
        alert(e.message);
    }
}

async function updateDevMachine() {
    const machineId = document.getElementById('machine-id').value;
    const name = document.getElementById('machine-name').value.trim();
    const ip = document.getElementById('machine-ip').value.trim();
    const port = document.getElementById('machine-port').value || 22;
    const hostname = document.getElementById('machine-hostname').value.trim();
    const environment = document.getElementById('machine-environment').value;
    const cpu = document.getElementById('machine-cpu').value.trim();
    const memory = document.getElementById('machine-memory').value.trim();
    const os = document.getElementById('machine-os').value.trim();
    const ownerId = document.getElementById('machine-owner').value;
    const orgId = document.getElementById('machine-organization').value;
    const description = document.getElementById('machine-description').value.trim();
    
    if (!name || !ip) {
        alert('请填写名称和IP地址');
        return;
    }
    
    const data = {
        name,
        ip,
        port: parseInt(port),
        hostname: hostname || null,
        environment,
        cpu: cpu || null,
        memory: memory || null,
        os: os || null,
        owner_id: ownerId ? parseInt(ownerId) : null,
        organization_id: orgId ? parseInt(orgId) : null,
        description: description || null,
        status: 1
    };
    
    try {
        await apiRequest(`${API_BASE}/dev-machines/${machineId}`, {
            method: 'PUT',
            body: JSON.stringify(data)
        });
        closeSidePanel();
        loadDevMachines();
    } catch (e) {
        alert(e.message);
    }
}

async function deleteDevMachine(machineId) {
    if (!confirm('确定删除该研发机器吗？')) return;
    try {
        await apiRequest(`${API_BASE}/dev-machines/${machineId}`, {
            method: 'DELETE'
        });
        loadDevMachines();
    } catch (e) {
        alert(e.message);
    }
}

async function loadDbInstances() {
    const instances = await apiRequest(`${API_BASE}/db-instances`);
    renderDbInstancesTable(instances);
}

function renderDbInstancesTable(instances) {
    const contentBody = document.getElementById('content-body');
    
    const canEdit = currentUser && (currentUser.role === 'admin' || currentUser.can_edit);
    const canDelete = currentUser && (currentUser.role === 'admin' || currentUser.can_delete);

    document.getElementById('header-actions').innerHTML = canEdit ? `
        <button class="btn btn-primary" onclick="openEditDbPanel()">添加数据库实例</button>
    ` : '';

    const tableHtml = `
        <div class="data-panel">
            <div class="filter-bar">
                <span class="filter-label">数据库类型:</span>
                <select class="filter-select" id="db-type-filter" onchange="filterDbInstances()">
                    <option value="">全部</option>
                    <option value="MySQL">MySQL</option>
                    <option value="PostgreSQL">PostgreSQL</option>
                    <option value="Redis">Redis</option>
                    <option value="MongoDB">MongoDB</option>
                    <option value="Elasticsearch">Elasticsearch</option>
                    <option value="ClickHouse">ClickHouse</option>
                </select>
                <span class="filter-label">环境:</span>
                <select class="filter-select" id="db-env-filter" onchange="filterDbInstances()">
                    <option value="">全部</option>
                    <option value="dev">开发环境</option>
                    <option value="test">测试环境</option>
                    <option value="prod">生产环境</option>
                </select>
            </div>
            <div class="data-table-wrapper">
                <table class="data-table" id="db-instances-table">
                    <thead>
                        <tr>
                            <th>名称</th>
                            <th>类型</th>
                            <th>版本</th>
                            <th>地址</th>
                            <th>环境</th>
                            <th>状态</th>
                            <th>负责人</th>
                            <th>归属组织</th>
                            <th>字符集</th>
                            <th>备注</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${instances.map(db => `
                            <tr data-db-type="${db.db_type}" data-env="${db.environment}" data-status="${db.status}">
                                <td><strong>${db.name}</strong></td>
                                <td>${db.db_type}</td>
                                <td>${db.version || '-'}</td>
                                <td>${db.ip}:${db.port}</td>
                                <td><span class="env-badge ${db.environment}">${getEnvText(db.environment)}</span></td>
                                <td><span class="status-badge ${db.status === 1 ? 'online' : 'offline'}"><span class="status-dot"></span>${db.status === 1 ? '在线' : '离线'}</span></td>
                                <td>${db.owner_name || '-'}</td>
                                <td>${db.organization_name || '-'}</td>
                                <td>${db.charset}</td>
                                <td>
                                    <span class="truncated-text" title="${db.description || ''}">${truncateText(db.description, 20)}</span>
                                </td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            </div>
        </div>
    `;
    contentBody.innerHTML = tableHtml;
}

async function openEditDbPanel(instanceId = null) {
    const [organizations, owners] = await Promise.all([
        apiRequest(`${API_BASE}/organizations`),
        apiRequest(`${API_BASE}/owners`)
    ]);
    
    const titleEl = document.getElementById('side-panel-title');
    const bodyEl = document.getElementById('side-panel-body');
    
    const isEdit = instanceId !== null;
    const instance = isEdit ? await apiRequest(`${API_BASE}/db-instances/${instanceId}`) : null;
    
    titleEl.textContent = isEdit ? '修改数据库实例' : '添加数据库实例';
    
    bodyEl.innerHTML = `
        ${isEdit ? `<input type="hidden" id="db-id" value="${instanceId}">` : ''}
        <div class="form-group">
            <label class="form-label">名称 *</label>
            <input type="text" class="form-input" id="db-name" placeholder="数据库实例名称" value="${isEdit ? instance.name : ''}">
        </div>
        <div class="form-group">
            <label class="form-label">数据库类型 *</label>
            <select class="form-input" id="db-type">
                <option value="MySQL" ${isEdit && instance.db_type === 'MySQL' ? 'selected' : ''}>MySQL</option>
                <option value="PostgreSQL" ${isEdit && instance.db_type === 'PostgreSQL' ? 'selected' : ''}>PostgreSQL</option>
                <option value="Redis" ${isEdit && instance.db_type === 'Redis' ? 'selected' : ''}>Redis</option>
                <option value="MongoDB" ${isEdit && instance.db_type === 'MongoDB' ? 'selected' : ''}>MongoDB</option>
                <option value="Elasticsearch" ${isEdit && instance.db_type === 'Elasticsearch' ? 'selected' : ''}>Elasticsearch</option>
                <option value="ClickHouse" ${isEdit && instance.db_type === 'ClickHouse' ? 'selected' : ''}>ClickHouse</option>
            </select>
        </div>
        <div class="form-group">
            <label class="form-label">版本</label>
            <input type="text" class="form-input" id="db-version" placeholder="版本" value="${isEdit ? instance.version || '' : ''}">
        </div>
        <div class="form-group">
            <label class="form-label">IP地址 *</label>
            <input type="text" class="form-input" id="db-ip" placeholder="IP地址" value="${isEdit ? instance.ip : ''}">
        </div>
        <div class="form-group">
            <label class="form-label">端口</label>
            <input type="number" class="form-input" id="db-port" placeholder="端口" value="${isEdit ? instance.port : '3306'}">
        </div>
        <div class="form-group">
            <label class="form-label">字符集</label>
            <input type="text" class="form-input" id="db-charset" placeholder="字符集" value="${isEdit ? instance.charset : 'utf8mb4'}">
        </div>
        <div class="form-group">
            <label class="form-label">环境</label>
            <select class="form-input" id="db-environment">
                <option value="dev" ${isEdit && instance.environment === 'dev' ? 'selected' : ''}>开发环境</option>
                <option value="test" ${isEdit && instance.environment === 'test' ? 'selected' : ''}>测试环境</option>
                <option value="prod" ${isEdit && instance.environment === 'prod' ? 'selected' : ''}>生产环境</option>
            </select>
        </div>
        <div class="form-group">
            <label class="form-label">负责人</label>
            <select class="form-input" id="db-owner">
                <option value="">请选择</option>
                ${owners.map(o => `<option value="${o.id}" ${isEdit && instance.owner_id === o.id ? 'selected' : ''}>${o.username}</option>`).join('')}
            </select>
        </div>
        <div class="form-group">
            <label class="form-label">归属组织</label>
            <select class="form-input" id="db-organization">
                <option value="">请选择</option>
                ${organizations.map(o => `<option value="${o.id}" ${isEdit && instance.organization_id === o.id ? 'selected' : ''}>${o.name}</option>`).join('')}
            </select>
        </div>
        <div class="form-group">
            <label class="form-label">描述</label>
            <textarea class="form-input form-textarea" id="db-description" placeholder="描述">${isEdit ? instance.description || '' : ''}</textarea>
        </div>
        <div class="modal-actions">
            <button class="btn btn-cancel" onclick="closeSidePanel()">取消</button>
            <button class="btn btn-primary" onclick="${isEdit ? `updateDbInstance()` : `addDbInstance()`}">${isEdit ? '保存修改' : '添加'}</button>
        </div>
    `;
    
    document.getElementById('side-panel').classList.add('active');
}

async function addDbInstance() {
    const name = document.getElementById('db-name').value.trim();
    const dbType = document.getElementById('db-type').value;
    const version = document.getElementById('db-version').value.trim();
    const ip = document.getElementById('db-ip').value.trim();
    const port = document.getElementById('db-port').value || 3306;
    const charset = document.getElementById('db-charset').value.trim();
    const environment = document.getElementById('db-environment').value;
    const ownerId = document.getElementById('db-owner').value;
    const orgId = document.getElementById('db-organization').value;
    const description = document.getElementById('db-description').value.trim();
    
    if (!name || !dbType || !ip) {
        alert('请填写名称、数据库类型和IP地址');
        return;
    }
    
    const data = {
        name,
        db_type: dbType,
        version: version || null,
        ip,
        port: parseInt(port),
        charset: charset || 'utf8mb4',
        environment,
        owner_id: ownerId ? parseInt(ownerId) : null,
        organization_id: orgId ? parseInt(orgId) : null,
        description: description || null,
        status: 1
    };
    
    try {
        await apiRequest(`${API_BASE}/db-instances`, {
            method: 'POST',
            body: JSON.stringify(data)
        });
        closeSidePanel();
        loadDbInstances();
    } catch (e) {
        alert(e.message);
    }
}

async function updateDbInstance() {
    const instanceId = document.getElementById('db-id').value;
    const name = document.getElementById('db-name').value.trim();
    const dbType = document.getElementById('db-type').value;
    const version = document.getElementById('db-version').value.trim();
    const ip = document.getElementById('db-ip').value.trim();
    const port = document.getElementById('db-port').value || 3306;
    const charset = document.getElementById('db-charset').value.trim();
    const environment = document.getElementById('db-environment').value;
    const ownerId = document.getElementById('db-owner').value;
    const orgId = document.getElementById('db-organization').value;
    const description = document.getElementById('db-description').value.trim();
    
    if (!name || !dbType || !ip) {
        alert('请填写名称、数据库类型和IP地址');
        return;
    }
    
    const data = {
        name,
        db_type: dbType,
        version: version || null,
        ip,
        port: parseInt(port),
        charset: charset || 'utf8mb4',
        environment,
        owner_id: ownerId ? parseInt(ownerId) : null,
        organization_id: orgId ? parseInt(orgId) : null,
        description: description || null,
        status: 1
    };
    
    try {
        await apiRequest(`${API_BASE}/db-instances/${instanceId}`, {
            method: 'PUT',
            body: JSON.stringify(data)
        });
        closeSidePanel();
        loadDbInstances();
    } catch (e) {
        alert(e.message);
    }
}

async function deleteDbInstance(instanceId) {
    if (!confirm('确定删除该数据库实例吗？')) return;
    try {
        await apiRequest(`${API_BASE}/db-instances/${instanceId}`, {
            method: 'DELETE'
        });
        loadDbInstances();
    } catch (e) {
        alert(e.message);
    }
}

function filterDevMachines() {
    const envFilter = document.getElementById('env-filter-bar')?.value || '';
    const statusFilter = document.getElementById('status-filter')?.value || '';
    const rows = document.querySelectorAll('#machines-table tbody tr');

    rows.forEach(row => {
        const envMatch = !envFilter || row.dataset.env === envFilter;
        const statusMatch = statusFilter === '' || row.dataset.status === statusFilter;
        row.style.display = envMatch && statusMatch ? '' : 'none';
    });
}

function filterDbInstances() {
    const dbTypeFilter = document.getElementById('db-type-filter')?.value || '';
    const envFilter = document.getElementById('db-env-filter')?.value || '';
    const rows = document.querySelectorAll('#db-instances-table tbody tr');

    rows.forEach(row => {
        const typeMatch = !dbTypeFilter || row.dataset.dbType === dbTypeFilter;
        const envMatch = !envFilter || row.dataset.env === envFilter;
        row.style.display = typeMatch && envMatch ? '' : 'none';
    });
}

function getEnvText(env) {
    const envMap = {
        'dev': '开发',
        'test': '测试',
        'prod': '生产'
    };
    return envMap[env] || env;
}

function truncateText(text, maxLength) {
    if (!text) return '-';
    if (text.length <= maxLength) return text;
    return text.substring(0, maxLength) + '...';
}

function initCollapseSidebar() {
    const sidebar = document.getElementById('sidebar');
    const collapseBtn = document.getElementById('collapse-btn');

    collapseBtn.addEventListener('click', () => {
        sidebar.classList.toggle('collapsed');
    });
}

function initLogoClick() {
    const logo = document.querySelector('.logo');
    if (logo) {
        logo.addEventListener('click', goHome);
    }
}

function initAuthState() {
    const token = localStorage.getItem('token');
    if (token) {
        apiRequest(`${API_BASE}/auth/me`).then(user => {
            currentUser = user;
            updateAuthUI();
        }).catch(() => {
            localStorage.removeItem('token');
            updateAuthUI();
        });
    }
}

document.addEventListener('DOMContentLoaded', () => {
    initCollapseSidebar();
    initLogoClick();
    initAuthState();
    updateAuthUI();
    fetchCategories();
});

// 凭据管理功能
let devMachines = [];
let dbInstances = [];
let credentials = [];

async function showCredentialsPage() {
    currentCategory = null;
    document.querySelectorAll('.nav-item').forEach(i => i.classList.remove('active'));
    const credNavItem = Array.from(document.querySelectorAll('.nav-item')).find(i => i.dataset.name === 'credentials');
    if (credNavItem) credNavItem.classList.add('active');
    document.getElementById('page-title').textContent = '凭据管理';
    
    try {
        const [machines, instances, creds] = await Promise.all([
            apiRequest(`${API_BASE}/dev-machines`),
            apiRequest(`${API_BASE}/db-instances`),
            apiRequest(`${API_BASE}/admin/credentials`)
        ]);
        devMachines = machines;
        dbInstances = instances;
        credentials = creds;
        renderCredentialsPage();
    } catch (e) {
        alert(e.message);
    }
}

function renderCredentialsPage() {
    const contentBody = document.getElementById('content-body');
    document.getElementById('header-actions').innerHTML = `
        <button class="btn btn-primary" onclick="showAddCredentialModal()">添加凭据</button>
    `;
    
    const tableHtml = `
        <div class="data-panel">
            <div class="data-table-wrapper">
                <table class="data-table" id="credentials-table">
                    <thead>
                        <tr>
                            <th>资源名称</th>
                            <th>资源类型</th>
                            <th>用户名</th>
                            <th>密码</th>
                            <th>描述</th>
                            <th>操作</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${credentials.map(cred => {
                            const typeText = cred.resource_type === 'dev_machine' ? '研发机器' : '数据库';
                            return `
                                <tr>
                                    <td><strong>${cred.resource_name || ''}</strong></td>
                                    <td>${typeText}</td>
                                    <td>${cred.username}</td>
                                    <td><span class="password-field">${cred.password}</span></td>
                                    <td>${cred.description || '-'}</td>
                                    <td>
                                        <button class="btn btn-sm btn-primary" onclick="showEditCredentialModal(${cred.id})">编辑</button>
                                        <button class="btn btn-sm btn-danger" onclick="deleteCredential(${cred.id})">删除</button>
                                    </td>
                                </tr>
                            `;
                        }).join('')}
                    </tbody>
                </table>
            </div>
        </div>
    `;
    contentBody.innerHTML = tableHtml;
}

function showAddCredentialModal() {
    const modal = document.createElement('div');
    modal.className = 'modal-overlay';
    modal.id = 'add-cred-modal';
    
    const machineOptions = devMachines.map(m => `<option value="${m.id}">${m.name}</option>`).join('');
    const dbOptions = dbInstances.map(d => `<option value="${d.id}">${d.name}</option>`).join('');
    
    modal.innerHTML = `
        <div class="modal-content" onclick="event.stopPropagation()">
            <h2 class="modal-header">添加凭据</h2>
            <div class="form-group">
                <label class="form-label">资源类型</label>
                <select class="form-input" id="cred-type" onchange="updateResourceOptions()">
                    <option value="dev_machine">研发机器</option>
                    <option value="db_instance">数据库</option>
                </select>
            </div>
            <div class="form-group">
                <label class="form-label">资源</label>
                <select class="form-input" id="cred-resource-id">
                    ${machineOptions}
                </select>
            </div>
            <div class="form-group">
                <label class="form-label">用户名</label>
                <input type="text" class="form-input" id="cred-username" placeholder="请输入用户名">
            </div>
            <div class="form-group">
                <label class="form-label">密码</label>
                <input type="text" class="form-input" id="cred-password" placeholder="请输入密码">
            </div>
            <div class="form-group">
                <label class="form-label">描述</label>
                <textarea class="form-input" id="cred-description" rows="3" placeholder="可选"></textarea>
            </div>
            <div class="modal-actions">
                <button class="btn btn-cancel" onclick="closeAddCredModal()">取消</button>
                <button class="btn btn-primary" onclick="addCredential()">保存</button>
            </div>
        </div>
    `;
    modal.addEventListener('click', () => closeAddCredModal());
    document.body.appendChild(modal);
}

function updateResourceOptions() {
    const type = document.getElementById('cred-type').value;
    const select = document.getElementById('cred-resource-id');
    if (type === 'dev_machine') {
        select.innerHTML = devMachines.map(m => `<option value="${m.id}">${m.name}</option>`).join('');
    } else {
        select.innerHTML = dbInstances.map(d => `<option value="${d.id}">${d.name}</option>`).join('');
    }
}

function closeAddCredModal() {
    const modal = document.getElementById('add-cred-modal');
    if (modal) modal.remove();
}

async function addCredential() {
    const data = {
        resource_type: document.getElementById('cred-type').value,
        resource_id: parseInt(document.getElementById('cred-resource-id').value),
        username: document.getElementById('cred-username').value,
        password: document.getElementById('cred-password').value,
        description: document.getElementById('cred-description').value
    };
    if (!data.username || !data.password) {
        alert('请填写用户名和密码');
        return;
    }
    
    try {
        await apiRequest(`${API_BASE}/admin/credentials`, {
            method: 'POST',
            body: JSON.stringify(data)
        });
        closeAddCredModal();
        showCredentialsPage();
    } catch (e) {
        alert(e.message);
    }
}

function showEditCredentialModal(id) {
    const cred = credentials.find(c => c.id === id);
    if (!cred) return;
    
    const modal = document.createElement('div');
    modal.className = 'modal-overlay';
    modal.id = 'edit-cred-modal';
    
    const machineOptions = devMachines.map(m => `<option value="${m.id}" ${m.id === cred.resource_id && cred.resource_type === 'dev_machine' ? 'selected' : ''}>${m.name}</option>`).join('');
    const dbOptions = dbInstances.map(d => `<option value="${d.id}" ${d.id === cred.resource_id && cred.resource_type === 'db_instance' ? 'selected' : ''}>${d.name}</option>`).join('');
    
    modal.innerHTML = `
        <div class="modal-content" onclick="event.stopPropagation()">
            <h2 class="modal-header">编辑凭据</h2>
            <div class="form-group">
                <label class="form-label">资源类型</label>
                <select class="form-input" id="edit-cred-type" onchange="updateEditResourceOptions()">
                    <option value="dev_machine" ${cred.resource_type === 'dev_machine' ? 'selected' : ''}>研发机器</option>
                    <option value="db_instance" ${cred.resource_type === 'db_instance' ? 'selected' : ''}>数据库</option>
                </select>
            </div>
            <div class="form-group">
                <label class="form-label">资源</label>
                <select class="form-input" id="edit-cred-resource-id">
                    ${cred.resource_type === 'dev_machine' ? machineOptions : dbOptions}
                </select>
            </div>
            <div class="form-group">
                <label class="form-label">用户名</label>
                <input type="text" class="form-input" id="edit-cred-username" value="${cred.username}" placeholder="请输入用户名">
            </div>
            <div class="form-group">
                <label class="form-label">密码</label>
                <input type="text" class="form-input" id="edit-cred-password" value="${cred.password}" placeholder="请输入密码">
            </div>
            <div class="form-group">
                <label class="form-label">描述</label>
                <textarea class="form-input" id="edit-cred-description" rows="3" placeholder="可选">${cred.description || ''}</textarea>
            </div>
            <div class="modal-actions">
                <button class="btn btn-cancel" onclick="closeEditCredModal()">取消</button>
                <button class="btn btn-primary" onclick="updateCredential(${id})">保存</button>
            </div>
        </div>
    `;
    modal.addEventListener('click', () => closeEditCredModal());
    document.body.appendChild(modal);
}

function updateEditResourceOptions() {
    const type = document.getElementById('edit-cred-type').value;
    const select = document.getElementById('edit-cred-resource-id');
    if (type === 'dev_machine') {
        select.innerHTML = devMachines.map(m => `<option value="${m.id}">${m.name}</option>`).join('');
    } else {
        select.innerHTML = dbInstances.map(d => `<option value="${d.id}">${d.name}</option>`).join('');
    }
}

function closeEditCredModal() {
    const modal = document.getElementById('edit-cred-modal');
    if (modal) modal.remove();
}

async function updateCredential(id) {
    const data = {
        resource_type: document.getElementById('edit-cred-type').value,
        resource_id: parseInt(document.getElementById('edit-cred-resource-id').value),
        username: document.getElementById('edit-cred-username').value,
        password: document.getElementById('edit-cred-password').value,
        description: document.getElementById('edit-cred-description').value
    };
    if (!data.username || !data.password) {
        alert('请填写用户名和密码');
        return;
    }
    
    try {
        await apiRequest(`${API_BASE}/admin/credentials/${id}`, {
            method: 'PUT',
            body: JSON.stringify(data)
        });
        closeEditCredModal();
        showCredentialsPage();
    } catch (e) {
        alert(e.message);
    }
}

async function deleteCredential(id) {
    if (!confirm('确定删除此凭据吗？')) return;
    try {
        await apiRequest(`${API_BASE}/admin/credentials/${id}`, {
            method: 'DELETE'
        });
        showCredentialsPage();
    } catch (e) {
        alert(e.message);
    }
}

// 用户管理功能
let allUsers = [];

async function showUserManagementPage() {
    currentCategory = null;
    document.querySelectorAll('.nav-item').forEach(i => i.classList.remove('active'));
    const userNavItem = Array.from(document.querySelectorAll('.nav-item')).find(i => i.dataset.name === 'users');
    if (userNavItem) userNavItem.classList.add('active');
    document.getElementById('page-title').textContent = '用户管理';
    document.getElementById('header-actions').innerHTML = `
        <button class="btn btn-primary" onclick="showAddUserModal()">添加用户</button>
    `;

    try {
        const [users, cats] = await Promise.all([
            apiRequest(`${API_BASE}/admin/users`),
            apiRequest(`${API_BASE}/categories`)
        ]);
        allUsers = users;
        window.allCategories = cats;
        renderUserManagementTable();
    } catch (e) {
        alert(e.message);
    }
}

function renderUserManagementTable() {
    const contentBody = document.getElementById('content-body');

    const tableHtml = `
        <div class="data-panel">
            <div style="padding:12px 16px;font-size:14px;color:var(--text-secondary);border-bottom:1px solid var(--border-color);">
                共 <strong>${allUsers.length}</strong> 个用户
            </div>
            <div class="data-table-wrapper">
                <table class="data-table" id="users-table">
                    <thead>
                        <tr>
                            <th>用户名</th>
                            <th>邮箱</th>
                            <th>角色</th>
                            <th>状态</th>
                            <th>可编辑</th>
                            <th>可删除</th>
                            <th>分类权限</th>
                            <th>操作</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${allUsers.map(user => `
                            <tr data-user-id="${user.id}">
                                <td><strong>${user.username}</strong></td>
                                <td>${user.email || '-'}</td>
                                <td>
                                    <select class="role-select" onchange="updateUserRole(${user.id}, this.value)">
                                        <option value="guest" ${user.role === 'guest' ? 'selected' : ''}>访客</option>
                                        <option value="registered" ${user.role === 'registered' ? 'selected' : ''}>普通用户</option>
                                        <option value="admin" ${user.role === 'admin' ? 'selected' : ''}>管理员</option>
                                    </select>
                                </td>
                                <td>
                                    <label class="switch">
                                        <input type="checkbox" ${user.is_active ? 'checked' : ''} onchange="updateUserStatus(${user.id}, this.checked ? 1 : 0)">
                                        <span class="slider"></span>
                                    </label>
                                </td>
                                <td>
                                    <label class="switch">
                                        <input type="checkbox" ${user.can_edit ? 'checked' : ''} onchange="updateUserAction(${user.id}, 'can_edit', this.checked)">
                                        <span class="slider"></span>
                                    </label>
                                </td>
                                <td>
                                    <label class="switch">
                                        <input type="checkbox" ${user.can_delete ? 'checked' : ''} onchange="updateUserAction(${user.id}, 'can_delete', this.checked)">
                                        <span class="slider"></span>
                                    </label>
                                </td>
                                <td>
                                    <button class="btn btn-sm btn-primary" onclick="showUserCategoryPermModal(${user.id})">设置分类</button>
                                </td>
                                <td>
                                    <button class="btn btn-sm btn-info" onclick="showResetPasswordModal(${user.id})">重置密码</button>
                                </td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            </div>
        </div>
    `;
    contentBody.innerHTML = tableHtml;
}

async function updateUserRole(userId, role) {
    try {
        await apiRequest(`${API_BASE}/admin/users/${userId}/role`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ role })
        });
        showUserManagementPage();
    } catch (e) {
        alert(e.message);
    }
}

async function updateUserStatus(userId, isActive) {
    try {
        await apiRequest(`${API_BASE}/admin/users/${userId}/status`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ is_active: isActive })
        });
    } catch (e) {
        alert(e.message);
        showUserManagementPage();
    }
}

async function updateUserAction(userId, action, value) {
    try {
        const user = allUsers.find(u => u.id === userId);
        const data = {
            can_edit: action === 'can_edit' ? value : user.can_edit,
            can_delete: action === 'can_delete' ? value : user.can_delete
        };
        await apiRequest(`${API_BASE}/admin/users/${userId}/actions`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
    } catch (e) {
        alert(e.message);
        showUserManagementPage();
    }
}

function showUserCategoryPermModal(userId) {
    const user = allUsers.find(u => u.id === userId);
    if (!user) return;

    const modal = document.createElement('div');
    modal.className = 'modal-overlay';
    modal.id = 'user-cat-modal';

    const enabledCats = user.permissions.map(p => p.category_id);

    modal.innerHTML = `
        <div class="modal-content" onclick="event.stopPropagation()">
            <h2 class="modal-header">设置 ${user.username} 的分类权限</h2>
            <div class="category-perm-list">
                ${window.allCategories.map(cat => `
                    <div class="category-perm-item">
                        <label>
                            <input type="checkbox" value="${cat.id}" ${enabledCats.includes(cat.id) ? 'checked' : ''}>
                            ${cat.name}
                        </label>
                    </div>
                `).join('')}
            </div>
            <div class="modal-actions">
                <button class="btn btn-cancel" onclick="closeUserCatModal()">取消</button>
                <button class="btn btn-primary" onclick="saveUserCategoryPerm(${userId})">保存</button>
            </div>
        </div>
    `;
    modal.addEventListener('click', () => closeUserCatModal());
    document.body.appendChild(modal);
}

function closeUserCatModal() {
    const modal = document.getElementById('user-cat-modal');
    if (modal) modal.remove();
}

async function saveUserCategoryPerm(userId) {
    const checkboxes = document.querySelectorAll('#user-cat-modal input[type="checkbox"]:checked');
    const categoryPermissions = Array.from(checkboxes).map(cb => ({
        category_id: parseInt(cb.value),
        enabled: true
    }));

    try {
        await apiRequest(`${API_BASE}/admin/users/${userId}/categories`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ category_permissions: categoryPermissions })
        });
        closeUserCatModal();
        showUserManagementPage();
    } catch (e) {
        alert(e.message);
    }
}

function showAddUserModal() {
    const modal = document.createElement('div');
    modal.className = 'modal-overlay';
    modal.id = 'add-user-modal';
    modal.innerHTML = `
        <div class="modal-content" onclick="event.stopPropagation()">
            <h2 class="modal-header">添加用户</h2>
            <div class="form-group">
                <label class="form-label">用户名 *</label>
                <input type="text" class="form-input" id="new-user-username" placeholder="请输入用户名">
            </div>
            <div class="form-group">
                <label class="form-label">邮箱</label>
                <input type="email" class="form-input" id="new-user-email" placeholder="请输入邮箱（可选）">
            </div>
            <div class="form-group">
                <label class="form-label">密码 *</label>
                <input type="password" class="form-input" id="new-user-password" placeholder="至少6位密码">
            </div>
            <div class="form-group">
                <label class="form-label">角色</label>
                <select class="form-input" id="new-user-role">
                    <option value="registered">普通用户</option>
                    <option value="admin">管理员</option>
                </select>
            </div>
            <div class="modal-actions">
                <button class="btn btn-cancel" onclick="closeAddUserModal()">取消</button>
                <button class="btn btn-primary" onclick="addUser()">添加</button>
            </div>
        </div>
    `;
    modal.addEventListener('click', () => closeAddUserModal());
    document.body.appendChild(modal);
}

function closeAddUserModal() {
    const modal = document.getElementById('add-user-modal');
    if (modal) modal.remove();
}

async function addUser() {
    const username = document.getElementById('new-user-username').value.trim();
    const email = document.getElementById('new-user-email').value.trim();
    const password = document.getElementById('new-user-password').value;
    const role = document.getElementById('new-user-role').value;

    if (!username || !password) {
        alert('请填写用户名和密码');
        return;
    }
    if (password.length < 6) {
        alert('密码长度至少为6位');
        return;
    }

    try {
        await apiRequest(`${API_BASE}/admin/users`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, email: email || null, password, role })
        });
        closeAddUserModal();
        showUserManagementPage();
    } catch (e) {
        alert(e.message);
    }
}

function showResetPasswordModal(userId) {
    const user = allUsers.find(u => u.id === userId);
    if (!user) return;

    const modal = document.createElement('div');
    modal.className = 'modal-overlay';
    modal.id = 'reset-pwd-modal';
    modal.innerHTML = `
        <div class="modal-content" onclick="event.stopPropagation()">
            <h2 class="modal-header">重置密码 - ${user.username}</h2>
            <div class="form-group">
                <label class="form-label">新密码 *</label>
                <input type="password" class="form-input" id="reset-pwd-input" placeholder="至少6位">
            </div>
            <div class="form-group">
                <label class="form-label">确认密码 *</label>
                <input type="password" class="form-input" id="reset-pwd-confirm" placeholder="再次输入新密码">
            </div>
            <div class="modal-actions">
                <button class="btn btn-cancel" onclick="closeResetPasswordModal()">取消</button>
                <button class="btn btn-primary" onclick="resetUserPassword(${userId})">确认重置</button>
            </div>
        </div>
    `;
    modal.addEventListener('click', () => closeResetPasswordModal());
    document.body.appendChild(modal);
}

function closeResetPasswordModal() {
    const modal = document.getElementById('reset-pwd-modal');
    if (modal) modal.remove();
}

async function resetUserPassword(userId) {
    const password = document.getElementById('reset-pwd-input').value;
    const confirm = document.getElementById('reset-pwd-confirm').value;

    if (password.length < 6) {
        alert('密码长度至少为6位');
        return;
    }
    if (password !== confirm) {
        alert('两次输入的密码不一致');
        return;
    }

    try {
        await apiRequest(`${API_BASE}/admin/users/${userId}/reset-password`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ password })
        });
        closeResetPasswordModal();
        alert('密码重置成功');
    } catch (e) {
        alert(e.message);
    }
}

// ========== API Key 管理功能 ==========

let apiKeysList = [];

async function showApiKeysPage() {
    currentCategory = null;
    document.querySelectorAll('.nav-item').forEach(i => i.classList.remove('active'));
    const apiKeyNavItem = Array.from(document.querySelectorAll('.nav-item')).find(i => i.dataset.name === 'api_keys');
    if (apiKeyNavItem) apiKeyNavItem.classList.add('active');
    document.getElementById('page-title').textContent = 'API Key 管理';
    
    try {
        apiKeysList = await apiRequest(`${API_BASE}/api-keys`);
        renderApiKeysTable();
    } catch (e) {
        alert(e.message);
    }
}

function renderApiKeysTable() {
    const contentBody = document.getElementById('content-body');
    document.getElementById('header-actions').innerHTML = `
        <button class="btn btn-primary" onclick="showCreateApiKeyModal()">创建 API Key</button>
    `;
    
    const tableHtml = `
        <div class="data-panel">
            <div class="data-table-wrapper">
                <table class="data-table" id="api-keys-table">
                    <thead>
                        <tr>
                            <th>名称</th>
                            <th>前缀</th>
                            <th>状态</th>
                            <th>最后使用</th>
                            <th>创建时间</th>
                            <th>操作</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${apiKeysList.length === 0 ? `
                            <tr>
                                <td colspan="6" class="empty-state">
                                    暂无 API Key，点击上方按钮创建
                                </td>
                            </tr>
                        ` : apiKeysList.map(key => `
                            <tr>
                                <td><strong>${key.key_name}</strong></td>
                                <td><code class="api-key-prefix">${key.key_prefix}</code></td>
                                <td><span class="status-badge ${key.is_active ? 'online' : 'offline'}"><span class="status-dot"></span>${key.is_active ? '启用' : '禁用'}</span></td>
                                <td>${key.last_used_at ? formatDate(key.last_used_at) : '从未使用'}</td>
                                <td>${formatDate(key.create_time)}</td>
                                <td>
                                    <button class="btn btn-sm btn-info" onclick="showApiKeyLogs(${key.id})">日志</button>
                                    <button class="btn btn-sm btn-danger" onclick="deleteApiKey(${key.id}, '${key.key_name}')">删除</button>
                                </td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            </div>
        </div>
    `;
    contentBody.innerHTML = tableHtml;
}

function showCreateApiKeyModal() {
    const modal = document.createElement('div');
    modal.className = 'modal-overlay';
    modal.id = 'create-api-key-modal';
    
    modal.innerHTML = `
        <div class="modal-content" onclick="event.stopPropagation()">
            <h2 class="modal-header">创建 API Key</h2>
            <div class="form-group">
                <label class="form-label">Key 名称 *</label>
                <input type="text" class="form-input" id="new-api-key-name" placeholder="给这个 Key 起个名字，方便识别">
            </div>
            <div class="form-group">
                <label class="form-label">过期时间（可选）</label>
                <input type="datetime-local" class="form-input" id="new-api-key-expire">
                <p class="form-hint">留空表示永不过期</p>
            </div>
            <div class="form-group">
                <label class="form-label">备注（可选）</label>
                <textarea class="form-input form-textarea" id="new-api-key-desc" placeholder="可选备注信息"></textarea>
            </div>
            <div class="modal-actions">
                <button class="btn btn-cancel" onclick="closeCreateApiKeyModal()">取消</button>
                <button class="btn btn-primary" onclick="createApiKey()">创建</button>
            </div>
        </div>
    `;
    modal.addEventListener('click', () => closeCreateApiKeyModal());
    document.body.appendChild(modal);
}

function closeCreateApiKeyModal() {
    const modal = document.getElementById('create-api-key-modal');
    if (modal) modal.remove();
}

async function createApiKey() {
    const name = document.getElementById('new-api-key-name').value.trim();
    const expireValue = document.getElementById('new-api-key-expire').value;
    
    if (!name) {
        alert('请输入 Key 名称');
        return;
    }
    
    const data = {
        key_name: name,
        scopes: []
    };
    
    if (expireValue) {
        data.expires_at = new Date(expireValue).toISOString();
    }
    
    try {
        const result = await apiRequest(`${API_BASE}/api-keys`, {
            method: 'POST',
            body: JSON.stringify(data)
        });
        
        closeCreateApiKeyModal();
        showApiKeyCreatedModal(result);
        await showApiKeysPage();
    } catch (e) {
        alert(e.message);
    }
}

function showApiKeyCreatedModal(result) {
    const modal = document.createElement('div');
    modal.className = 'modal-overlay';
    modal.id = 'api-key-created-modal';
    
    modal.innerHTML = `
        <div class="modal-content" onclick="event.stopPropagation()">
            <h2 class="modal-header">✅ API Key 创建成功</h2>
            <div class="warning-box">
                <p>⚠️ 请立即复制并保存此 Key！它只会显示这一次。</p>
            </div>
            <div class="form-group">
                <label class="form-label">API Key</label>
                <div class="api-key-display">
                    <input type="text" class="form-input" id="created-api-key" value="${result.api_key}" readonly>
                    <button class="btn btn-primary btn-sm" onclick="copyApiKey()">复制</button>
                </div>
            </div>
            <div class="form-group">
                <label class="form-label">Key 名称</label>
                <input type="text" class="form-input" value="${result.key_name}" readonly>
            </div>
            <div class="form-group">
                <label class="form-label">前缀（用于识别）</label>
                <input type="text" class="form-input" value="${result.key_prefix}" readonly>
            </div>
            <div class="modal-actions">
                <button class="btn btn-primary" onclick="closeApiKeyCreatedModal()">已保存</button>
            </div>
        </div>
    `;
    document.body.appendChild(modal);
}

function copyApiKey() {
    const input = document.getElementById('created-api-key');
    input.select();
    document.execCommand('copy');
    alert('已复制到剪贴板！');
}

function closeApiKeyCreatedModal() {
    const modal = document.getElementById('api-key-created-modal');
    if (modal) modal.remove();
}

async function deleteApiKey(id, name) {
    if (!confirm(`确定要删除 API Key "${name}" 吗？\n删除后将无法恢复。`)) return;
    
    try {
        await apiRequest(`${API_BASE}/api-keys/${id}`, {
            method: 'DELETE'
        });
        await showApiKeysPage();
    } catch (e) {
        alert(e.message);
    }
}

let currentViewingApiKeyId = null;
let apiKeyLogs = [];

async function showApiKeyLogs(id) {
    currentViewingApiKeyId = id;
    const apiKey = apiKeysList.find(k => k.id === id);
    
    try {
        apiKeyLogs = await apiRequest(`${API_BASE}/api-keys/${id}/logs`);
        renderApiKeyLogsModal(apiKey);
    } catch (e) {
        alert(e.message);
    }
}

function renderApiKeyLogsModal(apiKey) {
    const modal = document.createElement('div');
    modal.className = 'modal-overlay';
    modal.id = 'api-key-logs-modal';
    
    modal.innerHTML = `
        <div class="modal-content large-modal" onclick="event.stopPropagation()">
            <h2 class="modal-header">API Key 使用日志 - ${apiKey.key_name}</h2>
            <div class="data-table-wrapper">
                <table class="data-table" id="api-key-logs-table">
                    <thead>
                        <tr>
                            <th>时间</th>
                            <th>方法</th>
                            <th>端点</th>
                            <th>IP</th>
                            <th>状态码</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${apiKeyLogs.length === 0 ? `
                            <tr>
                                <td colspan="5" class="empty-state">
                                    暂无使用记录
                                </td>
                            </tr>
                        ` : apiKeyLogs.map(log => `
                            <tr>
                                <td>${formatDate(log.created_at)}</td>
                                <td><code>${log.method}</code></td>
                                <td><code class="api-endpoint">${log.endpoint}</code></td>
                                <td>${log.ip_address || '-'}</td>
                                <td><span class="status-code ${log.response_status >= 200 && log.response_status < 300 ? 'success' : log.response_status >= 400 ? 'error' : 'info'}">${log.response_status || '-'}</span></td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            </div>
            <div class="modal-actions">
                <button class="btn btn-cancel" onclick="closeApiKeyLogsModal()">关闭</button>
            </div>
        </div>
    `;
    document.body.appendChild(modal);
}

function closeApiKeyLogsModal() {
    const modal = document.getElementById('api-key-logs-modal');
    if (modal) modal.remove();
}

function formatDate(dateStr) {
    if (!dateStr) return '-';
    const date = new Date(dateStr);
    return date.toLocaleString('zh-CN');
}
