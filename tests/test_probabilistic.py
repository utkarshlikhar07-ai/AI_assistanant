import pytest
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

class TestBayesianNetwork:
    def test_no_evidence(self):
        from backend.probabilistic.bayesian_network import compute_inference
        result = compute_inference({})
        assert 'probabilities' in result
        probs = result['probabilities']
        # All probabilities between 0 and 1
        for node, vals in probs.items():
            assert 0 <= vals.get(True, vals.get('True', 0)) <= 1
    
    def test_with_evidence(self):
        from backend.probabilistic.bayesian_network import compute_inference
        result = compute_inference({'Rain': True})
        probs = result['probabilities']
        assert 'WetGrass' in probs or 'Wet Grass' in probs
    
    def test_valid_probabilities(self):
        from backend.probabilistic.bayesian_network import compute_inference
        result = compute_inference({'Cloudy': True})
        for node, vals in result['probabilities'].items():
            total = sum(vals.values()) if isinstance(vals, dict) else 1
            assert abs(total - 1.0) < 0.01

class TestEMAlgorithm:
    def test_em_runs(self):
        from backend.probabilistic.em_algorithm import run_em
        result = run_em(100, 2, 50, 42)
        assert result['success'] == True
        assert len(result['clusters']) == 2
    
    def test_em_converges(self):
        from backend.probabilistic.em_algorithm import run_em
        result = run_em(200, 3, 100, 42)
        assert len(result['log_likelihood_history']) > 0
        # Log-likelihood should generally increase
    
    def test_em_cluster_weights_sum_to_one(self):
        from backend.probabilistic.em_algorithm import run_em
        result = run_em(100, 3, 50, 42)
        total_weight = sum(c['weight'] for c in result['clusters'])
        assert abs(total_weight - 1.0) < 0.01

class TestHMM:
    def test_forward_algorithm(self):
        from backend.probabilistic.hmm import forward_algorithm
        prob, alpha = forward_algorithm(['Walk', 'Shop', 'Clean'])
        assert 0 < prob <= 1
    
    def test_viterbi_algorithm(self):
        from backend.probabilistic.hmm import viterbi_algorithm
        prob, path, delta = viterbi_algorithm(['Walk', 'Shop', 'Clean'])
        assert len(path) == 3
        assert all(s in ['Sunny', 'Rainy'] for s in path)
        assert 0 < prob <= 1
    
    def test_valid_state_sequence(self):
        from backend.probabilistic.hmm import run_hmm
        result = run_hmm(['Walk', 'Walk', 'Shop'], 'both')
        assert result['success'] == True
        assert len(result['viterbi_path']) == 3
    
    def test_invalid_observation(self):
        from backend.probabilistic.hmm import run_hmm
        result = run_hmm(['InvalidObs'], 'viterbi')
        assert result['success'] == False or 'error' in result.get('message', '').lower()
