// JARVIS AI - Main Application Controller
// Handles navigation, API communication, health checks, settings, toasts, and activity logging

let API_BASE = (typeof window !== 'undefined' && window.location.origin && window.location.origin !== 'null' && window.location.protocol.startsWith('http'))
    ? `${window.location.origin}/api`
    : 'http://127.0.0.1:8000/api';

// ============================================================================
// SETTINGS & LOCAL STORAGE MANAGEMENT
// ============================================================================
const DEFAULT_SETTINGS = {
    theme: 'dark',
    animSpeed: 'normal',
    voiceEnabled: true,
    ttsEnabled: false,
    voiceLang: 'en-US',
    apiEndpoint: 'http://127.0.0.1:8000',
    apiTimeout: 30000,
    saveHistory: true
};

let currentSettings = { ...DEFAULT_SETTINGS };

function loadSettings() {
    try {
        const saved = localStorage.getItem('jarvis_settings');
        if (saved) {
            currentSettings = Object.assign({}, DEFAULT_SETTINGS, JSON.parse(saved));
        }
    } catch (e) {
        console.warn('Failed to parse saved settings, using defaults', e);
        currentSettings = { ...DEFAULT_SETTINGS };
    }

    // Apply API Endpoint
    if (currentSettings.apiEndpoint) {
        let base = currentSettings.apiEndpoint.replace(/\/+$/, '');
        API_BASE = base.endsWith('/api') ? base : base + '/api';
    }

    // Reflect in Settings UI if elements exist
    const themeSelect = document.getElementById('theme-select');
    if (themeSelect) themeSelect.value = currentSettings.theme;

    const animSelect = document.getElementById('anim-speed-select');
    if (animSelect) animSelect.value = currentSettings.animSpeed;

    const voiceToggle = document.getElementById('voice-toggle');
    if (voiceToggle) voiceToggle.checked = currentSettings.voiceEnabled;

    const ttsToggle = document.getElementById('tts-toggle');
    if (ttsToggle) ttsToggle.checked = currentSettings.ttsEnabled;

    const langSelect = document.getElementById('voice-lang-select');
    if (langSelect) langSelect.value = currentSettings.voiceLang;

    const apiInput = document.getElementById('api-endpoint');
    if (apiInput) apiInput.value = currentSettings.apiEndpoint;

    const timeoutInput = document.getElementById('api-timeout');
    if (timeoutInput) timeoutInput.value = currentSettings.apiTimeout;

    const histToggle = document.getElementById('history-toggle');
    if (histToggle) histToggle.checked = currentSettings.saveHistory;

    applyTheme(currentSettings.theme);
}

function saveSettings() {
    const themeSelect = document.getElementById('theme-select');
    const animSelect = document.getElementById('anim-speed-select');
    const voiceToggle = document.getElementById('voice-toggle');
    const ttsToggle = document.getElementById('tts-toggle');
    const langSelect = document.getElementById('voice-lang-select');
    const apiInput = document.getElementById('api-endpoint');
    const timeoutInput = document.getElementById('api-timeout');
    const histToggle = document.getElementById('history-toggle');

    if (themeSelect) currentSettings.theme = themeSelect.value;
    if (animSelect) currentSettings.animSpeed = animSelect.value;
    if (voiceToggle) currentSettings.voiceEnabled = voiceToggle.checked;
    if (ttsToggle) currentSettings.ttsEnabled = ttsToggle.checked;
    if (langSelect) currentSettings.voiceLang = langSelect.value;
    if (apiInput && apiInput.value.trim()) currentSettings.apiEndpoint = apiInput.value.trim();
    if (timeoutInput && timeoutInput.value) currentSettings.apiTimeout = parseInt(timeoutInput.value, 10) || 30000;
    if (histToggle) currentSettings.saveHistory = histToggle.checked;

    let base = currentSettings.apiEndpoint.replace(/\/+$/, '');
    API_BASE = base.endsWith('/api') ? base : base + '/api';

    try {
        localStorage.setItem('jarvis_settings', JSON.stringify(currentSettings));
        showToast('Settings saved successfully', 'success');
    } catch (e) {
        showToast('Error saving settings: ' + e.message, 'error');
    }

    applyTheme(currentSettings.theme);
}

function applyTheme(theme) {
    document.body.classList.remove('theme-dark', 'theme-darker', 'theme-light');
    if (theme === 'darker') {
        document.body.classList.add('theme-darker');
        document.documentElement.style.setProperty('--bg-primary', '#05070d');
        document.documentElement.style.setProperty('--bg-secondary', '#090d1a');
    } else if (theme === 'light') {
        document.body.classList.add('theme-light');
        document.documentElement.style.setProperty('--bg-primary', '#f8fafc');
        document.documentElement.style.setProperty('--bg-secondary', '#e2e8f0');
        document.documentElement.style.setProperty('--text-primary', '#0f172a');
        document.documentElement.style.setProperty('--text-secondary', '#475569');
        document.documentElement.style.setProperty('--bg-card', 'rgba(0,0,0,0.04)');
    } else {
        document.body.classList.add('theme-dark');
        document.documentElement.style.removeProperty('--bg-primary');
        document.documentElement.style.removeProperty('--bg-secondary');
        document.documentElement.style.removeProperty('--text-primary');
        document.documentElement.style.removeProperty('--text-secondary');
        document.documentElement.style.removeProperty('--bg-card');
    }
}

function getAnimDuration() {
    switch (currentSettings.animSpeed) {
        case 'slow': return 800;
        case 'fast': return 150;
        default: return 400;
    }
}

// ============================================================================
// TOAST NOTIFICATIONS
// ============================================================================
function showToast(message, type = 'info', duration = 3500) {
    let container = document.getElementById('toast-container');
    if (!container) {
        container = document.createElement('div');
        container.id = 'toast-container';
        container.style.position = 'fixed';
        container.style.bottom = '24px';
        container.style.right = '24px';
        container.style.zIndex = '99999';
        container.style.display = 'flex';
        container.style.flexDirection = 'column';
        container.style.gap = '10px';
        container.style.pointerEvents = 'none';
        document.body.appendChild(container);
    }

    const toast = document.createElement('div');
    toast.className = `toast toast-${type} card-glass`;
    toast.style.pointerEvents = 'auto';
    toast.style.minWidth = '260px';
    toast.style.maxWidth = '380px';
    toast.style.padding = '12px 18px';
    toast.style.borderRadius = '8px';
    toast.style.fontSize = '0.9rem';
    toast.style.display = 'flex';
    toast.style.alignItems = 'center';
    toast.style.justifyContent = 'space-between';
    toast.style.gap = '12px';
    toast.style.boxShadow = '0 8px 30px rgba(0,0,0,0.45)';
    toast.style.backdropFilter = 'blur(12px)';
    toast.style.transition = 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)';
    toast.style.opacity = '0';
    toast.style.transform = 'translateY(20px)';

    let icon = 'ℹ️';
    let borderColor = 'rgba(0, 212, 255, 0.5)';
    if (type === 'success') {
        icon = '✅';
        borderColor = 'rgba(16, 185, 129, 0.6)';
    } else if (type === 'error') {
        icon = '⚠️';
        borderColor = 'rgba(239, 68, 68, 0.6)';
    } else if (type === 'warning') {
        icon = '⚡';
        borderColor = 'rgba(245, 158, 11, 0.6)';
    }

    toast.style.border = `1px solid ${borderColor}`;
    toast.innerHTML = `
        <div style="display:flex;align-items:center;gap:10px;line-height:1.4;">
            <span style="font-size:1.1rem;">${icon}</span>
            <span>${escapeHtml(message)}</span>
        </div>
        <button style="background:none;border:none;color:#94a3b8;cursor:pointer;font-size:1.1rem;padding:0;line-height:1;" title="Dismiss">&times;</button>
    `;

    const closeBtn = toast.querySelector('button');
    closeBtn.addEventListener('click', () => removeToast(toast));

    container.appendChild(toast);

    requestAnimationFrame(() => {
        toast.style.opacity = '1';
        toast.style.transform = 'translateY(0)';
    });

    const timeout = setTimeout(() => {
        removeToast(toast);
    }, duration);

    function removeToast(el) {
        clearTimeout(timeout);
        el.style.opacity = '0';
        el.style.transform = 'translateY(15px)';
        setTimeout(() => {
            if (el.parentNode) el.parentNode.removeChild(el);
        }, 300);
    }
}

function escapeHtml(text) {
    if (!text) return '';
    const map = { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;' };
    return String(text).replace(/[&<>"']/g, m => map[m]);
}

// ============================================================================
// API HELPER
// ============================================================================
async function apiCall(endpoint, method = 'GET', body = null) {
    const url = endpoint.startsWith('http') ? endpoint : `${API_BASE}${endpoint}`;
    const timeoutMs = currentSettings.apiTimeout || 30000;
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), timeoutMs);

    const opts = {
        method,
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        },
        signal: controller.signal
    };

    if (body !== null && method !== 'GET' && method !== 'HEAD') {
        opts.body = typeof body === 'string' ? body : JSON.stringify(body);
    }

    try {
        const response = await fetch(url, opts);
        clearTimeout(timeoutId);

        let data;
        const contentType = response.headers.get('content-type') || '';
        if (contentType.includes('application/json')) {
            data = await response.json();
        } else {
            const rawText = await response.text();
            try {
                data = JSON.parse(rawText);
            } catch (_) {
                data = { message: rawText };
            }
        }

        if (!response.ok) {
            const errMsg = data.detail || data.message || `Request failed with HTTP ${response.status}`;
            const err = new Error(errMsg);
            err.status = response.status;
            err.data = data;
            throw err;
        }

        return data;
    } catch (e) {
        clearTimeout(timeoutId);
        if (e.name === 'AbortError') {
            const abortErr = new Error(`Request timed out after ${timeoutMs / 1000} seconds`);
            console.error('API Timeout Error:', abortErr);
            throw abortErr;
        }
        console.error(`API Error [${method} ${endpoint}]:`, e);
        throw e;
    }
}

async function testAPIConnection() {
    const statusEl = document.getElementById('api-status');
    if (statusEl) {
        statusEl.textContent = 'Testing connection...';
        statusEl.style.color = '#00d4ff';
    }

    try {
        const result = await apiCall('/health');
        if (statusEl) {
            statusEl.textContent = `Connected! ${result.message || 'JARVIS is online'} (v${result.version || '1.0'})`;
            statusEl.style.color = '#10b981';
        }
        showToast('Backend API is healthy and reachable', 'success');
        updateBackendStatus(true);
    } catch (e) {
        if (statusEl) {
            statusEl.textContent = `Connection failed: ${e.message}`;
            statusEl.style.color = '#ef4444';
        }
        showToast('Failed to connect to backend: ' + e.message, 'error');
        updateBackendStatus(false);
    }
}

function updateBackendStatus(online) {
    const statusDots = document.querySelectorAll('.sidebar-status .status-dot, .chat-status-label .status-dot');
    statusDots.forEach(dot => {
        if (online) {
            dot.classList.remove('offline');
            dot.classList.add('online');
        } else {
            dot.classList.remove('online');
            dot.classList.add('offline');
        }
    });

    const sidebarLabel = document.querySelector('.sidebar-status span');
    if (sidebarLabel) {
        sidebarLabel.textContent = online ? 'JARVIS Online' : 'JARVIS Offline';
    }

    const statCardOnline = document.querySelector('.stat-card.status-online .stat-value');
    if (statCardOnline) {
        statCardOnline.textContent = online ? 'Online' : 'Offline';
    }
}

// ============================================================================
// NAVIGATION & SECTION SWITCHING
// ============================================================================
const navLinks = document.querySelectorAll('.nav-link');
const sections = document.querySelectorAll('.content-section');

function showSection(sectionId, tabId = null) {
    if (!sectionId) sectionId = 'dashboard';

    // Normalize name
    const cleanId = sectionId.replace(/^section-/, '');
    const targetSection = document.getElementById('section-' + cleanId);

    if (!targetSection) {
        console.warn(`Section '#section-${cleanId}' not found.`);
        return;
    }

    // Toggle active section
    sections.forEach(s => s.classList.remove('active'));
    targetSection.classList.add('active');

    // Toggle nav link
    navLinks.forEach(link => {
        if (link.dataset.section === cleanId) {
            link.classList.add('active');
        } else {
            link.classList.remove('active');
        }
    });

    // Update document title
    const formattedTitle = cleanId.charAt(0).toUpperCase() + cleanId.slice(1);
    document.title = `JARVIS AI — ${formattedTitle}`;

    // Update hash without triggering hashchange recursion
    if (window.location.hash.replace('#', '') !== cleanId) {
        history.replaceState(null, '', `#${cleanId}`);
    }

    // Scroll to top of content
    window.scrollTo({ top: 0, behavior: 'smooth' });

    // Activate specific tab if provided
    if (tabId) {
        switchTab(cleanId, tabId);
    }
}

// Global navigateTo function (referenced by HTML onclick attributes)
function navigateTo(sectionId, tabId = null) {
    showSection(sectionId, tabId);
}

// Tab Switcher Helper
function switchTab(sectionCleanId, tabId) {
    let tabBarId = '';
    if (sectionCleanId === 'search') tabBarId = 'search-tabs';
    else if (sectionCleanId === 'puzzles') tabBarId = 'puzzle-tabs';
    else if (sectionCleanId === 'probabilistic') tabBarId = 'prob-tabs';

    const tabBar = document.getElementById(tabBarId);
    if (!tabBar) return;

    // Find tab button
    const targetBtn = tabBar.querySelector(`[data-tab="${tabId}"]`);
    if (targetBtn) {
        targetBtn.click();
    }
}

// Global Tab Manager Setup
function setupTabBars() {
    const tabBars = document.querySelectorAll('.tab-bar');
    tabBars.forEach(bar => {
        const buttons = bar.querySelectorAll('.tab-btn');
        buttons.forEach(btn => {
            btn.addEventListener('click', () => {
                const targetTab = btn.dataset.tab;
                if (!targetTab) return;

                // Deactivate all sibling buttons
                buttons.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');

                // Find matching tab pane
                // Could be inside the same section
                const section = bar.closest('.content-section') || document;
                const contents = section.querySelectorAll('.tab-content');
                contents.forEach(content => {
                    content.classList.remove('active');
                });

                const targetPane = document.getElementById(`tab-${targetTab}`);
                if (targetPane) {
                    targetPane.classList.add('active');
                }
            });
        });
    });
}

// ============================================================================
// ACTIVITY TRACKING & LOCAL HISTORY
// ============================================================================
const MAX_ACTIVITIES = 50;

function logActivity(type, title, meta = '', icon = '⚡') {
    if (!currentSettings.saveHistory) return;

    const activity = {
        id: Date.now(),
        type,
        title,
        meta,
        icon,
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        date: new Date().toLocaleDateString([], { month: 'short', day: 'numeric' })
    };

    let activities = getActivities();
    activities.unshift(activity);
    if (activities.length > MAX_ACTIVITIES) {
        activities = activities.slice(0, MAX_ACTIVITIES);
    }

    try {
        localStorage.setItem('jarvis_activities', JSON.stringify(activities));
    } catch (e) {
        console.warn('Storage quota exceeded, cannot save activity', e);
    }

    renderActivities();
    renderHistorySection();
}

function getActivities() {
    try {
        const saved = localStorage.getItem('jarvis_activities');
        return saved ? JSON.parse(saved) : [];
    } catch (e) {
        return [];
    }
}

function renderActivities() {
    const listEl = document.querySelector('.activity-list');
    if (!listEl) return;

    const activities = getActivities().slice(0, 5);
    if (activities.length === 0) return; // Keep default HTML if empty

    listEl.innerHTML = activities.map(item => `
        <div class="activity-item">
            <div class="activity-dot ${getActivityDotColor(item.type)}"></div>
            <div class="activity-content">
                <span class="activity-title">${escapeHtml(item.title)}</span>
                <span class="activity-time">${item.time}</span>
            </div>
        </div>
    `).join('');
}

function getActivityDotColor(type) {
    switch (type) {
        case 'search': return 'cyan';
        case 'puzzle': return 'blue';
        case 'probabilistic': return 'purple';
        case 'chat': return 'cyan';
        case 'wumpus': return 'blue';
        default: return 'cyan';
    }
}

function renderHistorySection() {
    const container = document.getElementById('history-list');
    if (!container) return;

    const filterVal = (document.getElementById('history-filter')?.value || 'all').toLowerCase();
    const searchVal = (document.getElementById('history-search')?.value || '').toLowerCase().trim();

    let list = getActivities();
    if (filterVal !== 'all') {
        list = list.filter(item => item.type === filterVal);
    }
    if (searchVal) {
        list = list.filter(item =>
            item.title.toLowerCase().includes(searchVal) ||
            item.meta.toLowerCase().includes(searchVal)
        );
    }

    if (list.length === 0) {
        container.innerHTML = `
            <div class="card-glass" style="padding: 2.5rem; text-align: center; color: var(--text-secondary);">
                <p style="font-size: 1.1rem; margin-bottom: 0.5rem;">No history items found.</p>
                <small>Run algorithms or interact with JARVIS to populate this activity log.</small>
            </div>
        `;
        return;
    }

    container.innerHTML = list.map(item => `
        <div class="history-item card-glass">
            <div class="history-icon">${item.icon || '⚡'}</div>
            <div class="history-content">
                <div class="history-title">${escapeHtml(item.title)}</div>
                <div class="history-meta">${escapeHtml(item.meta)}</div>
                <div class="history-time">${item.date}, ${item.time}</div>
            </div>
        </div>
    `).join('');
}

function clearHistory() {
    localStorage.removeItem('jarvis_activities');
    renderHistorySection();
    renderActivities();
    showToast('Activity history cleared', 'info');
}

function clearAllHistory() {
    clearHistory();
    if (typeof window.clearConversation === 'function') {
        window.clearConversation(false);
    }
    showToast('All conversation and activity history purged', 'info');
}

function exportData() {
    const data = {
        settings: currentSettings,
        activities: getActivities(),
        exportedAt: new Date().toISOString()
    };

    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `jarvis_data_${new Date().toISOString().slice(0, 10)}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    showToast('Exported JARVIS state to JSON', 'success');
}

// ============================================================================
// INITIALIZATION
// ============================================================================
window.addEventListener('DOMContentLoaded', () => {
    loadSettings();
    setupTabBars();

    // Bind navigation click listeners
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const section = link.dataset.section;
            if (section) showSection(section);
        });
    });

    // Bind quick action elements
    document.querySelectorAll('[data-navigate]').forEach(el => {
        el.addEventListener('click', () => {
            showSection(el.dataset.navigate);
        });
    });

    // History filters & search input
    const historyFilter = document.getElementById('history-filter');
    if (historyFilter) {
        historyFilter.addEventListener('change', renderHistorySection);
    }
    const historySearch = document.getElementById('history-search');
    if (historySearch) {
        historySearch.addEventListener('input', renderHistorySection);
    }

    // Hash change handler for browser back/forward buttons
    window.addEventListener('hashchange', () => {
        const hash = window.location.hash.replace('#', '');
        if (hash) showSection(hash);
    });

    // Initial section from URL hash or default to dashboard
    const initialHash = window.location.hash.replace('#', '');
    if (initialHash) {
        showSection(initialHash);
    } else {
        showSection('dashboard');
    }

    // Initial health check
    apiCall('/health')
        .then(res => {
            updateBackendStatus(res.status === 'ok');
            console.log('JARVIS backend status:', res);
        })
        .catch(err => {
            updateBackendStatus(false);
            console.warn('Backend not reachable on initial startup:', err.message);
        });

    renderActivities();
    renderHistorySection();
});

// Global exports
window.API_BASE = API_BASE;
window.apiCall = apiCall;
window.showSection = showSection;
window.navigateTo = navigateTo;
window.showToast = showToast;
window.logActivity = logActivity;
window.saveSettings = saveSettings;
window.testAPIConnection = testAPIConnection;
window.clearHistory = clearHistory;
window.clearAllHistory = clearAllHistory;
window.exportData = exportData;
window.currentSettings = currentSettings;
window.getAnimDuration = getAnimDuration;
