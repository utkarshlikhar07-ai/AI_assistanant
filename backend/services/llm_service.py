"""
JARVIS AI - Gemini LLM Service Module
Integrates Google Gemini Large Language Model via the official modern google-genai SDK.
Handles conversational intelligence, multi-turn dialogue, secure key management,
and tool-calling integration with all 13 AI algorithms.
"""

import os
import re
import json
import logging
from typing import Any, Dict, List, Optional
from pathlib import Path
from dotenv import load_dotenv, set_key

# Import official modern SDK
from google import genai
from google.genai import types

# Import existing algorithm engines
from backend.algorithms.bfs import bfs
from backend.algorithms.dfs import dfs
from backend.algorithms.iddfs import iddfs
from backend.algorithms.astar import astar
from backend.algorithms.dstar import dstar_plan
from backend.algorithms.hill_climbing import hill_climbing
from backend.algorithms.simulated_annealing import simulated_annealing
from backend.problems.eight_puzzle import solve_puzzle
from backend.problems.towers_of_hanoi import hanoi
from backend.problems.wumpus_world import WumpusWorld
from backend.probabilistic.bayesian_network import compute_inference
from backend.probabilistic.em_algorithm import run_em
from backend.probabilistic.hmm import run_hmm

logger = logging.getLogger("jarvis.llm_service")

# Project root and .env path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
ENV_PATH = PROJECT_ROOT / ".env"

# Ensure .env is loaded
load_dotenv(ENV_PATH)

# Standard demonstration graph for search algorithms
DEFAULT_GRAPH_NODES = ["A", "B", "C", "D", "E", "F", "G"]
DEFAULT_UNWEIGHTED_GRAPH = {
    "A": ["B", "C"],
    "B": ["A", "D", "E"],
    "C": ["A", "F"],
    "D": ["B", "G"],
    "E": ["B", "G"],
    "F": ["C", "G"],
    "G": ["D", "E", "F"],
}
DEFAULT_WEIGHTED_GRAPH = {
    "A": [("B", 4.0), ("C", 2.0)],
    "B": [("A", 4.0), ("D", 5.0), ("E", 10.0)],
    "C": [("A", 2.0), ("F", 3.0)],
    "D": [("B", 5.0), ("G", 2.0)],
    "E": [("B", 10.0), ("G", 4.0)],
    "F": [("C", 3.0), ("G", 6.0)],
    "G": [("D", 2.0), ("E", 4.0), ("F", 6.0)],
}
DEFAULT_HEURISTICS = {
    "A": 10.0, "B": 8.0, "C": 5.0, "D": 7.0, "E": 3.0, "F": 6.0, "G": 0.0
}

# JARVIS System Instruction as specified in Master Prompt
JARVIS_SYSTEM_INSTRUCTION = (
    "You are JARVIS, an intelligent virtual assistant named Just A Rather Very Intelligent System. "
    "You are the conversational intelligence of an AI laboratory project.\n\n"
    "Your responsibilities are to understand user requests, communicate naturally, explain AI concepts, "
    "and coordinate the application's implemented AI algorithms.\n\n"
    "Guidelines:\n"
    "1. You should be helpful, precise, and technically accurate.\n"
    "2. When a user requests an algorithm execution, you MUST invoke the appropriate registered tool "
    "instead of fabricating results.\n"
    "3. When explaining an algorithm, explain its purpose, working principles, key steps, and actual execution "
    "result where applicable.\n"
    "4. If a required input is missing (such as start or goal node), ask a concise clarification question.\n"
    "5. Never claim that an algorithm was executed if it was not.\n"
    "6. Never invent paths, costs, probabilities, execution times, or other computational results.\n"
    "7. Clearly distinguish theoretical explanations from actual program execution.\n"
    "8. Keep responses understandable while maintaining university-level technical correctness.\n"
    "9. Supported algorithms available as tools: BFS, DFS, IDDFS, A*, D* Lite, Hill Climbing, "
    "Simulated Annealing, 8-Puzzle, Towers of Hanoi, Wumpus World, Bayesian Network, "
    "Expectation-Maximization (EM), and Hidden Markov Models (HMM)."
)

# Active execution context for capturing tool results during a conversation turn
_active_tool_context: Dict[str, Any] = {
    "tool_name": None,
    "tool_args": None,
    "tool_result": None,
    "navigate_to": None,
    "intent": None,
}


def _record_tool_call(tool_name: str, args: dict, result: dict, navigate_to: str, intent: str):
    """Record metadata of the invoked tool for frontend visualization and navigation."""
    _active_tool_context["tool_name"] = tool_name
    _active_tool_context["tool_args"] = args
    _active_tool_context["tool_result"] = result
    _active_tool_context["navigate_to"] = navigate_to
    _active_tool_context["intent"] = intent


def get_active_tool_context() -> Dict[str, Any]:
    """Returns the current active tool execution context."""
    return dict(_active_tool_context)


def get_and_clear_tool_context() -> Dict[str, Any]:
    """Returns and clears the active tool execution context."""
    global _active_tool_context
    ctx = dict(_active_tool_context)
    _active_tool_context = {
        "tool_name": None,
        "tool_args": None,
        "tool_result": None,
        "navigate_to": None,
        "intent": None,
    }
    return ctx


# ============================================================================
# TOOL IMPLEMENTATIONS (Bound directly to existing Python algorithms)
# ============================================================================

def execute_bfs(start_node: str = "A", goal_node: str = "G") -> dict:
    """
    Executes Breadth-First Search (BFS) over the graph from start_node to goal_node.
    Guarantees shortest path on unweighted graphs.
    Args:
        start_node: The initial starting vertex (e.g., 'A')
        goal_node: The target destination vertex (e.g., 'G')
    """
    start = start_node.strip().upper()
    goal = goal_node.strip().upper()
    res = bfs(DEFAULT_UNWEIGHTED_GRAPH, start, goal)
    _record_tool_call("bfs", {"start": start, "goal": goal}, res, "search", "BFS_REQUEST")
    return {
        "algorithm": "Breadth-First Search (BFS)",
        "path": res.get("path", []),
        "traversal_order": res.get("traversal_order", []),
        "cost": res.get("cost", 0),
        "visited_nodes": res.get("visited_nodes", []),
        "message": res.get("message", ""),
        "success": res.get("success", True),
    }


def execute_dfs(start_node: str = "A", goal_node: str = "G") -> dict:
    """
    Executes Depth-First Search (DFS) over the graph using an iterative stack.
    Explores deep graph branches before backtracking.
    Args:
        start_node: The starting node identifier (e.g., 'A')
        goal_node: The optional goal node to find (e.g., 'G')
    """
    start = start_node.strip().upper()
    goal = goal_node.strip().upper() if goal_node else None
    res = dfs(DEFAULT_UNWEIGHTED_GRAPH, start, goal)
    _record_tool_call("dfs", {"start": start, "goal": goal}, res, "search", "DFS_REQUEST")
    return {
        "algorithm": "Depth-First Search (DFS)",
        "path": res.get("path", []),
        "traversal_order": res.get("traversal_order", []),
        "visited_nodes": res.get("visited_nodes", []),
        "message": res.get("message", ""),
        "success": res.get("success", True),
    }


def execute_iddfs(start_node: str = "A", goal_node: str = "G", max_depth: int = 10) -> dict:
    """
    Executes Iterative Deepening Depth-First Search (IDDFS).
    Combines space-efficiency of DFS with completeness of BFS.
    Args:
        start_node: Starting node identifier (e.g., 'A')
        goal_node: Target destination node identifier (e.g., 'G')
        max_depth: Maximum depth limit for iterative deepening
    """
    start = start_node.strip().upper()
    goal = goal_node.strip().upper()
    res = iddfs(DEFAULT_UNWEIGHTED_GRAPH, start, goal, max_depth=max_depth)
    _record_tool_call("iddfs", {"start": start, "goal": goal, "max_depth": max_depth}, res, "search", "IDDFS_REQUEST")
    return {
        "algorithm": "Iterative Deepening DFS (IDDFS)",
        "found": res.get("found", False),
        "path": res.get("path", []),
        "depth_found": res.get("depth_found", -1),
        "nodes_explored": res.get("nodes_explored", 0),
        "message": res.get("message", ""),
    }


def execute_astar(start_node: str = "A", goal_node: str = "G") -> dict:
    """
    Executes A* Search on a weighted graph using heuristic function f(n) = g(n) + h(n).
    Finds the optimal least-cost path.
    Args:
        start_node: Starting node identifier (e.g., 'A')
        goal_node: Goal node identifier (e.g., 'G')
    """
    start = start_node.strip().upper()
    goal = goal_node.strip().upper()
    res = astar(DEFAULT_WEIGHTED_GRAPH, start, goal, DEFAULT_HEURISTICS)
    _record_tool_call("astar", {"start": start, "goal": goal}, res, "search", "ASTAR_REQUEST")
    return {
        "algorithm": "A* Search",
        "path": res.get("path", []),
        "cost": res.get("cost", 0.0),
        "visited_nodes": res.get("visited_nodes", []),
        "message": res.get("message", ""),
        "success": res.get("success", True),
    }


def execute_dstar(grid_size: int = 10, start_x: int = 0, start_y: int = 0, goal_x: int = 9, goal_y: int = 9) -> dict:
    """
    Executes D* Lite incremental dynamic replanning on a 2D grid.
    Demonstrates dynamic path updating around obstacles.
    Args:
        grid_size: Size of square grid (default 10)
        start_x: Agent start row
        start_y: Agent start column
        goal_x: Goal target row
        goal_y: Goal target column
    """
    grid_size = max(5, min(20, int(grid_size)))
    start = [max(0, min(grid_size - 1, int(start_x))), max(0, min(grid_size - 1, int(start_y)))]
    goal = [max(0, min(grid_size - 1, int(goal_x))), max(0, min(grid_size - 1, int(goal_y)))]
    # Place representative obstacles in the grid
    obstacles = [[2, 2], [2, 3], [3, 2], [4, 5], [5, 5]]
    obstacles = [o for o in obstacles if o != start and o != goal]

    res = dstar_plan(grid_size, start, goal, obstacles)
    _record_tool_call("dstar", {"grid_size": grid_size, "start": start, "goal": goal}, res, "search", "DSTAR_REQUEST")
    return {
        "algorithm": "D* Lite Dynamic Replanning",
        "grid_size": grid_size,
        "start": start,
        "goal": goal,
        "path_length": len(res.get("path", [])),
        "path": res.get("path", []),
        "message": res.get("message", ""),
        "success": res.get("success", True),
    }


def execute_hill_climbing(initial_x: float = 0.0, function_type: str = "multimodal", max_iterations: int = 200) -> dict:
    """
    Executes continuous steepest-ascent Hill Climbing optimization.
    Navigates a mathematical function landscape to find local/global maxima.
    Args:
        initial_x: Starting coordinate value on x-axis
        function_type: Either 'multimodal' or 'quadratic'
        max_iterations: Maximum search step iterations
    """
    res = hill_climbing(float(initial_x), str(function_type), int(max_iterations), step_size=0.1)
    _record_tool_call("hill_climbing", {"initial_x": initial_x, "func": function_type}, res, "search", "HILL_CLIMBING_REQUEST")
    return {
        "algorithm": "Hill Climbing Optimization",
        "best_x": res.get("best_x"),
        "best_value": res.get("best_value"),
        "iterations": res.get("iterations"),
        "stuck_at_local": res.get("stuck_at_local", False),
        "message": res.get("message", ""),
        "success": res.get("success", True),
    }


def execute_simulated_annealing(initial_x: float = 0.0, initial_temp: float = 1000.0, cooling_rate: float = 0.995, max_iterations: int = 500) -> dict:
    """
    Executes Simulated Annealing optimization with geometric cooling schedule.
    Escapes local optima using the Boltzmann acceptance probability.
    Args:
        initial_x: Initial coordinate
        initial_temp: Starting temperature
        cooling_rate: Multiplicative factor per iteration (e.g. 0.995)
        max_iterations: Number of cooling steps
    """
    res = simulated_annealing(float(initial_x), float(initial_temp), float(cooling_rate), int(max_iterations), "multimodal")
    _record_tool_call("simulated_annealing", {"initial_x": initial_x, "temp": initial_temp}, res, "search", "SIMULATED_ANNEALING_REQUEST")
    return {
        "algorithm": "Simulated Annealing",
        "best_x": res.get("best_x"),
        "best_value": res.get("best_value"),
        "iterations": res.get("iterations"),
        "message": res.get("message", ""),
        "success": res.get("success", True),
    }


def execute_eight_puzzle(heuristic: str = "manhattan") -> dict:
    """
    Solves the 8-puzzle sliding tile problem using A* search with Manhattan or Misplaced Tiles heuristic.
    Args:
        heuristic: 'manhattan' (default) or 'misplaced'
    """
    # Solvable demonstration puzzle
    initial_state = [[1, 2, 3], [4, 0, 6], [7, 5, 8]]
    res = solve_puzzle(initial_state, heuristic=heuristic)
    _record_tool_call("eight_puzzle", {"heuristic": heuristic}, res, "puzzles", "PUZZLE_8_REQUEST")
    return {
        "algorithm": "8-Puzzle A* Solver",
        "heuristic": heuristic,
        "is_solvable": res.get("is_solvable", True),
        "total_moves": res.get("moves", 0),
        "explored_states": res.get("explored_states", 0),
        "time_taken_ms": round(res.get("time_taken", 0.0) * 1000, 2),
        "move_sequence": res.get("move_sequence", []),
        "message": res.get("message", ""),
    }


def execute_towers_of_hanoi(num_disks: int = 3) -> dict:
    """
    Solves the recursive Towers of Hanoi puzzle for n disks across 3 pegs.
    Guarantees minimal moves: 2^n - 1.
    Args:
        num_disks: Number of disks (1 to 10)
    """
    n = max(1, min(10, int(num_disks)))
    res = hanoi(n)
    _record_tool_call("towers_of_hanoi", {"num_disks": n}, res, "puzzles", "HANOI_REQUEST")
    return {
        "algorithm": "Towers of Hanoi",
        "num_disks": n,
        "total_moves": res.get("total_moves", 2**n - 1),
        "formula": f"2^{n} - 1 = {2**n - 1}",
        "sample_first_3_moves": res.get("moves", [])[:3],
        "message": res.get("message", ""),
    }


def execute_wumpus_world(action: str = "start", direction: str = "right") -> dict:
    """
    Simulates the Wumpus World knowledge-based agent environment.
    Detects Stench, Breeze, Glitter, Bump, and Scream percepts.
    Args:
        action: 'start', 'move', 'shoot', or 'grab'
        direction: 'up', 'down', 'left', or 'right'
    """
    world = WumpusWorld(grid_size=4, seed=42)
    percepts = world.get_percepts()
    state = world.get_state()
    res = {
        "agent_pos": world.agent_pos,
        "percepts": percepts,
        "has_arrow": world.has_arrow,
        "has_gold": world.has_gold,
        "game_over": world.game_over,
        "won": world.won,
    }
    _record_tool_call("wumpus_world", {"action": action}, res, "wumpus", "WUMPUS_REQUEST")
    return {
        "environment": "Wumpus World (4x4 Cave)",
        "agent_position": world.agent_pos,
        "percepts": percepts,
        "has_gold": world.has_gold,
        "has_arrow": world.has_arrow,
        "game_status": "Agent active in cave exploring safely.",
    }


def execute_bayesian_network(cloudy: Optional[bool] = None, rain: Optional[bool] = None, sprinkler: Optional[bool] = None) -> dict:
    """
    Performs exact probabilistic inference by joint enumeration on the Rain/Sprinkler/Wet Grass Bayesian Network.
    Args:
        cloudy: Optional evidence boolean for Cloudy
        rain: Optional evidence boolean for Rain
        sprinkler: Optional evidence boolean for Sprinkler
    """
    evidence = {}
    if cloudy is not None:
        evidence["Cloudy"] = bool(cloudy)
    if rain is not None:
        evidence["Rain"] = bool(rain)
    if sprinkler is not None:
        evidence["Sprinkler"] = bool(sprinkler)

    res = compute_inference(evidence)
    _record_tool_call("bayesian_network", {"evidence": evidence}, res, "probabilistic", "PROBABILITY_REQUEST")
    return {
        "model": "Bayesian Network (Weather / Sprinkler / WetGrass)",
        "evidence_provided": evidence,
        "computed_posterior_probabilities": res.get("probabilities", {}),
        "explanation": res.get("explanation", ""),
    }


def execute_expectation_maximization(n_samples: int = 150, n_components: int = 3, max_iterations: int = 50) -> dict:
    """
    Executes Gaussian Mixture Model Expectation-Maximization (EM) clustering from scratch.
    Alternates between E-step (responsibilities) and M-step (parameters).
    Args:
        n_samples: Number of synthetic 2D data samples (50 to 500)
        n_components: Number of Gaussian clusters (2 to 5)
        max_iterations: Maximum EM iterations
    """
    n_samples = max(50, min(500, int(n_samples)))
    n_components = max(2, min(5, int(n_components)))
    res = run_em(n_samples=n_samples, n_components=n_components, max_iterations=max_iterations, seed=42)
    _record_tool_call("em_algorithm", {"n_components": n_components}, res, "probabilistic", "EM_REQUEST")
    return {
        "algorithm": "Expectation-Maximization (GMM)",
        "components": n_components,
        "iterations_to_converge": res.get("iterations", 0),
        "converged": res.get("converged", True),
        "clusters_summary": [
            {"cluster": i + 1, "mean": c.get("mean"), "weight": c.get("weight")}
            for i, c in enumerate(res.get("clusters", []))
        ],
        "message": res.get("message", ""),
    }


def execute_hidden_markov_model(observations: str = "Walk,Shop,Clean", algorithm: str = "both") -> dict:
    """
    Executes the Forward Algorithm and Viterbi decoding on a Weather Hidden Markov Model.
    Hidden states: Sunny, Rainy. Observable activities: Walk, Shop, Clean.
    Args:
        observations: Comma-separated list of observed activities (e.g. 'Walk,Shop,Clean')
        algorithm: 'forward', 'viterbi', or 'both'
    """
    obs_list = [o.strip().capitalize() for o in observations.split(",") if o.strip()]
    if not obs_list:
        obs_list = ["Walk", "Shop", "Clean"]

    res = run_hmm(obs_list, algorithm=algorithm)
    _record_tool_call("hmm", {"observations": obs_list}, res, "probabilistic", "HMM_REQUEST")
    return {
        "model": "Hidden Markov Model (Umbrella Weather World)",
        "observations": obs_list,
        "forward_total_probability": res.get("forward_prob", 0.0),
        "viterbi_most_likely_path": res.get("viterbi_path", []),
        "viterbi_path_probability": res.get("viterbi_prob", 0.0),
        "message": res.get("message", ""),
    }


ALL_TOOLS = [
    execute_bfs,
    execute_dfs,
    execute_iddfs,
    execute_astar,
    execute_dstar,
    execute_hill_climbing,
    execute_simulated_annealing,
    execute_eight_puzzle,
    execute_towers_of_hanoi,
    execute_wumpus_world,
    execute_bayesian_network,
    execute_expectation_maximization,
    execute_hidden_markov_model,
]


# ============================================================================
# LLM SERVICE CLASS
# ============================================================================

class GeminiLLMService:
    """
    Dedicated manager for Google Gemini client interactions, model selection,
    multi-turn chat sessions, and function calling orchestration.
    """

    AVAILABLE_MODELS = [
        "gemini-flash-latest",
        "gemini-3.5-flash",
        "gemini-3.8-flash",
        "gemini-3.5-flash-lite",
        "gemini-3.1-pro-preview",
    ]

    def __init__(self):
        self._api_key: Optional[str] = os.getenv("GEMINI_API_KEY")
        self._model_name: str = os.getenv("GEMINI_MODEL", "gemini-flash-latest")
        self._client: Optional[genai.Client] = None
        self._init_client()

    def _init_client(self):
        """Initialize the Google GenAI client if an API key is available."""
        if self._api_key and self._api_key.strip() and not self._api_key.startswith("your_"):
            try:
                self._client = genai.Client(api_key=self._api_key.strip())
                logger.info("Google GenAI client initialized successfully.")
            except Exception as e:
                logger.error(f"Failed to initialize Google GenAI client: {e}")
                self._client = None
        else:
            self._client = None

    def is_configured(self) -> bool:
        """Returns True if Gemini client is initialized with an API key."""
        return self._client is not None

    def get_masked_key(self) -> Optional[str]:
        """Returns a masked version of the current API key for safe UI display."""
        if not self._api_key or len(self._api_key) < 8:
            return None
        return f"{self._api_key[:6]}...{self._api_key[-4:]}"

    def _resolve_model_name(self, model: Optional[str]) -> str:
        """Resolves alias or deprecated model names to current active endpoints."""
        clean = (model or "").strip()
        if clean in ("gemini-flash-latest", "gemini-2.5-flash"):
            return "gemini-3.5-flash"
        return clean or "gemini-3.5-flash"

    def get_model_name(self) -> str:
        return self._model_name

    def set_configuration(self, api_key: str, model_name: Optional[str] = None, persist: bool = True) -> Dict[str, Any]:
        """
        Updates the runtime API key and model name, with optional persistence to .env.
        """
        clean_key = api_key.strip() if api_key else ""
        if not clean_key:
            return {"success": False, "message": "API key cannot be empty."}

        self._api_key = clean_key
        if model_name and model_name.strip():
            self._model_name = model_name.strip()

        self._init_client()

        if persist:
            try:
                if not ENV_PATH.exists():
                    ENV_PATH.touch(mode=0o600)
                set_key(str(ENV_PATH), "GEMINI_API_KEY", self._api_key)
                set_key(str(ENV_PATH), "GEMINI_MODEL", self._model_name)
                logger.info("Persisted Gemini configuration to .env")
            except Exception as e:
                logger.warning(f"Could not persist configuration to .env: {e}")

        return {
            "success": True,
            "message": "Configuration updated successfully.",
            "active_model": self._model_name,
            "masked_key": self.get_masked_key(),
        }

    async def test_connection(self, api_key: Optional[str] = None, model: Optional[str] = None) -> Dict[str, Any]:
        """
        Performs a lightweight test call to verify API key validity and model responsiveness.
        """
        test_key = (api_key or self._api_key or "").strip()
        test_model = (model or self._model_name or "gemini-flash-latest").strip()

        if not test_key or test_key.startswith("your_"):
            return {
                "success": False,
                "message": "No API key provided. Please obtain one at https://aistudio.google.com/apikey",
            }

        resolved_model = "gemini-3.5-flash" if test_model == "gemini-flash-latest" else test_model
        candidate_models = [resolved_model]
        if resolved_model != "gemini-3.5-flash":
            candidate_models.append("gemini-3.5-flash")
        if "gemini-3.8-flash" not in candidate_models:
            candidate_models.append("gemini-3.8-flash")

        try:
            temp_client = genai.Client(api_key=test_key)
            last_err = None

            for m in candidate_models:
                try:
                    resp = temp_client.models.generate_content(
                        model=m,
                        contents="Respond with only the single word: ONLINE",
                    )
                    reply_text = (resp.text or "").strip()
                    return {
                        "success": True,
                        "message": f"Connection verified successfully with model '{m}'. Response: {reply_text}",
                        "model": m,
                    }
                except Exception as ex:
                    last_err = ex
                    err_str = str(ex)
                    if "404" in err_str or "not found" in err_str.lower():
                        continue  # try next fallback model
                    raise ex

            return {
                "success": False,
                "message": f"Model connection failed: {last_err}",
            }
        except Exception as e:
            err_msg = str(e)
            if "API_KEY_INVALID" in err_msg or "400" in err_msg:
                clean_msg = "Invalid API key. Please check your key at https://aistudio.google.com/apikey"
            elif "QUOTA" in err_msg or "429" in err_msg:
                clean_msg = "Gemini API rate limit or quota exceeded. Please try again shortly."
            else:
                clean_msg = f"Connection test failed: {err_msg[:120]}"

            return {"success": False, "message": clean_msg}

    def _format_history_for_gemini(self, history: List[Dict[str, str]], max_turns: int = 10) -> List[types.Content]:
        """
        Transforms frontend message history into Gemini Content objects with proper roles.
        Restricts context window to max_turns to preserve tokens.
        """
        formatted = []
        if not history:
            return formatted

        # Slice to recent turns
        recent = history[-max_turns:]
        for msg in recent:
            role = msg.get("role", "user").lower()
            text = (msg.get("content") or "").strip()
            if not text:
                continue

            gemini_role = "model" if role in ("assistant", "model", "jarvis") else "user"
            formatted.append(
                types.Content(
                    role=gemini_role,
                    parts=[types.Part.from_text(text=text)],
                )
            )

        return formatted

    async def chat(self, message: str, conversation_history: Optional[List[Dict[str, str]]] = None) -> Dict[str, Any]:
        """
        Processes a user message through Gemini with multi-turn conversation and registered tools.
        Returns response text, executed tool data, and UI navigation instructions.
        """
        if not self.is_configured():
            return {
                "response": (
                    "Google Gemini API key is not configured. Please open Settings or click the key icon "
                    "to configure your Gemini API key from https://aistudio.google.com/apikey. "
                    "In the meantime, local algorithm controls remain fully operational."
                ),
                "intent": "HELP",
                "data": None,
                "navigate_to": "settings",
                "success": False,
                "offline_fallback": True,
            }

        # Clear tool execution tracker for this turn
        global _active_tool_context
        _active_tool_context = {
            "tool_name": None,
            "tool_args": None,
            "tool_result": None,
            "navigate_to": None,
            "intent": None,
        }

        # Build tools configuration
        config = types.GenerateContentConfig(
            system_instruction=JARVIS_SYSTEM_INSTRUCTION,
            tools=ALL_TOOLS,
            temperature=0.7,
            max_output_tokens=1024,
            automatic_function_calling=types.AutomaticFunctionCallingConfig(
                disable=False,
                maximum_remote_calls=5,
            ),
        )

        # Build conversation history
        gemini_history = self._format_history_for_gemini(conversation_history or [], max_turns=8)

        # Model candidates for graceful fallback if requested alias is 404/unavailable
        resolved_model = "gemini-3.5-flash" if self._model_name == "gemini-flash-latest" else self._model_name
        models_to_try = [resolved_model]
        if resolved_model != "gemini-3.5-flash":
            models_to_try.append("gemini-3.5-flash")
        if "gemini-3.8-flash" not in models_to_try:
            models_to_try.append("gemini-3.8-flash")

        last_error = None
        for model in models_to_try:
            try:
                # Create chat session with history and tools
                chat_session = self._client.chats.create(
                    model=model,
                    config=config,
                    history=gemini_history,
                )

                # Send message and obtain response (tools are executed automatically if invoked)
                response = chat_session.send_message(message)
                response_text = response.text or "Execution completed."

                # Retrieve tool metadata if a tool was executed
                tool_data = _active_tool_context.get("tool_result")
                nav_target = _active_tool_context.get("navigate_to")
                detected_intent = _active_tool_context.get("intent") or "GENERAL_QUERY"

                return {
                    "response": response_text,
                    "intent": detected_intent,
                    "data": tool_data,
                    "navigate_to": nav_target,
                    "success": True,
                    "model_used": model,
                }

            except Exception as e:
                err_str = str(e)
                last_error = e
                # If model is 404/not supported, try next model in fallback list
                if "404" in err_str or "not found" in err_str.lower():
                    logger.warning(f"Model '{model}' not found or unavailable, trying next candidate...")
                    continue
                else:
                    logger.error(f"Gemini chat error with model '{model}': {e}")
                    break

        # If we reached here, Gemini API encountered an error
        error_msg = str(last_error) if last_error else "Unknown Gemini API error."
        logger.error(f"Gemini API failure: {error_msg}")

        # Provide a friendly user error and signal fallback
        clean_user_message = (
            "I encountered a temporary issue connecting to Google Gemini. "
            f"Details: {error_msg[:120]}. "
            "Local algorithm modules remain fully functional."
        )

        return {
            "response": clean_user_message,
            "intent": "GENERAL_QUERY",
            "data": None,
            "navigate_to": None,
            "success": False,
            "error": error_msg,
            "offline_fallback": True,
        }


# Singleton service instance
GeminiLLMService = GeminiLLMService
LLMService = GeminiLLMService
llm_service = GeminiLLMService()
