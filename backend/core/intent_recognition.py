"""
JARVIS AI - Intent Recognition Module
Keyword-based intent classification with entity extraction.
"""
import re
from typing import Any

# ─── Intent Constants ────────────────────────────────────────────────────────

GREETING = "greeting"
GENERAL_QUERY = "general_query"
CALCULATION = "calculation"
EXPLAIN_ALGORITHM = "explain_algorithm"
BFS_REQUEST = "bfs_request"
DFS_REQUEST = "dfs_request"
IDDFS_REQUEST = "iddfs_request"
ASTAR_REQUEST = "astar_request"
DSTAR_REQUEST = "dstar_request"
PUZZLE_8_REQUEST = "puzzle_8_request"
WUMPUS_REQUEST = "wumpus_request"
HANOI_REQUEST = "hanoi_request"
PROBABILITY_REQUEST = "probability_request"
HMM_REQUEST = "hmm_request"
OPTIMIZATION_REQUEST = "optimization_request"
HILL_CLIMBING_REQUEST = "hill_climbing_request"
SIMULATED_ANNEALING_REQUEST = "simulated_annealing_request"
EM_REQUEST = "em_request"
HELP = "help"

# ─── Keyword Patterns ────────────────────────────────────────────────────────

INTENT_PATTERNS: dict[str, list[str]] = {
    GREETING: [
        "hello", "hi", "hey", "good morning", "good afternoon", "good evening",
        "howdy", "greetings", "what's up", "sup", "yo",
    ],
    HELP: [
        "help", "what can you do", "what are your capabilities", "show me what",
        "guide me", "assist me", "support", "options", "features", "commands",
        "how do i", "how to use",
    ],
    BFS_REQUEST: [
        "bfs", "breadth first", "breadth-first", "breadth first search",
        "level order", "shortest path bfs",
    ],
    DFS_REQUEST: [
        "dfs", "depth first", "depth-first", "depth first search",
        "graph traversal dfs",
    ],
    IDDFS_REQUEST: [
        "iddfs", "iterative deepening", "iterative-deepening",
        "iterative deepening depth first", "id-dfs", "iddfs search",
    ],
    ASTAR_REQUEST: [
        "a star", "a*", "astar", "a-star", "a* search", "a star search",
        "heuristic search", "informed search",
    ],
    DSTAR_REQUEST: [
        "d star", "d*", "dstar", "d-star", "d* search", "dynamic replanning",
        "dynamic path planning", "d star lite",
    ],
    PUZZLE_8_REQUEST: [
        "8 puzzle", "eight puzzle", "8-puzzle", "sliding puzzle",
        "tile puzzle", "15 puzzle", "solve puzzle",
    ],
    WUMPUS_REQUEST: [
        "wumpus", "wumpus world", "hunt the wumpus", "wumpus game",
        "wumpus cave", "gold and wumpus",
    ],
    HANOI_REQUEST: [
        "hanoi", "tower of hanoi", "towers of hanoi", "hanoi puzzle",
        "disk puzzle", "hanoi problem",
    ],
    HILL_CLIMBING_REQUEST: [
        "hill climbing", "hill-climbing", "hill climb", "steepest ascent",
        "local search hill", "gradient ascent",
    ],
    SIMULATED_ANNEALING_REQUEST: [
        "simulated annealing", "sim anneal", "annealing", "sa optimization",
        "simulated annealing algorithm",
    ],
    OPTIMIZATION_REQUEST: [
        "optimize", "optimization", "find maximum", "find minimum",
        "maximize", "minimize", "best solution", "optimal",
    ],
    PROBABILITY_REQUEST: [
        "bayesian", "bayes", "bayesian network", "probability", "probabilistic",
        "conditional probability", "prior", "posterior", "belief network",
    ],
    HMM_REQUEST: [
        "hmm", "hidden markov", "markov model", "hidden markov model",
        "viterbi", "forward algorithm", "markov chain",
    ],
    EM_REQUEST: [
        "em algorithm", "expectation maximization", "expectation-maximization",
        "em clustering", "gaussian mixture", "gmm", "mixture model",
    ],
    EXPLAIN_ALGORITHM: [
        "explain", "what is", "how does", "describe", "tell me about",
        "definition of", "meaning of", "teach me", "clarify",
    ],
    CALCULATION: [
        "calculate", "compute", "evaluate", "solve", "what is the result",
        "how much", "how many", "sum of", "product of", "difference",
    ],
    GENERAL_QUERY: [
        "what", "why", "where", "when", "who", "which", "can you",
        "could you", "would you", "is it", "are you",
    ],
}

# Algorithm name aliases for entity extraction
ALGORITHM_ALIASES: dict[str, str] = {
    "bfs": "BFS", "breadth first": "BFS", "breadth-first": "BFS",
    "dfs": "DFS", "depth first": "DFS", "depth-first": "DFS",
    "iddfs": "IDDFS", "iterative deepening": "IDDFS",
    "a*": "A*", "a star": "A*", "astar": "A*", "a-star": "A*",
    "d*": "D*", "d star": "D*", "dstar": "D*",
    "hill climbing": "HillClimbing", "hill-climbing": "HillClimbing",
    "simulated annealing": "SimulatedAnnealing",
    "bayesian": "Bayesian", "hmm": "HMM",
    "em algorithm": "EM", "expectation maximization": "EM",
}


# ─── Entity Extraction ───────────────────────────────────────────────────────

def _extract_numbers(text: str) -> list[float]:
    """Extract numeric values from text."""
    return [float(m) for m in re.findall(r"-?\d+(?:\.\d+)?", text)]


def _extract_node_names(text: str) -> list[str]:
    """Extract potential graph node names (single letters or short capitalized words)."""
    # Single uppercase letters (classic node names like A, B, C)
    single = re.findall(r"\b([A-Z])\b", text)
    # Words explicitly mentioned as nodes
    node_words = re.findall(r"\bnode\s+([A-Za-z0-9_]+)", text, re.IGNORECASE)
    return list(dict.fromkeys(single + node_words))  # deduplicate, preserve order


def _extract_algorithms(text: str) -> list[str]:
    """Extract algorithm names mentioned in the text."""
    text_lower = text.lower()
    found = []
    for alias, canonical in ALGORITHM_ALIASES.items():
        if alias in text_lower and canonical not in found:
            found.append(canonical)
    return found


def _extract_entities(text: str) -> dict[str, Any]:
    """Return a dict of extracted entities from the user's text."""
    return {
        "numbers": _extract_numbers(text),
        "nodes": _extract_node_names(text),
        "algorithms": _extract_algorithms(text),
        "raw_text": text,
    }


# ─── Confidence Scoring ──────────────────────────────────────────────────────

def _score_intent(text: str, intent: str, patterns: list[str]) -> float:
    """Return a confidence score [0.0, 1.0] for a single intent."""
    text_lower = text.lower()
    matches = sum(1 for p in patterns if p in text_lower)
    if matches == 0:
        return 0.0
    # Weight by how many keywords matched relative to total patterns
    base_score = min(matches / max(len(patterns) * 0.15, 1), 1.0)
    # Boost for exact multi-word matches
    exact_bonus = sum(0.2 for p in patterns if len(p.split()) > 1 and p in text_lower)
    return min(base_score + exact_bonus, 1.0)


# ─── Main Recognition Function ───────────────────────────────────────────────

def recognize_intent(text: str) -> dict[str, Any]:
    """
    Classify the user's text into one of the JARVIS intents.

    Returns:
        {
            "intent": str,
            "confidence": float,
            "entities": dict,
        }
    """
    if not text or not text.strip():
        return {"intent": GENERAL_QUERY, "confidence": 0.0, "entities": {}}

    text_stripped = text.strip()
    scores: dict[str, float] = {}

    for intent, patterns in INTENT_PATTERNS.items():
        scores[intent] = _score_intent(text_stripped, intent, patterns)

    # Pick the highest-scoring intent
    best_intent = max(scores, key=lambda k: scores[k])
    best_score = scores[best_intent]

    # If no intent has any signal, fall back to GENERAL_QUERY
    if best_score == 0.0:
        best_intent = GENERAL_QUERY
        best_score = 0.1

    # Tie-break: more specific intents beat GENERAL_QUERY / EXPLAIN_ALGORITHM
    if best_score < 0.15 and best_intent in (GENERAL_QUERY, EXPLAIN_ALGORITHM):
        # Check if any domain-specific intent has a small score
        domain_intents = [
            i for i in scores
            if i not in (GENERAL_QUERY, EXPLAIN_ALGORITHM, GREETING, HELP, CALCULATION)
        ]
        domain_best = max(domain_intents, key=lambda k: scores[k], default=None)
        if domain_best and scores[domain_best] > 0:
            best_intent = domain_best
            best_score = scores[domain_best]

    entities = _extract_entities(text_stripped)

    return {
        "intent": best_intent,
        "confidence": round(best_score, 3),
        "entities": entities,
    }
