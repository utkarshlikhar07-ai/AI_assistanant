"""
JARVIS AI - Pydantic v2 Schemas
"""
from typing import Optional
from pydantic import BaseModel, Field


# ─── Graph / Search ───────────────────────────────────────────────────────────

class GraphRequest(BaseModel):
    nodes: list[str]
    edges: list[list]
    start: str
    goal: Optional[str] = None
    weighted: bool = False
    heuristics: dict[str, float] = Field(default_factory=dict)


class GraphResponse(BaseModel):
    traversal_order: list[str]
    path: list[str]
    visited_nodes: list[str]
    steps: list[dict]
    cost: float
    algorithm: str
    message: str
    success: bool


class AStarRequest(BaseModel):
    nodes: list[str]
    edges: list[dict]
    start: str
    goal: str
    heuristics: dict[str, float]


class DStarRequest(BaseModel):
    grid_size: int = 10
    start: list[int] = Field(default_factory=lambda: [0, 0])
    goal: list[int] = Field(default_factory=lambda: [9, 9])
    obstacles: list[list[int]] = Field(default_factory=list)


class DStarResponse(BaseModel):
    path: list[list[int]]
    replanning_steps: list[dict]
    message: str
    success: bool


# ─── Optimization ─────────────────────────────────────────────────────────────

class HillClimbingRequest(BaseModel):
    initial_x: float = 0.0
    func_type: str = "multimodal"
    max_iterations: int = 1000
    step_size: float = 0.1


class SimAnnealRequest(BaseModel):
    initial_x: float = 0.0
    initial_temp: float = 1000.0
    cooling_rate: float = 0.995
    max_iterations: int = 1000
    func_type: str = "multimodal"


class OptimizationResponse(BaseModel):
    best_x: float
    best_value: float
    history: list[dict]
    iterations: int
    message: str
    success: bool


# ─── Wumpus World ─────────────────────────────────────────────────────────────

class WumpusRequest(BaseModel):
    grid_size: int = 4
    seed: Optional[int] = None


class WumpusAction(BaseModel):
    action: str
    direction: Optional[str] = None


class WumpusResponse(BaseModel):
    grid_state: list[list[dict]]
    agent_pos: list[int]
    percepts: dict
    knowledge: dict
    game_status: str
    message: str
    success: bool


# ─── 8-Puzzle ─────────────────────────────────────────────────────────────────

class EightPuzzleRequest(BaseModel):
    initial_state: list[list[int]]
    heuristic: str = "manhattan"


class EightPuzzleResponse(BaseModel):
    solution_path: list[list[list[int]]]
    moves: int
    explored_states: int
    time_taken: float
    message: str
    success: bool
    is_solvable: bool


# ─── Tower of Hanoi ───────────────────────────────────────────────────────────

class HanoiRequest(BaseModel):
    num_disks: int = 3


class HanoiResponse(BaseModel):
    moves: list[dict]
    total_moves: int
    message: str
    success: bool


# ─── Assistant ────────────────────────────────────────────────────────────────

class AssistantRequest(BaseModel):
    message: str
    conversation_history: list[dict] = Field(default_factory=list)


class AssistantResponse(BaseModel):
    response: str
    intent: str
    data: Optional[dict] = None
    navigate_to: Optional[str] = None
    success: bool = True
    llm_powered: Optional[bool] = False


# ─── Probabilistic ────────────────────────────────────────────────────────────

class BayesianRequest(BaseModel):
    evidence: dict[str, bool] = Field(default_factory=dict)


class BayesianResponse(BaseModel):
    probabilities: dict
    explanation: str
    network_structure: dict
    success: bool


class EMRequest(BaseModel):
    n_samples: int = 200
    n_components: int = 3
    max_iterations: int = 100
    seed: int = 42


class EMResponse(BaseModel):
    clusters: list[dict]
    log_likelihood_history: list[float]
    iterations: int
    converged: bool
    message: str
    success: bool


class HMMRequest(BaseModel):
    observations: list[str]
    algorithm: str = "both"


class HMMResponse(BaseModel):
    forward_prob: float
    viterbi_path: list[str]
    viterbi_prob: float
    state_probs: list[dict]
    message: str
    success: bool


# ─── IDDFS ────────────────────────────────────────────────────────────────────

class IDDFSRequest(BaseModel):
    nodes: list[str]
    edges: list[list]
    start: str
    goal: str
    max_depth: int = 10


class IDDFSResponse(BaseModel):
    found: bool
    path: list[str]
    depth_found: int
    iterations: list[dict]
    nodes_explored: int
    message: str
    success: bool


# ─── LLM / Gemini ─────────────────────────────────────────────────────────────

class LLMStatusResponse(BaseModel):
    enabled: bool
    configured: bool
    active_model: str
    masked_key: str
    available_models: list[str]


class LLMConfigureRequest(BaseModel):
    api_key: str
    model: Optional[str] = None


class LLMConfigureResponse(BaseModel):
    success: bool
    message: str
    active_model: Optional[str] = None
    masked_key: Optional[str] = None


class LLMTestRequest(BaseModel):
    api_key: Optional[str] = None
    model: Optional[str] = None


class LLMTestResponse(BaseModel):
    success: bool
    message: str
    model: Optional[str] = None
