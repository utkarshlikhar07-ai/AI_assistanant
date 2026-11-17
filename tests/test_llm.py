"""
JARVIS AI - Google Gemini LLM Integration Tests
Comprehensive unit and integration tests for:
- LLM Service initialization, masking, and model resolution
- Multi-turn conversation pruning and history formatting
- Algorithm tool dispatchers and context tracking
- LLM API endpoints (/api/llm/status, /api/llm/configure, /api/llm/test-connection)
- Assistant service chat with mocked Gemini responses and offline fallback
"""

import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from backend.main import app
from backend.services.llm_service import (
    LLMService,
    GeminiLLMService,
    llm_service,
    execute_bfs,
    execute_dfs,
    execute_iddfs,
    execute_eight_puzzle,
    execute_towers_of_hanoi,
    execute_bayesian_network,
    get_and_clear_tool_context,
)
from backend.services.assistant_service import process_message


@pytest.fixture
def client():
    return TestClient(app)


def test_llm_service_masked_key():
    """Verify that sensitive API keys are properly masked."""
    service = GeminiLLMService()
    service._api_key = "AQ.Ab8RN6Lxmhr5Lw8tUwXaB2xyjtKpMB98RQ9KN9Uh4Yl3d84CVw"
    masked = service.get_masked_key()
    assert masked is not None
    assert masked.startswith("AQ.Ab8")
    assert masked.endswith("4CVw")
    assert "..." in masked
    assert "B2xyjtKpMB98" not in masked


def test_llm_service_masked_key_none():
    """Verify behavior when no key is set."""
    service = GeminiLLMService()
    service._api_key = None
    assert service.get_masked_key() is None


def test_llm_service_model_alias_resolution():
    """Verify that deprecated/alias model names resolve to valid active models."""
    service = GeminiLLMService()
    assert service._resolve_model_name("gemini-flash-latest") == "gemini-3.5-flash"
    assert service._resolve_model_name("gemini-2.5-flash") == "gemini-3.5-flash"
    assert service._resolve_model_name("gemini-3.8-flash") == "gemini-3.8-flash"


def test_llm_service_history_pruning():
    """Verify conversation history pruning retains recent turns."""
    service = GeminiLLMService()
    # Create 30 turns
    history = []
    for i in range(15):
        history.append({"role": "user", "content": f"User question {i}"})
        history.append({"role": "assistant", "content": f"Assistant answer {i}"})

    contents = service._format_history_for_gemini(history, max_turns=10)
    assert len(contents) == 10
    assert contents[0].role == "user"
    assert contents[-1].role == "model"


def test_llm_tools_execution():
    """Verify that LLM algorithm tool functions directly call deterministic algorithms."""
    # BFS tool
    bfs_res = execute_bfs("A", "D")
    assert "Breadth-First Search" in bfs_res["algorithm"]
    assert "traversal_order" in bfs_res
    assert "path" in bfs_res
    assert get_and_clear_tool_context() is not None

    # 8-Puzzle tool
    puzzle_res = execute_eight_puzzle("manhattan")
    assert "8-Puzzle" in puzzle_res["algorithm"]
    assert puzzle_res["is_solvable"] is True
    assert puzzle_res["total_moves"] >= 0

    # Towers of Hanoi tool
    hanoi_res = execute_towers_of_hanoi(3)
    assert hanoi_res["total_moves"] == 7

    # Bayesian Network tool
    bayes_res = execute_bayesian_network(cloudy=True)
    assert "computed_posterior_probabilities" in bayes_res


def test_api_llm_status(client):
    """Test GET /api/llm/status returns masked key and configuration state."""
    response = client.get("/api/llm/status")
    assert response.status_code == 200
    data = response.json()
    assert "enabled" in data
    assert "configured" in data
    assert "active_model" in data
    assert "masked_key" in data
    assert "available_models" in data
    if data["masked_key"]:
        assert "..." in data["masked_key"]


def test_api_llm_configure_validation(client):
    """Test POST /api/llm/configure rejects empty keys."""
    response = client.post("/api/llm/configure", json={"api_key": "   "})
    assert response.status_code == 400


def test_api_llm_test_connection_mocked(client):
    """Test POST /api/llm/test-connection with mocked response."""
    with patch.object(llm_service, "test_connection") as mock_test:
        mock_test.return_value = {
            "success": True,
            "message": "Connection established successfully.",
            "model": "gemini-3.5-flash",
        }
        response = client.post("/api/llm/test-connection", json={
            "api_key": "test_fake_key",
            "model": "gemini-3.5-flash",
        })
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "gemini-3.5-flash" in data["model"]


@pytest.mark.asyncio
async def test_assistant_chat_llm_fallback():
    """Verify that AssistantService gracefully falls back to deterministic rule engine if LLM fails."""
    with patch.object(llm_service, "is_configured", return_value=False):
        res = await process_message("hello jarvis", [])
        assert res["response"] != ""
        assert res["intent"] == "greeting"
        assert res.get("llm_powered") is False


@pytest.mark.asyncio
async def test_assistant_chat_llm_success():
    """Verify that AssistantService returns llm_powered=True and structured data when LLM succeeds."""
    mock_llm_result = {
        "success": True,
        "response": "Breadth-First Search traverses level by level.",
        "intent": "BFS_REQUEST",
        "data": {
            "algorithm": "BFS",
            "traversal_order": ["A", "B", "C"],
            "path": ["A", "C"],
            "visited_nodes": ["A", "B", "C"],
        },
        "navigate_to": "search",
        "model": "gemini-3.5-flash",
    }

    with patch.object(llm_service, "is_configured", return_value=True):
        with patch.object(llm_service, "chat") as mock_chat:
            mock_chat.return_value = mock_llm_result

            res = await process_message("run bfs for me", [])
            assert "Breadth-First Search" in res["response"]
            assert res["llm_powered"] is True
            assert res["data"] is not None
            assert res["data"]["algorithm"] == "BFS"
            assert res["navigate_to"] == "search"
