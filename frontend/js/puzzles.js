// JARVIS AI - Puzzle Solver Controller
// Implements 8-Puzzle Solver with A* animation and interactive play, and Towers of Hanoi recursive visualizer

// ============================================================================
// 8-PUZZLE SOLVER
// ============================================================================
let puzzleState = [1, 2, 3, 4, 5, 6, 7, 8, 0]; // 0 represents the blank tile
let puzzleAnimationTimer = null;
let puzzleSolving = false;

function renderPuzzle(state) {
    const grid = document.getElementById('puzzle-grid');
    if (!grid) return;

    grid.innerHTML = '';
    state.forEach((num, index) => {
        const tile = document.createElement('div');
        tile.className = `puzzle-tile ${num === 0 ? 'blank' : ''}`;
        tile.dataset.index = index;
        tile.textContent = num === 0 ? '' : num;

        // Interactive tile clicking to slide manually
        tile.addEventListener('click', () => {
            if (puzzleSolving) return;
            handleTileClick(index);
        });

        grid.appendChild(tile);
    });
}

function handleTileClick(index) {
    const blankIndex = puzzleState.indexOf(0);
    const row = Math.floor(index / 3);
    const col = index % 3;
    const blankRow = Math.floor(blankIndex / 3);
    const blankCol = blankIndex % 3;

    // Check Manhattan adjacency
    const isAdjacent = (Math.abs(row - blankRow) + Math.abs(col - blankCol)) === 1;

    if (isAdjacent) {
        // Swap tile and blank
        puzzleState[blankIndex] = puzzleState[index];
        puzzleState[index] = 0;
        renderPuzzle(puzzleState);

        const statusEl = document.getElementById('puzzle-status');
        if (statusEl) statusEl.textContent = isSolved(puzzleState) ? 'Solved! 🎉' : 'Manual Play';
    }
}

function isSolved(state) {
    const goal = [1, 2, 3, 4, 5, 6, 7, 8, 0];
    return state.every((val, idx) => val === goal[idx]);
}

function randomizePuzzle() {
    if (puzzleSolving) return;
    if (puzzleAnimationTimer) clearInterval(puzzleAnimationTimer);

    // Generate random state by making 30 valid random moves from solved state
    // This strictly guarantees that the resulting configuration is solvable!
    let current = [1, 2, 3, 4, 5, 6, 7, 8, 0];
    let lastBlank = 8;

    for (let step = 0; step < 40; step++) {
        const blankIdx = current.indexOf(0);
        const r = Math.floor(blankIdx / 3);
        const c = blankIdx % 3;
        const neighbors = [];

        if (r > 0) neighbors.push(blankIdx - 3); // Up
        if (r < 2) neighbors.push(blankIdx + 3); // Down
        if (c > 0) neighbors.push(blankIdx - 1); // Left
        if (c < 2) neighbors.push(blankIdx + 1); // Right

        // Filter out moving immediately back to the previous blank position if possible
        const choices = neighbors.filter(idx => idx !== lastBlank);
        const chosen = choices.length > 0 ? choices[Math.floor(Math.random() * choices.length)] : neighbors[0];

        lastBlank = blankIdx;
        current[blankIdx] = current[chosen];
        current[chosen] = 0;
    }

    puzzleState = current;
    renderPuzzle(puzzleState);

    const solvableEl = document.getElementById('puzzle-solvable');
    if (solvableEl) solvableEl.textContent = 'Yes';

    const statusEl = document.getElementById('puzzle-status');
    if (statusEl) statusEl.textContent = 'Randomized';

    const movesEl = document.getElementById('puzzle-moves');
    if (movesEl) movesEl.textContent = '0';
    const statesEl = document.getElementById('puzzle-states');
    if (statesEl) statesEl.textContent = '0';
    const timeEl = document.getElementById('puzzle-time');
    if (timeEl) timeEl.textContent = '0ms';

    showToast('Randomized 8-puzzle configuration', 'info', 1500);
}

function resetPuzzle() {
    if (puzzleAnimationTimer) clearInterval(puzzleAnimationTimer);
    puzzleSolving = false;
    puzzleState = [1, 2, 3, 4, 5, 6, 7, 8, 0];
    renderPuzzle(puzzleState);

    const statusEl = document.getElementById('puzzle-status');
    if (statusEl) statusEl.textContent = 'Ready';

    const movesEl = document.getElementById('puzzle-moves');
    if (movesEl) movesEl.textContent = '0';
    const statesEl = document.getElementById('puzzle-states');
    if (statesEl) statesEl.textContent = '0';
    const timeEl = document.getElementById('puzzle-time');
    if (timeEl) timeEl.textContent = '0ms';
    const solvableEl = document.getElementById('puzzle-solvable');
    if (solvableEl) solvableEl.textContent = 'Yes';

    const stepsContainer = document.getElementById('puzzle-solution-steps');
    if (stepsContainer) stepsContainer.innerHTML = '';

    showToast('Reset 8-puzzle to goal state', 'info', 1200);
}

async function solvePuzzle() {
    if (puzzleSolving) return;

    if (isSolved(puzzleState)) {
        showToast('Puzzle is already solved!', 'success', 2000);
        return;
    }

    const heuristic = document.getElementById('puzzle-heuristic')?.value || 'manhattan';
    const statusEl = document.getElementById('puzzle-status');
    const movesEl = document.getElementById('puzzle-moves');
    const statesEl = document.getElementById('puzzle-states');
    const timeEl = document.getElementById('puzzle-time');
    const solvableEl = document.getElementById('puzzle-solvable');
    const stepsContainer = document.getElementById('puzzle-solution-steps');

    if (statusEl) statusEl.textContent = 'Solving with A*...';
    puzzleSolving = true;

    // Convert flat array to 3x3 matrix for backend
    const matrixState = [
        [puzzleState[0], puzzleState[1], puzzleState[2]],
        [puzzleState[3], puzzleState[4], puzzleState[5]],
        [puzzleState[6], puzzleState[7], puzzleState[8]]
    ];

    try {
        showToast(`Solving with ${heuristic} heuristic...`, 'info', 1500);
        const res = await apiCall('/puzzles/eight-puzzle', 'POST', {
            initial_state: matrixState,
            heuristic: heuristic
        });

        if (solvableEl) solvableEl.textContent = res.is_solvable ? 'Yes' : 'No';
        if (movesEl) movesEl.textContent = res.moves;
        if (statesEl) statesEl.textContent = res.explored_states;
        if (timeEl) timeEl.textContent = `${Math.round(res.time_taken * 1000)}ms`;

        if (!res.is_solvable || !res.solution_path || res.solution_path.length === 0) {
            if (statusEl) statusEl.textContent = 'Unsolvable';
            puzzleSolving = false;
            showToast('This puzzle configuration is unsolvable', 'error');
            return;
        }

        if (statusEl) statusEl.textContent = `Solved in ${res.moves} moves! Animating...`;

        // Render solution steps list
        if (stepsContainer) {
            stepsContainer.innerHTML = `
                <div style="font-weight:600;margin-bottom:8px;color:var(--accent-cyan);">Solution Steps (${res.solution_path.length} states):</div>
                <div class="steps-scroll" style="display:flex;gap:8px;overflow-x:auto;padding-bottom:8px;">
                    ${res.solution_path.map((st, i) => `
                        <button class="step-chip card-glass" style="padding:4px 8px;font-size:0.8rem;cursor:pointer;white-space:nowrap;" onclick="displayPuzzleStep(${i})">
                            Step ${i}
                        </button>
                    `).join('')}
                </div>
            `;
            window.cachedPuzzlePath = res.solution_path;
        }

        // Animate solution path
        animatePuzzleSolution(res.solution_path);

        logActivity('puzzle', `8-Puzzle (${heuristic})`, `${res.moves} moves · ${res.explored_states} states explored`, '🧩');

    } catch (e) {
        puzzleSolving = false;
        if (statusEl) statusEl.textContent = 'Error';
        showToast(`8-Puzzle Error: ${e.message}`, 'error');
    }
}

function displayPuzzleStep(stepIndex) {
    if (!window.cachedPuzzlePath || !window.cachedPuzzlePath[stepIndex]) return;
    const matrix = window.cachedPuzzlePath[stepIndex];
    puzzleState = matrix.flat();
    renderPuzzle(puzzleState);
}

function animatePuzzleSolution(path) {
    let stepIndex = 0;
    const speed = window.getAnimDuration ? Math.max(150, window.getAnimDuration()) : 350;

    if (puzzleAnimationTimer) clearInterval(puzzleAnimationTimer);

    puzzleAnimationTimer = setInterval(() => {
        if (stepIndex < path.length) {
            const matrix = path[stepIndex];
            puzzleState = matrix.flat();
            renderPuzzle(puzzleState);

            const statusEl = document.getElementById('puzzle-status');
            if (statusEl) statusEl.textContent = `Step ${stepIndex} / ${path.length - 1}`;
            stepIndex++;
        } else {
            clearInterval(puzzleAnimationTimer);
            puzzleAnimationTimer = null;
            puzzleSolving = false;
            const statusEl = document.getElementById('puzzle-status');
            if (statusEl) statusEl.textContent = 'Completed! 🎉';
            showToast('8-Puzzle animation complete!', 'success');
        }
    }, speed);
}

// ============================================================================
// TOWERS OF HANOI
// ============================================================================
let hanoiDisks = 3;
let hanoiPegs = { A: [], B: [], C: [] };
let hanoiMoves = [];
let hanoiMoveIndex = 0;
let hanoiTimer = null;
let hanoiPaused = false;
let hanoiTotalMoves = 7;

function initHanoi(n = 3) {
    hanoiDisks = Math.min(8, Math.max(1, n));
    hanoiPegs = {
        A: [],
        B: [],
        C: []
    };
    // Largest disk at bottom (index 0), smallest at top (index n-1)
    for (let i = hanoiDisks; i >= 1; i--) {
        hanoiPegs.A.push(i);
    }
    hanoiMoves = [];
    hanoiMoveIndex = 0;
    hanoiTotalMoves = Math.pow(2, hanoiDisks) - 1;

    renderHanoi();

    const moveCountEl = document.getElementById('hanoi-move-count');
    if (moveCountEl) moveCountEl.textContent = '0';

    const totalMovesEl = document.getElementById('hanoi-total-moves');
    if (totalMovesEl) totalMovesEl.textContent = hanoiTotalMoves;

    const statusEl = document.getElementById('hanoi-status');
    if (statusEl) statusEl.textContent = 'Ready';

    const startBtn = document.getElementById('hanoi-start-btn');
    if (startBtn) {
        startBtn.textContent = '▶ Start';
        startBtn.disabled = false;
    }

    const pauseBtn = document.getElementById('hanoi-pause-btn');
    if (pauseBtn) {
        pauseBtn.disabled = true;
        pauseBtn.textContent = '⏸ Pause';
    }

    const logScroll = document.getElementById('hanoi-log-scroll');
    if (logScroll) logScroll.innerHTML = '<div style="color:var(--text-secondary);font-size:0.85rem;">Press Start to solve Towers of Hanoi.</div>';
}

function renderHanoi() {
    ['a', 'b', 'c'].forEach(pegChar => {
        const pegUpper = pegChar.toUpperCase();
        const pegDisksEl = document.getElementById(`peg-${pegChar}-disks`);
        if (!pegDisksEl) return;

        pegDisksEl.innerHTML = '';
        const disks = hanoiPegs[pegUpper] || [];

        disks.forEach(diskSize => {
            const diskEl = document.createElement('div');
            diskEl.className = `hanoi-disk disk-${diskSize}`;
            diskEl.textContent = diskSize;

            // Width relative to disk count
            const pct = 25 + (diskSize / hanoiDisks) * 70;
            diskEl.style.width = `${pct}%`;
            diskEl.style.height = '18px';
            diskEl.style.margin = '2px auto';
            diskEl.style.borderRadius = '4px';
            diskEl.style.display = 'flex';
            diskEl.style.alignItems = 'center';
            diskEl.style.justifyContent = 'center';
            diskEl.style.fontSize = '10px';
            diskEl.style.fontWeight = 'bold';
            diskEl.style.color = '#ffffff';

            // Distinct gradient color per disk
            const colors = [
                'linear-gradient(90deg, #00d4ff, #0066ff)',
                'linear-gradient(90deg, #7c3aed, #a855f7)',
                'linear-gradient(90deg, #10b981, #059669)',
                'linear-gradient(90deg, #f59e0b, #d97706)',
                'linear-gradient(90deg, #ef4444, #dc2626)',
                'linear-gradient(90deg, #ec4899, #db2777)',
                'linear-gradient(90deg, #6366f1, #4f46e5)',
                'linear-gradient(90deg, #14b8a6, #0d9488)'
            ];
            diskEl.style.background = colors[(diskSize - 1) % colors.length];
            diskEl.style.boxShadow = '0 2px 8px rgba(0,0,0,0.4)';

            pegDisksEl.appendChild(diskEl);
        });
    });
}

async function startHanoi() {
    if (hanoiTimer && !hanoiPaused) return;

    // If resumed from pause
    if (hanoiPaused && hanoiTimer) {
        hanoiPaused = false;
        const pauseBtn = document.getElementById('hanoi-pause-btn');
        if (pauseBtn) pauseBtn.textContent = '⏸ Pause';
        runHanoiStepLoop();
        return;
    }

    const numDisks = parseInt(document.getElementById('hanoi-disks')?.value, 10) || 3;
    initHanoi(numDisks);

    const statusEl = document.getElementById('hanoi-status');
    const startBtn = document.getElementById('hanoi-start-btn');
    const pauseBtn = document.getElementById('hanoi-pause-btn');

    if (statusEl) statusEl.textContent = 'Solving...';
    if (startBtn) startBtn.disabled = true;

    try {
        const res = await apiCall('/puzzles/hanoi', 'POST', { num_disks: numDisks });
        hanoiMoves = res.moves || [];
        hanoiMoveIndex = 0;

        if (statusEl) statusEl.textContent = 'Running...';
        if (pauseBtn) pauseBtn.disabled = false;

        const logScroll = document.getElementById('hanoi-log-scroll');
        if (logScroll) logScroll.innerHTML = '';

        runHanoiStepLoop();

        logActivity('puzzle', `Towers of Hanoi (${numDisks} disks)`, `${res.total_moves} moves required`, '🗼');

    } catch (e) {
        if (statusEl) statusEl.textContent = 'Error';
        if (startBtn) startBtn.disabled = false;
        showToast(`Hanoi Error: ${e.message}`, 'error');
    }
}

function runHanoiStepLoop() {
    const speedInput = document.getElementById('hanoi-speed');
    const speed = parseInt(speedInput?.value, 10) || 500;

    if (hanoiTimer) clearTimeout(hanoiTimer);

    const step = () => {
        if (hanoiPaused) return;

        if (hanoiMoveIndex < hanoiMoves.length) {
            const mv = hanoiMoves[hanoiMoveIndex];
            const fromPeg = (mv.from || mv.from_peg || 'A').toUpperCase();
            const toPeg = (mv.to || mv.to_peg || 'C').toUpperCase();

            // Execute move in state
            if (hanoiPegs[fromPeg] && hanoiPegs[fromPeg].length > 0) {
                const disk = hanoiPegs[fromPeg].pop();
                hanoiPegs[toPeg].push(disk);
            }

            renderHanoi();
            hanoiMoveIndex++;

            const moveCountEl = document.getElementById('hanoi-move-count');
            if (moveCountEl) moveCountEl.textContent = hanoiMoveIndex;

            // Log step
            const logScroll = document.getElementById('hanoi-log-scroll');
            if (logScroll) {
                const logItem = document.createElement('div');
                logItem.style.fontSize = '0.85rem';
                logItem.style.padding = '3px 0';
                logItem.style.borderBottom = '1px solid rgba(255,255,255,0.05)';
                logItem.innerHTML = `<strong>#${hanoiMoveIndex}:</strong> Move disk from <span style="color:#00d4ff;">${fromPeg}</span> → <span style="color:#10b981;">${toPeg}</span>`;
                logScroll.prepend(logItem);
            }

            hanoiTimer = setTimeout(step, speed);
        } else {
            // Done
            hanoiTimer = null;
            const statusEl = document.getElementById('hanoi-status');
            if (statusEl) statusEl.textContent = 'Completed! 🎉';
            const pauseBtn = document.getElementById('hanoi-pause-btn');
            if (pauseBtn) pauseBtn.disabled = true;
            const startBtn = document.getElementById('hanoi-start-btn');
            if (startBtn) {
                startBtn.disabled = false;
                startBtn.textContent = '▶ Start Again';
            }
            showToast(`Towers of Hanoi completed in ${hanoiMoveIndex} moves!`, 'success');
        }
    };

    hanoiTimer = setTimeout(step, speed);
}

function pauseHanoi() {
    const pauseBtn = document.getElementById('hanoi-pause-btn');
    if (!pauseBtn) return;

    if (hanoiPaused) {
        hanoiPaused = false;
        pauseBtn.textContent = '⏸ Pause';
        runHanoiStepLoop();
    } else {
        hanoiPaused = true;
        pauseBtn.textContent = '▶ Resume';
        if (hanoiTimer) clearTimeout(hanoiTimer);
    }
}

function resetHanoi() {
    if (hanoiTimer) clearTimeout(hanoiTimer);
    hanoiTimer = null;
    hanoiPaused = false;
    const numDisks = parseInt(document.getElementById('hanoi-disks')?.value, 10) || 3;
    initHanoi(numDisks);
    showToast('Reset Towers of Hanoi', 'info', 1200);
}

// ============================================================================
// INITIALIZATION
// ============================================================================
window.addEventListener('DOMContentLoaded', () => {
    renderPuzzle(puzzleState);
    initHanoi(3);

    const hanoiDisksInput = document.getElementById('hanoi-disks');
    if (hanoiDisksInput) {
        hanoiDisksInput.addEventListener('change', () => {
            const n = parseInt(hanoiDisksInput.value, 10) || 3;
            initHanoi(n);
        });
    }
});

// Global exports
window.solvePuzzle = solvePuzzle;
window.randomizePuzzle = randomizePuzzle;
window.resetPuzzle = resetPuzzle;
window.displayPuzzleStep = displayPuzzleStep;
window.startHanoi = startHanoi;
window.pauseHanoi = pauseHanoi;
window.resetHanoi = resetHanoi;
