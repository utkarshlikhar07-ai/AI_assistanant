import pytest
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

class TestEightPuzzle:
    def test_solvable_detection(self):
        from backend.problems.eight_puzzle import is_solvable
        solvable = [1,2,3,4,5,6,7,8,0]  # already solved
        assert is_solvable(solvable) == True
    
    def test_unsolvable_detection(self):
        from backend.problems.eight_puzzle import is_solvable
        unsolvable = [1,2,3,4,5,6,8,7,0]  # one swap = unsolvable
        assert is_solvable(unsolvable) == False
    
    def test_simple_solve(self):
        from backend.problems.eight_puzzle import solve_puzzle
        # Nearly solved - just move blank
        initial = [[1,2,3],[4,5,6],[7,0,8]]
        result = solve_puzzle(initial, 'manhattan')
        assert result['is_solvable'] == True
        if result['success']:
            assert result['moves'] > 0
    
    def test_validate_duplicate_tiles(self):
        from backend.problems.eight_puzzle import solve_puzzle
        invalid = [[1,1,3],[4,5,6],[7,8,0]]
        result = solve_puzzle(invalid, 'manhattan')
        # Should handle gracefully
        assert 'success' in result

class TestHanoi:
    def test_hanoi_3_disks(self):
        from backend.problems.towers_of_hanoi import hanoi
        result = hanoi(3)
        assert result['total_moves'] == 7  # 2^3 - 1
        assert result['success'] == True
    
    def test_hanoi_1_disk(self):
        from backend.problems.towers_of_hanoi import hanoi
        result = hanoi(1)
        assert result['total_moves'] == 1
    
    def test_hanoi_move_count_formula(self):
        from backend.problems.towers_of_hanoi import hanoi
        for n in range(1, 7):
            result = hanoi(n)
            assert result['total_moves'] == 2**n - 1
    
    def test_hanoi_has_peg_states(self):
        from backend.problems.towers_of_hanoi import hanoi
        result = hanoi(3)
        assert all('pegs_state' in m for m in result['moves'])

class TestWumpusWorld:
    def test_world_creation(self):
        from backend.problems.wumpus_world import WumpusWorld
        world = WumpusWorld(4, seed=42)
        assert world.agent_pos == [0, 0]
        assert world.wumpus_alive == True
        assert world.game_over == False
    
    def test_agent_starts_safe(self):
        from backend.problems.wumpus_world import WumpusWorld
        world = WumpusWorld(4, seed=42)
        # [0,0] should not have pit or wumpus
        cell = world.grid[0][0]
        assert not cell.get('pit', False)
        assert not cell.get('wumpus', False)
    
    def test_percepts_at_start(self):
        from backend.problems.wumpus_world import WumpusWorld
        world = WumpusWorld(4, seed=42)
        percepts = world.get_percepts()
        assert 'stench' in percepts
        assert 'breeze' in percepts
        assert 'glitter' in percepts
    
    def test_gold_collection(self):
        from backend.problems.wumpus_world import WumpusWorld
        world = WumpusWorld(4, seed=42)
        # Manually place gold at agent position
        world.grid[0][0]['gold'] = True
        world.grab_gold()
        assert world.has_gold == True
