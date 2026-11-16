import uuid

from fastapi import APIRouter, HTTPException, Query

from backend.models.schemas import (
    WumpusRequest,
    WumpusAction,
    WumpusResponse,
    EightPuzzleRequest,
    EightPuzzleResponse,
    HanoiRequest,
    HanoiResponse,
)
from backend.problems.wumpus_world import WumpusWorld, create_world
from backend.problems.eight_puzzle import solve_puzzle, is_solvable
from backend.problems.towers_of_hanoi import hanoi

router = APIRouter()

# ---------------------------------------------------------------------------
# In-memory Wumpus World sessions  {session_id -> WumpusWorld}
# ---------------------------------------------------------------------------
wumpus_sessions: dict[str, WumpusWorld] = {}


# ---------------------------------------------------------------------------
# Wumpus World endpoints
# ---------------------------------------------------------------------------

@router.post("/wumpus/new", response_model=WumpusResponse)
async def new_wumpus_game(request: WumpusRequest):
    """Create a new Wumpus World game and return its initial state."""
    if request.grid_size < 2 or request.grid_size > 10:
        raise HTTPException(status_code=400, detail="grid_size must be between 2 and 10.")

    world = create_world(grid_size=request.grid_size, seed=request.seed)
    session_id = str(uuid.uuid4())
    wumpus_sessions[session_id] = world

    state = world.get_state()
    return WumpusResponse(
        grid_state=state["grid_state"],
        agent_pos=state["agent_pos"],
        percepts=state["percepts"],
        knowledge=state["knowledge"],
        game_status=state["game_status"],
        message=f"New Wumpus World created (session: {session_id}). Good luck!",
        success=True,
    )


@router.post("/wumpus/action", response_model=WumpusResponse)
async def wumpus_action(
    action: WumpusAction,
    session_id: str = Query(default="default"),
):
    """Perform an action on an existing Wumpus World session."""
    # Lazily create a default session when none exists
    if session_id not in wumpus_sessions:
        if session_id == "default":
            wumpus_sessions["default"] = create_world()
        else:
            raise HTTPException(
                status_code=404,
                detail=f"Session '{session_id}' not found. Start a new game via /wumpus/new.",
            )

    world = wumpus_sessions[session_id]
    act = action.action.lower()

    # --- Dispatch action ---
    if act in ("move_up", "up"):
        result = world.move("up")
    elif act in ("move_down", "down"):
        result = world.move("down")
    elif act in ("move_left", "left"):
        result = world.move("left")
    elif act in ("move_right", "right"):
        result = world.move("right")
    elif act == "forward":
        result = world.move("forward")
    elif act in ("move", "move_forward"):
        direction = (action.direction or "forward").lower()
        result = world.move(direction)
    elif act == "turn_left":
        result = world.turn("left")
    elif act == "turn_right":
        result = world.turn("right")
    elif act in ("shoot", "shoot_arrow"):
        result = world.shoot_arrow()
    elif act in ("grab", "grab_gold"):
        result = world.grab_gold()
    elif act in ("climb", "climb_out"):
        result = world.climb_out()
    else:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Unknown action '{action.action}'. Valid actions: "
                "move_up, move_down, move_left, move_right, forward, "
                "turn_left, turn_right, shoot_arrow, grab_gold, climb_out."
            ),
        )

    return WumpusResponse(
        grid_state=result.get("grid_state", []),
        agent_pos=result.get("agent_pos", [0, 0]),
        percepts=result.get("percepts", {}),
        knowledge=result.get("knowledge", {}),
        game_status=result.get("game_status", "playing"),
        message=result.get("message", ""),
        success=result.get("success", True),
    )


# ---------------------------------------------------------------------------
# 8-Puzzle endpoint
# ---------------------------------------------------------------------------

@router.post("/eight-puzzle", response_model=EightPuzzleResponse)
async def solve_eight_puzzle(request: EightPuzzleRequest):
    """Solve an 8-puzzle using A* and return the solution path."""
    # Flatten the input (may be nested list[list[int]])
    if request.initial_state and isinstance(request.initial_state[0], list):
        flat = [x for row in request.initial_state for x in row]
    else:
        flat = list(request.initial_state)

    # Validate
    if len(flat) != 9:
        raise HTTPException(status_code=400, detail="initial_state must contain exactly 9 numbers.")
    if sorted(flat) != list(range(9)):
        raise HTTPException(
            status_code=400,
            detail="initial_state must be a permutation of 0–8 (0 represents the blank tile).",
        )

    heuristic = request.heuristic.lower()
    if heuristic not in ("manhattan", "misplaced"):
        raise HTTPException(
            status_code=400,
            detail="heuristic must be 'manhattan' or 'misplaced'.",
        )

    result = solve_puzzle(flat, heuristic=heuristic)

    return EightPuzzleResponse(
        solution_path=result["solution_path"],
        moves=result["moves"],
        explored_states=result["explored_states"],
        time_taken=result["time_taken"],
        message=result["message"],
        success=result["success"],
        is_solvable=result["is_solvable"],
    )


# ---------------------------------------------------------------------------
# Tower of Hanoi endpoint
# ---------------------------------------------------------------------------

@router.post("/hanoi", response_model=HanoiResponse)
async def towers_of_hanoi(request: HanoiRequest):
    """Solve the Tower of Hanoi for n disks and return the full move list."""
    n = request.num_disks
    if n < 1 or n > 15:
        raise HTTPException(
            status_code=400,
            detail="num_disks must be between 1 and 15.",
        )

    result = hanoi(n)

    return HanoiResponse(
        moves=result["moves"],
        total_moves=result["total_moves"],
        message=result["message"],
        success=result["success"],
    )
