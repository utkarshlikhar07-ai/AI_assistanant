"""
Hidden Markov Model – Weather example.

Hidden states : Sunny, Rainy
Observations  : Walk, Shop, Clean

Implements:
  * Forward algorithm  – compute P(O | lambda)
  * Viterbi algorithm  – find the most likely state sequence
"""

import numpy as np
from typing import List, Tuple, Dict

# ---------------------------------------------------------------------------
# Model parameters
# ---------------------------------------------------------------------------

STATES: List[str] = ["Sunny", "Rainy"]
OBSERVATIONS: List[str] = ["Walk", "Shop", "Clean"]

# Initial state probabilities π
PI: Dict[str, float] = {"Sunny": 0.6, "Rainy": 0.4}

# Transition matrix  A[from_state][to_state]
A: Dict[str, Dict[str, float]] = {
    "Sunny": {"Sunny": 0.7, "Rainy": 0.3},
    "Rainy": {"Sunny": 0.4, "Rainy": 0.6},
}

# Emission matrix  B[state][observation]
B: Dict[str, Dict[str, float]] = {
    "Sunny": {"Walk": 0.6, "Shop": 0.3, "Clean": 0.1},
    "Rainy": {"Walk": 0.1, "Shop": 0.4, "Clean": 0.5},
}


# ---------------------------------------------------------------------------
# Forward algorithm
# ---------------------------------------------------------------------------

def forward_algorithm(observations: List[str]) -> Tuple[float, List[Dict[str, float]]]:
    """
    Compute P(O | lambda) using the forward (alpha) recursion.

    alpha[t][s] = P(o_1, …, o_t, q_t = s | lambda)

    Recurrences
    -----------
    Initialisation  :  alpha[0][s] = PI[s] * B[s][o_0]
    Induction       :  alpha[t][s] = B[s][o_t] * sum_{s'} alpha[t-1][s'] * A[s'][s]
    Termination     :  P(O) = sum_s alpha[T-1][s]

    Returns
    -------
    (probability, alpha_matrix)
    alpha_matrix is a list of dicts {state: probability} for each time step.
    """
    T = len(observations)
    alpha: List[Dict[str, float]] = []

    # --- Initialisation ---
    alpha_0 = {}
    for s in STATES:
        alpha_0[s] = PI[s] * B[s][observations[0]]
    alpha.append(alpha_0)

    # --- Induction ---
    for t in range(1, T):
        obs_t = observations[t]
        alpha_t = {}
        for s in STATES:
            total = sum(alpha[t - 1][s_prev] * A[s_prev][s] for s_prev in STATES)
            alpha_t[s] = B[s][obs_t] * total
        alpha.append(alpha_t)

    # --- Termination ---
    probability = sum(alpha[T - 1][s] for s in STATES)
    return probability, alpha


# ---------------------------------------------------------------------------
# Viterbi algorithm
# ---------------------------------------------------------------------------

def viterbi_algorithm(
    observations: List[str],
) -> Tuple[float, List[str], List[Dict[str, float]]]:
    """
    Find the most likely hidden state sequence using Viterbi.

    delta[t][s] = max probability of any path ending in state s at time t,
                  having generated o_1 … o_t.
    psi[t][s]   = argmax of the predecessor state.

    Recurrences
    -----------
    Initialisation  :  delta[0][s] = PI[s] * B[s][o_0];  psi[0][s] = None
    Induction       :  delta[t][s] = B[s][o_t] * max_{s'} delta[t-1][s'] * A[s'][s]
                       psi[t][s]   = argmax_{s'} delta[t-1][s'] * A[s'][s]
    Termination     :  q*_T = argmax_s delta[T-1][s]
    Backtracking    :  trace psi back to t=0

    Returns
    -------
    (probability, state_sequence, delta_matrix)
    delta_matrix is a list of dicts {state: delta_value} per time step.
    """
    T = len(observations)
    delta: List[Dict[str, float]] = []
    psi: List[Dict[str, str | None]] = []

    # --- Initialisation ---
    delta_0 = {s: PI[s] * B[s][observations[0]] for s in STATES}
    psi_0 = {s: None for s in STATES}
    delta.append(delta_0)
    psi.append(psi_0)

    # --- Induction ---
    for t in range(1, T):
        obs_t = observations[t]
        delta_t: Dict[str, float] = {}
        psi_t: Dict[str, str] = {}
        for s in STATES:
            candidates = {s_prev: delta[t - 1][s_prev] * A[s_prev][s] for s_prev in STATES}
            best_prev = max(candidates, key=candidates.__getitem__)
            delta_t[s] = B[s][obs_t] * candidates[best_prev]
            psi_t[s] = best_prev
        delta.append(delta_t)
        psi.append(psi_t)

    # --- Termination ---
    best_last = max(STATES, key=lambda s: delta[T - 1][s])
    probability = delta[T - 1][best_last]

    # --- Backtracking ---
    path: List[str] = [best_last]
    for t in range(T - 1, 0, -1):
        path.append(psi[t][path[-1]])
    path.reverse()

    return probability, path, delta


# ---------------------------------------------------------------------------
# Public runner
# ---------------------------------------------------------------------------

def run_hmm(observations: List[str], algorithm: str = "both") -> dict:
    """
    Run Forward and/or Viterbi on the given observation sequence.

    Parameters
    ----------
    observations : list of str  (must be in OBSERVATIONS)
    algorithm    : "forward" | "viterbi" | "both"

    Returns
    -------
    dict with forward_prob, viterbi_path, viterbi_prob, state_probs,
    message, success.
    """
    # Validate
    invalid = [o for o in observations if o not in OBSERVATIONS]
    if invalid:
        return {
            "forward_prob": 0.0,
            "viterbi_path": [],
            "viterbi_prob": 0.0,
            "state_probs": [],
            "message": f"Invalid observations: {invalid}. Must be one of {OBSERVATIONS}.",
            "success": False,
        }

    if not observations:
        return {
            "forward_prob": 0.0,
            "viterbi_path": [],
            "viterbi_prob": 0.0,
            "state_probs": [],
            "message": "Observation sequence is empty.",
            "success": False,
        }

    try:
        forward_prob = 0.0
        viterbi_path: List[str] = []
        viterbi_prob = 0.0
        alpha_matrix: List[Dict[str, float]] = []
        delta_matrix: List[Dict[str, float]] = []

        if algorithm in ("forward", "both"):
            forward_prob, alpha_matrix = forward_algorithm(observations)

        if algorithm in ("viterbi", "both"):
            viterbi_prob, viterbi_path, delta_matrix = viterbi_algorithm(observations)

        # Per-timestep state probabilities derived from forward alpha
        # (normalised so they sum to 1 at each step, giving P(q_t=s | o_1..o_t))
        if alpha_matrix:
            state_probs = []
            for alpha_t in alpha_matrix:
                total = sum(alpha_t.values())
                if total > 0:
                    state_probs.append({s: alpha_t[s] / total for s in STATES})
                else:
                    state_probs.append({s: 0.0 for s in STATES})
        elif delta_matrix:
            # Fallback: use delta (un-normalised)
            state_probs = []
            for delta_t in delta_matrix:
                total = sum(delta_t.values())
                if total > 0:
                    state_probs.append({s: delta_t[s] / total for s in STATES})
                else:
                    state_probs.append({s: 0.0 for s in STATES})
        else:
            state_probs = []

        algo_desc = {
            "forward": "Forward algorithm",
            "viterbi": "Viterbi algorithm",
            "both": "Forward + Viterbi algorithms",
        }.get(algorithm, algorithm)

        message = (
            f"{algo_desc} completed for {len(observations)} observation(s). "
            f"P(O|λ) = {forward_prob:.6e}. "
            f"Most likely path: {' → '.join(viterbi_path) if viterbi_path else 'N/A'}."
        )

        return {
            "forward_prob": float(forward_prob),
            "viterbi_path": viterbi_path,
            "viterbi_prob": float(viterbi_prob),
            "state_probs": state_probs,
            "message": message,
            "success": True,
        }

    except Exception as exc:
        return {
            "forward_prob": 0.0,
            "viterbi_path": [],
            "viterbi_prob": 0.0,
            "state_probs": [],
            "message": f"HMM computation failed: {exc}",
            "success": False,
        }
