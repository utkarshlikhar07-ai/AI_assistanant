"""
JARVIS AI - Algorithms API Router
Connects search, pathfinding, and optimization endpoints to implementations.
"""
import os
import sys
from fastapi import APIRouter, HTTPException

# Ensure mini_project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from backend.models.schemas import (
    GraphRequest,
    GraphResponse,
    AStarRequest,
    DStarRequest,
    DStarResponse,
    HillClimbingRequest,
    SimAnnealRequest,
    OptimizationResponse,
    IDDFSRequest,
    IDDFSResponse,
)
from backend.algorithms.bfs import bfs
from backend.algorithms.dfs import dfs
from backend.algorithms.iddfs import iddfs
from backend.algorithms.astar import astar
from backend.algorithms.dstar import dstar_plan, DStarLite
from backend.algorithms.hill_climbing import hill_climbing
from backend.algorithms.simulated_annealing import simulated_annealing

router = APIRouter()


def build_graph(nodes: list, edges: list, weighted: bool = False) -> dict:
    """
    Convert list of [src, dst] or [src, dst, weight] or edge dicts to adjacency dict.
    Undirected graph representation.
    """
    graph: dict = {str(n): [] for n in nodes}
    for edge in edges:
        if isinstance(edge, dict):
            src = str(edge.get("src") or edge.get("from") or edge.get("source") or edge.get("u", ""))
            dst = str(edge.get("dst") or edge.get("to") or edge.get("target") or edge.get("v", ""))
            if not src or not dst:
                continue
            weight_val = edge.get("weight") if "weight" in edge else edge.get("cost", 1.0)
            try:
                weight = float(weight_val)
            except (ValueError, TypeError):
                weight = 1.0

            if src not in graph:
                graph[src] = []
            if dst not in graph:
                graph[dst] = []

            if weighted:
                graph[src].append((dst, weight))
                graph[dst].append((src, weight))
            else:
                graph[src].append(dst)
                graph[dst].append(src)

        elif isinstance(edge, (list, tuple)) and len(edge) >= 2:
            src, dst = str(edge[0]), str(edge[1])
            if src not in graph:
                graph[src] = []
            if dst not in graph:
                graph[dst] = []

            if weighted:
                weight = float(edge[2]) if len(edge) > 2 else 1.0
                graph[src].append((dst, weight))
                graph[dst].append((src, weight))
            else:
                graph[src].append(dst)
                graph[dst].append(src)

    return graph


@router.post("/bfs", response_model=GraphResponse)
async def run_bfs(request: GraphRequest):
    """
    Run Breadth-First Search on the given graph.
    """
    if not request.nodes:
        raise HTTPException(status_code=400, detail="Graph nodes list cannot be empty.")

    if request.start not in request.nodes:
        raise HTTPException(
            status_code=400,
            detail=f"Start node '{request.start}' not found in graph nodes."
        )

    if request.goal and request.goal not in request.nodes:
        raise HTTPException(
            status_code=400,
            detail=f"Goal node '{request.goal}' not found in graph nodes."
        )

    graph = build_graph(request.nodes, request.edges, weighted=request.weighted)
    result = bfs(graph, request.start, request.goal)

    success = bool(result.get("path")) if request.goal else bool(result.get("traversal_order"))

    return GraphResponse(
        traversal_order=result.get("traversal_order", []),
        path=result.get("path", []),
        visited_nodes=result.get("visited_nodes", []),
        steps=result.get("steps", []),
        cost=float(result.get("cost", 0.0)),
        algorithm="BFS",
        message=result.get("message", "BFS completed successfully."),
        success=success,
    )


@router.post("/dfs", response_model=GraphResponse)
async def run_dfs(request: GraphRequest):
    """
    Run Depth-First Search on the given graph.
    """
    if not request.nodes:
        raise HTTPException(status_code=400, detail="Graph nodes list cannot be empty.")

    if request.start not in request.nodes:
        raise HTTPException(
            status_code=400,
            detail=f"Start node '{request.start}' not found in graph nodes."
        )

    if request.goal and request.goal not in request.nodes:
        raise HTTPException(
            status_code=400,
            detail=f"Goal node '{request.goal}' not found in graph nodes."
        )

    graph = build_graph(request.nodes, request.edges, weighted=request.weighted)
    result = dfs(graph, request.start, request.goal)

    success = bool(result.get("path")) if request.goal else bool(result.get("traversal_order"))

    return GraphResponse(
        traversal_order=result.get("traversal_order", []),
        path=result.get("path", []),
        visited_nodes=result.get("visited_nodes", []),
        steps=result.get("steps", []),
        cost=float(result.get("cost", 0.0)),
        algorithm="DFS",
        message=result.get("message", "DFS completed successfully."),
        success=success,
    )


@router.post("/iddfs", response_model=IDDFSResponse)
async def run_iddfs(request: IDDFSRequest):
    """
    Run Iterative Deepening Depth-First Search.
    """
    if not request.nodes:
        raise HTTPException(status_code=400, detail="Graph nodes list cannot be empty.")

    if request.start not in request.nodes:
        raise HTTPException(
            status_code=400,
            detail=f"Start node '{request.start}' not found in graph nodes."
        )

    if request.goal not in request.nodes:
        raise HTTPException(
            status_code=400,
            detail=f"Goal node '{request.goal}' not found in graph nodes."
        )

    if request.max_depth < 0:
        raise HTTPException(status_code=400, detail="max_depth must be non-negative.")

    graph = build_graph(request.nodes, request.edges, weighted=False)
    result = iddfs(graph, request.start, request.goal, request.max_depth)

    return IDDFSResponse(
        found=result.get("found", False),
        path=result.get("path", []),
        depth_found=result.get("depth_found", -1),
        iterations=result.get("iterations", []),
        nodes_explored=result.get("nodes_explored", 0),
        message=result.get("message", "IDDFS completed."),
        success=result.get("found", False),
    )


@router.post("/astar")
async def run_astar(request: AStarRequest):
    """
    Run A* Search on a weighted graph with heuristics.
    """
    if not request.nodes:
        raise HTTPException(status_code=400, detail="Graph nodes list cannot be empty.")

    if request.start not in request.nodes:
        raise HTTPException(
            status_code=400,
            detail=f"Start node '{request.start}' not found in graph nodes."
        )

    if request.goal not in request.nodes:
        raise HTTPException(
            status_code=400,
            detail=f"Goal node '{request.goal}' not found in graph nodes."
        )

    graph = build_graph(request.nodes, request.edges, weighted=True)
    result = astar(graph, request.start, request.goal, request.heuristics)

    success = result.get("success", bool(result.get("path")))

    return {
        "traversal_order": result.get("visited_nodes", []),
        "path": result.get("path", []),
        "visited_nodes": result.get("visited_nodes", []),
        "steps": result.get("steps", []),
        "cost": float(result.get("cost", 0.0)),
        "algorithm": "A*",
        "message": result.get("message", "A* search completed."),
        "success": success,
    }


@router.post("/dstar", response_model=DStarResponse)
async def run_dstar(request: DStarRequest):
    """
    Run D* Lite dynamic pathfinding on an NxN grid.
    """
    if not (5 <= request.grid_size <= 50):
        raise HTTPException(
            status_code=400,
            detail="grid_size must be between 5 and 50."
        )

    if len(request.start) != 2 or not (0 <= request.start[0] < request.grid_size and 0 <= request.start[1] < request.grid_size):
        raise HTTPException(
            status_code=400,
            detail=f"Start coordinate {request.start} is out of bounds for {request.grid_size}x{request.grid_size} grid."
        )

    if len(request.goal) != 2 or not (0 <= request.goal[0] < request.grid_size and 0 <= request.goal[1] < request.grid_size):
        raise HTTPException(
            status_code=400,
            detail=f"Goal coordinate {request.goal} is out of bounds for {request.grid_size}x{request.grid_size} grid."
        )

    result = dstar_plan(
        grid_size=request.grid_size,
        start=request.start,
        goal=request.goal,
        obstacles=request.obstacles,
    )

    return DStarResponse(
        path=result.get("path", []),
        replanning_steps=result.get("replanning_steps", []),
        message=result.get("message", "D* planning completed."),
        success=result.get("success", False),
    )


@router.post("/hill-climbing", response_model=OptimizationResponse)
async def run_hill_climbing(request: HillClimbingRequest):
    """
    Run Steepest-Ascent Hill Climbing continuous optimization.
    """
    if request.step_size <= 0:
        raise HTTPException(status_code=400, detail="step_size must be positive.")

    if request.max_iterations <= 0:
        raise HTTPException(status_code=400, detail="max_iterations must be positive.")

    result = hill_climbing(
        initial_x=request.initial_x,
        func_type=request.func_type,
        max_iterations=request.max_iterations,
        step_size=request.step_size,
    )

    return OptimizationResponse(
        best_x=float(result.get("best_x", 0.0)),
        best_value=float(result.get("best_value", 0.0)),
        history=result.get("history", []),
        iterations=int(result.get("iterations", 0)),
        message=result.get("message", "Hill Climbing optimization completed."),
        success=result.get("success", True),
    )


@router.post("/simulated-annealing", response_model=OptimizationResponse)
async def run_simulated_annealing(request: SimAnnealRequest):
    """
    Run Simulated Annealing optimization with Boltzmann acceptance probability.
    """
    if request.initial_temp <= 0:
        raise HTTPException(status_code=400, detail="initial_temp must be positive.")

    if not (0 < request.cooling_rate < 1):
        raise HTTPException(status_code=400, detail="cooling_rate must be between 0 and 1.")

    if request.max_iterations <= 0:
        raise HTTPException(status_code=400, detail="max_iterations must be positive.")

    result = simulated_annealing(
        initial_x=request.initial_x,
        initial_temp=request.initial_temp,
        cooling_rate=request.cooling_rate,
        max_iterations=request.max_iterations,
        func_type=request.func_type,
    )

    return OptimizationResponse(
        best_x=float(result.get("best_x", 0.0)),
        best_value=float(result.get("best_value", 0.0)),
        history=result.get("history", []),
        iterations=int(result.get("iterations", 0)),
        message=result.get("message", "Simulated Annealing optimization completed."),
        success=result.get("success", True),
    )


@router.get("/sample-graph")
async def get_sample_graph():
    """
    Return a sample pre-configured graph for demonstration and testing.
    """
    return {
        "nodes": ["A", "B", "C", "D", "E", "F", "G"],
        "edges": [
            ["A", "B"],
            ["A", "C"],
            ["B", "D"],
            ["B", "E"],
            ["C", "F"],
            ["D", "G"],
            ["E", "G"],
            ["F", "G"],
        ],
        "weighted_edges": [
            {"src": "A", "dst": "B", "weight": 4},
            {"src": "A", "dst": "C", "weight": 2},
            {"src": "B", "dst": "D", "weight": 5},
            {"src": "B", "dst": "E", "weight": 10},
            {"src": "C", "dst": "F", "weight": 3},
            {"src": "D", "dst": "G", "weight": 2},
            {"src": "E", "dst": "G", "weight": 4},
            {"src": "F", "dst": "G", "weight": 6},
        ],
        "heuristics": {
            "A": 10,
            "B": 8,
            "C": 5,
            "D": 7,
            "E": 3,
            "F": 6,
            "G": 0,
        },
    }
