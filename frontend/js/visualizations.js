// JARVIS AI - Visualizations Engine
// High-performance Canvas visualizers for Graphs, Grids, Optimization, and Probabilistic Clustering

// Cache for Chart.js instances to avoid canvas reuse errors
const activeCharts = {};

// ============================================================================
// GRAPH VISUALIZER (Canvas 2D)
// ============================================================================
class GraphVisualizer {
    constructor(canvasId) {
        this.canvasId = canvasId;
        this.canvas = document.getElementById(canvasId);
        this.ctx = this.canvas ? this.canvas.getContext('2d') : null;
        this.nodes = {};      // { name: { x, y, state, h } }
        this.edges = [];      // [ { u, v, weight, inPath } ]
        this.animationTimer = null;
        this.weighted = false;
        this.hasHeuristics = false;

        // Auto-scale canvas for Retina/HiDPI
        this.setupHiDPI();
    }

    setupHiDPI() {
        if (!this.canvas || !this.ctx) return;
        const dpr = window.devicePixelRatio || 1;
        const rect = this.canvas.getBoundingClientRect();
        const displayWidth = rect.width || this.canvas.width || 400;
        const displayHeight = rect.height || this.canvas.height || 300;

        if (this.canvas.width !== displayWidth * dpr || this.canvas.height !== displayHeight * dpr) {
            this.canvas.width = displayWidth * dpr;
            this.canvas.height = displayHeight * dpr;
            this.ctx.scale(dpr, dpr);
        }
        this.displayWidth = displayWidth;
        this.displayHeight = displayHeight;
    }

    setGraph(nodes, edges, weighted = false, heuristics = {}) {
        this.setupHiDPI();
        this.weighted = weighted;
        this.heuristics = heuristics || {};
        this.hasHeuristics = Object.keys(this.heuristics).length > 0;
        this.nodes = {};
        this.edges = [];

        if (!this.canvas || !this.ctx) return;

        const width = this.displayWidth || 400;
        const height = this.displayHeight || 300;
        const centerX = width / 2;
        const centerY = height / 2;
        const radius = Math.min(width, height) * 0.38;

        const totalNodes = nodes.length;
        nodes.forEach((name, i) => {
            const angle = (2 * Math.PI * i) / totalNodes - Math.PI / 2;
            const x = centerX + radius * Math.cos(angle);
            const y = centerY + radius * Math.sin(angle);
            this.nodes[String(name)] = {
                x,
                y,
                state: 'default', // 'default', 'visiting', 'visited', 'path'
                h: this.heuristics[name] !== undefined ? this.heuristics[name] : null
            };
        });

        // Store edges
        edges.forEach(e => {
            let u, v, weight = 1.0;
            if (Array.isArray(e)) {
                u = String(e[0]);
                v = String(e[1]);
                if (e.length > 2) weight = parseFloat(e[2]) || 1.0;
            } else if (typeof e === 'object') {
                u = String(e.from || e.src || e.from_node || e.u);
                v = String(e.to || e.dst || e.to_node || e.v);
                weight = parseFloat(e.weight || e.cost) || 1.0;
            }
            if (this.nodes[u] && this.nodes[v]) {
                this.edges.push({ u, v, weight, inPath: false });
            }
        });

        this.draw();
    }

    draw() {
        if (!this.ctx) return;
        const ctx = this.ctx;
        const w = this.displayWidth || 400;
        const h = this.displayHeight || 300;

        ctx.clearRect(0, 0, w, h);

        // 1. Draw Edges
        this.edges.forEach(edge => {
            const n1 = this.nodes[edge.u];
            const n2 = this.nodes[edge.v];
            if (!n1 || !n2) return;

            ctx.beginPath();
            ctx.moveTo(n1.x, n1.y);
            ctx.lineTo(n2.x, n2.y);

            if (edge.inPath) {
                ctx.strokeStyle = '#f59e0b'; // Gold for path
                ctx.lineWidth = 4;
                ctx.shadowColor = 'rgba(245, 158, 11, 0.7)';
                ctx.shadowBlur = 10;
            } else {
                ctx.strokeStyle = 'rgba(148, 163, 184, 0.25)';
                ctx.lineWidth = 2;
                ctx.shadowBlur = 0;
            }
            ctx.stroke();
            ctx.shadowBlur = 0;

            // Draw edge weight if weighted
            if (this.weighted) {
                const midX = (n1.x + n2.x) / 2;
                const midY = (n1.y + n2.y) / 2;
                ctx.fillStyle = '#00d4ff';
                ctx.font = '11px Inter, sans-serif';
                ctx.textAlign = 'center';
                ctx.textBaseline = 'middle';

                // Pill background for weight
                ctx.fillStyle = 'rgba(10, 14, 26, 0.85)';
                ctx.fillRect(midX - 10, midY - 8, 20, 16);
                ctx.fillStyle = '#94a3b8';
                ctx.fillText(edge.weight, midX, midY);
            }
        });

        // 2. Draw Nodes
        const nodeRadius = 18;
        Object.entries(this.nodes).forEach(([name, node]) => {
            ctx.beginPath();
            ctx.arc(node.x, node.y, nodeRadius, 0, 2 * Math.PI);

            // Styling based on state
            if (node.state === 'path') {
                ctx.fillStyle = '#f59e0b'; // Gold
                ctx.strokeStyle = '#fbbf24';
                ctx.shadowColor = 'rgba(245, 158, 11, 0.9)';
                ctx.shadowBlur = 15;
            } else if (node.state === 'visiting') {
                ctx.fillStyle = '#00d4ff'; // Cyan
                ctx.strokeStyle = '#ffffff';
                ctx.shadowColor = 'rgba(0, 212, 255, 0.9)';
                ctx.shadowBlur = 16;
            } else if (node.state === 'visited') {
                ctx.fillStyle = '#0066ff'; // Blue
                ctx.strokeStyle = '#38bdf8';
                ctx.shadowColor = 'rgba(0, 102, 255, 0.6)';
                ctx.shadowBlur = 8;
            } else {
                ctx.fillStyle = '#1e293b'; // Slate dark
                ctx.strokeStyle = '#475569';
                ctx.shadowBlur = 0;
            }

            ctx.lineWidth = 2.5;
            ctx.fill();
            ctx.stroke();
            ctx.shadowBlur = 0;

            // Label
            ctx.fillStyle = node.state === 'default' ? '#e2e8f0' : '#ffffff';
            ctx.font = 'bold 12px Inter, sans-serif';
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            ctx.fillText(name, node.x, node.y);

            // Draw heuristic value below node if present
            if (this.hasHeuristics && node.h !== null) {
                ctx.fillStyle = '#94a3b8';
                ctx.font = '10px Inter, sans-serif';
                ctx.fillText(`h=${node.h}`, node.x, node.y + nodeRadius + 12);
            }
        });
    }

    animateTraversal(traversalOrder, path = [], onComplete = null) {
        this.reset();
        if (!traversalOrder || traversalOrder.length === 0) {
            if (path && path.length > 0) this.highlightPath(path);
            if (onComplete) onComplete();
            return;
        }

        const speed = window.getAnimDuration ? window.getAnimDuration() : 400;
        let index = 0;

        const step = () => {
            if (index > 0) {
                const prev = traversalOrder[index - 1];
                if (this.nodes[prev]) this.nodes[prev].state = 'visited';
            }

            if (index < traversalOrder.length) {
                const current = traversalOrder[index];
                if (this.nodes[current]) this.nodes[current].state = 'visiting';
                this.draw();
                index++;
                this.animationTimer = setTimeout(step, speed);
            } else {
                // Done traversal, highlight path
                if (path && path.length > 0) {
                    setTimeout(() => {
                        this.highlightPath(path);
                        if (onComplete) onComplete();
                    }, speed);
                } else {
                    if (onComplete) onComplete();
                }
            }
        };

        step();
    }

    highlightPath(path) {
        if (!path || path.length === 0) return;

        // Mark path nodes
        path.forEach(name => {
            if (this.nodes[name]) this.nodes[name].state = 'path';
        });

        // Mark path edges
        for (let i = 0; i < path.length - 1; i++) {
            const u = path[i];
            const v = path[i + 1];
            this.edges.forEach(e => {
                if ((e.u === u && e.v === v) || (e.u === v && e.v === u)) {
                    e.inPath = true;
                }
            });
        }

        this.draw();
    }

    reset() {
        if (this.animationTimer) {
            clearTimeout(this.animationTimer);
            this.animationTimer = null;
        }
        Object.values(this.nodes).forEach(n => { n.state = 'default'; });
        this.edges.forEach(e => { e.inPath = false; });
        this.draw();
    }
}

// ============================================================================
// GRID VISUALIZER (D* Lite Canvas 2D)
// ============================================================================
class GridVisualizer {
    constructor(canvasId) {
        this.canvasId = canvasId;
        this.canvas = document.getElementById(canvasId);
        this.ctx = this.canvas ? this.canvas.getContext('2d') : null;
        this.gridSize = 10;
        this.start = [0, 0];
        this.goal = [9, 9];
        this.obstacles = new Set();
        this.path = [];

        this.setupHiDPI();
        this.setupInteraction();
    }

    setupHiDPI() {
        if (!this.canvas || !this.ctx) return;
        const dpr = window.devicePixelRatio || 1;
        const rect = this.canvas.getBoundingClientRect();
        const displayWidth = rect.width || this.canvas.width || 400;
        const displayHeight = rect.height || this.canvas.height || 300;

        if (this.canvas.width !== displayWidth * dpr || this.canvas.height !== displayHeight * dpr) {
            this.canvas.width = displayWidth * dpr;
            this.canvas.height = displayHeight * dpr;
            this.ctx.scale(dpr, dpr);
        }
        this.displayWidth = displayWidth;
        this.displayHeight = displayHeight;
    }

    setupInteraction() {
        if (!this.canvas) return;
        this.canvas.addEventListener('click', (e) => {
            const rect = this.canvas.getBoundingClientRect();
            const clickX = e.clientX - rect.left;
            const clickY = e.clientY - rect.top;

            const cellSize = Math.min(this.displayWidth, this.displayHeight) / this.gridSize;
            const offsetX = (this.displayWidth - cellSize * this.gridSize) / 2;
            const offsetY = (this.displayHeight - cellSize * this.gridSize) / 2;

            const c = Math.floor((clickX - offsetX) / cellSize);
            const r = Math.floor((clickY - offsetY) / cellSize);

            if (r >= 0 && r < this.gridSize && c >= 0 && c < this.gridSize) {
                // Don't toggle start or goal
                if ((r === this.start[0] && c === this.start[1]) || (r === this.goal[0] && c === this.goal[1])) {
                    return;
                }
                const key = `${r},${c}`;
                if (this.obstacles.has(key)) {
                    this.obstacles.delete(key);
                } else {
                    this.obstacles.add(key);
                }
                this.draw();
            }
        });
    }

    setGrid(gridSize, start, goal, obstacles = [], path = []) {
        this.setupHiDPI();
        this.gridSize = gridSize || 10;
        this.start = start || [0, 0];
        this.goal = goal || [gridSize - 1, gridSize - 1];
        this.obstacles = new Set();
        if (obstacles) {
            obstacles.forEach(obs => {
                if (Array.isArray(obs) && obs.length >= 2) {
                    this.obstacles.add(`${obs[0]},${obs[1]}`);
                }
            });
        }
        this.path = path || [];
        this.draw();
    }

    draw() {
        if (!this.ctx) return;
        const ctx = this.ctx;
        const w = this.displayWidth || 400;
        const h = this.displayHeight || 300;

        ctx.clearRect(0, 0, w, h);

        const cellSize = Math.min(w, h) / this.gridSize;
        const offsetX = (w - cellSize * this.gridSize) / 2;
        const offsetY = (h - cellSize * this.gridSize) / 2;

        const pathSet = new Set();
        this.path.forEach(p => {
            if (Array.isArray(p)) pathSet.add(`${p[0]},${p[1]}`);
        });

        // 1. Draw Grid Cells
        for (let r = 0; r < this.gridSize; r++) {
            for (let c = 0; c < this.gridSize; c++) {
                const x = offsetX + c * cellSize;
                const y = offsetY + r * cellSize;
                const key = `${r},${c}`;

                ctx.beginPath();
                ctx.rect(x + 1, y + 1, cellSize - 2, cellSize - 2);

                if (r === this.start[0] && c === this.start[1]) {
                    ctx.fillStyle = '#10b981'; // Green Start
                    ctx.fill();
                    ctx.fillStyle = '#ffffff';
                    ctx.font = `bold ${Math.max(10, cellSize * 0.4)}px sans-serif`;
                    ctx.textAlign = 'center';
                    ctx.textBaseline = 'middle';
                    ctx.fillText('S', x + cellSize / 2, y + cellSize / 2);
                } else if (r === this.goal[0] && c === this.goal[1]) {
                    ctx.fillStyle = '#ef4444'; // Red Goal
                    ctx.fill();
                    ctx.fillStyle = '#ffffff';
                    ctx.font = `bold ${Math.max(10, cellSize * 0.4)}px sans-serif`;
                    ctx.textAlign = 'center';
                    ctx.textBaseline = 'middle';
                    ctx.fillText('G', x + cellSize / 2, y + cellSize / 2);
                } else if (this.obstacles.has(key)) {
                    ctx.fillStyle = '#334155'; // Dark slate obstacle
                    ctx.fill();
                } else if (pathSet.has(key)) {
                    ctx.fillStyle = 'rgba(0, 212, 255, 0.45)'; // Path cell
                    ctx.fill();
                } else {
                    ctx.fillStyle = 'rgba(255, 255, 255, 0.03)';
                    ctx.fill();
                }

                ctx.strokeStyle = 'rgba(255, 255, 255, 0.08)';
                ctx.lineWidth = 1;
                ctx.stroke();
            }
        }

        // 2. Draw Connected Path Line
        if (this.path && this.path.length > 1) {
            ctx.beginPath();
            ctx.strokeStyle = '#00d4ff';
            ctx.lineWidth = Math.max(2, cellSize * 0.2);
            ctx.lineCap = 'round';
            ctx.lineJoin = 'round';

            this.path.forEach((p, idx) => {
                const px = offsetX + p[1] * cellSize + cellSize / 2;
                const py = offsetY + p[0] * cellSize + cellSize / 2;
                if (idx === 0) ctx.moveTo(px, py);
                else ctx.lineTo(px, py);
            });
            ctx.shadowColor = 'rgba(0, 212, 255, 0.8)';
            ctx.shadowBlur = 8;
            ctx.stroke();
            ctx.shadowBlur = 0;
        }
    }

    getObstaclesList() {
        return Array.from(this.obstacles).map(s => s.split(',').map(Number));
    }
}

// ============================================================================
// OPTIMIZATION LINE CHART (Chart.js or Canvas Fallback)
// ============================================================================
function drawOptimizationChart(canvasId, history, title = 'Optimization Progress') {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;

    if (!history || history.length === 0) {
        renderCanvasEmptyState(canvas, 'No optimization history available');
        return;
    }

    const labels = history.map((item, idx) => item.iteration !== undefined ? item.iteration : idx);
    const dataValues = history.map(item => item.value !== undefined ? item.value : (item.current_value || 0));

    // If Chart.js is loaded
    if (window.Chart) {
        if (activeCharts[canvasId]) {
            activeCharts[canvasId].destroy();
        }

        const ctx = canvas.getContext('2d');
        activeCharts[canvasId] = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: title,
                    data: dataValues,
                    borderColor: '#00d4ff',
                    backgroundColor: 'rgba(0, 212, 255, 0.1)',
                    borderWidth: 2,
                    tension: 0.2,
                    pointRadius: history.length > 100 ? 0 : 2,
                    pointHoverRadius: 4,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: true, labels: { color: '#94a3b8' } },
                    tooltip: {
                        mode: 'index',
                        intersect: false,
                        backgroundColor: 'rgba(10, 14, 26, 0.9)',
                        titleColor: '#00d4ff',
                        borderColor: 'rgba(0, 212, 255, 0.3)',
                        borderWidth: 1
                    }
                },
                scales: {
                    x: {
                        grid: { color: 'rgba(255, 255, 255, 0.05)' },
                        ticks: { color: '#64748b', maxTicksLimit: 10 }
                    },
                    y: {
                        grid: { color: 'rgba(255, 255, 255, 0.05)' },
                        ticks: { color: '#64748b' }
                    }
                }
            }
        });
        return;
    }

    // Fallback: Custom Canvas 2D Line Chart
    drawCustomLineChart(canvas, labels, dataValues, title);
}

// ============================================================================
// EM CLUSTERS VISUALIZER (Scatter Plot & Gaussian Ellipses)
// ============================================================================
function drawEMClusters(canvasId, dataPoints, clusters) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // HiDPI setup
    const dpr = window.devicePixelRatio || 1;
    const rect = canvas.getBoundingClientRect();
    const w = rect.width || canvas.width || 400;
    const h = rect.height || canvas.height || 300;

    if (canvas.width !== w * dpr || canvas.height !== h * dpr) {
        canvas.width = w * dpr;
        canvas.height = h * dpr;
        ctx.scale(dpr, dpr);
    }

    ctx.clearRect(0, 0, w, h);

    if (!dataPoints || dataPoints.length === 0) {
        renderCanvasEmptyState(canvas, 'No cluster data available');
        return;
    }

    // Calculate bounds
    let minX = Infinity, maxX = -Infinity, minY = Infinity, maxY = -Infinity;
    dataPoints.forEach(p => {
        const x = Array.isArray(p) ? p[0] : p.x;
        const y = Array.isArray(p) ? p[1] : p.y;
        if (x < minX) minX = x;
        if (x > maxX) maxX = x;
        if (y < minY) minY = y;
        if (y > maxY) maxY = y;
    });

    const padX = (maxX - minX) * 0.15 || 1;
    const padY = (maxY - minY) * 0.15 || 1;
    minX -= padX; maxX += padX;
    minY -= padY; maxY += padY;

    const toScreenX = (x) => 30 + ((x - minX) / (maxX - minX)) * (w - 60);
    const toScreenY = (y) => h - 30 - ((y - minY) / (maxY - minY)) * (h - 60);

    // Component colors
    const clusterColors = [
        '#00d4ff', // Cyan
        '#7c3aed', // Purple
        '#10b981', // Emerald
        '#f59e0b', // Amber
        '#ec4899', // Pink
        '#3b82f6'  // Blue
    ];

    // 1. Draw Data Points
    dataPoints.forEach(p => {
        const x = Array.isArray(p) ? p[0] : p.x;
        const y = Array.isArray(p) ? p[1] : p.y;
        const cluster = p.cluster !== undefined ? p.cluster : 0;
        const color = clusterColors[cluster % clusterColors.length];

        ctx.beginPath();
        ctx.arc(toScreenX(x), toScreenY(y), 3.5, 0, 2 * Math.PI);
        ctx.fillStyle = color;
        ctx.globalAlpha = 0.65;
        ctx.fill();
    });
    ctx.globalAlpha = 1.0;

    // 2. Draw Cluster Centers & Confidence Ellipses
    if (clusters && Array.isArray(clusters)) {
        clusters.forEach((cl, i) => {
            const color = clusterColors[i % clusterColors.length];
            const mean = cl.mean || [0, 0];
            const cov = cl.covariance || [[1, 0], [0, 1]];

            const cx = toScreenX(mean[0]);
            const cy = toScreenY(mean[1]);

            // Draw center marker
            ctx.beginPath();
            ctx.arc(cx, cy, 6, 0, 2 * Math.PI);
            ctx.fillStyle = '#ffffff';
            ctx.strokeStyle = color;
            ctx.lineWidth = 3;
            ctx.fill();
            ctx.stroke();

            // Draw Ellipse (approximate 2-sigma contour)
            const varX = (cov[0] && cov[0][0]) ? cov[0][0] : 1;
            const varY = (cov[1] && cov[1][1]) ? cov[1][1] : 1;
            const rX = Math.sqrt(Math.abs(varX)) * ((w - 60) / (maxX - minX)) * 2;
            const rY = Math.sqrt(Math.abs(varY)) * ((h - 60) / (maxY - minY)) * 2;

            ctx.beginPath();
            ctx.ellipse(cx, cy, Math.max(8, rX), Math.max(8, rY), 0, 0, 2 * Math.PI);
            ctx.strokeStyle = color;
            ctx.lineWidth = 2;
            ctx.setLineDash([4, 4]);
            ctx.stroke();
            ctx.setLineDash([]);
        });
    }
}

// ============================================================================
// CONVERGENCE LINE CHART (Log-Likelihood)
// ============================================================================
function drawConvergenceChart(canvasId, llHistory) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;

    if (!llHistory || llHistory.length === 0) {
        renderCanvasEmptyState(canvas, 'No convergence data available');
        return;
    }

    const labels = llHistory.map((_, i) => i + 1);

    if (window.Chart) {
        if (activeCharts[canvasId]) {
            activeCharts[canvasId].destroy();
        }

        const ctx = canvas.getContext('2d');
        activeCharts[canvasId] = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Log-Likelihood',
                    data: llHistory,
                    borderColor: '#7c3aed',
                    backgroundColor: 'rgba(124, 58, 237, 0.12)',
                    borderWidth: 2,
                    tension: 0.2,
                    pointRadius: llHistory.length > 50 ? 0 : 3,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: true, labels: { color: '#94a3b8' } }
                },
                scales: {
                    x: {
                        grid: { color: 'rgba(255, 255, 255, 0.05)' },
                        ticks: { color: '#64748b' }
                    },
                    y: {
                        grid: { color: 'rgba(255, 255, 255, 0.05)' },
                        ticks: { color: '#64748b' }
                    }
                }
            }
        });
        return;
    }

    drawCustomLineChart(canvas, labels, llHistory, 'Log-Likelihood Convergence');
}

// ============================================================================
// CANVAS 2D FALLBACK LINE CHART HELPER
// ============================================================================
function drawCustomLineChart(canvas, labels, values, title) {
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const dpr = window.devicePixelRatio || 1;
    const rect = canvas.getBoundingClientRect();
    const w = rect.width || canvas.width || 400;
    const h = rect.height || canvas.height || 200;

    if (canvas.width !== w * dpr || canvas.height !== h * dpr) {
        canvas.width = w * dpr;
        canvas.height = h * dpr;
        ctx.scale(dpr, dpr);
    }

    ctx.clearRect(0, 0, w, h);

    const padLeft = 55;
    const padRight = 20;
    const padTop = 30;
    const padBottom = 30;

    const chartW = w - padLeft - padRight;
    const chartH = h - padTop - padBottom;

    let minV = Math.min(...values);
    let maxV = Math.max(...values);
    if (minV === maxV) { minV -= 1; maxV += 1; }

    const toScreenX = (i) => padLeft + (i / (values.length - 1 || 1)) * chartW;
    const toScreenY = (v) => padTop + chartH - ((v - minV) / (maxV - minV)) * chartH;

    // Title
    ctx.fillStyle = '#94a3b8';
    ctx.font = '12px Inter, sans-serif';
    ctx.textAlign = 'left';
    ctx.fillText(title, padLeft, padTop - 10);

    // Axes
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.1)';
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(padLeft, padTop);
    ctx.lineTo(padLeft, padTop + chartH);
    ctx.lineTo(padLeft + chartW, padTop + chartH);
    ctx.stroke();

    // Min/Max labels
    ctx.fillStyle = '#64748b';
    ctx.font = '10px monospace';
    ctx.textAlign = 'right';
    ctx.fillText(maxV.toFixed(2), padLeft - 6, padTop + 10);
    ctx.fillText(minV.toFixed(2), padLeft - 6, padTop + chartH);

    // Line Path
    ctx.beginPath();
    ctx.strokeStyle = '#00d4ff';
    ctx.lineWidth = 2;
    values.forEach((v, i) => {
        const x = toScreenX(i);
        const y = toScreenY(v);
        if (i === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
    });
    ctx.stroke();
}

function renderCanvasEmptyState(canvas, message) {
    const ctx = canvas.getContext('2d');
    if (!ctx) return;
    const w = canvas.width;
    const h = canvas.height;
    ctx.clearRect(0, 0, w, h);
    ctx.fillStyle = '#64748b';
    ctx.font = '13px Inter, sans-serif';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(message, w / 2, h / 2);
}

// Global exports
window.GraphVisualizer = GraphVisualizer;
window.GridVisualizer = GridVisualizer;
window.drawOptimizationChart = drawOptimizationChart;
window.drawEMClusters = drawEMClusters;
window.drawConvergenceChart = drawConvergenceChart;
