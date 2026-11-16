from fastapi import APIRouter, HTTPException
from backend.models.schemas import (
    BayesianRequest,
    BayesianResponse,
    EMRequest,
    EMResponse,
    HMMRequest,
    HMMResponse,
)
from backend.probabilistic.bayesian_network import compute_inference
from backend.probabilistic.em_algorithm import run_em
from backend.probabilistic.hmm import run_hmm, OBSERVATIONS, STATES

router = APIRouter()


@router.post("/bayesian", response_model=BayesianResponse)
async def bayesian_inference(request: BayesianRequest):
    """
    Perform exact Bayesian inference using full joint enumeration.
    """
    try:
        result = compute_inference(request.evidence)
        return BayesianResponse(
            probabilities=result["probabilities"],
            explanation=result["explanation"],
            network_structure=result["network_structure"],
            success=True,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Bayesian inference error: {str(e)}"
        )


@router.post("/em", response_model=EMResponse)
async def expectation_maximization(request: EMRequest):
    """
    Run Expectation-Maximization on 2D synthetic Gaussian mixture data.
    """
    if not (2 <= request.n_components <= 5):
        raise HTTPException(
            status_code=400,
            detail="Number of components must be between 2 and 5.",
        )
    if not (50 <= request.n_samples <= 1000):
        raise HTTPException(
            status_code=400,
            detail="Number of samples must be between 50 and 1000.",
        )
    if request.max_iterations < 1 or request.max_iterations > 500:
        raise HTTPException(
            status_code=400,
            detail="Max iterations must be between 1 and 500.",
        )

    try:
        result = run_em(
            n_samples=request.n_samples,
            n_components=request.n_components,
            max_iterations=request.max_iterations,
            seed=request.seed,
        )
        if not result.get("success", False):
            raise HTTPException(
                status_code=500,
                detail=result.get("message", "EM algorithm failed to complete."),
            )

        return EMResponse(
            clusters=result["clusters"],
            log_likelihood_history=result["log_likelihood_history"],
            iterations=result["iterations"],
            converged=result["converged"],
            message=result["message"],
            success=result["success"],
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"EM error: {str(e)}")


@router.post("/hmm", response_model=HMMResponse)
async def hidden_markov_model(request: HMMRequest):
    """
    Run Hidden Markov Model inference (Forward algorithm and/or Viterbi).
    """
    if not request.observations:
        raise HTTPException(
            status_code=400, detail="Observations list cannot be empty."
        )

    invalid_obs = [o for o in request.observations if o not in OBSERVATIONS]
    if invalid_obs:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid observations: {invalid_obs}. Allowed: {OBSERVATIONS}",
        )

    if request.algorithm not in ("forward", "viterbi", "both"):
        raise HTTPException(
            status_code=400,
            detail="Algorithm must be one of 'forward', 'viterbi', or 'both'.",
        )

    try:
        result = run_hmm(request.observations, algorithm=request.algorithm)
        if not result.get("success", False):
            raise HTTPException(
                status_code=500,
                detail=result.get("message", "HMM execution failed."),
            )

        return HMMResponse(
            forward_prob=result["forward_prob"],
            viterbi_path=result["viterbi_path"],
            viterbi_prob=result["viterbi_prob"],
            state_probs=result["state_probs"],
            message=result["message"],
            success=result["success"],
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"HMM error: {str(e)}")


@router.get("/hmm/options")
async def get_hmm_options():
    """
    Return available states and observations for HMM.
    """
    return {"states": STATES, "observations": OBSERVATIONS}
