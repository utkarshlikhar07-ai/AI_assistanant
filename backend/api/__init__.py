"""
JARVIS AI - API Router Aggregator
Exports all routers for use in main.py.
Other agents will add their full implementations to this package;
this module re-exports whatever is available and falls back to stubs.
"""
from fastapi import APIRouter

# ─── Assistant Router ─────────────────────────────────────────────────────────
try:
    from backend.api.assistant import router as assistant_router
except ImportError:
    assistant_router = APIRouter()

# ─── Algorithms Router ────────────────────────────────────────────────────────
try:
    from backend.api.algorithms import router as algorithms_router
except ImportError:
    algorithms_router = APIRouter()

# ─── Puzzles Router ───────────────────────────────────────────────────────────
try:
    from backend.api.puzzles import router as puzzles_router
except ImportError:
    puzzles_router = APIRouter()

# ─── Probabilistic Router ─────────────────────────────────────────────────────
try:
    from backend.api.probabilistic import router as probabilistic_router
except ImportError:
    probabilistic_router = APIRouter()

__all__ = [
    "assistant_router",
    "algorithms_router",
    "puzzles_router",
    "probabilistic_router",
]
