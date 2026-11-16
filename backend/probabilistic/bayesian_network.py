"""
Bayesian Network: Weather / Sprinkler / Grass-Wet example.

Network structure:
    Cloudy -> Rain
    Cloudy -> Sprinkler
    Rain   -> WetGrass
    Sprinkler -> WetGrass

Inference is done by full enumeration of the joint distribution (exact).
"""

from itertools import product
from typing import Dict

# ---------------------------------------------------------------------------
# Conditional Probability Tables
# ---------------------------------------------------------------------------

# P(Cloudy)
CPT_CLOUDY = {True: 0.5, False: 0.5}

# P(Sprinkler | Cloudy)
CPT_SPRINKLER = {True: 0.1, False: 0.5}   # key = Cloudy value

# P(Rain | Cloudy)
CPT_RAIN = {True: 0.8, False: 0.2}         # key = Cloudy value

# P(WetGrass | Sprinkler, Rain)
CPT_WETGRASS = {
    (True,  True):  0.99,
    (True,  False): 0.90,
    (False, True):  0.90,
    (False, False): 0.01,
}

NODES = ["Cloudy", "Rain", "Sprinkler", "WetGrass"]

EDGES = [
    ("Cloudy", "Rain"),
    ("Cloudy", "Sprinkler"),
    ("Rain",   "WetGrass"),
    ("Sprinkler", "WetGrass"),
]

CPTS_DESCRIPTION = {
    "Cloudy": {
        "parents": [],
        "table": {"P(Cloudy=T)": 0.5, "P(Cloudy=F)": 0.5},
    },
    "Sprinkler": {
        "parents": ["Cloudy"],
        "table": {
            "P(Sprinkler=T|Cloudy=T)": 0.1,
            "P(Sprinkler=T|Cloudy=F)": 0.5,
        },
    },
    "Rain": {
        "parents": ["Cloudy"],
        "table": {
            "P(Rain=T|Cloudy=T)": 0.8,
            "P(Rain=T|Cloudy=F)": 0.2,
        },
    },
    "WetGrass": {
        "parents": ["Sprinkler", "Rain"],
        "table": {
            "P(WG=T|S=T,R=T)": 0.99,
            "P(WG=T|S=T,R=F)": 0.90,
            "P(WG=T|S=F,R=T)": 0.90,
            "P(WG=T|S=F,R=F)": 0.01,
        },
    },
}


# ---------------------------------------------------------------------------
# Joint probability of one complete assignment
# ---------------------------------------------------------------------------

def _joint(c: bool, r: bool, s: bool, w: bool) -> float:
    """Compute P(Cloudy=c, Rain=r, Sprinkler=s, WetGrass=w)."""
    p_c = CPT_CLOUDY[c]
    p_s = CPT_SPRINKLER[c] if s else (1.0 - CPT_SPRINKLER[c])
    p_r = CPT_RAIN[c]      if r else (1.0 - CPT_RAIN[c])
    p_w_raw = CPT_WETGRASS[(s, r)]
    p_w = p_w_raw if w else (1.0 - p_w_raw)
    return p_c * p_s * p_r * p_w


# ---------------------------------------------------------------------------
# Public inference function
# ---------------------------------------------------------------------------

def compute_inference(evidence: Dict[str, bool]) -> dict:
    """
    Compute posterior probabilities for all nodes given evidence.

    Parameters
    ----------
    evidence : dict  e.g. {"Rain": True, "Cloudy": False}

    Returns
    -------
    dict with keys:
        probabilities    – {node: {True: p, False: 1-p}}
        explanation      – human-readable summary
        network_structure – {nodes, edges, cpts}
    """
    node_order = ["Cloudy", "Rain", "Sprinkler", "WetGrass"]

    def consistent(assignment: dict) -> bool:
        """Return True when this assignment is compatible with evidence."""
        for node, val in evidence.items():
            if assignment[node] != val:
                return False
        return True

    # Enumerate all 2^4 = 16 complete assignments
    all_assignments = list(product([True, False], repeat=4))

    # Normalising constant Z = P(evidence)
    Z = 0.0
    for vals in all_assignments:
        asgn = dict(zip(node_order, vals))
        if consistent(asgn):
            Z += _joint(*vals)

    if Z == 0.0:
        raise ValueError("Evidence has zero probability – inconsistent evidence.")

    # Marginal for each node
    probabilities: Dict[str, Dict[bool, float]] = {}
    for query_node in node_order:
        p_true = 0.0
        for vals in all_assignments:
            asgn = dict(zip(node_order, vals))
            if consistent(asgn) and asgn[query_node] is True:
                p_true += _joint(*vals)
        p_true /= Z
        probabilities[query_node] = {True: round(p_true, 6), False: round(1.0 - p_true, 6)}

    # Build explanation
    ev_str = ", ".join(f"{k}={'T' if v else 'F'}" for k, v in evidence.items()) if evidence else "none"
    lines = [f"Evidence: {ev_str}", "Posterior probabilities:"]
    for node in node_order:
        pt = probabilities[node][True]
        pf = probabilities[node][False]
        lines.append(f"  P({node}=T | evidence) = {pt:.4f},  P({node}=F | evidence) = {pf:.4f}")

    explanation = "\n".join(lines)

    return {
        "probabilities": {
            node: {str(k): v for k, v in prob.items()}
            for node, prob in probabilities.items()
        },
        "explanation": explanation,
        "network_structure": {
            "nodes": NODES,
            "edges": [list(e) for e in EDGES],
            "cpts": CPTS_DESCRIPTION,
        },
    }
