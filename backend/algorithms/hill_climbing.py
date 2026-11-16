import numpy as np
import math
from typing import Optional


def objective_function(x: float, func_type: str = "multimodal") -> float:
    """
    Evaluate the objective function at x.

    func_type
    ---------
    'multimodal'  :  x·sin(x) + x·cos(2x)
                     Has many local maxima – ideal for showing the local-optima trap.
    'quadratic'   :  -(x-3)² + 9
                     Single global maximum at x=3, value=9.
    """
    if func_type == "quadratic":
        return -(x - 3.0) ** 2 + 9.0
    # default: multimodal
    return x * math.sin(x) + x * math.cos(2.0 * x)


def hill_climbing(
    initial_x: float,
    func_type: str = "multimodal",
    max_iterations: int = 1000,
    step_size: float = 0.1,
) -> dict:
    """
    Steepest-ascent hill climbing (continuous, 1-D).

    At each iteration the algorithm evaluates two neighbours
    (x − step_size and x + step_size) and moves to the better one if it
    improves the current value.  Terminates when neither neighbour is
    better (local maximum) or the iteration limit is reached.

    Returns
    -------
    dict:
        best_x         : float
        best_value     : float
        history        : list[{iteration, x, value, action}]
        iterations     : int
        message        : str
        success        : bool    (True when a local/global max is confirmed)
        stuck_at_local : bool
    """
    if step_size <= 0:
        return _empty_result("step_size must be positive.")
    if max_iterations <= 0:
        return _empty_result("max_iterations must be positive.")

    current_x     = float(initial_x)
    current_value = objective_function(current_x, func_type)

    history: list[dict] = []
    history.append({
        "iteration": 0,
        "x":         round(current_x, 6),
        "value":     round(current_value, 6),
        "action":    "Initialise",
    })

    for iteration in range(1, max_iterations + 1):
        # Explore two neighbours
        left_x  = current_x - step_size
        right_x = current_x + step_size

        left_v  = objective_function(left_x,  func_type)
        right_v = objective_function(right_x, func_type)

        best_neighbor_x = left_x  if left_v > right_v else right_x
        best_neighbor_v = left_v  if left_v > right_v else right_v

        if best_neighbor_v > current_value:
            action      = f"Move to x={round(best_neighbor_x, 6)} (↑ value)"
            current_x   = best_neighbor_x
            current_value = best_neighbor_v
        else:
            # No improvement – we are at a local maximum
            history.append({
                "iteration": iteration,
                "x":         round(current_x, 6),
                "value":     round(current_value, 6),
                "action":    "No improvement — stuck at local maximum",
            })
            return {
                "best_x":         round(current_x, 6),
                "best_value":     round(current_value, 6),
                "history":        history,
                "iterations":     iteration,
                "message": (
                    f"Stuck at local maximum x={round(current_x,6)}, "
                    f"value={round(current_value,6)} after {iteration} iteration(s)."
                ),
                "success":        True,
                "stuck_at_local": True,
            }

        history.append({
            "iteration": iteration,
            "x":         round(current_x, 6),
            "value":     round(current_value, 6),
            "action":    action,
        })

    return {
        "best_x":         round(current_x, 6),
        "best_value":     round(current_value, 6),
        "history":        history,
        "iterations":     max_iterations,
        "message": (
            f"Reached iteration limit ({max_iterations}). "
            f"Best: x={round(current_x,6)}, value={round(current_value,6)}."
        ),
        "success":        True,
        "stuck_at_local": False,
    }


def _empty_result(message: str) -> dict:
    return {
        "best_x":         0.0,
        "best_value":     0.0,
        "history":        [],
        "iterations":     0,
        "message":        message,
        "success":        False,
        "stuck_at_local": False,
    }
