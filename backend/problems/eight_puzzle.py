import heapq
import time
from typing import Optional


GOAL_STATE = (1, 2, 3, 4, 5, 6, 7, 8, 0)   # standard 8-puzzle goal
GRID_SIZE = 3

# Direction labels for blank movement
MOVE_LABELS = {(-1, 0): 'up', (1, 0): 'down', (0, -1): 'left', (0, 1): 'right'}


# ---------------------------------------------------------------------------
# Heuristics
# ---------------------------------------------------------------------------

def manhattan_distance(state: list, goal: list) -> int:
    """Sum of Manhattan distances for all tiles (excluding blank)."""
    total = 0
    n = int(len(state) ** 0.5)
    goal_pos = {val: divmod(i, n) for i, val in enumerate(goal)}
    for i, val in enumerate(state):
        if val == 0:
            continue
        gr, gc = goal_pos[val]
        cr, cc = divmod(i, n)
        total += abs(cr - gr) + abs(cc - gc)
    return total


def misplaced_tiles(state: list, goal: list) -> int:
    """Count of non-blank tiles not in their goal position."""
    return sum(1 for i, (s, g) in enumerate(zip(state, goal)) if s != g and s != 0)


# ---------------------------------------------------------------------------
# Solvability
# ---------------------------------------------------------------------------

def is_solvable(state: list) -> bool:
    """
    For a 3×3 puzzle, the puzzle is solvable iff the number of inversions
    among non-blank tiles is even.
    """
    flat = [x for x in state if x != 0]
    inversions = 0
    for i in range(len(flat)):
        for j in range(i + 1, len(flat)):
            if flat[i] > flat[j]:
                inversions += 1
    return inversions % 2 == 0


# ---------------------------------------------------------------------------
# A* solver
# ---------------------------------------------------------------------------

def _get_neighbors(state: tuple) -> list:
    """Return (new_state, move_label) pairs reachable from state."""
    idx = state.index(0)
    row, col = divmod(idx, GRID_SIZE)
    neighbors = []
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nr, nc = row + dr, col + dc
        if 0 <= nr < GRID_SIZE and 0 <= nc < GRID_SIZE:
            nidx = nr * GRID_SIZE + nc
            lst = list(state)
            lst[idx], lst[nidx] = lst[nidx], lst[idx]
            label = MOVE_LABELS[(dr, dc)]
            neighbors.append((tuple(lst), label))
    return neighbors


def _reconstruct_path(came_from: dict, current: tuple):
    """Return (state_sequence, move_sequence) lists from start to current."""
    states = []
    moves = []
    while current in came_from:
        parent, move_label = came_from[current]
        states.append(current)
        moves.append(move_label)
        current = parent
    states.append(current)
    states.reverse()
    moves.reverse()
    return states, moves


def _flat_to_grid(flat: tuple) -> list:
    return [list(flat[i * GRID_SIZE:(i + 1) * GRID_SIZE]) for i in range(GRID_SIZE)]


def solve_puzzle(initial_state: list, heuristic: str = "manhattan") -> dict:
    """
    Solve the 8-puzzle using A* search.

    initial_state: flattened list of 9 numbers (0 = blank tile).
    heuristic    : 'manhattan' | 'misplaced'
    Returns a dict with solution_path, moves, explored_states, time_taken,
    message, success, is_solvable, move_sequence.
    """
    start_time = time.time()

    # Flatten if nested list was passed
    if initial_state and isinstance(initial_state[0], list):
        flat_initial = [x for row in initial_state for x in row]
    else:
        flat_initial = list(initial_state)

    solvable = is_solvable(flat_initial)
    goal = list(GOAL_STATE)

    base_result = {
        'solution_path': [],
        'moves': 0,
        'explored_states': 0,
        'time_taken': 0.0,
        'message': '',
        'success': False,
        'is_solvable': solvable,
        'move_sequence': [],
    }

    if not solvable:
        base_result['message'] = "Puzzle is not solvable."
        base_result['time_taken'] = time.time() - start_time
        return base_result

    start = tuple(flat_initial)
    goal_t = GOAL_STATE

    if start == goal_t:
        base_result['success'] = True
        base_result['message'] = "Already solved!"
        base_result['solution_path'] = [_flat_to_grid(start)]
        base_result['time_taken'] = time.time() - start_time
        return base_result

    h_func = manhattan_distance if heuristic == "manhattan" else misplaced_tiles

    # Priority queue: (f, g, state)
    counter = 0  # tie-breaker
    open_heap = []
    h0 = h_func(list(start), goal)
    heapq.heappush(open_heap, (h0, 0, counter, start))

    came_from: dict = {}        # state -> (parent_state, move_label)
    g_score: dict = {start: 0}

    explored = 0
    MAX_EXPLORED = 100_000

    while open_heap:
        f, g, _, current = heapq.heappop(open_heap)

        if g > g_score.get(current, float('inf')):
            continue

        if current == goal_t:
            states, moves = _reconstruct_path(came_from, current)
            elapsed = time.time() - start_time
            solution_path = [_flat_to_grid(s) for s in states]
            base_result.update({
                'success': True,
                'solution_path': solution_path,
                'moves': len(moves),
                'explored_states': explored,
                'time_taken': round(elapsed, 4),
                'message': f"Solved in {len(moves)} moves, explored {explored} states.",
                'move_sequence': moves,
            })
            return base_result

        explored += 1
        if explored > MAX_EXPLORED:
            base_result['message'] = "Search limit reached (100 000 states)."
            base_result['explored_states'] = explored
            base_result['time_taken'] = round(time.time() - start_time, 4)
            return base_result

        for neighbor, move_label in _get_neighbors(current):
            tentative_g = g + 1
            if tentative_g < g_score.get(neighbor, float('inf')):
                g_score[neighbor] = tentative_g
                came_from[neighbor] = (current, move_label)
                h = h_func(list(neighbor), goal)
                counter += 1
                heapq.heappush(open_heap, (tentative_g + h, tentative_g, counter, neighbor))

    # Open set exhausted without finding goal
    elapsed = time.time() - start_time
    base_result['message'] = "No solution found."
    base_result['explored_states'] = explored
    base_result['time_taken'] = round(elapsed, 4)
    return base_result
