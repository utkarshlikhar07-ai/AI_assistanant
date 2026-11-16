from typing import Optional


def iddfs(graph: dict, start: str, goal: str, max_depth: int = 10) -> dict:
    """
    Iterative Deepening Depth-First Search.

    For each depth limit d (0 … max_depth) it runs a depth-limited DFS.
    Stops as soon as the goal is found or all depths are exhausted.

    Returns
    -------
    dict:
        found          : bool
        path           : list[str]
        depth_found    : int          (-1 if not found)
        iterations     : list[dict]   per-depth: {depth, nodes_explored, nodes_visited, cutoff}
        nodes_explored : int          total across all iterations
        message        : str
    """
    if not graph:
        return _empty_result("Graph is empty.", goal)

    if start not in graph:
        return _empty_result(f"Start node '{start}' not found in graph.", goal)

    if goal not in graph:
        return _empty_result(f"Goal node '{goal}' not found in graph.", goal)

    iterations: list[dict] = []
    total_explored = 0

    for depth_limit in range(max_depth + 1):
        result, path, explored, visited_set = _depth_limited_dfs(
            graph, start, goal, depth_limit
        )
        total_explored += explored

        iterations.append({
            "depth":          depth_limit,
            "nodes_explored": explored,
            "nodes_visited":  sorted(visited_set),
            "cutoff":         result == "cutoff",
        })

        if result == "found":
            return {
                "found":          True,
                "path":           path,
                "depth_found":    depth_limit,
                "iterations":     iterations,
                "nodes_explored": total_explored,
                "message": (
                    f"Goal '{goal}' found at depth {depth_limit} "
                    f"after exploring {total_explored} node(s) total."
                ),
            }

        if result == "not_found":
            # The search space is fully explored (no cutoff) – pointless to go deeper
            break

    return {
        "found":          False,
        "path":           [],
        "depth_found":    -1,
        "iterations":     iterations,
        "nodes_explored": total_explored,
        "message": (
            f"Goal '{goal}' not found within depth limit {max_depth}. "
            f"Total nodes explored: {total_explored}."
        ),
    }


# ── depth-limited DFS (recursive via explicit call stack) ─────────────────────

def _depth_limited_dfs(
    graph: dict,
    start: str,
    goal:  str,
    limit: int,
) -> tuple[str, list[str], int, set]:
    """
    Returns (result, path, nodes_explored, visited_set).
    result: 'found' | 'cutoff' | 'not_found'
    """
    # Iterative implementation using an explicit stack:
    # Each frame: (node, parent_map_snapshot, depth)
    # We track path via parent dict built incrementally.

    # Stack: (node, depth, parent)
    stack: list[tuple[str, int, Optional[str]]] = [(start, 0, None)]
    parent:  dict[str, Optional[str]] = {}
    visited_set: set[str] = set()
    nodes_explored = 0
    cutoff_occurred = False

    # We may revisit nodes at different depths (IDDFS characteristic),
    # so we do NOT mark visited globally – only within a single path to avoid cycles.
    # We use a path-set per branch; simulate with DFS + depth tracking.

    # For true IDDFS path-awareness we keep a "current path" approach.
    # Reformulate: recursive-style via explicit call stack with backtracking info.

    result, path = _dls_recursive(graph, start, goal, limit, set())
    # Count every node touched (including re-expansions)
    nodes_explored, visited_set = _count_dls(graph, start, goal, limit)

    return result, path, nodes_explored, visited_set


def _dls_recursive(
    graph: dict,
    node:  str,
    goal:  str,
    limit: int,
    path_set: set,
) -> tuple[str, list[str]]:
    """
    Recursive depth-limited DFS.
    Returns ('found', path) | ('cutoff', []) | ('not_found', [])
    """
    if node == goal:
        return "found", [node]

    if limit == 0:
        return "cutoff", []

    cutoff_occurred = False
    neighbors = graph.get(node, [])

    for neighbor in neighbors:
        if neighbor in path_set:   # avoid cycles within current path
            continue
        path_set.add(neighbor)
        result, sub_path = _dls_recursive(graph, neighbor, goal, limit - 1, path_set)
        path_set.discard(neighbor)

        if result == "found":
            return "found", [node] + sub_path
        if result == "cutoff":
            cutoff_occurred = True

    return ("cutoff" if cutoff_occurred else "not_found"), []


def _count_dls(
    graph: dict,
    start: str,
    goal:  str,
    limit: int,
) -> tuple[int, set]:
    """Walk the same DLS tree and count every node expansion."""
    count = 0
    visited: set[str] = set()

    # Iterative: (node, depth, path_set)
    stack = [(start, 0, frozenset())]
    while stack:
        node, depth, path_set = stack.pop()
        count += 1
        visited.add(node)

        if node == goal:
            continue
        if depth == limit:
            continue

        for neighbor in graph.get(node, []):
            if neighbor not in path_set:
                stack.append((neighbor, depth + 1, path_set | {neighbor}))

    return count, visited


def _empty_result(message: str, goal: str) -> dict:
    return {
        "found":          False,
        "path":           [],
        "depth_found":    -1,
        "iterations":     [],
        "nodes_explored": 0,
        "message":        message,
    }
