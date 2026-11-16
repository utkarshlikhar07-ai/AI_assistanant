"""
JARVIS AI - Assistant Service
Orchestrates intent recognition, response generation, and algorithm routing.
"""
from backend.core.intent_recognition import (
    recognize_intent,
    GREETING, GENERAL_QUERY, CALCULATION, EXPLAIN_ALGORITHM,
    BFS_REQUEST, DFS_REQUEST, IDDFS_REQUEST, ASTAR_REQUEST, DSTAR_REQUEST,
    PUZZLE_8_REQUEST, WUMPUS_REQUEST, HANOI_REQUEST, PROBABILITY_REQUEST,
    HMM_REQUEST, OPTIMIZATION_REQUEST, HILL_CLIMBING_REQUEST,
    SIMULATED_ANNEALING_REQUEST, EM_REQUEST, HELP,
)
from backend.core.response_engine import generate_response

# ─── Navigation Mapping ──────────────────────────────────────────────────────

NAVIGATE_TO_MAP: dict[str, str] = {
    BFS_REQUEST: "search",
    DFS_REQUEST: "search",
    IDDFS_REQUEST: "search",
    ASTAR_REQUEST: "search",
    DSTAR_REQUEST: "search",
    PUZZLE_8_REQUEST: "puzzles",
    WUMPUS_REQUEST: "wumpus",
    HANOI_REQUEST: "puzzles",
    HILL_CLIMBING_REQUEST: "search",
    SIMULATED_ANNEALING_REQUEST: "search",
    OPTIMIZATION_REQUEST: "search",
    PROBABILITY_REQUEST: "probabilistic",
    HMM_REQUEST: "probabilistic",
    EM_REQUEST: "probabilistic",
    GREETING: "chat",
    HELP: "chat",
    EXPLAIN_ALGORITHM: "chat",
    CALCULATION: "chat",
    GENERAL_QUERY: "chat",
}


# ─── Algorithm Quick-Run Helpers ─────────────────────────────────────────────

def _quick_bfs(entities: dict) -> dict | None:
    """Return lightweight BFS info if nodes and edges can be inferred."""
    nodes = entities.get("nodes", [])
    if len(nodes) >= 2:
        return {
            "note": "Navigate to the Search interface to run BFS with a full graph definition.",
            "detected_nodes": nodes,
        }
    return None


def _quick_hanoi(entities: dict) -> dict | None:
    """Return precomputed Hanoi move count if a disk number was found."""
    numbers = entities.get("numbers", [])
    if numbers:
        n = int(numbers[0])
        if 1 <= n <= 20:
            return {"num_disks": n, "total_moves": 2 ** n - 1}
    return None


def _quick_optimization(entities: dict) -> dict | None:
    """Return hint data for optimisation requests."""
    return {
        "supported_methods": ["Hill Climbing", "Simulated Annealing"],
        "note": "Navigate to the Optimisation interface for interactive visualisation.",
    }


# ─── Main Service Function ───────────────────────────────────────────────────

async def process_message(message: str, history: list) -> dict:
    """
    Process a user message and return a structured JARVIS response.

    Parameters
    ----------
    message : str
        The raw user message.
    history : list
        Previous conversation turns (list of {role, content} dicts).

    Returns
    -------
    dict
        {
            "response": str,
            "intent": str,
            "data": dict | None,
            "navigate_to": str | None,
            "success": bool,
        }
    """
    try:
        # 1. Recognise intent and extract entities
        recognition = recognize_intent(message)
        intent: str = recognition["intent"]
        confidence: float = recognition["confidence"]
        entities: dict = recognition["entities"]

        # 2. Gather supplemental data where we can compute it quickly
        data: dict | None = None

        if intent == HANOI_REQUEST:
            data = _quick_hanoi(entities)
        elif intent in (BFS_REQUEST, DFS_REQUEST, IDDFS_REQUEST):
            data = _quick_bfs(entities)
        elif intent in (OPTIMIZATION_REQUEST, HILL_CLIMBING_REQUEST, SIMULATED_ANNEALING_REQUEST):
            data = _quick_optimization(entities)

        # Attach confidence for transparency
        if data is None:
            data = {}
        data["confidence"] = confidence

        # 3. Generate response text
        response_text = generate_response(intent, entities, data)

        # 4. Determine navigation target
        navigate_to: str | None = NAVIGATE_TO_MAP.get(intent)

        return {
            "response": response_text,
            "intent": intent,
            "data": data,
            "navigate_to": navigate_to,
            "success": True,
        }

    except Exception as exc:  # pylint: disable=broad-except
        return {
            "response": (
                "I encountered an unexpected error while processing your request. "
                f"Details: {exc}. Please try again or rephrase your query."
            ),
            "intent": GENERAL_QUERY,
            "data": None,
            "navigate_to": None,
            "success": False,
        }
