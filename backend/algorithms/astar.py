import heapq
from typing import Optional


def astar(graph: dict, start: str, goal: str, heuristics: dict) -> dict:
    """
    A* search algorithm.

    Parameters
    ----------
    graph : dict
        Weighted adjacency list  {node: [(neighbor, weight), ...]}
    start : str
        Starting node.
    goal : str
        Target node.
    heuristics : dict
        Admissible heuristic values  {node: h_value}

    Returns
    -------
    dict:
        path         : list[str]
        cost         : float
        visited_nodes: list[str]
        steps        : list[dict]  each: {step, current, g, h, f, open_set, closed_set, action}
        message      : str
        success      : bool
    """
    if not graph:
        return _empty_result("Graph is empty.", start, goal)

    if start not in graph:
        return _empty_result(f"Start node '{start}' not found in graph.", start, goal)

    if goal not in graph:
        return _empty_result(f"Goal node '{goal}' not found in graph.", start, goal)

    INF = float("inf")

    g: dict[str, float] = {node: INF for node in graph}
    g[start] = 0.0

    h = lambda n: float(heuristics.get(n, 0))

    came_from: dict[str, Optional[str]] = {start: None}

    counter = 0
    open_heap: list[tuple] = [(g[start] + h(start), counter, start)]
    open_set:  set[str]    = {start}
    closed_set: set[str]   = set()

    visited_order: list[str] = []
    steps: list[dict] = []
    step_num = 0

    while open_heap:
        f_curr, _, current = heapq.heappop(open_heap)
        open_set.discard(current)

        if current in closed_set:
            continue

        closed_set.add(current)
        visited_order.append(current)

        g_curr = g[current]
        h_curr = h(current)
        action = f"Expand node '{current}' (f={g_curr + h_curr:.3f})"

        if current == goal:
            action = f"Goal '{goal}' reached! f={g_curr + h_curr:.3f}"
            steps.append({
                "step":       step_num,
                "current":    current,
                "g":          round(g_curr, 4),
                "h":          round(h_curr, 4),
                "f":          round(g_curr + h_curr, 4),
                "open_set":   _heap_snapshot(open_heap, g, h),
                "closed_set": sorted(closed_set),
                "action":     action,
            })
            path = _reconstruct(came_from, goal)
            return {
                "path":          path,
                "cost":          round(g[goal], 4),
                "visited_nodes": visited_order,
                "steps":         steps,
                "message":       f"Path found: {' -> '.join(path)} (cost={g[goal]:.4f})",
                "success":       True,
            }

        steps.append({
            "step":       step_num,
            "current":    current,
            "g":          round(g_curr, 4),
            "h":          round(h_curr, 4),
            "f":          round(g_curr + h_curr, 4),
            "open_set":   _heap_snapshot(open_heap, g, h),
            "closed_set": sorted(closed_set),
            "action":     action,
        })
        step_num += 1

        for neighbor, weight in graph.get(current, []):
            if neighbor in closed_set:
                continue

            tentative_g = g_curr + weight

            if tentative_g < g.get(neighbor, INF):
                g[neighbor]        = tentative_g
                came_from[neighbor] = current
                f_new = tentative_g + h(neighbor)
                counter += 1
                heapq.heappush(open_heap, (f_new, counter, neighbor))
                open_set.add(neighbor)

    return _empty_result(
        f"No path found from '{start}' to '{goal}'.", start, goal,
        visited_nodes=visited_order, steps=steps
    )


def _reconstruct(came_from: dict, goal: str) -> list:
    path: list[str] = []
    node: Optional[str] = goal
    while node is not None:
        path.append(node)
        node = came_from.get(node)
    path.reverse()
    return path


def _heap_snapshot(heap, g, h) -> list:
    seen: set = set()
    result = []
    for f, _, node in heap:
        if node not in seen:
            seen.add(node)
            result.append({"node": node, "g": round(g.get(node, 0), 4),
                           "h": round(h(node), 4), "f": round(f, 4)})
    return result


def _empty_result(
    message: str,
    start: str,
    goal: str,
    visited_nodes: Optional[list] = None,
    steps: Optional[list] = None,
) -> dict:
    return {
        "path":          [],
        "cost":          0.0,
        "visited_nodes": visited_nodes or [],
        "steps":         steps or [],
        "message":       message,
        "success":       False,
    }
