// JARVIS AI - Google Gemini LLM Integration Controller
// Handles Gemini LLM status checks, configuration modal, key testing, and UI synchronization.

let geminiState = {
    configured: false,
    activeModel: 'gemini-3.5-flash',
    maskedKey: null,
    availableModels: ['gemini-3.5-flash', 'gemini-3.8-flash']
};

/**
 * Fetch and synchronize the Google Gemini status with the backend.
 */
async function checkGeminiStatus() {
    try {
        const status = await apiCall('/llm/status', 'GET');
        geminiState.configured = !!(status.configured && status.enabled);
        geminiState.activeModel = status.active_model || 'gemini-3.5-flash';
        geminiState.maskedKey = status.masked_key || null;
        if (Array.isArray(status.available_models) && status.available_models.length > 0) {
            geminiState.availableModels = status.available_models;
        }

        updateGeminiUI();
        return geminiState;
    } catch (err) {
        console.warn('Gemini status check failed:', err.message);
        geminiState.configured = false;
        updateGeminiUI();
        return geminiState;
    }
}

/**
 * Update all Gemini-related UI badges, pills, and settings fields.
 */
function updateGeminiUI() {
    // 1. Update Chat Header Pill
    const pill = document.getElementById('gemini-status-pill');
    const pillDot = document.getElementById('gemini-pill-dot');
    const pillText = document.getElementById('gemini-pill-text');

    if (pill && pillDot && pillText) {
        if (geminiState.configured) {
            pill.className = 'gemini-status-pill online';
            pill.title = `Gemini LLM Active (${geminiState.activeModel}) - Click to configure`;
            pillDot.className = 'status-dot online small';
            pillText.innerHTML = `<strong>Gemini:</strong> ${escapeHtml(geminiState.activeModel)}`;
        } else {
            pill.className = 'gemini-status-pill offline';
            pill.title = 'Gemini LLM Offline (Using Local Fallback) - Click to configure';
            pillDot.className = 'status-dot offline small';
            pillText.innerHTML = '<strong>Gemini:</strong> Offline (Fallback)';
        }
    }

    // 2. Populate and synchronize modal fields
    const modalKeyInput = document.getElementById('gemini-modal-key');
    const modalModelSelect = document.getElementById('gemini-modal-model');
    const modalStatusBanner = document.getElementById('gemini-modal-status-banner');

    if (modalModelSelect) {
        populateModelDropdown(modalModelSelect, geminiState.availableModels, geminiState.activeModel);
    }

    if (modalStatusBanner) {
        if (geminiState.configured) {
            modalStatusBanner.className = 'gemini-status-banner banner-success';
            modalStatusBanner.innerHTML = `
                <div class="banner-icon">✓</div>
                <div class="banner-content">
                    <span class="banner-title">Gemini AI Active</span>
                    <span class="banner-sub">Key: <code>${escapeHtml(geminiState.maskedKey || 'Configured')}</code> &bull; Model: <code>${escapeHtml(geminiState.activeModel)}</code></span>
                </div>
            `;
        } else {
            modalStatusBanner.className = 'gemini-status-banner banner-warning';
            modalStatusBanner.innerHTML = `
                <div class="banner-icon">⚡</div>
                <div class="banner-content">
                    <span class="banner-title">Offline Fallback Mode</span>
                    <span class="banner-sub">No active Gemini key. JARVIS will use local deterministic intent recognition.</span>
                </div>
            `;
        }
    }

    // 3. Populate and synchronize Settings Section fields
    const settingsModelSelect = document.getElementById('settings-gemini-model');
    const settingsStatusBanner = document.getElementById('settings-gemini-status-banner');

    if (settingsModelSelect) {
        populateModelDropdown(settingsModelSelect, geminiState.availableModels, geminiState.activeModel);
    }

    if (settingsStatusBanner) {
        if (geminiState.configured) {
            settingsStatusBanner.innerHTML = `<span class="badge badge-success">● Active</span> Key: <code>${escapeHtml(geminiState.maskedKey || 'Configured')}</code> &bull; Model: <code>${escapeHtml(geminiState.activeModel)}</code>`;
        } else {
            settingsStatusBanner.innerHTML = `<span class="badge badge-warning">● Offline</span> Using deterministic pattern matching fallback`;
        }
    }
}

/**
 * Helper to populate a select element with model choices.
 */
function populateModelDropdown(selectEl, models, currentModel) {
    if (!selectEl) return;
    const previousVal = selectEl.value;
    selectEl.innerHTML = '';
    models.forEach(model => {
        const opt = document.createElement('option');
        opt.value = model;
        opt.textContent = model + (model.includes('flash') ? ' (Recommended)' : '');
        if (model === currentModel) {
            opt.selected = true;
        }
        selectEl.appendChild(opt);
    });
    if (previousVal && models.includes(previousVal) && !currentModel) {
        selectEl.value = previousVal;
    }
}

/**
 * Open the Gemini Configuration Modal.
 */
function openGeminiModal() {
    const modal = document.getElementById('gemini-modal');
    if (!modal) return;
    modal.classList.add('active');
    document.body.style.overflow = 'hidden';

    // Clear result message
    const resBox = document.getElementById('gemini-modal-result');
    if (resBox) {
        resBox.innerHTML = '';
        resBox.style.display = 'none';
    }

    // Refresh state
    checkGeminiStatus();

    // Focus key input
    setTimeout(() => {
        const keyInput = document.getElementById('gemini-modal-key');
        if (keyInput) keyInput.focus();
    }, 100);
}

/**
 * Close the Gemini Configuration Modal.
 */
function closeGeminiModal() {
    const modal = document.getElementById('gemini-modal');
    if (!modal) return;
    modal.classList.remove('active');
    document.body.style.overflow = '';
}

/**
 * Toggle visibility of an API key input.
 */
function toggleKeyVisibility(inputId, btnEl) {
    const input = document.getElementById(inputId);
    if (!input) return;
    if (input.type === 'password') {
        input.type = 'text';
        if (btnEl) btnEl.textContent = '🔒';
    } else {
        input.type = 'password';
        if (btnEl) btnEl.textContent = '👁';
    }
}

/**
 * Test the Gemini API connection.
 */
async function testGeminiConnection(keyInputId, modelSelectId, resultBoxId, btnEl) {
    const keyInput = document.getElementById(keyInputId);
    const modelSelect = document.getElementById(modelSelectId);
    const resultBox = document.getElementById(resultBoxId);

    const apiKey = keyInput ? keyInput.value.trim() : null;
    const model = modelSelect ? modelSelect.value : null;

    if (resultBox) {
        resultBox.style.display = 'block';
        resultBox.className = 'test-result-box loading';
        resultBox.innerHTML = '<span class="spinner-small"></span> Testing connection to Google Gemini API...';
    }

    if (btnEl) btnEl.disabled = true;

    try {
        const payload = {};
        if (apiKey) payload.api_key = apiKey;
        if (model) payload.model = model;

        const res = await apiCall('/llm/test-connection', 'POST', payload);
        if (btnEl) btnEl.disabled = false;

        if (resultBox) {
            if (res.success) {
                resultBox.className = 'test-result-box success';
                resultBox.innerHTML = `✅ <strong>Connected:</strong> ${escapeHtml(res.message)} (Model: ${escapeHtml(res.model || model)})`;
                showToast('Gemini API test successful!', 'success');
            } else {
                resultBox.className = 'test-result-box error';
                resultBox.innerHTML = `❌ <strong>Error:</strong> ${escapeHtml(res.message)}`;
                showToast('Gemini API test failed: ' + res.message, 'error');
            }
        }
    } catch (e) {
        if (btnEl) btnEl.disabled = false;
        if (resultBox) {
            resultBox.className = 'test-result-box error';
            resultBox.innerHTML = `❌ <strong>Connection Error:</strong> ${escapeHtml(e.message)}`;
        }
        showToast('Gemini connection test failed: ' + e.message, 'error');
    }
}

/**
 * Save new Gemini configuration (API Key + Model).
 */
async function saveGeminiConfiguration(keyInputId, modelSelectId, resultBoxId, btnEl) {
    const keyInput = document.getElementById(keyInputId);
    const modelSelect = document.getElementById(modelSelectId);
    const resultBox = document.getElementById(resultBoxId);

    const apiKey = keyInput ? keyInput.value.trim() : '';
    const model = modelSelect ? modelSelect.value : 'gemini-3.5-flash';

    if (!apiKey) {
        if (resultBox) {
            resultBox.style.display = 'block';
            resultBox.className = 'test-result-box error';
            resultBox.innerHTML = '⚠️ Please enter a valid Gemini API key.';
        }
        showToast('Please provide an API key.', 'warning');
        return;
    }

    if (resultBox) {
        resultBox.style.display = 'block';
        resultBox.className = 'test-result-box loading';
        resultBox.innerHTML = '<span class="spinner-small"></span> Validating and saving configuration...';
    }

    if (btnEl) btnEl.disabled = true;

    try {
        const res = await apiCall('/llm/configure', 'POST', {
            api_key: apiKey,
            model: model
        });

        if (btnEl) btnEl.disabled = false;

        if (res.success) {
            if (resultBox) {
                resultBox.className = 'test-result-box success';
                resultBox.innerHTML = `✅ ${escapeHtml(res.message)} &bull; Active: <code>${escapeHtml(res.masked_key || '')}</code>`;
            }
            if (keyInput) keyInput.value = ''; // Clear plaintext input after saving
            showToast('Gemini LLM configured and activated!', 'success');
            await checkGeminiStatus();
            setTimeout(() => {
                closeGeminiModal();
            }, 1200);
        } else {
            if (resultBox) {
                resultBox.className = 'test-result-box error';
                resultBox.innerHTML = `❌ ${escapeHtml(res.message)}`;
            }
            showToast('Configuration failed: ' + res.message, 'error');
        }
    } catch (e) {
        if (btnEl) btnEl.disabled = false;
        if (resultBox) {
            resultBox.className = 'test-result-box error';
            resultBox.innerHTML = `❌ <strong>Save Error:</strong> ${escapeHtml(e.message)}`;
        }
        showToast('Failed to save Gemini configuration: ' + e.message, 'error');
    }
}

// Global exports
window.geminiState = geminiState;
window.checkGeminiStatus = checkGeminiStatus;
window.updateGeminiUI = updateGeminiUI;
window.openGeminiModal = openGeminiModal;
window.closeGeminiModal = closeGeminiModal;
window.toggleKeyVisibility = toggleKeyVisibility;
window.testGeminiConnection = testGeminiConnection;
window.saveGeminiConfiguration = saveGeminiConfiguration;
