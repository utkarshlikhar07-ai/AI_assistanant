"""
JARVIS AI - Response Engine
Generates contextual, personality-rich responses for all intents.
"""
from backend.core.intent_recognition import (
    GREETING, GENERAL_QUERY, CALCULATION, EXPLAIN_ALGORITHM,
    BFS_REQUEST, DFS_REQUEST, IDDFS_REQUEST, ASTAR_REQUEST, DSTAR_REQUEST,
    PUZZLE_8_REQUEST, WUMPUS_REQUEST, HANOI_REQUEST, PROBABILITY_REQUEST,
    HMM_REQUEST, OPTIMIZATION_REQUEST, HILL_CLIMBING_REQUEST,
    SIMULATED_ANNEALING_REQUEST, EM_REQUEST, HELP,
)

# ─── Algorithm Explanations ──────────────────────────────────────────────────

ALGORITHM_EXPLANATIONS: dict[str, str] = {
    "BFS": (
        "Breadth-First Search (BFS) explores a graph level by level, visiting all "
        "neighbours of the current node before moving deeper. It is guaranteed to find "
        "the shortest path in an unweighted graph. Time complexity: O(V + E). "
        "Space complexity: O(V) for the queue."
    ),
    "DFS": (
        "Depth-First Search (DFS) dives as deep as possible along each branch before "
        "backtracking. It uses a stack (or recursion) and is useful for cycle detection, "
        "topological sort, and connectivity checks. Time complexity: O(V + E). "
        "It does not guarantee the shortest path."
    ),
    "IDDFS": (
        "Iterative Deepening Depth-First Search (IDDFS) combines the memory efficiency "
        "of DFS with the completeness of BFS. It runs DFS repeatedly with increasing "
        "depth limits until the goal is found. It is optimal for unweighted graphs and "
        "uses O(d) space, where d is the solution depth."
    ),
    "A*": (
        "A* Search uses a heuristic function h(n) to guide the search towards the goal "
        "efficiently. It evaluates nodes via f(n) = g(n) + h(n), where g(n) is the "
        "cost from start and h(n) is the estimated cost to goal. With an admissible "
        "heuristic it is both complete and optimal."
    ),
    "D*": (
        "D* (Dynamic A*) is an incremental heuristic search algorithm designed for "
        "dynamic environments. D* Lite, the most common variant, efficiently replans "
        "when new obstacles are discovered, making it ideal for robot navigation in "
        "partially known environments."
    ),
    "HillClimbing": (
        "Hill Climbing is a local search algorithm that continuously moves towards "
        "states with higher objective values. It is fast and memory-efficient but "
        "can get trapped in local optima, plateaus, or ridges. Variants like "
        "random-restart hill climbing mitigate these issues."
    ),
    "SimulatedAnnealing": (
        "Simulated Annealing (SA) is a probabilistic optimisation technique inspired "
        "by annealing in metallurgy. It occasionally accepts worse solutions with a "
        "probability that decreases over time (the 'temperature'). This allows SA to "
        "escape local optima and converge to near-global solutions."
    ),
    "Bayesian": (
        "A Bayesian Network is a probabilistic graphical model representing variables "
        "and their conditional dependencies via a directed acyclic graph. It applies "
        "Bayes' theorem to compute posterior probabilities given evidence, making it "
        "powerful for reasoning under uncertainty."
    ),
    "HMM": (
        "A Hidden Markov Model (HMM) models systems assumed to be a Markov process "
        "with unobservable (hidden) states. Key algorithms: Forward Algorithm "
        "(compute observation probability), Viterbi Algorithm (decode the most likely "
        "state sequence), and Baum-Welch (learn model parameters)."
    ),
    "EM": (
        "The Expectation-Maximisation (EM) algorithm iteratively estimates parameters "
        "of statistical models with latent variables. The E-step computes expected "
        "log-likelihood; the M-step maximises it. It is widely used for Gaussian "
        "Mixture Models and other clustering tasks."
    ),
}

# ─── Response Templates ──────────────────────────────────────────────────────

def _fmt_data_hint(data: dict | None) -> str:
    if not data:
        return ""
    return " I have included the computed data in the response payload."


def generate_response(intent: str, entities: dict, data: dict | None = None) -> str:
    """
    Generate a JARVIS-style response for the given intent, entities, and optional data.

    Parameters
    ----------
    intent : str
        One of the intent constants from intent_recognition.
    entities : dict
        Extracted entities (numbers, nodes, algorithms, raw_text).
    data : dict | None
        Optional computed result data to reference in the response.

    Returns
    -------
    str
        A professional, helpful, slightly formal JARVIS response.
    """
    mentioned_algos: list[str] = entities.get("algorithms", [])
    numbers: list[float] = entities.get("numbers", [])
    nodes: list[str] = entities.get("nodes", [])
    raw_text: str = entities.get("raw_text", "")
    data_hint = _fmt_data_hint(data)

    # ── Greeting ──────────────────────────────────────────────────────────────
    if intent == GREETING:
        return (
            "Good day. I am JARVIS — Just A Rather Very Intelligent System. "
            "I specialise in AI algorithms, graph search, probabilistic reasoning, "
            "and interactive puzzles. How may I assist you today?"
        )

    # ── Help ──────────────────────────────────────────────────────────────────
    if intent == HELP:
        return (
            "Certainly. Here is what I am capable of:\n\n"
            "**Graph Search Algorithms**\n"
            "- BFS (Breadth-First Search)\n"
            "- DFS (Depth-First Search)\n"
            "- IDDFS (Iterative Deepening DFS)\n"
            "- A* Search\n"
            "- D* (Dynamic A*)\n\n"
            "**Optimisation**\n"
            "- Hill Climbing\n"
            "- Simulated Annealing\n\n"
            "**Classic AI Puzzles**\n"
            "- 8-Puzzle (Sliding Tile)\n"
            "- Tower of Hanoi\n"
            "- Wumpus World\n\n"
            "**Probabilistic Reasoning**\n"
            "- Bayesian Networks\n"
            "- Hidden Markov Models (HMM)\n"
            "- Expectation-Maximisation (EM)\n\n"
            "Simply ask me to run, explain, or demonstrate any of the above. "
            "I shall navigate you to the appropriate interface automatically."
        )

    # ── BFS ───────────────────────────────────────────────────────────────────
    if intent == BFS_REQUEST:
        node_hint = f" involving nodes {', '.join(nodes)}" if nodes else ""
        result_hint = (
            f" The search completed successfully.{data_hint}"
            if data and data.get("success") else data_hint
        )
        return (
            f"Initiating Breadth-First Search{node_hint}. "
            "BFS explores all neighbours at the present depth prior to moving on "
            "to nodes at the next depth level, guaranteeing the shortest path in "
            f"unweighted graphs.{result_hint} "
            "Navigating you to the Search Algorithms interface."
        )

    # ── DFS ───────────────────────────────────────────────────────────────────
    if intent == DFS_REQUEST:
        node_hint = f" for nodes {', '.join(nodes)}" if nodes else ""
        return (
            f"Running Depth-First Search{node_hint}. "
            "DFS traverses as far as possible along each branch before backtracking, "
            "making it effective for exploring all reachable nodes and detecting cycles."
            f"{data_hint} Navigating you to the Search Algorithms interface."
        )

    # ── IDDFS ─────────────────────────────────────────────────────────────────
    if intent == IDDFS_REQUEST:
        return (
            "Executing Iterative Deepening Depth-First Search. "
            "IDDFS combines the space efficiency of DFS with the completeness "
            "and optimality guarantees of BFS by progressively increasing the "
            f"depth limit.{data_hint} "
            "Navigating you to the Search Algorithms interface."
        )

    # ── A* ────────────────────────────────────────────────────────────────────
    if intent == ASTAR_REQUEST:
        return (
            "Engaging A* Search. "
            "A* uses an admissible heuristic function to guide the frontier, "
            "balancing the actual cost g(n) and the estimated cost to goal h(n) "
            f"via f(n) = g(n) + h(n).{data_hint} "
            "Navigating you to the Search Algorithms interface."
        )

    # ── D* ────────────────────────────────────────────────────────────────────
    if intent == DSTAR_REQUEST:
        return (
            "Activating D* (Dynamic A*) Search. "
            "D* Lite is designed for dynamic environments where obstacles may appear "
            "or disappear, triggering efficient incremental replanning without "
            f"restarting from scratch.{data_hint} "
            "Navigating you to the Search Algorithms interface."
        )

    # ── 8-Puzzle ──────────────────────────────────────────────────────────────
    if intent == PUZZLE_8_REQUEST:
        return (
            "Loading the 8-Puzzle Solver. "
            "The sliding-tile puzzle will be solved using A* Search with either "
            "the Manhattan distance or misplaced-tiles heuristic. "
            "I will verify solvability before attempting a solution."
            f"{data_hint} Navigating you to the Puzzles interface."
        )

    # ── Wumpus World ──────────────────────────────────────────────────────────
    if intent == WUMPUS_REQUEST:
        return (
            "Entering the Wumpus World. "
            "The agent will navigate a cave using logical inference to avoid Pits "
            "and the Wumpus while seeking the Gold. Percepts include Breeze, Stench, "
            f"Glitter, Bump, and Scream.{data_hint} "
            "Navigating you to the Wumpus World interface."
        )

    # ── Tower of Hanoi ────────────────────────────────────────────────────────
    if intent == HANOI_REQUEST:
        disks = int(numbers[0]) if numbers else 3
        moves = 2 ** disks - 1
        return (
            f"Computing Tower of Hanoi solution for {disks} disk(s). "
            f"The optimal solution requires exactly {moves} move(s), "
            "following the recursive strategy of moving the top n−1 disks to an "
            "auxiliary peg, moving the largest disk, then reconstructing."
            f"{data_hint} Navigating you to the Puzzles interface."
        )

    # ── Hill Climbing ─────────────────────────────────────────────────────────
    if intent == HILL_CLIMBING_REQUEST:
        return (
            "Running Hill Climbing optimisation. "
            "The algorithm will iteratively move to neighbouring states with higher "
            "objective values. Note that it may converge to a local optimum — "
            "random restarts can help overcome this limitation."
            f"{data_hint} Navigating you to the Optimisation interface."
        )

    # ── Simulated Annealing ───────────────────────────────────────────────────
    if intent == SIMULATED_ANNEALING_REQUEST:
        return (
            "Initiating Simulated Annealing. "
            "The algorithm starts at high temperature, allowing uphill moves to escape "
            "local optima. As the temperature cools according to the cooling schedule, "
            "the search converges towards the global optimum."
            f"{data_hint} Navigating you to the Optimisation interface."
        )

    # ── Generic Optimisation ──────────────────────────────────────────────────
    if intent == OPTIMIZATION_REQUEST:
        return (
            "I can assist with optimisation tasks. "
            "JARVIS supports Hill Climbing and Simulated Annealing. "
            "Hill Climbing is fast but can get stuck in local optima; "
            "Simulated Annealing uses a probabilistic acceptance criterion to "
            "escape them. Which method would you prefer?"
            f"{data_hint}"
        )

    # ── Bayesian Network ──────────────────────────────────────────────────────
    if intent == PROBABILITY_REQUEST:
        return (
            "Engaging Bayesian reasoning engine. "
            "I will compute posterior probabilities using the pre-configured "
            "Bayesian network. Provide evidence variables and I will update "
            "the belief state accordingly using Bayes' theorem."
            f"{data_hint} Navigating you to the Probabilistic Reasoning interface."
        )

    # ── HMM ───────────────────────────────────────────────────────────────────
    if intent == HMM_REQUEST:
        return (
            "Loading the Hidden Markov Model module. "
            "I will apply the Forward Algorithm to compute the observation sequence "
            "probability, and the Viterbi Algorithm to decode the most likely hidden "
            f"state sequence.{data_hint} "
            "Navigating you to the Probabilistic Reasoning interface."
        )

    # ── EM Algorithm ──────────────────────────────────────────────────────────
    if intent == EM_REQUEST:
        return (
            "Starting Expectation-Maximisation clustering. "
            "The EM algorithm will iteratively fit a Gaussian Mixture Model to the "
            "generated data, converging when the log-likelihood improvement falls "
            f"below the threshold.{data_hint} "
            "Navigating you to the Probabilistic Reasoning interface."
        )

    # ── Explain Algorithm ─────────────────────────────────────────────────────
    if intent == EXPLAIN_ALGORITHM:
        if mentioned_algos:
            algo = mentioned_algos[0]
            explanation = ALGORITHM_EXPLANATIONS.get(algo)
            if explanation:
                return f"**{algo}** — {explanation}"
        return (
            "I can explain any of the following algorithms: "
            + ", ".join(ALGORITHM_EXPLANATIONS.keys())
            + ". Which one interests you?"
        )

    # ── Calculation ───────────────────────────────────────────────────────────
    if intent == CALCULATION:
        if numbers:
            return (
                f"I can see you are working with the number(s): {', '.join(str(n) for n in numbers)}. "
                "For graph algorithms I can compute shortest paths, traversal orders, and costs. "
                "For optimisation I can find function maxima or minima. "
                "Could you clarify what calculation you would like me to perform?"
            )
        return (
            "I am ready to perform computations. Please specify the algorithm or "
            "problem you would like me to solve, along with any relevant parameters."
        )

    # ── General / Fallback ────────────────────────────────────────────────────
    return (
        "I am JARVIS, your AI assistant specialising in algorithms and intelligent systems. "
        "I did not quite catch your specific request — could you elaborate? "
        "You might ask me to run BFS, A*, solve an 8-Puzzle, play Wumpus World, "
        "or analyse a Bayesian network, among many other capabilities. "
        "Type 'help' for a full list of what I can do."
    )
