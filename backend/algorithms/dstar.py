import heapq
import math
from typing import Optional


class DStarLite:
    """
    D* Lite – Incremental path planner for grids with dynamic obstacles.

    Reference: Koenig & Likhachev (2002), "D* Lite".

    The algorithm searches backwards from the goal to the start so that
    when obstacles appear near the robot's current position only a small
    portion of the search tree needs to be repaired.

    Convention
    ----------
    Coordinates are (row, col) tuples.
    Movement is 4-connected (up / down / left / right).
    Travel cost between adjacent cells is 1.0 (∞ through obstacles).
    """

    INF = float("inf")

    def __init__(
        self,
        grid_size: int,
        start: list,
        goal: list,
        obstacles: list,
    ):
        self.grid_size = grid_size
        self.start = tuple(start)   # current robot position (updated as robot moves)
        self.goal  = tuple(goal)
        self.obstacles: set = {tuple(o) for o in obstacles}

        # Key modifier – accumulates heuristic changes as the robot moves
        self.km: float = 0.0

        # g[s]   : best known cost-to-goal from s  (∞ initially)
        # rhs[s] : one-step-lookahead cost-to-goal  (∞ initially, 0 at goal)
        self.g:   dict = {}
        self.rhs: dict = {}

        # Priority queue – list of (key, node)
        self.U: list = []
        self._in_queue: dict = {}   # node -> key currently in queue (for lazy deletion)

        self.replanning_steps: list[dict] = []

        self.initialize()
        self.compute_shortest_path()

    # ── geometry helpers ──────────────────────────────────────────────────────

    def _in_bounds(self, s: tuple) -> bool:
        r, c = s
        return 0 <= r < self.grid_size and 0 <= c < self.grid_size

    def _is_free(self, s: tuple) -> bool:
        return self._in_bounds(s) and s not in self.obstacles

    def _neighbors(self, s: tuple) -> list:
        r, c = s
        return [
            n for n in [(r-1,c),(r+1,c),(r,c-1),(r,c+1)]
            if self._in_bounds(n)
        ]

    def _cost(self, a: tuple, b: tuple) -> float:
        """Travel cost between adjacent cells (∞ if either is an obstacle)."""
        if a in self.obstacles or b in self.obstacles:
            return self.INF
        return 1.0

    def heuristic(self, a, b) -> float:
        """Manhattan distance heuristic (admissible for 4-connected grids)."""
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    # ── D* Lite core ──────────────────────────────────────────────────────────

    def calculate_key(self, s: tuple) -> tuple:
        """
        D* Lite key: (min(g,rhs)+h(start,s)+km,  min(g,rhs))
        """
        g_s   = self.g.get(s, self.INF)
        rhs_s = self.rhs.get(s, self.INF)
        mn = min(g_s, rhs_s)
        return (mn + self.heuristic(self.start, s) + self.km, mn)

    def _enqueue(self, s: tuple):
        key = self.calculate_key(s)
        heapq.heappush(self.U, (key, s))
        self._in_queue[s] = key

    def _top_key(self) -> tuple:
        while self.U:
            key, s = self.U[0]
            # lazy deletion: ignore stale entries
            if self._in_queue.get(s) == key:
                return key
            heapq.heappop(self.U)
        return (self.INF, self.INF)

    def _top(self) -> Optional[tuple]:
        while self.U:
            key, s = self.U[0]
            if self._in_queue.get(s) == key:
                return s
            heapq.heappop(self.U)
        return None

    def _pop(self) -> Optional[tuple]:
        while self.U:
            key, s = heapq.heappop(self.U)
            if self._in_queue.get(s) == key:
                del self._in_queue[s]
                return s
        return None

    def initialize(self):
        """Set all g/rhs to ∞, then seed the goal."""
        for r in range(self.grid_size):
            for c in range(self.grid_size):
                s = (r, c)
                self.g[s]   = self.INF
                self.rhs[s] = self.INF

        self.rhs[self.goal] = 0.0
        self._enqueue(self.goal)

    def update_vertex(self, u: tuple):
        """
        Recompute rhs[u] from its successors and re-insert into the queue
        if it is inconsistent.
        """
        if u != self.goal:
            best = self.INF
            for s_prime in self._neighbors(u):
                v = self._cost(u, s_prime) + self.g.get(s_prime, self.INF)
                if v < best:
                    best = v
            self.rhs[u] = best

        # Remove from queue (mark stale)
        if u in self._in_queue:
            del self._in_queue[u]

        if self.g.get(u, self.INF) != self.rhs.get(u, self.INF):
            self._enqueue(u)

    def compute_shortest_path(self) -> list:
        """
        Main D* Lite loop.  Processes vertices until the start is consistent.
        Returns list of replanning step dicts.
        """
        steps: list[dict] = []
        step_idx = len(self.replanning_steps)

        while True:
            top_key = self._top_key()
            start_key = self.calculate_key(self.start)
            g_s   = self.g.get(self.start, self.INF)
            rhs_s = self.rhs.get(self.start, self.INF)

            if top_key >= start_key and g_s == rhs_s:
                break   # start is consistent

            u = self._pop()
            if u is None:
                break

            u_key = self.calculate_key(u)

            if top_key < u_key:
                # Key increased – reinsert
                self._enqueue(u)
            elif self.g.get(u, self.INF) > self.rhs.get(u, self.INF):
                # Over-consistent: lower g to rhs
                self.g[u] = self.rhs[u]
                for s in self._neighbors(u):
                    self.update_vertex(s)
            else:
                # Under-consistent: raise g to ∞
                self.g[u] = self.INF
                self.update_vertex(u)
                for s in self._neighbors(u):
                    self.update_vertex(s)

            steps.append({
                "step":        step_idx,
                "expanded":    list(u),
                "g":           round(self.g.get(u, self.INF), 4) if self.g.get(u, self.INF) != self.INF else "∞",
                "rhs":         round(self.rhs.get(u, self.INF), 4) if self.rhs.get(u, self.INF) != self.INF else "∞",
                "queue_size":  len(self._in_queue),
            })
            step_idx += 1

        self.replanning_steps.extend(steps)
        return steps

    def get_path(self) -> list:
        """
        Reconstruct the path from start to goal by greedily following
        lowest-cost neighbours (standard D* Lite path extraction).
        Returns list of [row, col] pairs, or [] if no path exists.
        """
        if self.g.get(self.start, self.INF) == self.INF:
            return []

        path = [list(self.start)]
        current = self.start
        visited_path: set = {current}

        while current != self.goal:
            best_cost = self.INF
            best_next = None
            for neighbor in self._neighbors(current):
                c = self._cost(current, neighbor) + self.g.get(neighbor, self.INF)
                if c < best_cost:
                    best_cost = c
                    best_next = neighbor
            if best_next is None or best_next in visited_path:
                return []   # broken path
            current = best_next
            visited_path.add(current)
            path.append(list(current))

        return path

    def add_obstacle(self, pos: list) -> dict:
        """
        Mark a cell as an obstacle, update affected vertices, replan.
        Returns replanning info.
        """
        s = tuple(pos)
        if s == self.goal or s == self.start:
            return {"success": False, "message": "Cannot block start or goal.", "steps": []}

        self.obstacles.add(s)

        # All edges incident to s have changed cost (now ∞)
        affected = [s] + self._neighbors(s)
        for v in affected:
            self.update_vertex(v)

        new_steps = self.compute_shortest_path()
        new_path  = self.get_path()
        return {
            "success":   bool(new_path),
            "obstacle":  pos,
            "new_path":  new_path,
            "steps":     new_steps,
            "message":   f"Obstacle added at {pos}. {'Path replanned.' if new_path else 'No path exists.'}",
        }

    def remove_obstacle(self, pos: list) -> dict:
        """Remove a previously added obstacle and replan."""
        s = tuple(pos)
        if s not in self.obstacles:
            return {"success": False, "message": f"{pos} is not an obstacle.", "steps": []}

        self.obstacles.discard(s)
        affected = [s] + self._neighbors(s)
        for v in affected:
            self.update_vertex(v)

        new_steps = self.compute_shortest_path()
        new_path  = self.get_path()
        return {
            "success":   bool(new_path),
            "obstacle":  pos,
            "new_path":  new_path,
            "steps":     new_steps,
            "message":   f"Obstacle removed at {pos}. Path replanned.",
        }


# ── module-level function ─────────────────────────────────────────────────────

def dstar_plan(
    grid_size: int,
    start: list,
    goal: list,
    obstacles: list,
) -> dict:
    """
    Plan a path on a grid using D* Lite.

    Parameters
    ----------
    grid_size : int         Square grid dimension (grid_size × grid_size).
    start     : [row, col]  Robot start cell.
    goal      : [row, col]  Destination cell.
    obstacles : [[r,c], …]  Initially blocked cells.

    Returns
    -------
    dict:
        path             : list[[row, col]]
        replanning_steps : list[dict]
        message          : str
        success          : bool
    """
    try:
        planner  = DStarLite(grid_size, start, goal, obstacles)
        path     = planner.get_path()
        success  = bool(path)
        message  = (
            f"Path found from {start} to {goal} with {len(path)} cell(s)."
            if success
            else f"No path found from {start} to {goal}."
        )
        return {
            "path":             path,
            "replanning_steps": planner.replanning_steps,
            "message":          message,
            "success":          success,
        }
    except Exception as exc:
        return {
            "path":             [],
            "replanning_steps": [],
            "message":          f"D* Lite error: {exc}",
            "success":          False,
        }
