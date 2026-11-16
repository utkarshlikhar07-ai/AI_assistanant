// JARVIS AI - Search & Optimization Algorithms Controller
// Manages BFS, DFS, IDDFS, A*, D* Lite, Hill Climbing, and Simulated Annealing

// Instances of GraphVisualizers for each tab
const graphVisualizers = {};
let dstarVisualizer = null;

// ============================================================================
// GRAPH PARSING & SELECT HELPERS
// ============================================================================
function parseNodes(nodesStr) {
    if (!nodesStr) return [];
    return nodesStr.split(',')
        .map(s => s.trim())
        .filter(s => s.length > 0);
}

function parseEdges(edgesStr, weighted = false) {
    if (!edgesStr) return [];
    const lines = edgesStr.split('\n');
    const edges = [];

    lines.forEach(line => {
        const parts = line.trim().split(/\s+/).filter(Boolean);
        if (parts.length >= 2) {
            const u = parts[0];
            const v = parts[1];
            let w = 1.0;
            if (parts.length >= 3) {
                w = parseFloat(parts[2]) || 1.0;
            }
            if (weighted) {
                edges.push({ from_node: u, to_node: v, weight: w });
            } else {
                edges.push([u, v]);
            }
        }
    });

    return edges;
}

function parseHeuristics(heuristicsStr, nodes) {
    const heuristics = {};
    if (!heuristicsStr) {
        nodes.forEach(n => { heuristics[n] = 0.0; });
        return heuristics;
    }

    try {
        // Try parsing JSON first
        const parsed = JSON.parse(heuristicsStr);
        Object.entries(parsed).forEach(([k, v]) => {
            heuristics[String(k).trim()] = parseFloat(v) || 0.0;
        });
        return heuristics;
    } catch (_) {
        // Parse line-by-line format: "A: 10" or "A 10"
        heuristicsStr.split('\n').forEach(line => {
            const match = line.match(/^([^:\s]+)[:\s]+([\d.-]+)/);
            if (match) {
                heuristics[match[1].trim()] = parseFloat(match[2]) || 0.0;
            }
        });
    }

    // Default missing nodes to 0.0
    nodes.forEach(n => {
        if (heuristics[n] === undefined) heuristics[n] = 0.0;
    });

    return heuristics;
}

function updateNodeDropdowns(prefix) {
    const nodesInput = document.getElementById(`${prefix}-nodes`);
    const startSelect = document.getElementById(`${prefix}-start`);
    const goalSelect = document.getElementById(`${prefix}-goal`);

    if (!nodesInput || !startSelect) return;

    const nodes = parseNodes(nodesInput.value);
    const prevStart = startSelect.value;
    const prevGoal = goalSelect ? goalSelect.value : null;

    startSelect.innerHTML = '';
    if (goalSelect) goalSelect.innerHTML = '';

    nodes.forEach(n => {
        const opt1 = document.createElement('option');
        opt1.value = n;
        opt1.textContent = n;
        startSelect.appendChild(opt1);

        if (goalSelect) {
            const opt2 = document.createElement('option');
            opt2.value = n;
            opt2.textContent = n;
            goalSelect.appendChild(opt2);
        }
    });

    if (nodes.includes(prevStart)) startSelect.value = prevStart;
    else if (nodes.length > 0) startSelect.value = nodes[0];

    if (goalSelect) {
        if (nodes.includes(prevGoal)) goalSelect.value = prevGoal;
        else if (nodes.length > 1) goalSelect.value = nodes[nodes.length - 1];
    }

    // Refresh visualizer initial graph state
    refreshVisualizerGraph(prefix);
}

function refreshVisualizerGraph(prefix) {
    const viz = graphVisualizers[prefix];
    if (!viz) return;

    const nodesInput = document.getElementById(`${prefix}-nodes`);
    const edgesInput = document.getElementById(`${prefix}-edges`);
    if (!nodesInput || !edgesInput) return;

    const nodes = parseNodes(nodesInput.value);
    const weighted = prefix === 'astar';
    const edges = parseEdges(edgesInput.value, weighted);

    let heuristics = {};
    if (prefix === 'astar') {
        const hInput = document.getElementById('astar-heuristics');
        if (hInput) heuristics = parseHeuristics(hInput.value, nodes);
    }

    viz.setGraph(nodes, edges, weighted, heuristics);
}

// ============================================================================
// ALGORITHM RUNNERS DISPATCHER
// ============================================================================
async function runSearchAlgo(algo) {
    switch (algo) {
        case 'bfs': return await runBFS();
        case 'dfs': return await runDFS();
        case 'iddfs': return await runIDDFS();
        case 'astar': return await runAstar();
        case 'dstar': return await runDstar();
        case 'hillclimb': return await runHillClimbing();
        case 'simulated':
        case 'sa': return await runSimulatedAnnealing();
        default:
            console.error(`Unknown algorithm: ${algo}`);
    }
}

function resetSearchAlgo(algo) {
    const prefixMap = {
        'bfs': 'bfs',
        'dfs': 'dfs',
        'iddfs': 'iddfs',
        'astar': 'astar',
        'dstar': 'dstar',
        'hillclimb': 'hc',
        'simulated': 'sa',
        'sa': 'sa'
    };
    const prefix = prefixMap[algo] || algo;

    const resultsPanel = document.getElementById(`${prefix}-results`) || document.getElementById(`${algo}-results`);
    if (resultsPanel) resultsPanel.style.display = 'none';

    if (graphVisualizers[prefix]) {
        graphVisualizers[prefix].reset();
    } else if (prefix === 'dstar' && dstarVisualizer) {
        dstarVisualizer.setGrid(10, [0, 0], [9, 9], [], []);
    }

    showToast(`Reset ${algo.toUpperCase()}`, 'info', 1500);
}

// ============================================================================
// 1. BREADTH-FIRST SEARCH (BFS)
// ============================================================================
async function runBFS() {
    const nodes = parseNodes(document.getElementById('bfs-nodes')?.value);
    const edges = parseEdges(document.getElementById('bfs-edges')?.value, false);
    const start = document.getElementById('bfs-start')?.value;
    const goal = document.getElementById('bfs-goal')?.value;

    if (!nodes.length || !start) {
        showToast('Please provide valid nodes and start node', 'warning');
        return;
    }

    const resultsPanel = document.getElementById('bfs-results');
    const traversalEl = document.getElementById('bfs-traversal');
    const pathEl = document.getElementById('bfs-path');
    const stepsBody = document.getElementById('bfs-steps-body');

    try {
        showToast('Running BFS...', 'info', 1500);
        const res = await apiCall('/algorithms/bfs', 'POST', {
            nodes,
            edges,
            start,
            goal: goal || null,
            weighted: false
        });

        if (resultsPanel) resultsPanel.style.display = 'block';

        if (traversalEl) traversalEl.textContent = (res.traversal_order || []).join(' → ');
        if (pathEl) pathEl.textContent = (res.path && res.path.length > 0) ? res.path.join(' → ') : 'No path found';

        // Populate steps table
        if (stepsBody && res.steps) {
            stepsBody.innerHTML = res.steps.map((st, i) => `
                <tr>
                    <td>${st.step !== undefined ? st.step : i + 1}</td>
                    <td><strong>${escapeHtml(st.current || st.node || '-')}</strong></td>
                    <td><code>${escapeHtml(Array.isArray(st.queue) ? st.queue.join(', ') : (st.queue || '-'))}</code></td>
                    <td>${escapeHtml(Array.isArray(st.visited) ? st.visited.join(', ') : (st.visited || '-'))}</td>
                </tr>
            `).join('');
        }

        // Animate canvas
        if (graphVisualizers['bfs']) {
            graphVisualizers['bfs'].setGraph(nodes, edges, false);
            graphVisualizers['bfs'].animateTraversal(res.traversal_order || [], res.path || []);
        }

        logActivity('search', `BFS: ${start} → ${goal}`, `Path: ${res.path?.join('→')} (Cost: ${res.cost})`, '🔍');
        showToast(`BFS complete: ${res.message || 'Path found!'}`, 'success');

    } catch (e) {
        showToast(`BFS Error: ${e.message}`, 'error');
    }
}

// ============================================================================
// 2. DEPTH-FIRST SEARCH (DFS)
// ============================================================================
async function runDFS() {
    const nodes = parseNodes(document.getElementById('dfs-nodes')?.value);
    const edges = parseEdges(document.getElementById('dfs-edges')?.value, false);
    const start = document.getElementById('dfs-start')?.value;
    const goal = document.getElementById('dfs-goal')?.value;

    if (!nodes.length || !start) {
        showToast('Please provide valid nodes and start node', 'warning');
        return;
    }

    const resultsPanel = document.getElementById('dfs-results');
    const traversalEl = document.getElementById('dfs-traversal');
    const pathEl = document.getElementById('dfs-path');
    const stepsBody = document.getElementById('dfs-steps-body');

    try {
        showToast('Running DFS...', 'info', 1500);
        const res = await apiCall('/algorithms/dfs', 'POST', {
            nodes,
            edges,
            start,
            goal: goal || null,
            weighted: false
        });

        if (resultsPanel) resultsPanel.style.display = 'block';

        if (traversalEl) traversalEl.textContent = (res.traversal_order || []).join(' → ');
        if (pathEl) pathEl.textContent = (res.path && res.path.length > 0) ? res.path.join(' → ') : 'No path found';

        // Populate steps table
        if (stepsBody && res.steps) {
            stepsBody.innerHTML = res.steps.map((st, i) => `
                <tr>
                    <td>${st.step !== undefined ? st.step : i + 1}</td>
                    <td><strong>${escapeHtml(st.current || st.node || '-')}</strong></td>
                    <td><code>${escapeHtml(Array.isArray(st.stack) ? st.stack.join(', ') : (st.stack || '-'))}</code></td>
                    <td>${escapeHtml(Array.isArray(st.visited) ? st.visited.join(', ') : (st.visited || '-'))}</td>
                </tr>
            `).join('');
        }

        // Animate canvas
        if (graphVisualizers['dfs']) {
            graphVisualizers['dfs'].setGraph(nodes, edges, false);
            graphVisualizers['dfs'].animateTraversal(res.traversal_order || [], res.path || []);
        }

        logActivity('search', `DFS: ${start} → ${goal}`, `Path: ${res.path?.join('→')} (Cost: ${res.cost})`, '🔍');
        showToast(`DFS complete: ${res.message || 'Path found!'}`, 'success');

    } catch (e) {
        showToast(`DFS Error: ${e.message}`, 'error');
    }
}

// ============================================================================
// 3. ITERATIVE DEEPENING DEPTH-FIRST SEARCH (IDDFS)
// ============================================================================
async function runIDDFS() {
    const nodes = parseNodes(document.getElementById('iddfs-nodes')?.value);
    const edges = parseEdges(document.getElementById('iddfs-edges')?.value, false);
    const start = document.getElementById('iddfs-start')?.value;
    const goal = document.getElementById('iddfs-goal')?.value;
    const maxDepth = parseInt(document.getElementById('iddfs-maxdepth')?.value, 10) || 10;

    if (!nodes.length || !start || !goal) {
        showToast('Please provide nodes, start node, and goal node', 'warning');
        return;
    }

    const resultsPanel = document.getElementById('iddfs-results');
    const pathEl = document.getElementById('iddfs-path');
    const depthEl = document.getElementById('iddfs-depth');
    const stepsBody = document.getElementById('iddfs-steps-body');

    try {
        showToast('Running IDDFS...', 'info', 1500);
        const res = await apiCall('/algorithms/iddfs', 'POST', {
            nodes,
            edges,
            start,
            goal,
            max_depth: maxDepth
        });

        if (resultsPanel) resultsPanel.style.display = 'block';

        if (pathEl) pathEl.textContent = (res.path && res.path.length > 0) ? res.path.join(' → ') : 'Goal not found';
        if (depthEl) depthEl.textContent = res.depth_found !== -1 ? res.depth_found : 'Exceeded max depth';

        // Populate steps table (iterations of deepening)
        if (stepsBody && res.iterations) {
            stepsBody.innerHTML = res.iterations.map(iter => `
                <tr>
                    <td><strong>Depth ${iter.depth}</strong></td>
                    <td>${escapeHtml((iter.visited || iter.traversal_order || []).join(' → '))}</td>
                    <td>${iter.found ? '<span style="color:#10b981;font-weight:600;">Goal Found</span>' : '<span style="color:#94a3b8;">Searching...</span>'}</td>
                </tr>
            `).join('');
        }

        // Animate canvas
        if (graphVisualizers['iddfs']) {
            graphVisualizers['iddfs'].setGraph(nodes, edges, false);
            // Collect all visited nodes from last iteration
            const lastIter = res.iterations ? res.iterations[res.iterations.length - 1] : null;
            const visited = lastIter ? (lastIter.visited || lastIter.traversal_order || []) : [];
            graphVisualizers['iddfs'].animateTraversal(visited, res.path || []);
        }

        logActivity('search', `IDDFS: ${start} → ${goal}`, `Depth: ${res.depth_found}, Explored: ${res.nodes_explored}`, '🔍');
        showToast(`IDDFS complete: ${res.message || (res.found ? 'Goal reached!' : 'Not found')}`, res.found ? 'success' : 'info');

    } catch (e) {
        showToast(`IDDFS Error: ${e.message}`, 'error');
    }
}

// ============================================================================
// 4. A* SEARCH
// ============================================================================
async function runAstar() {
    const nodes = parseNodes(document.getElementById('astar-nodes')?.value);
    const edges = parseEdges(document.getElementById('astar-edges')?.value, true);
    const heuristics = parseHeuristics(document.getElementById('astar-heuristics')?.value, nodes);
    const start = document.getElementById('astar-start')?.value;
    const goal = document.getElementById('astar-goal')?.value;

    if (!nodes.length || !start || !goal) {
        showToast('Please provide nodes, start node, and goal node', 'warning');
        return;
    }

    const resultsPanel = document.getElementById('astar-results');
    const pathEl = document.getElementById('astar-path');
    const costEl = document.getElementById('astar-cost');
    const stepsBody = document.getElementById('astar-steps-body');

    try {
        showToast('Running A* Search...', 'info', 1500);
        const res = await apiCall('/algorithms/astar', 'POST', {
            nodes,
            edges,
            start,
            goal,
            heuristics
        });

        if (resultsPanel) resultsPanel.style.display = 'block';

        if (pathEl) pathEl.textContent = (res.path && res.path.length > 0) ? res.path.join(' → ') : 'No path found';
        if (costEl) costEl.textContent = res.cost !== undefined ? res.cost : '0';

        // Populate steps table
        if (stepsBody && res.steps) {
            stepsBody.innerHTML = res.steps.map((st, i) => `
                <tr>
                    <td>${st.step !== undefined ? st.step : i + 1}</td>
                    <td><strong>${escapeHtml(st.current || st.node || '-')}</strong></td>
                    <td>g=${st.g !== undefined ? st.g : '-'}, h=${st.h !== undefined ? st.h : '-'}</td>
                    <td><strong style="color:var(--accent-cyan);">${st.f !== undefined ? st.f : '-'}</strong></td>
                    <td>${escapeHtml((st.open_set || []).map(o => typeof o === 'object' ? `${o.node}(f=${o.f})` : o).join(', '))}</td>
                </tr>
            `).join('');
        }

        // Animate canvas
        if (graphVisualizers['astar']) {
            graphVisualizers['astar'].setGraph(nodes, edges, true, heuristics);
            graphVisualizers['astar'].animateTraversal(res.traversal_order || res.visited_nodes || [], res.path || []);
        }

        logActivity('search', `A*: ${start} → ${goal}`, `Path: ${res.path?.join('→')} (Cost: ${res.cost})`, '🔍');
        showToast(`A* complete: ${res.message || 'Optimal path found!'}`, 'success');

    } catch (e) {
        showToast(`A* Error: ${e.message}`, 'error');
    }
}

// ============================================================================
// 5. D* LITE
// ============================================================================
async function runDstar() {
    const gridSize = parseInt(document.getElementById('dstar-gridsize')?.value, 10) || 10;
    const startStr = document.getElementById('dstar-start')?.value || '0,0';
    const goalStr = document.getElementById('dstar-goal')?.value || `${gridSize - 1},${gridSize - 1}`;

    const start = startStr.split(',').map(Number);
    const goal = goalStr.split(',').map(Number);

    const obstacles = dstarVisualizer ? dstarVisualizer.getObstaclesList() : [];

    const resultsPanel = document.getElementById('dstar-results');
    const pathLenEl = document.getElementById('dstar-pathlen');
    const replanEl = document.getElementById('dstar-replan');

    try {
        showToast('Running D* Lite path planning...', 'info', 1500);
        const res = await apiCall('/algorithms/dstar', 'POST', {
            grid_size: gridSize,
            start,
            goal,
            obstacles
        });

        if (resultsPanel) resultsPanel.style.display = 'block';

        if (pathLenEl) pathLenEl.textContent = res.path ? res.path.length : 0;
        if (replanEl) replanEl.textContent = (res.replanning_steps || []).length;

        // Render planned path on grid
        if (dstarVisualizer) {
            dstarVisualizer.setGrid(gridSize, start, goal, obstacles, res.path);
        }

        logActivity('search', `D* Lite (${gridSize}x${gridSize})`, `Path Length: ${res.path?.length}, Obstacles: ${obstacles.length}`, '🔍');
        showToast(`D* Lite: ${res.message || 'Path successfully calculated!'}`, 'success');

    } catch (e) {
        showToast(`D* Lite Error: ${e.message}`, 'error');
    }
}

// ============================================================================
// 6. HILL CLIMBING
// ============================================================================
async function runHillClimbing() {
    const initialX = parseFloat(document.getElementById('hc-initial-x')?.value) || 0.0;
    const funcType = document.getElementById('hc-func')?.value || 'multimodal';
    const stepSize = parseFloat(document.getElementById('hc-step')?.value) || 0.1;
    const maxIters = parseInt(document.getElementById('hc-maxiter')?.value, 10) || 1000;

    const resultsPanel = document.getElementById('hillclimb-results');
    const bestXEl = document.getElementById('hc-best-x');
    const bestValEl = document.getElementById('hc-best-val');
    const itersEl = document.getElementById('hc-iters');

    try {
        showToast('Running Hill Climbing...', 'info', 1500);
        const res = await apiCall('/algorithms/hill-climbing', 'POST', {
            initial_x: initialX,
            func_type: funcType,
            step_size: stepSize,
            max_iterations: maxIters
        });

        if (resultsPanel) resultsPanel.style.display = 'block';

        if (bestXEl) bestXEl.textContent = Number(res.best_x).toFixed(4);
        if (bestValEl) bestValEl.textContent = Number(res.best_value).toFixed(4);
        if (itersEl) itersEl.textContent = res.iterations || (res.history ? res.history.length : 0);

        // Draw optimization chart
        drawOptimizationChart('hillclimb-canvas', res.history || [], `Hill Climbing (${funcType})`);

        logActivity('search', `Hill Climbing (${funcType})`, `Best x: ${Number(res.best_x).toFixed(2)}, Value: ${Number(res.best_value).toFixed(2)}`, '📈');
        showToast(`Hill Climbing finished in ${res.iterations} steps`, 'success');

    } catch (e) {
        showToast(`Hill Climbing Error: ${e.message}`, 'error');
    }
}

// ============================================================================
// 7. SIMULATED ANNEALING
// ============================================================================
async function runSimulatedAnnealing() {
    const initialX = parseFloat(document.getElementById('sa-initial-x')?.value) || 0.0;
    const initialTemp = parseFloat(document.getElementById('sa-initial-temp')?.value) || 1000.0;
    const coolingRate = parseFloat(document.getElementById('sa-cooling')?.value) || 0.995;
    const maxIters = parseInt(document.getElementById('sa-maxiter')?.value, 10) || 1000;
    const funcType = document.getElementById('sa-func')?.value || 'multimodal';

    const resultsPanel = document.getElementById('sa-results');
    const bestXEl = document.getElementById('sa-best-x');
    const bestValEl = document.getElementById('sa-best-val');
    const itersEl = document.getElementById('sa-iters');

    try {
        showToast('Running Simulated Annealing...', 'info', 1500);
        const res = await apiCall('/algorithms/simulated-annealing', 'POST', {
            initial_x: initialX,
            initial_temp: initialTemp,
            cooling_rate: coolingRate,
            max_iterations: maxIters,
            func_type: funcType
        });

        if (resultsPanel) resultsPanel.style.display = 'block';

        if (bestXEl) bestXEl.textContent = Number(res.best_x).toFixed(4);
        if (bestValEl) bestValEl.textContent = Number(res.best_value).toFixed(4);
        if (itersEl) itersEl.textContent = res.iterations || (res.history ? res.history.length : 0);

        // Draw optimization chart
        drawOptimizationChart('sa-canvas', res.history || [], `Simulated Annealing (${funcType})`);

        logActivity('search', `Simulated Annealing (${funcType})`, `Best x: ${Number(res.best_x).toFixed(2)}, Value: ${Number(res.best_value).toFixed(2)}`, '🔥');
        showToast(`Simulated Annealing finished in ${res.iterations} steps`, 'success');

    } catch (e) {
        showToast(`Simulated Annealing Error: ${e.message}`, 'error');
    }
}

// ============================================================================
// INITIALIZATION & EVENT BINDINGS
// ============================================================================
window.addEventListener('DOMContentLoaded', () => {
    // Instantiate visualizers
    ['bfs', 'dfs', 'iddfs', 'astar'].forEach(algo => {
        const canvasId = `${algo}-canvas`;
        if (document.getElementById(canvasId)) {
            graphVisualizers[algo] = new GraphVisualizer(canvasId);
            updateNodeDropdowns(algo);
        }
    });

    if (document.getElementById('dstar-canvas')) {
        dstarVisualizer = new GridVisualizer('dstar-canvas');
        dstarVisualizer.setGrid(10, [0, 0], [9, 9], [[2, 2], [2, 3], [2, 4], [3, 4], [4, 4], [5, 4]]);
    }

    // Bind change listeners to node/edge inputs to auto-refresh dropdowns & canvas
    ['bfs', 'dfs', 'iddfs', 'astar'].forEach(algo => {
        const nodesInput = document.getElementById(`${algo}-nodes`);
        if (nodesInput) {
            nodesInput.addEventListener('input', () => updateNodeDropdowns(algo));
        }
        const edgesInput = document.getElementById(`${algo}-edges`);
        if (edgesInput) {
            edgesInput.addEventListener('input', () => refreshVisualizerGraph(algo));
        }
    });

    const astarHInput = document.getElementById('astar-heuristics');
    if (astarHInput) {
        astarHInput.addEventListener('input', () => refreshVisualizerGraph('astar'));
    }

    // Grid size listener for D*
    const dstarGridSize = document.getElementById('dstar-gridsize');
    if (dstarGridSize) {
        dstarGridSize.addEventListener('change', () => {
            const size = parseInt(dstarGridSize.value, 10) || 10;
            const goalEl = document.getElementById('dstar-goal');
            if (goalEl) goalEl.value = `${size - 1},${size - 1}`;
            if (dstarVisualizer) {
                dstarVisualizer.setGrid(size, [0, 0], [size - 1, size - 1]);
            }
        });
    }
});

// Global exports
window.runSearchAlgo = runSearchAlgo;
window.resetSearchAlgo = resetSearchAlgo;
window.runBFS = runBFS;
window.runDFS = runDFS;
window.runIDDFS = runIDDFS;
window.runAstar = runAstar;
window.runDstar = runDstar;
window.runHillClimbing = runHillClimbing;
window.runSimulatedAnnealing = runSimulatedAnnealing;
window.graphVisualizers = graphVisualizers;
