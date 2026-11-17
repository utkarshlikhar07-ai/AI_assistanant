"""
JARVIS AI - LLM API Router
Endpoints for managing Google Gemini API configuration, connection testing, and model status.
"""

from fastapi import APIRouter, HTTPException
from backend.models.schemas import (
    LLMStatusResponse,
    LLMConfigureRequest,
    LLMConfigureResponse,
    LLMTestRequest,
    LLMTestResponse,
)
from backend.services.llm_service import llm_service

router = APIRouter()


@router.get("/status", response_model=LLMStatusResponse)
async def get_llm_status():
    """
    Returns the current status of the Google Gemini LLM integration.
    Never exposes the raw API key; only a masked representation.
    """
    return LLMStatusResponse(
        enabled=llm_service.is_configured(),
        configured=llm_service.is_configured(),
        active_model=llm_service.get_model_name(),
        masked_key=llm_service.get_masked_key(),
        available_models=llm_service.AVAILABLE_MODELS,
    )


@router.post("/configure", response_model=LLMConfigureResponse)
async def configure_llm(request: LLMConfigureRequest):
    """
    Configure the Google Gemini API key and active model.
    The key is stored securely server-side and persisted to .env.
    """
    if not request.api_key or not request.api_key.strip():
        raise HTTPException(status_code=400, detail="API key cannot be empty.")

    result = llm_service.set_configuration(
        api_key=request.api_key.strip(),
        model_name=request.model,
        persist=True,
    )

    return LLMConfigureResponse(
        success=result["success"],
        message=result["message"],
        active_model=result.get("active_model"),
        masked_key=result.get("masked_key"),
    )


@router.post("/test-connection", response_model=LLMTestResponse)
async def test_llm_connection(request: LLMTestRequest = None):
    """
    Validate the Google Gemini API key by making a lightweight test ping.
    Does not consume user quota with large prompts.
    """
    api_key = request.api_key if request else None
    model = request.model if request else None

    result = await llm_service.test_connection(api_key=api_key, model=model)
    return LLMTestResponse(
        success=result["success"],
        message=result["message"],
        model=result.get("model"),
    )
