from typing import Optional


def dfs(graph: dict, start: str, goal: Optional[str] = None) -> dict:
    """
    Iterative Depth-First Search traversal / pathfinding.

    Parameters
    ----------
    graph : dict
        Adjacency list  {node: [neighbor, ...]}
    start : str
        Starting node.
    goal : str | None
        Target node.  If None, full traversal is performed.

    Returns
    -------
    dict with keys:
        traversal_order : list[str]
        path            : list[str]
        visited_nodes   : list[str]
        steps           : list[dict]  each: {step, current, stack, visited, action}
        cost            : int
        message         : str
    """
    if not graph:
        return _empty_result("Graph is empty.")

    if start not in graph:
        return _empty_result(f"Start node '{start}' not found in graph.")

    if goal is not None and goal not in graph:
        return _empty_result(f"Goal node '{goal}' not found in graph.")

    # ── iterative DFS ─────────────────────────────────────────────────────────
    # Stack stores (node, parent) pairs so we can reconstruct the path.
    stack:   list[tuple[str, Optional[str]]] = [(start, None)]
    visited: dict[str, bool]                 = {}
    parent:  dict[str, Optional[str]]        = {}

    traversal_order: list[str] = []
    steps: list[dict] = []
    step_num = 0
    goal_reached = False

    while stack:
        current, par = stack.pop()

        if current in visited:
            continue

        visited[current] = True
        parent[current]  = par
        traversal_order.append(current)

        action = f"Visit {current}"
        if goal and current == goal:
            action = f"Goal '{goal}' reached!"
            goal_reached = True

        steps.append({
            "step":    step_num,
            "current": current,
            "stack":   [s for s, _ in stack],
            "visited": list(visited.keys()),
            "action":  action,
        })
        step_num += 1

        if goal_reached:
            break

        # Push neighbors in reverse order so leftmost neighbor is explored first
        neighbors = graph.get(current, [])
        for neighbor in reversed(neighbors):
            if neighbor not in visited:
                stack.append((neighbor, current))

    # ── path reconstruction ───────────────────────────────────────────────────
    path: list[str] = []
    if goal:
        if goal_reached:
            node: Optional[str] = goal
            while node is not None:
                path.append(node)
                node = parent.get(node)
            path.reverse()
            message = f"Path found from '{start}' to '{goal}' with {len(path)-1} edge(s)."
        else:
            message = f"No path found from '{start}' to '{goal}'."
    else:
        message = f"DFS traversal complete. Visited {len(traversal_order)} node(s)."

    return {
        "traversal_order": traversal_order,
        "path":            path,
        "visited_nodes":   list(visited.keys()),
        "steps":           steps,
        "cost":            max(len(path) - 1, 0),
        "message":         message,
    }


def _empty_result(message: str) -> dict:
    return {
        "traversal_order": [],
        "path":            [],
        "visited_nodes":   [],
        "steps":           [],
        "cost":            0,
        "message":         message,
    }
