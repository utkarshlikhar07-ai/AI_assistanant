import random
from typing import Optional


class WumpusWorld:
    """
    4x4 (or configurable) grid world.
    Cell contents: agent, wumpus, pit, gold, empty
    Percepts: stench (adjacent to wumpus), breeze (adjacent to pit),
              glitter (gold in cell), bump (hit wall), scream (wumpus killed)
    """

    DIRECTIONS = ['right', 'up', 'left', 'down']
    DIR_VECTORS = {
        'right': (0, 1),
        'up': (1, 0),
        'left': (0, -1),
        'down': (-1, 0),
    }

    def __init__(self, grid_size: int = 4, seed: Optional[int] = None):
        self.grid_size = grid_size
        # grid[row][col]; row 0 = bottom, row grid_size-1 = top
        self.grid = [[{} for _ in range(grid_size)] for _ in range(grid_size)]
        self.agent_pos = [0, 0]   # [row, col] – start at bottom-left
        self.agent_dir = 'right'  # facing right initially
        self.has_arrow = True
        self.has_gold = False
        self.wumpus_alive = True
        self.game_over = False
        self.won = False
        self.score = 0
        self.last_scream = False        # wumpus just died this action
        self.last_bump = False          # agent just bumped a wall
        self.wumpus_pos: Optional[list] = None
        self.gold_pos: Optional[list] = None
        self.knowledge: dict = {}       # agent's knowledge about each cell
        self._generate_world(seed)

    # ------------------------------------------------------------------
    # World generation
    # ------------------------------------------------------------------

    def _generate_world(self, seed: Optional[int]):
        rng = random.Random(seed)
        n = self.grid_size

        # Reset grid
        self.grid = [[{} for _ in range(n)] for _ in range(n)]

        # --- Place wumpus (not at [0,0]) ---
        cells = [(r, c) for r in range(n) for c in range(n) if (r, c) != (0, 0)]
        wr, wc = rng.choice(cells)
        self.grid[wr][wc]['wumpus'] = True
        self.wumpus_pos = [wr, wc]

        # --- Place pits (20 % chance, not [0,0]) ---
        for r in range(n):
            for c in range(n):
                if (r, c) == (0, 0):
                    continue
                if rng.random() < 0.2:
                    self.grid[r][c]['pit'] = True

        # --- Place gold (not [0,0]) ---
        gr, gc = rng.choice(cells)
        self.grid[gr][gc]['gold'] = True
        self.gold_pos = [gr, gc]

        # --- Initialize knowledge base ---
        for r in range(n):
            for c in range(n):
                self.knowledge[f"{r},{c}"] = {
                    'visited': False,
                    'safe': False,
                    'possible_pit': False,
                    'possible_wumpus': False,
                    'confirmed_pit': False,
                    'confirmed_wumpus': False,
                }

        # Starting cell is known safe/visited
        self.knowledge['0,0']['safe'] = True
        self.knowledge['0,0']['visited'] = True

        # Score: each action costs 1; arrow costs 10; death costs 1000; gold = +1000
        self.score = 0

    # ------------------------------------------------------------------
    # Percepts
    # ------------------------------------------------------------------

    def _adjacent_cells(self, row: int, col: int) -> list:
        adj = []
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = row + dr, col + dc
            if 0 <= nr < self.grid_size and 0 <= nc < self.grid_size:
                adj.append((nr, nc))
        return adj

    def get_percepts(self) -> dict:
        r, c = self.agent_pos
        cell = self.grid[r][c]

        # Stench: adjacent to living wumpus
        stench = False
        if self.wumpus_alive:
            for nr, nc in self._adjacent_cells(r, c):
                if self.grid[nr][nc].get('wumpus') and self.wumpus_alive:
                    stench = True
                    break

        # Breeze: adjacent to pit
        breeze = any(self.grid[nr][nc].get('pit') for nr, nc in self._adjacent_cells(r, c))

        # Glitter: gold in current cell
        glitter = cell.get('gold', False) and not self.has_gold

        percepts = {
            'stench': stench,
            'breeze': breeze,
            'glitter': glitter,
            'bump': self.last_bump,
            'scream': self.last_scream,
        }

        # Reset ephemeral percepts after reading
        self.last_bump = False
        self.last_scream = False

        return percepts

    # ------------------------------------------------------------------
    # Actions
    # ------------------------------------------------------------------

    def move(self, direction: str) -> dict:
        """Move agent in a cardinal direction, or 'forward' (uses agent_dir)."""
        self.score -= 1
        self.last_scream = False
        self.last_bump = False

        if self.game_over:
            return self._result(False, "Game is over.", 'game_over')

        # Resolve direction
        if direction == 'forward':
            direction = self.agent_dir
        if direction not in self.DIR_VECTORS:
            return self._result(False, f"Unknown direction '{direction}'.", 'playing')

        dr, dc = self.DIR_VECTORS[direction]
        nr = self.agent_pos[0] + dr
        nc = self.agent_pos[1] + dc

        # Wall check
        if not (0 <= nr < self.grid_size and 0 <= nc < self.grid_size):
            self.last_bump = True
            percepts = self.get_percepts()
            self.update_knowledge(self.agent_pos, percepts)
            return self._result(True, "Bump! Hit a wall.", 'playing', percepts)

        # Move agent
        self.agent_dir = direction
        self.agent_pos = [nr, nc]
        cell = self.grid[nr][nc]

        # Pit
        if cell.get('pit'):
            self.score -= 1000
            self.game_over = True
            self.won = False
            percepts = self.get_percepts()
            return self._result(True, "You fell into a pit! Game over.", 'died', percepts)

        # Wumpus
        if cell.get('wumpus') and self.wumpus_alive:
            self.score -= 1000
            self.game_over = True
            self.won = False
            percepts = self.get_percepts()
            return self._result(True, "You were eaten by the Wumpus! Game over.", 'died', percepts)

        percepts = self.get_percepts()
        self.update_knowledge(self.agent_pos, percepts)
        return self._result(True, f"Moved {direction}.", 'playing', percepts)

    def turn(self, turn_dir: str) -> dict:
        """Turn agent left or right."""
        self.score -= 1
        if self.game_over:
            return self._result(False, "Game is over.", 'game_over')
        dirs = self.DIRECTIONS
        idx = dirs.index(self.agent_dir)
        if turn_dir == 'left':
            self.agent_dir = dirs[(idx + 1) % 4]
        elif turn_dir == 'right':
            self.agent_dir = dirs[(idx - 1) % 4]
        percepts = self.get_percepts()
        return self._result(True, f"Turned {turn_dir}. Now facing {self.agent_dir}.", 'playing', percepts)

    def shoot_arrow(self) -> dict:
        """Shoot arrow in current facing direction."""
        self.score -= 1
        self.last_scream = False
        if self.game_over:
            return self._result(False, "Game is over.", 'game_over')
        if not self.has_arrow:
            return self._result(False, "No arrow left.", 'playing')

        self.has_arrow = False
        self.score -= 10  # arrow cost

        dr, dc = self.DIR_VECTORS[self.agent_dir]
        r, c = self.agent_pos[0] + dr, self.agent_pos[1] + dc

        killed = False
        while 0 <= r < self.grid_size and 0 <= c < self.grid_size:
            if self.grid[r][c].get('wumpus') and self.wumpus_alive:
                self.wumpus_alive = False
                self.grid[r][c]['wumpus'] = False
                self.last_scream = True
                killed = True
                # Update knowledge: remove wumpus fear
                for key in self.knowledge:
                    self.knowledge[key]['confirmed_wumpus'] = False
                    self.knowledge[key]['possible_wumpus'] = False
                break
            r += dr
            c += dc

        percepts = self.get_percepts()
        msg = "Arrow fired. Wumpus killed! You hear a scream." if killed else "Arrow fired. No effect."
        return self._result(True, msg, 'playing', percepts)

    def grab_gold(self) -> dict:
        """Grab gold if present in current cell."""
        self.score -= 1
        if self.game_over:
            return self._result(False, "Game is over.", 'game_over')

        r, c = self.agent_pos
        if self.grid[r][c].get('gold') and not self.has_gold:
            self.grid[r][c]['gold'] = False
            self.has_gold = True
            self.score += 1000
            percepts = self.get_percepts()
            return self._result(True, "Gold grabbed! Now get out!", 'playing', percepts)

        percepts = self.get_percepts()
        return self._result(False, "No gold here to grab.", 'playing', percepts)

    def climb_out(self) -> dict:
        """Climb out of the cave. Only valid at [0,0]."""
        self.score -= 1
        if self.game_over:
            return self._result(False, "Game is over.", 'game_over')

        if self.agent_pos != [0, 0]:
            percepts = self.get_percepts()
            return self._result(False, "Can only climb out from the starting square [0,0].", 'playing', percepts)

        self.game_over = True
        self.won = self.has_gold
        final_score = self.score
        msg = (f"Escaped with the gold! Final score: {final_score}" if self.won
               else f"Escaped without gold. Final score: {final_score}")
        status = 'won' if self.won else 'escaped'
        return self._result(True, msg, status)

    # ------------------------------------------------------------------
    # Knowledge update (simple logical inference)
    # ------------------------------------------------------------------

    def update_knowledge(self, pos: list, percepts: dict):
        r, c = pos
        key = f"{r},{c}"
        kb = self.knowledge

        kb[key]['visited'] = True
        kb[key]['safe'] = True
        kb[key]['possible_pit'] = False
        kb[key]['confirmed_pit'] = False

        adj = self._adjacent_cells(r, c)

        if not percepts.get('breeze'):
            # No breeze → no pits adjacent → mark neighbours safe
            for nr, nc in adj:
                nk = f"{nr},{nc}"
                kb[nk]['possible_pit'] = False
                kb[nk]['confirmed_pit'] = False
                if not kb[nk]['visited']:
                    kb[nk]['safe'] = True
        else:
            # Breeze → at least one adjacent unvisited cell might be a pit
            for nr, nc in adj:
                nk = f"{nr},{nc}"
                if not kb[nk]['visited']:
                    kb[nk]['possible_pit'] = True

        if not percepts.get('stench') or not self.wumpus_alive:
            # No stench (or wumpus dead) → no wumpus adjacent
            for nr, nc in adj:
                nk = f"{nr},{nc}"
                kb[nk]['possible_wumpus'] = False
                kb[nk]['confirmed_wumpus'] = False
                if not kb[nk]['visited'] and not kb[nk]['possible_pit']:
                    kb[nk]['safe'] = True
        else:
            # Stench → wumpus might be in an adjacent unvisited cell
            unvisited_adj = [(nr, nc) for nr, nc in adj if not kb[f"{nr},{nc}"]['visited']]
            if len(unvisited_adj) == 1:
                # Exactly one candidate → confirmed wumpus location
                nr, nc = unvisited_adj[0]
                nk = f"{nr},{nc}"
                kb[nk]['confirmed_wumpus'] = True
                kb[nk]['possible_wumpus'] = True
            else:
                for nr, nc in unvisited_adj:
                    nk = f"{nr},{nc}"
                    kb[nk]['possible_wumpus'] = True

    # ------------------------------------------------------------------
    # State snapshot
    # ------------------------------------------------------------------

    def get_state(self) -> dict:
        percepts = self.get_percepts()
        status = 'playing'
        if self.game_over:
            status = 'won' if self.won else 'died'

        # Build serialisable grid
        grid_state = []
        for r in range(self.grid_size):
            row = []
            for c in range(self.grid_size):
                cell = dict(self.grid[r][c])
                cell['is_agent'] = (self.agent_pos == [r, c])
                row.append(cell)
            grid_state.append(row)

        return {
            'grid_state': grid_state,
            'agent_pos': self.agent_pos,
            'agent_dir': self.agent_dir,
            'percepts': percepts,
            'knowledge': self.knowledge,
            'game_status': status,
            'has_arrow': self.has_arrow,
            'has_gold': self.has_gold,
            'wumpus_alive': self.wumpus_alive,
            'score': self.score,
            'grid_size': self.grid_size,
        }

    # ------------------------------------------------------------------
    # Internal helper
    # ------------------------------------------------------------------

    def _result(self, success: bool, message: str, status: str, percepts: Optional[dict] = None) -> dict:
        if percepts is None:
            percepts = {}
        return {
            'success': success,
            'message': message,
            'percepts': percepts,
            'game_status': status,
            'agent_pos': self.agent_pos[:],
            'score': self.score,
            'has_gold': self.has_gold,
            'has_arrow': self.has_arrow,
            'wumpus_alive': self.wumpus_alive,
            'knowledge': self.knowledge,
            'grid_state': self._serialise_grid(),
        }

    def _serialise_grid(self) -> list:
        grid_state = []
        for r in range(self.grid_size):
            row = []
            for c in range(self.grid_size):
                cell = dict(self.grid[r][c])
                cell['is_agent'] = (self.agent_pos == [r, c])
                row.append(cell)
            grid_state.append(row)
        return grid_state


def create_world(grid_size: int = 4, seed: Optional[int] = None) -> WumpusWorld:
    return WumpusWorld(grid_size, seed)
