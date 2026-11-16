"""
EM Algorithm for Gaussian Mixture Models – implemented from scratch.

No sklearn GMM is used.  The E-step and M-step follow the standard derivations
for a mixture of univariate (per-dimension independent) Gaussians over 2-D data.
"""

import numpy as np
from typing import List


# ---------------------------------------------------------------------------
# Helper: univariate Gaussian PDF
# ---------------------------------------------------------------------------

def _gaussian_pdf(x: np.ndarray, mean: float, var: float) -> np.ndarray:
    """
    Evaluate N(x; mean, var) for a 1-D array x.
    var is the variance (sigma^2).  Clipped to avoid degenerate distributions.
    """
    var = max(var, 1e-6)
    coef = 1.0 / np.sqrt(2.0 * np.pi * var)
    return coef * np.exp(-0.5 * (x - mean) ** 2 / var)


# ---------------------------------------------------------------------------
# Gaussian Mixture Model via EM
# ---------------------------------------------------------------------------

class GaussianMixture:
    """
    EM-based Gaussian Mixture Model for 2-D data.

    Each component has an independent Gaussian per dimension so that the full
    density factors as N(x1; mu_k1, s_k1) * N(x2; mu_k2, s_k2).
    """

    def __init__(
        self,
        n_components: int = 3,
        max_iter: int = 100,
        tol: float = 1e-4,
        random_state: int = 42,
    ):
        self.n_components = n_components
        self.max_iter = max_iter
        self.tol = tol
        self.random_state = random_state

        # Learned parameters – shape (K, 2) for 2-D data
        self.means_: np.ndarray | None = None          # (K, 2)
        self.covariances_: np.ndarray | None = None    # (K, 2) – per-dim variances
        self.weights_: np.ndarray | None = None        # (K,)

    # ------------------------------------------------------------------
    # Initialisation
    # ------------------------------------------------------------------

    def _initialize(self, X: np.ndarray):
        """
        Randomly initialise means (by picking data points), unit variances,
        and uniform mixing weights.
        """
        rng = np.random.default_rng(self.random_state)
        n_samples = X.shape[0]
        idx = rng.choice(n_samples, size=self.n_components, replace=False)
        self.means_ = X[idx].copy().astype(float)                      # (K, 2)
        self.covariances_ = np.ones((self.n_components, 2), dtype=float)
        self.weights_ = np.full(self.n_components, 1.0 / self.n_components)

    # ------------------------------------------------------------------
    # E-step
    # ------------------------------------------------------------------

    def _e_step(self, X: np.ndarray) -> np.ndarray:
        """
        Compute responsibilities gamma[i, k] = P(z=k | x_i).

        gamma[i,k] = w_k * p(x_i | mu_k, Sigma_k)
                     ----------------------------------
                     sum_j  w_j * p(x_i | mu_j, Sigma_j)
        """
        n = X.shape[0]
        K = self.n_components
        # Compute unnormalised log-responsibilities for numerical stability
        log_resp = np.zeros((n, K))
        for k in range(K):
            # Product of per-dimension Gaussians = sum of log pdfs
            log_p = np.log(self.weights_[k] + 1e-300)
            for d in range(2):
                log_p = log_p + np.log(
                    _gaussian_pdf(X[:, d], self.means_[k, d], self.covariances_[k, d])
                    + 1e-300
                )
            log_resp[:, k] = log_p

        # Numerically stable softmax over components
        log_resp -= log_resp.max(axis=1, keepdims=True)
        resp = np.exp(log_resp)
        resp /= resp.sum(axis=1, keepdims=True)
        return resp  # (n, K)

    # ------------------------------------------------------------------
    # M-step
    # ------------------------------------------------------------------

    def _m_step(self, X: np.ndarray, gamma: np.ndarray):
        """
        Update parameters using the current responsibilities.

        N_k  = sum_i gamma[i, k]
        mu_k = sum_i gamma[i,k] * x_i  /  N_k
        s_k  = sum_i gamma[i,k] * (x_i - mu_k)^2  /  N_k   (per dimension)
        w_k  = N_k / N
        """
        n = X.shape[0]
        K = self.n_components
        N_k = gamma.sum(axis=0)  # (K,)

        new_means = np.zeros((K, 2))
        new_covs = np.zeros((K, 2))

        for k in range(K):
            nk = max(N_k[k], 1e-10)
            new_means[k] = (gamma[:, k, np.newaxis] * X).sum(axis=0) / nk
            diff = X - new_means[k]  # (n, 2)
            new_covs[k] = (gamma[:, k, np.newaxis] * diff ** 2).sum(axis=0) / nk
            # Minimum variance guard
            new_covs[k] = np.maximum(new_covs[k], 1e-6)

        self.means_ = new_means
        self.covariances_ = new_covs
        self.weights_ = N_k / n

    # ------------------------------------------------------------------
    # Log-likelihood
    # ------------------------------------------------------------------

    def _log_likelihood(self, X: np.ndarray) -> float:
        """
        log L = sum_i log( sum_k w_k * p(x_i | theta_k) )
        """
        n = X.shape[0]
        K = self.n_components
        ll = 0.0
        for i in range(n):
            mix = 0.0
            for k in range(K):
                p = self.weights_[k]
                for d in range(2):
                    p *= _gaussian_pdf(
                        np.array([X[i, d]]), self.means_[k, d], self.covariances_[k, d]
                    )[0]
                mix += p
            ll += np.log(mix + 1e-300)
        return float(ll)

    # ------------------------------------------------------------------
    # fit
    # ------------------------------------------------------------------

    def fit(self, X: np.ndarray) -> dict:
        """
        Run EM until convergence or max_iter.

        Returns
        -------
        dict with converged, iterations, log_likelihood_history, means,
        covariances, weights.
        """
        self._initialize(X)
        ll_history: List[float] = []
        converged = False

        for iteration in range(self.max_iter):
            gamma = self._e_step(X)
            self._m_step(X, gamma)
            ll = self._log_likelihood(X)
            ll_history.append(ll)

            if iteration > 0 and abs(ll_history[-1] - ll_history[-2]) < self.tol:
                converged = True
                break

        return {
            "converged": converged,
            "iterations": len(ll_history),
            "log_likelihood_history": ll_history,
            "means": self.means_.tolist(),
            "covariances": self.covariances_.tolist(),
            "weights": self.weights_.tolist(),
        }

    # ------------------------------------------------------------------
    # predict
    # ------------------------------------------------------------------

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Return the index of the most probable component for each sample."""
        gamma = self._e_step(X)
        return gamma.argmax(axis=1)


# ---------------------------------------------------------------------------
# Convenience runner
# ---------------------------------------------------------------------------

def run_em(
    n_samples: int = 200,
    n_components: int = 3,
    max_iterations: int = 100,
    seed: int = 42,
) -> dict:
    """
    Generate synthetic 2-D Gaussian mixture data, fit a GMM via EM, and
    return structured results.

    Returns
    -------
    dict with:
        clusters              – list of dicts per component
        log_likelihood_history
        iterations
        converged
        message
        success
        data_points           – {x: list, y: list}
    """
    try:
        rng = np.random.default_rng(seed)

        # --- Generate data ---
        K_true = n_components
        samples_per = n_samples // K_true
        remainder = n_samples - samples_per * K_true

        # True centres spread across [-5, 5]^2
        true_means = rng.uniform(-4, 4, size=(K_true, 2))
        X_parts = []
        for k in range(K_true):
            n_k = samples_per + (1 if k < remainder else 0)
            cov = np.diag(rng.uniform(0.5, 1.5, size=2))
            pts = rng.multivariate_normal(true_means[k], cov, size=n_k)
            X_parts.append(pts)
        X = np.vstack(X_parts)

        # --- Fit GMM ---
        gmm = GaussianMixture(
            n_components=n_components,
            max_iter=max_iterations,
            tol=1e-4,
            random_state=seed,
        )
        fit_result = gmm.fit(X)
        labels = gmm.predict(X)

        # --- Build cluster info ---
        clusters = []
        for k in range(n_components):
            mask = labels == k
            pts_x = X[mask, 0].tolist()
            pts_y = X[mask, 1].tolist()
            mean_vec = gmm.means_[k].tolist()
            var_vec = gmm.covariances_[k].tolist()
            clusters.append(
                {
                    "mean": mean_vec,
                    "variance": var_vec,
                    "weight": float(gmm.weights_[k]),
                    "points_x": pts_x,
                    "points_y": pts_y,
                    "assignments": int(mask.sum()),
                }
            )

        return {
            "clusters": clusters,
            "log_likelihood_history": fit_result["log_likelihood_history"],
            "iterations": fit_result["iterations"],
            "converged": fit_result["converged"],
            "message": (
                f"EM converged after {fit_result['iterations']} iterations."
                if fit_result["converged"]
                else f"EM reached max iterations ({max_iterations}) without converging."
            ),
            "success": True,
            "data_points": {"x": X[:, 0].tolist(), "y": X[:, 1].tolist()},
        }

    except Exception as exc:
        return {
            "clusters": [],
            "log_likelihood_history": [],
            "iterations": 0,
            "converged": False,
            "message": f"EM failed: {exc}",
            "success": False,
            "data_points": {"x": [], "y": []},
        }
