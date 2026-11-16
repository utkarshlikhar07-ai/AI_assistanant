// JARVIS AI - Probabilistic AI Controller
// Manages Bayesian Network inference, Expectation-Maximization (GMM), and Hidden Markov Models (HMM)

// ============================================================================
// 1. BAYESIAN NETWORK INFERENCE
// ============================================================================
const DEFAULT_PRIORS = {
    Burglary: 0.001,
    Earthquake: 0.002,
    Alarm: 0.0025,
    JohnCalls: 0.052,
    MaryCalls: 0.012
};

async function runBayesian() {
    const evidence = {};

    const evBurglary = document.getElementById('ev-burglary');
    const evEarthquake = document.getElementById('ev-earthquake');
    const evAlarm = document.getElementById('ev-alarm');
    const evJohn = document.getElementById('ev-johncalls');
    const evMary = document.getElementById('ev-marycalls');

    if (evBurglary && evBurglary.checked) evidence['Burglary'] = true;
    if (evEarthquake && evEarthquake.checked) evidence['Earthquake'] = true;
    if (evAlarm && evAlarm.checked) evidence['Alarm'] = true;
    if (evJohn && evJohn.checked) evidence['JohnCalls'] = true;
    if (evMary && evMary.checked) evidence['MaryCalls'] = true;

    try {
        showToast('Computing Bayesian posterior probabilities...', 'info', 1500);
        const res = await apiCall('/probabilistic/bayesian', 'POST', {
            evidence: evidence
        });

        const probs = res.probabilities || DEFAULT_PRIORS;

        updateBayesianBars(probs);

        const expEl = document.getElementById('bayesian-explanation');
        if (expEl) {
            const evKeys = Object.keys(evidence);
            const evText = evKeys.length > 0 ? evKeys.join(', ') : 'None (Prior distributions)';
            expEl.innerHTML = `
                <div style="font-weight:600;color:var(--accent-cyan);margin-bottom:6px;">Inference Results</div>
                <p><strong>Observed Evidence:</strong> ${evText}</p>
                <p style="margin-top:6px;">${escapeHtml(res.explanation || 'Exact inference computed using enumeration over joint distribution.')}</p>
            `;
        }

        const evSummary = Object.keys(evidence).length > 0 ? Object.keys(evidence).join('+') : 'Prior';
        logActivity('probabilistic', `Bayesian Inference: e=${evSummary}`, `P(Burglary)=${(probs.Burglary || 0).toFixed(4)}`, '📊');
        showToast('Bayesian inference computed successfully', 'success');

    } catch (e) {
        console.error('Bayesian error:', e);
        showToast(`Bayesian Error: ${e.message}`, 'error');
    }
}

function updateBayesianBars(probs) {
    const mapping = [
        { key: 'Burglary', barId: 'pb-burglary', valId: 'pv-burglary-val' },
        { key: 'Earthquake', barId: 'pb-earthquake', valId: 'pv-earthquake-val' },
        { key: 'Alarm', barId: 'pb-alarm', valId: 'pv-alarm-val' },
        { key: 'JohnCalls', barId: 'pb-john', valId: 'pv-john-val' },
        { key: 'MaryCalls', barId: 'pb-mary', valId: 'pv-mary-val' }
    ];

    mapping.forEach(({ key, barId, valId }) => {
        const p = probs[key] !== undefined ? probs[key] : (DEFAULT_PRIORS[key] || 0.0);
        const barEl = document.getElementById(barId);
        const valEl = document.getElementById(valId);

        if (barEl) {
            const pct = Math.max(1, Math.min(100, p * 100));
            barEl.style.width = `${pct.toFixed(1)}%`;
        }
        if (valEl) {
            valEl.textContent = p.toFixed(4);
        }
    });
}

function resetBayesian() {
    ['ev-burglary', 'ev-earthquake', 'ev-alarm', 'ev-johncalls', 'ev-marycalls'].forEach(id => {
        const el = document.getElementById(id);
        if (el) el.checked = false;
    });

    updateBayesianBars(DEFAULT_PRIORS);

    const expEl = document.getElementById('bayesian-explanation');
    if (expEl) {
        expEl.innerHTML = '<p>Select evidence variables and click Compute to see posterior probabilities.</p>';
    }

    showToast('Reset Bayesian evidence to priors', 'info', 1200);
}

// ============================================================================
// 2. EXPECTATION-MAXIMIZATION (GMM CLUSTERING)
// ============================================================================
let cachedEMData = null;

function generateEMData() {
    const seedEl = document.getElementById('em-seed');
    if (seedEl) {
        seedEl.value = Math.floor(Math.random() * 1000);
    }
    showToast(`New seed generated: ${seedEl ? seedEl.value : ''}. Click Run EM.`, 'info', 1500);
}

async function runEM() {
    const samples = parseInt(document.getElementById('em-samples')?.value, 10) || 200;
    const components = parseInt(document.getElementById('em-components')?.value, 10) || 3;
    const maxIter = parseInt(document.getElementById('em-maxiter')?.value, 10) || 100;
    const seed = parseInt(document.getElementById('em-seed')?.value, 10) || 42;

    const iterEl = document.getElementById('em-iter-count');
    const convEl = document.getElementById('em-converged');
    const loglikEl = document.getElementById('em-loglik');
    const clusterListEl = document.getElementById('em-cluster-list');

    try {
        showToast('Running Expectation-Maximization algorithm...', 'info', 1500);
        const res = await apiCall('/probabilistic/em', 'POST', {
            n_samples: samples,
            n_components: components,
            max_iterations: maxIter,
            seed: seed
        });

        if (iterEl) iterEl.textContent = res.iterations !== undefined ? res.iterations : '-';
        if (convEl) convEl.textContent = res.converged ? 'Yes ✓' : 'No ✗';
        if (loglikEl) {
            const lastLL = (res.log_likelihood_history && res.log_likelihood_history.length > 0)
                ? res.log_likelihood_history[res.log_likelihood_history.length - 1]
                : 0;
            loglikEl.textContent = Number(lastLL).toFixed(2);
        }

        // Generate synthetic data points according to fitted clusters for scatter plot visualization
        const syntheticPoints = generateSyntheticPointsFromClusters(res.clusters, samples, seed);
        cachedEMData = { points: syntheticPoints, clusters: res.clusters };

        // Draw scatter plot
        if (typeof window.drawEMClusters === 'function') {
            window.drawEMClusters('em-canvas', syntheticPoints, res.clusters);
        }

        // Draw convergence curve
        if (typeof window.drawConvergenceChart === 'function') {
            window.drawConvergenceChart('em-convergence-chart', res.log_likelihood_history || []);
        }

        // Render cluster summary cards
        if (clusterListEl && res.clusters) {
            clusterListEl.innerHTML = res.clusters.map((c, idx) => {
                const meanX = c.mean && c.mean[0] !== undefined ? Number(c.mean[0]).toFixed(3) : '0';
                const meanY = c.mean && c.mean[1] !== undefined ? Number(c.mean[1]).toFixed(3) : '0';
                const weight = c.weight !== undefined ? Number(c.weight).toFixed(3) : '0';
                return `
                    <div class="cluster-summary-card card-glass" style="padding:10px 14px;margin-bottom:8px;border-left:3px solid var(--accent-cyan);font-size:0.85rem;">
                        <div style="font-weight:600;color:var(--text-primary);margin-bottom:4px;">Cluster #${idx + 1}</div>
                        <div><strong>Weight (π):</strong> ${weight}</div>
                        <div><strong>Mean (μ):</strong> [${meanX}, ${meanY}]</div>
                    </div>
                `;
            }).join('');
        }

        logActivity('probabilistic', `EM Algorithm (${components} components)`, `Converged in ${res.iterations} iterations`, '📊');
        showToast(`EM completed: ${res.converged ? 'Converged' : 'Finished'} in ${res.iterations} iterations`, 'success');

    } catch (e) {
        console.error('EM error:', e);
        showToast(`EM Error: ${e.message}`, 'error');
    }
}

function generateSyntheticPointsFromClusters(clusters, nSamples, seed) {
    if (!clusters || clusters.length === 0) return [];
    const points = [];

    // Simple pseudo-random generator with seed
    let s = seed || 42;
    const pseudoRand = () => {
        s = (s * 9301 + 49297) % 233280;
        return s / 233280;
    };
    const randn = () => {
        const u = pseudoRand();
        const v = pseudoRand();
        return Math.sqrt(-2.0 * Math.log(u || 0.001)) * Math.cos(2.0 * Math.PI * v);
    };

    clusters.forEach((cl, clusterIdx) => {
        const count = Math.max(10, Math.floor(nSamples * (cl.weight || (1 / clusters.length))));
        const mx = (cl.mean && cl.mean[0]) || 0;
        const my = (cl.mean && cl.mean[1]) || 0;
        const stdX = Math.sqrt(Math.abs((cl.covariance && cl.covariance[0] && cl.covariance[0][0]) || 1));
        const stdY = Math.sqrt(Math.abs((cl.covariance && cl.covariance[1] && cl.covariance[1][1]) || 1));

        for (let i = 0; i < count; i++) {
            points.push({
                x: mx + randn() * stdX * 0.8,
                y: my + randn() * stdY * 0.8,
                cluster: clusterIdx
            });
        }
    });

    return points;
}

// ============================================================================
// 3. HIDDEN MARKOV MODEL (HMM)
// ============================================================================
function getSelectedObservations() {
    const checkboxes = document.querySelectorAll('.hmm-obs:checked');
    const obs = [];
    checkboxes.forEach(cb => {
        obs.push(cb.value);
    });
    return obs;
}

function updateHMMPreview() {
    const obs = getSelectedObservations();
    const previewEl = document.getElementById('hmm-sequence-preview');
    if (previewEl) {
        previewEl.textContent = obs.length > 0 ? obs.join(' → ') : 'None selected';
    }
}

async function runHMM() {
    const observations = getSelectedObservations();
    if (observations.length === 0) {
        showToast('Please select at least one observation', 'warning');
        return;
    }

    const algo = document.getElementById('hmm-algo')?.value || 'both';
    const fwdEl = document.getElementById('hmm-forward-prob');
    const pathEl = document.getElementById('hmm-viterbi-path');
    const vitProbEl = document.getElementById('hmm-viterbi-prob');
    const stateProbsEl = document.getElementById('hmm-state-probs');

    try {
        showToast('Running HMM inference...', 'info', 1500);
        const res = await apiCall('/probabilistic/hmm', 'POST', {
            observations: observations,
            algorithm: algo
        });

        if (fwdEl) {
            fwdEl.textContent = res.forward_prob !== undefined ? Number(res.forward_prob).toExponential(4) : 'N/A';
        }

        if (pathEl) {
            pathEl.textContent = (res.viterbi_path && res.viterbi_path.length > 0)
                ? res.viterbi_path.join(' → ')
                : 'N/A';
        }

        if (vitProbEl) {
            vitProbEl.textContent = res.viterbi_prob !== undefined ? Number(res.viterbi_prob).toExponential(4) : 'N/A';
        }

        // Render state posterior table / probabilities
        if (stateProbsEl && res.state_probs && res.state_probs.length > 0) {
            stateProbsEl.innerHTML = `
                <div style="font-weight:600;margin:12px 0 6px 0;color:var(--text-primary);font-size:0.85rem;">Step-by-Step State Distributions:</div>
                <div style="overflow-x:auto;">
                    <table style="width:100%;font-size:0.8rem;border-collapse:collapse;">
                        <thead>
                            <tr style="border-bottom:1px solid rgba(255,255,255,0.1);text-align:left;">
                                <th style="padding:4px;">Time Step</th>
                                <th style="padding:4px;">Observed</th>
                                <th style="padding:4px;">P(Sunny)</th>
                                <th style="padding:4px;">P(Rainy)</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${res.state_probs.map((st, i) => {
                                const pSunny = st.Sunny !== undefined ? (st.Sunny * 100).toFixed(1) : (st.sunny !== undefined ? (st.sunny * 100).toFixed(1) : '50.0');
                                const pRainy = st.Rainy !== undefined ? (st.Rainy * 100).toFixed(1) : (st.rainy !== undefined ? (st.rainy * 100).toFixed(1) : '50.0');
                                return `
                                    <tr style="border-bottom:1px solid rgba(255,255,255,0.04);">
                                        <td style="padding:4px;">t = ${i + 1}</td>
                                        <td style="padding:4px;color:var(--accent-cyan);">${escapeHtml(observations[i] || '-')}</td>
                                        <td style="padding:4px;">${pSunny}%</td>
                                        <td style="padding:4px;">${pRainy}%</td>
                                    </tr>
                                `;
                            }).join('')}
                        </tbody>
                    </table>
                </div>
            `;
        }

        const vPathStr = res.viterbi_path ? res.viterbi_path.join('→') : '';
        logActivity('probabilistic', `HMM Inference (${algo})`, `Obs: ${observations.join('→')} | Path: ${vPathStr}`, '📊');
        showToast('HMM inference completed successfully', 'success');

    } catch (e) {
        console.error('HMM error:', e);
        showToast(`HMM Error: ${e.message}`, 'error');
    }
}

function resetHMM() {
    const obsCheckboxes = document.querySelectorAll('.hmm-obs');
    obsCheckboxes.forEach(cb => {
        cb.checked = (cb.value === 'Walk' || cb.value === 'Shop');
    });

    updateHMMPreview();

    const fwdEl = document.getElementById('hmm-forward-prob');
    const pathEl = document.getElementById('hmm-viterbi-path');
    const vitProbEl = document.getElementById('hmm-viterbi-prob');
    const stateProbsEl = document.getElementById('hmm-state-probs');

    if (fwdEl) fwdEl.textContent = '—';
    if (pathEl) pathEl.textContent = '—';
    if (vitProbEl) vitProbEl.textContent = '—';
    if (stateProbsEl) stateProbsEl.innerHTML = '';

    showToast('Reset HMM sequence to default', 'info', 1200);
}

// ============================================================================
// INITIALIZATION
// ============================================================================
window.addEventListener('DOMContentLoaded', () => {
    // Listeners for HMM observation checkboxes
    const obsCheckboxes = document.querySelectorAll('.hmm-obs');
    obsCheckboxes.forEach(cb => {
        cb.addEventListener('change', updateHMMPreview);
    });
    updateHMMPreview();
});

// Global exports
window.runBayesian = runBayesian;
window.resetBayesian = resetBayesian;
window.generateEMData = generateEMData;
window.runEM = runEM;
window.runHMM = runHMM;
window.resetHMM = resetHMM;
