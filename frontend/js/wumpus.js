// JARVIS AI - Wumpus World Controller
// Manages 4x4 hazardous cave exploration, logical knowledge base inference, and action commands

let wumpusSessionId = 'default';
let currentWumpusState = null;

// ============================================================================
// WUMPUS WORLD ACTIONS
// ============================================================================
async function newWumpusGame() {
    try {
        showToast('Initializing new Wumpus World...', 'info', 1500);
        const res = await apiCall('/puzzles/wumpus/new', 'POST', {
            grid_size: 4
        });

        // Extract session ID if present in message or response
        const match = res.message ? res.message.match(/session:\s*([a-f0-9-]+)/i) : null;
        if (match) {
            wumpusSessionId = match[1];
        } else {
            wumpusSessionId = 'default';
        }

        updateWumpusUI(res);
        logActivity('wumpus', 'Wumpus World: New Game Started', '4x4 Cave Exploration', '🌍');
        showToast('New Wumpus game started! Find the gold and climb out.', 'success');

    } catch (e) {
        console.error('New Wumpus game error:', e);
        showToast(`Failed to start game: ${e.message}`, 'error');
    }
}

async function sendWumpusAction(action, direction = null) {
    try {
        const body = { action };
        if (direction) body.direction = direction;

        const endpoint = `/puzzles/wumpus/action?session_id=${encodeURIComponent(wumpusSessionId)}`;
        const res = await apiCall(endpoint, 'POST', body);

        updateWumpusUI(res);

        if (res.game_status === 'won') {
            showToast('🎉 CONGRATULATIONS! You escaped with the gold!', 'success', 5000);
            logActivity('wumpus', 'Wumpus World Victory!', `Final Score: ${res.score || 1000}`, '🏆');
        } else if (res.game_status === 'died') {
            showToast('💀 Game Over! The cave claimed another explorer.', 'error', 4000);
            logActivity('wumpus', 'Wumpus World: Agent Died', res.message || 'Game Over', '💀');
        }

    } catch (e) {
        console.error('Wumpus action error:', e);
        showToast(`Action error: ${e.message}`, 'error');
    }
}

function wumpusMove(direction) {
    sendWumpusAction('move', direction);
}

function wumpusShoot() {
    sendWumpusAction('shoot');
}

function wumpusGrab() {
    sendWumpusAction('grab');
}

function wumpusClimb() {
    sendWumpusAction('climb');
}

// ============================================================================
// UI RENDERING & STATE UPDATES
// ============================================================================
function updateWumpusUI(data) {
    currentWumpusState = data;

    const gridEl = document.getElementById('wumpus-grid');
    const agentPos = data.agent_pos || [0, 0];
    const gridState = data.grid_state || [];
    const percepts = data.percepts || {};
    const knowledge = data.knowledge || {};
    const status = data.game_status || 'playing';

    // 1. Render Grid
    // Standard Wumpus World coordinates: row 0 is bottom, row 3 is top.
    // Display row 3 at top down to row 0 at bottom.
    if (gridEl) {
        gridEl.innerHTML = '';
        for (let r = 3; r >= 0; r--) {
            for (let c = 0; c < 4; c++) {
                const cell = (gridState[r] && gridState[r][c]) ? gridState[r][c] : {};
                const isAgent = (agentPos[0] === r && agentPos[1] === c);
                const coordKey = `${r},${c}`;
                const cellKnowledge = knowledge[coordKey] || {};

                const cellEl = document.createElement('div');
                cellEl.className = 'wumpus-cell';

                // Status styling
                if (isAgent) {
                    cellEl.classList.add('has-agent');
                }
                if (cell.visited || cellKnowledge.visited) {
                    cellEl.classList.add('visited');
                }
                if (cellKnowledge.safe) {
                    cellEl.classList.add('safe');
                }

                // Inner content
                let iconsHtml = '';
                if (isAgent) {
                    iconsHtml += '<span class="cell-icon agent-icon" title="Agent">🤖</span>';
                }

                // Show items if revealed or game is over
                const gameOver = status === 'won' || status === 'died';

                if (cell.gold || (gameOver && cell.gold)) {
                    iconsHtml += '<span class="cell-icon gold-icon" title="Gold">💰</span>';
                }
                if (cell.wumpus || (gameOver && cell.wumpus)) {
                    iconsHtml += `<span class="cell-icon wumpus-icon" title="Wumpus">${data.wumpus_alive !== false ? '👹' : '💀'}</span>`;
                }
                if (cell.pit || (gameOver && cell.pit)) {
                    iconsHtml += '<span class="cell-icon pit-icon" title="Pit">🕳️</span>';
                }

                // Percept icons in cell
                if (cell.breeze && (cell.visited || gameOver)) {
                    iconsHtml += '<span class="cell-sub-icon" title="Breeze">💨</span>';
                }
                if (cell.stench && (cell.visited || gameOver)) {
                    iconsHtml += '<span class="cell-sub-icon" title="Stench">🦨</span>';
                }

                cellEl.innerHTML = `
                    <span class="cell-coord">[${r + 1},${c + 1}]</span>
                    <div class="cell-content">${iconsHtml}</div>
                `;

                gridEl.appendChild(cellEl);
            }
        }
    }

    // 2. Update Percepts
    updatePerceptIndicator('stench', percepts.stench);
    updatePerceptIndicator('breeze', percepts.breeze);
    updatePerceptIndicator('glitter', percepts.glitter);
    updatePerceptIndicator('bump', percepts.bump);
    updatePerceptIndicator('scream', percepts.scream);

    // 3. Update Knowledge Base Panel
    const kbEl = document.getElementById('kb-content');
    if (kbEl) {
        kbEl.innerHTML = '';
        const kbItems = [];

        // Current position info
        kbItems.push(`Agent at [${agentPos[0] + 1}, ${agentPos[1] + 1}].`);

        // Active percepts
        const activePercepts = Object.entries(percepts).filter(([_, v]) => v).map(([k]) => k.toUpperCase());
        if (activePercepts.length > 0) {
            kbItems.push(`Percepts sensed: <strong style="color:var(--accent-cyan);">${activePercepts.join(', ')}</strong>.`);
        } else {
            kbItems.push('No hazardous percepts detected in current room.');
        }

        // Inferred knowledge from backend
        Object.entries(knowledge).forEach(([coord, info]) => {
            const [r, c] = coord.split(',').map(n => Number(n) + 1);
            if (info.confirmed_wumpus) {
                kbItems.push(`<span style="color:#ef4444;font-weight:600;">⚠️ Confirmed Wumpus at [${r},${c}]</span>`);
            } else if (info.possible_wumpus) {
                kbItems.push(`Possible Wumpus near [${r},${c}].`);
            }
            if (info.confirmed_pit) {
                kbItems.push(`<span style="color:#ef4444;font-weight:600;">⚠️ Confirmed Pit at [${r},${c}]</span>`);
            } else if (info.possible_pit) {
                kbItems.push(`Possible Pit near [${r},${c}].`);
            }
            if (info.safe && !info.visited) {
                kbItems.push(`<span style="color:#10b981;">✓ Room [${r},${c}] inferred SAFE to enter.</span>`);
            }
        });

        kbEl.innerHTML = kbItems.map(item => `<div class="kb-item">${item}</div>`).join('');
    }

    // 4. Update Game Status
    const scoreEl = document.getElementById('wumpus-score');
    if (scoreEl) scoreEl.textContent = data.score !== undefined ? data.score : 0;

    const arrowsEl = document.getElementById('wumpus-arrows');
    if (arrowsEl) arrowsEl.textContent = data.has_arrow !== undefined ? (data.has_arrow ? '1' : '0') : '1';

    const goldEl = document.getElementById('wumpus-gold');
    if (goldEl) {
        goldEl.textContent = data.has_gold ? 'Collected 💰' : 'Not collected';
        goldEl.style.color = data.has_gold ? '#f59e0b' : '';
    }

    const aliveEl = document.getElementById('wumpus-alive');
    if (aliveEl) {
        aliveEl.textContent = data.wumpus_alive ? 'Alive 👹' : 'Dead 💀';
        aliveEl.style.color = data.wumpus_alive ? '#ef4444' : '#10b981';
    }

    const gameStatusEl = document.getElementById('wumpus-game-status');
    if (gameStatusEl) {
        if (status === 'won') {
            gameStatusEl.textContent = 'Victory! 🏆';
            gameStatusEl.style.color = '#10b981';
        } else if (status === 'died') {
            gameStatusEl.textContent = 'Defeated 💀';
            gameStatusEl.style.color = '#ef4444';
        } else {
            gameStatusEl.textContent = 'Exploring';
            gameStatusEl.style.color = 'var(--accent-cyan)';
        }
    }

    const messageEl = document.getElementById('wumpus-message');
    if (messageEl && data.message) {
        messageEl.textContent = data.message;
    }
}

function updatePerceptIndicator(name, active) {
    const itemEl = document.getElementById(`percept-${name}`);
    const valEl = document.getElementById(`pv-${name}`);

    if (valEl) {
        valEl.textContent = active ? 'YES' : 'No';
        valEl.style.color = active ? '#00d4ff' : '#94a3b8';
        valEl.style.fontWeight = active ? 'bold' : 'normal';
    }

    if (itemEl) {
        if (active) {
            itemEl.classList.add('active');
            itemEl.style.borderColor = 'rgba(0, 212, 255, 0.6)';
            itemEl.style.background = 'rgba(0, 212, 255, 0.1)';
        } else {
            itemEl.classList.remove('active');
            itemEl.style.borderColor = '';
            itemEl.style.background = '';
        }
    }
}

// ============================================================================
// KEYBOARD CONTROLS & INITIALIZATION
// ============================================================================
window.addEventListener('DOMContentLoaded', () => {
    // Initial board setup
    newWumpusGame();

    // Arrow keys & WASD to move agent when Wumpus section is active
    window.addEventListener('keydown', (e) => {
        const wumpusSec = document.getElementById('section-wumpus');
        if (!wumpusSec || !wumpusSec.classList.contains('active')) return;

        // Ignore if user is typing in an input
        if (['INPUT', 'TEXTAREA', 'SELECT'].includes(document.activeElement?.tagName)) return;

        switch (e.key) {
            case 'ArrowUp':
            case 'w':
            case 'W':
                e.preventDefault();
                wumpusMove('up');
                break;
            case 'ArrowDown':
            case 's':
            case 'S':
                e.preventDefault();
                wumpusMove('down');
                break;
            case 'ArrowLeft':
            case 'a':
            case 'A':
                e.preventDefault();
                wumpusMove('left');
                break;
            case 'ArrowRight':
            case 'd':
            case 'D':
                e.preventDefault();
                wumpusMove('right');
                break;
            case ' ':
                e.preventDefault();
                wumpusShoot();
                break;
            case 'g':
            case 'G':
                e.preventDefault();
                wumpusGrab();
                break;
            case 'c':
            case 'C':
                e.preventDefault();
                wumpusClimb();
                break;
        }
    });
});

// Global exports
window.wumpusMove = wumpusMove;
window.wumpusShoot = wumpusShoot;
window.wumpusGrab = wumpusGrab;
window.wumpusClimb = wumpusClimb;
window.newWumpusGame = newWumpusGame;
