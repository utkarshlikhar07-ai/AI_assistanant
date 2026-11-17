"""
JARVIS AI - Main FastAPI Application
"""
import os
import sys
from contextlib import asynccontextmanager
from pathlib import Path

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
BACKEND_DIR = Path(__file__).resolve().parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from dotenv import load_dotenv

load_dotenv()

# Import routers
try:
    from backend.api import assistant_router, algorithms_router, puzzles_router, probabilistic_router, llm_router
except ImportError:
    from api import assistant_router, algorithms_router, puzzles_router, probabilistic_router, llm_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    print("JARVIS AI backend starting up...")
    yield
    print("JARVIS AI backend shutting down...")


app = FastAPI(
    title="JARVIS AI",
    description="Just A Rather Very Intelligent System - AI Backend",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS middleware - allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(assistant_router, prefix="/api/assistant", tags=["assistant"])
app.include_router(algorithms_router, prefix="/api/algorithms", tags=["algorithms"])
app.include_router(puzzles_router, prefix="/api/puzzles", tags=["puzzles"])
app.include_router(probabilistic_router, prefix="/api/probabilistic", tags=["probabilistic"])
app.include_router(llm_router, prefix="/api/llm", tags=["llm"])


@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok", "message": "JARVIS AI is online", "version": "1.0.0"}


# Mount frontend static files
frontend_path = Path(__file__).parent.parent / "frontend"
if frontend_path.exists():
    css_path = frontend_path / "css"
    js_path = frontend_path / "js"
    assets_path = frontend_path / "assets"

    if css_path.exists():
        app.mount("/css", StaticFiles(directory=str(css_path)), name="css")
    if js_path.exists():
        app.mount("/js", StaticFiles(directory=str(js_path)), name="js")
    if assets_path.exists():
        app.mount("/assets", StaticFiles(directory=str(assets_path)), name="assets")

    app.mount("/static", StaticFiles(directory=str(frontend_path)), name="static")

    @app.get("/")
    async def serve_index():
        """Serve the frontend index.html."""
        index_file = frontend_path / "index.html"
        if index_file.exists():
            return FileResponse(str(index_file))
        return JSONResponse({"message": "Frontend not found"}, status_code=404)
else:
    @app.get("/")
    async def serve_root():
        return {"message": "JARVIS AI is online", "version": "1.0.0"}


if __name__ == "__main__":
    import uvicorn
    host = os.getenv("APP_HOST", "127.0.0.1")
    port = int(os.getenv("APP_PORT", "8000"))
    debug = os.getenv("APP_DEBUG", "false").lower() == "true"
    uvicorn.run("backend.main:app", host=host, port=port, reload=debug)
