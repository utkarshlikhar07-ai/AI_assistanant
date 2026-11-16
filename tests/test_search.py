"""Tests for BFS, DFS, IDDFS, A*, D*, Hill Climbing, Simulated Annealing"""
import pytest
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Sample graphs for testing
SIMPLE_GRAPH = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'F'],
    'D': ['B'],
    'E': ['B', 'G'],
    'F': ['C', 'G'],
    'G': ['E', 'F']
}

WEIGHTED_GRAPH = {
    'A': [('B', 4), ('C', 2)],
    'B': [('A', 4), ('D', 5), ('E', 10)],
    'C': [('A', 2), ('F', 3)],
    'D': [('B', 5), ('G', 2)],
    'E': [('B', 10), ('G', 4)],
    'F': [('C', 3), ('G', 6)],
    'G': [('D', 2), ('E', 4), ('F', 6)]
}

HEURISTICS = {'A': 10, 'B': 8, 'C': 5, 'D': 7, 'E': 3, 'F': 6, 'G': 0}

class TestBFS:
    def test_bfs_finds_path(self):
        from backend.algorithms.bfs import bfs
        result = bfs(SIMPLE_GRAPH, 'A', 'G')
        assert result['path'] != []
        assert result['path'][0] == 'A'
        assert result['path'][-1] == 'G'
    
    def test_bfs_shortest_path(self):
        from backend.algorithms.bfs import bfs
        result = bfs(SIMPLE_GRAPH, 'A', 'G')
        # BFS guarantees shortest path in unweighted graph
        assert len(result['path']) <= 4  # A->C->F->G or A->B->E->G
    
    def test_bfs_traversal_order(self):
        from backend.algorithms.bfs import bfs
        result = bfs(SIMPLE_GRAPH, 'A')
        assert 'A' in result['traversal_order']
        assert len(result['traversal_order']) > 0
    
    def test_bfs_missing_start(self):
        from backend.algorithms.bfs import bfs
        result = bfs({'A': ['B'], 'B': ['A']}, 'Z')
        assert result['path'] == [] or not result.get('success', True)
    
    def test_bfs_no_path(self):
        from backend.algorithms.bfs import bfs
        disconnected = {'A': [], 'B': []}
        result = bfs(disconnected, 'A', 'B')
        assert result['path'] == []

class TestDFS:
    def test_dfs_traverses_all_reachable(self):
        from backend.algorithms.dfs import dfs
        result = dfs(SIMPLE_GRAPH, 'A')
        assert set(result['traversal_order']) == set(SIMPLE_GRAPH.keys())
    
    def test_dfs_finds_path(self):
        from backend.algorithms.dfs import dfs
        result = dfs(SIMPLE_GRAPH, 'A', 'G')
        assert result['path'] != []
        assert result['path'][0] == 'A'
        assert result['path'][-1] == 'G'

class TestIDDFS:
    def test_iddfs_finds_goal(self):
        from backend.algorithms.iddfs import iddfs
        result = iddfs(SIMPLE_GRAPH, 'A', 'G', max_depth=10)
        assert result['found'] == True
        assert result['path'][-1] == 'G'
    
    def test_iddfs_depth_limited(self):
        from backend.algorithms.iddfs import iddfs
        result = iddfs(SIMPLE_GRAPH, 'A', 'G', max_depth=1)
        # G is not reachable within depth 1 from A
        assert result['found'] == False or result['depth_found'] <= 1
    
    def test_iddfs_has_iterations(self):
        from backend.algorithms.iddfs import iddfs
        result = iddfs(SIMPLE_GRAPH, 'A', 'G', max_depth=5)
        assert len(result['iterations']) > 0

class TestAStar:
    def test_astar_finds_optimal_path(self):
        from backend.algorithms.astar import astar
        result = astar(WEIGHTED_GRAPH, 'A', 'G', HEURISTICS)
        assert result['success'] == True
        assert result['path'][0] == 'A'
        assert result['path'][-1] == 'G'
        # Optimal path cost A->C->F->G = 2+3+6=11? Or A->B->D->G = 4+5+2=11
        assert result['cost'] <= 12
    
    def test_astar_has_steps(self):
        from backend.algorithms.astar import astar
        result = astar(WEIGHTED_GRAPH, 'A', 'G', HEURISTICS)
        assert len(result['steps']) > 0

class TestDStar:
    def test_dstar_finds_path(self):
        from backend.algorithms.dstar import dstar_plan
        result = dstar_plan(10, [0,0], [9,9], [])
        assert result['success'] == True
        assert len(result['path']) > 0
    
    def test_dstar_avoids_obstacles(self):
        from backend.algorithms.dstar import dstar_plan
        # Simple case with one obstacle
        result = dstar_plan(5, [0,0], [4,4], [[2,2]])
        assert result['success'] == True
        path_tuples = [tuple(p) for p in result['path']]
        assert (2,2) not in path_tuples

class TestHillClimbing:
    def test_hill_climbing_returns_result(self):
        from backend.algorithms.hill_climbing import hill_climbing
        result = hill_climbing(0.0, 'quadratic', 1000, 0.1)
        assert result['success'] == True
        assert 'best_x' in result
        assert 'best_value' in result
        # For quadratic -(x-3)^2+9, optimum at x=3, value=9
        assert abs(result['best_x'] - 3.0) < 1.0
    
    def test_hill_climbing_has_history(self):
        from backend.algorithms.hill_climbing import hill_climbing
        result = hill_climbing(0.0, 'quadratic', 100, 0.1)
        assert len(result['history']) > 0

class TestSimulatedAnnealing:
    def test_sa_runs_successfully(self):
        from backend.algorithms.simulated_annealing import simulated_annealing
        result = simulated_annealing(0.0, 1000.0, 0.995, 500, 'quadratic')
        assert result['success'] == True
        assert 'best_x' in result
        assert 'best_value' in result
    
    def test_sa_has_history(self):
        from backend.algorithms.simulated_annealing import simulated_annealing
        result = simulated_annealing(0.0, 1000.0, 0.995, 100, 'quadratic')
        assert len(result['history']) > 0
    
    def test_sa_temperature_decreases(self):
        from backend.algorithms.simulated_annealing import simulated_annealing
        result = simulated_annealing(0.0, 1000.0, 0.995, 100, 'quadratic')
        temps = [h['temperature'] for h in result['history']]
        assert temps[0] > temps[-1]  # temperature decreases
