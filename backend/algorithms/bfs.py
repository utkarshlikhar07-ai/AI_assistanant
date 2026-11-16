from collections import deque, defaultdict
from typing import Optional


def bfs(graph: dict, start: str, goal: Optional[str] = None) -> dict:
    """
    Breadth-First Search traversal / pathfinding.

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
        path            : list[str]   (start→goal if goal given, else [])
        visited_nodes   : list[str]
        steps           : list[dict]  each step: {step, current, queue, visited, action}
        cost            : int         number of edges in path
        message         : str
    """
    # ── validation ───────────────────────────────────────────────────────────
    if not graph:
        return _empty_result("Graph is empty.")

    if start not in graph:
        return _empty_result(f"Start node '{start}' not found in graph.")

    if goal is not None and goal not in graph:
        return _empty_result(f"Goal node '{goal}' not found in graph.")

    # ── BFS ──────────────────────────────────────────────────────────────────
    visited: dict[str, bool] = {}       # node -> True when dequeued
    parent:  dict[str, Optional[str]] = {start: None}
    queue   = deque([start])
    visited[start] = True

    traversal_order: list[str] = []
    steps: list[dict] = []
    step_num = 0

    while queue:
        current = queue.popleft()
        traversal_order.append(current)

        action = f"Visit {current}"
        if goal and current == goal:
            action = f"Goal '{goal}' reached!"

        steps.append({
            "step":    step_num,
            "current": current,
            "queue":   list(queue),
            "visited": list(visited.keys()),
            "action":  action,
        })
        step_num += 1

        if goal and current == goal:
            break

        neighbors = graph.get(current, [])
        for neighbor in neighbors:
            if neighbor not in visited:
                visited[neighbor] = True
                parent[neighbor]  = current
                queue.append(neighbor)

    # ── path reconstruction ───────────────────────────────────────────────────
    path: list[str] = []
    if goal:
        if goal in parent or goal == start:
            node: Optional[str] = goal
            while node is not None:
                path.append(node)
                node = parent.get(node)
            path.reverse()
            message = f"Path found from '{start}' to '{goal}' with {len(path)-1} edge(s)."
        else:
            message = f"No path found from '{start}' to '{goal}'."
    else:
        message = f"BFS traversal complete. Visited {len(traversal_order)} node(s)."

    return {
        "traversal_order": traversal_order,
        "path":            path,
        "visited_nodes":   list(visited.keys()),
        "steps":           steps,
        "cost":            max(len(path) - 1, 0),
        "message":         message,
    }


# ── helpers ───────────────────────────────────────────────────────────────────

def _empty_result(message: str) -> dict:
    return {
        "traversal_order": [],
        "path":            [],
        "visited_nodes":   [],
        "steps":           [],
        "cost":            0,
        "message":         message,
    }
