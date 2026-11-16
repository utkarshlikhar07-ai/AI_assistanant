import pytest
from fastapi.testclient import TestClient
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

@pytest.fixture
def client():
    from backend.main import app
    return TestClient(app)

class TestHealthEndpoint:
    def test_health_check(self, client):
        response = client.get('/api/health')
        assert response.status_code == 200
        data = response.json()
        assert data['status'] == 'ok'

class TestAssistantAPI:
    def test_chat_basic(self, client):
        response = client.post('/api/assistant/chat', json={'message': 'Hello JARVIS', 'conversation_history': []})
        assert response.status_code == 200
        data = response.json()
        assert 'response' in data
        assert data['success'] == True
    
    def test_chat_bfs_intent(self, client):
        response = client.post('/api/assistant/chat', json={'message': 'explain BFS algorithm', 'conversation_history': []})
        assert response.status_code == 200
        data = response.json()
        assert 'bfs' in data['response'].lower() or 'breadth' in data['response'].lower()
    
    def test_capabilities(self, client):
        response = client.get('/api/assistant/capabilities')
        assert response.status_code == 200

class TestAlgorithmsAPI:
    SAMPLE_GRAPH = {
        'nodes': ['A','B','C','D'],
        'edges': [['A','B'],['B','C'],['C','D'],['A','D']],
        'start': 'A',
        'goal': 'D',
        'weighted': False,
        'heuristics': {}
    }
    
    def test_bfs_endpoint(self, client):
        response = client.post('/api/algorithms/bfs', json=self.SAMPLE_GRAPH)
        assert response.status_code == 200
        data = response.json()
        assert data['success'] == True
        assert 'path' in data
    
    def test_dfs_endpoint(self, client):
        response = client.post('/api/algorithms/dfs', json=self.SAMPLE_GRAPH)
        assert response.status_code == 200
    
    def test_iddfs_endpoint(self, client):
        body = {'nodes':['A','B','C'],'edges':[['A','B'],['B','C']],'start':'A','goal':'C','max_depth':5}
        response = client.post('/api/algorithms/iddfs', json=body)
        assert response.status_code == 200
    
    def test_astar_endpoint(self, client):
        body = {
            'nodes': ['A','B','C'],
            'edges': [{'src':'A','dst':'B','weight':1},{'src':'B','dst':'C','weight':2}],
            'start': 'A',
            'goal': 'C',
            'heuristics': {'A':3,'B':2,'C':0}
        }
        response = client.post('/api/algorithms/astar', json=body)
        assert response.status_code == 200
    
    def test_dstar_endpoint(self, client):
        body = {'grid_size':5,'start':[0,0],'goal':[4,4],'obstacles':[]}
        response = client.post('/api/algorithms/dstar', json=body)
        assert response.status_code == 200
    
    def test_hill_climbing_endpoint(self, client):
        body = {'initial_x':0.0,'func_type':'quadratic','max_iterations':100,'step_size':0.1}
        response = client.post('/api/algorithms/hill-climbing', json=body)
        assert response.status_code == 200
    
    def test_sa_endpoint(self, client):
        body = {'initial_x':0.0,'initial_temp':100.0,'cooling_rate':0.95,'max_iterations':100,'func_type':'quadratic'}
        response = client.post('/api/algorithms/simulated-annealing', json=body)
        assert response.status_code == 200

class TestPuzzlesAPI:
    def test_hanoi_endpoint(self, client):
        response = client.post('/api/puzzles/hanoi', json={'num_disks':3})
        assert response.status_code == 200
        data = response.json()
        assert data['total_moves'] == 7
    
    def test_wumpus_new_game(self, client):
        response = client.post('/api/puzzles/wumpus/new', json={'grid_size':4})
        assert response.status_code == 200
    
    def test_eight_puzzle(self, client):
        body = {'initial_state':[[1,2,3],[4,5,6],[7,0,8]],'heuristic':'manhattan'}
        response = client.post('/api/puzzles/eight-puzzle', json=body)
        assert response.status_code == 200

class TestProbabilisticAPI:
    def test_bayesian_endpoint(self, client):
        response = client.post('/api/probabilistic/bayesian', json={'evidence':{}})
        assert response.status_code == 200
        data = response.json()
        assert data['success'] == True
    
    def test_em_endpoint(self, client):
        response = client.post('/api/probabilistic/em', json={'n_samples':50,'n_components':2,'max_iterations':20,'seed':42})
        assert response.status_code == 200
    
    def test_hmm_endpoint(self, client):
        response = client.post('/api/probabilistic/hmm', json={'observations':['Walk','Shop','Clean'],'algorithm':'both'})
        assert response.status_code == 200
        data = response.json()
        assert data['success'] == True
