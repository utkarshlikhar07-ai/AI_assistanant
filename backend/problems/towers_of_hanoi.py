from typing import Optional


def hanoi(n: int, source: str = 'A', target: str = 'C', auxiliary: str = 'B') -> dict:
    """
    Solve the Tower of Hanoi problem for n disks.

    Returns:
        {
            moves: list[dict],   # each: {move_num, disk, from_peg, to_peg, pegs_state}
            total_moves: int,    # = 2^n - 1
            message: str,
            success: bool,
        }

    Disks are integers where 1 = smallest, n = largest.
    Initial peg state: source has [n, n-1, …, 2, 1] (top of list = top of peg).
    """
    if n < 1:
        return {
            'moves': [],
            'total_moves': 0,
            'message': "Number of disks must be at least 1.",
            'success': False,
        }

    # Peg state: each peg holds a stack (list); index 0 = bottom of stack
    pegs: dict = {
        source: list(range(n, 0, -1)),  # [n, n-1, ..., 2, 1] – largest at bottom
        auxiliary: [],
        target: [],
    }

    moves: list = []
    move_counter = [0]   # mutable so inner function can mutate it

    def _snapshot() -> dict:
        return {peg: list(stack) for peg, stack in pegs.items()}

    def _move(disk_count: int, src: str, tgt: str, aux: str):
        if disk_count == 0:
            return
        # Move n-1 disks from src to aux using tgt as buffer
        _move(disk_count - 1, src, aux, tgt)
        # Move the largest remaining disk from src to tgt
        disk = pegs[src].pop()
        pegs[tgt].append(disk)
        move_counter[0] += 1
        moves.append({
            'move_num': move_counter[0],
            'disk': disk,
            'from_peg': src,
            'to_peg': tgt,
            'pegs_state': _snapshot(),
        })
        # Move n-1 disks from aux to tgt using src as buffer
        _move(disk_count - 1, aux, tgt, src)

    _move(n, source, target, auxiliary)

    total = 2 ** n - 1
    return {
        'moves': moves,
        'total_moves': total,
        'message': f"Tower of Hanoi solved for {n} disk(s) in {total} move(s).",
        'success': True,
    }
