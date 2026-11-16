"""
JARVIS AI - Assistant API Router
Handles conversational AI interactions, system capabilities, and conversation state.
"""
from fastapi import APIRouter, HTTPException
from backend.models.schemas import AssistantRequest, AssistantResponse
from backend.services.assistant_service import process_message

router = APIRouter()


@router.post("/chat", response_model=AssistantResponse)
async def chat(request: AssistantRequest):
    """
    Main chat endpoint.
    Processes user query and returns intelligent JARVIS assistant response with navigation instructions.
    """
    if not request.message or not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty.")

    result = await process_message(request.message.strip(), request.conversation_history)

    return AssistantResponse(
        response=result.get("response", "I could not generate a response."),
        intent=result.get("intent", "GENERAL_QUERY"),
        data=result.get("data"),
        navigate_to=result.get("navigate_to"),
        success=result.get("success", True),
    )


@router.get("/capabilities")
async def get_capabilities():
    """
    Return comprehensive list of JARVIS AI capabilities and example commands.
    """
    return {
        "capabilities": [
            "Graph traversal: BFS, DFS, IDDFS",
            "Shortest path: A*, D* Lite",
            "Optimization: Hill Climbing, Simulated Annealing",
            "Puzzle solving: 8-Puzzle with A*",
            "Wumpus World simulation",
            "Towers of Hanoi",
            "Bayesian Network inference",
            "EM Algorithm with Gaussian Mixtures",
            "Hidden Markov Model (Forward + Viterbi)",
            "Mathematical calculations",
            "Algorithm explanations",
        ],
        "example_commands": [
            "Find the shortest path from A to G using BFS",
            "Run DFS on a graph starting from A",
            "Solve the 8-puzzle",
            "Show me Wumpus World",
            "Explain how A* works",
            "Run simulated annealing to find the maximum",
            "Predict weather states using HMM for Walk, Shop, Walk",
            "Solve Tower of Hanoi with 4 disks",
            "Run Bayesian network with Rain=True evidence",
        ],
    }


@router.delete("/conversation")
async def clear_conversation():
    """
    Clear current conversation context and memory.
    """
    return {"message": "Conversation cleared", "success": True}


@router.get("/intents")
async def list_intents():
    """
    Return all supported intent names.
    """
    from backend.core import intent_recognition as ir
    return {
        "intents": [
            ir.GREETING, ir.HELP, ir.BFS_REQUEST, ir.DFS_REQUEST,
            ir.IDDFS_REQUEST, ir.ASTAR_REQUEST, ir.DSTAR_REQUEST,
            ir.PUZZLE_8_REQUEST, ir.WUMPUS_REQUEST, ir.HANOI_REQUEST,
            ir.HILL_CLIMBING_REQUEST, ir.SIMULATED_ANNEALING_REQUEST,
            ir.OPTIMIZATION_REQUEST, ir.PROBABILITY_REQUEST,
            ir.HMM_REQUEST, ir.EM_REQUEST,
            ir.EXPLAIN_ALGORITHM, ir.CALCULATION, ir.GENERAL_QUERY,
        ]
    }
