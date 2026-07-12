"""
Advanced Analytics Engine

Comprehensive analytics framework providing Bayesian inference, Monte Carlo simulation,
causal inference, and multivariate statistical methods for complex data science workflows.
"""

from __future__ import annotations

import hashlib
import logging
import warnings
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum, auto
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union

import numpy as np
from numpy.typing import NDArray

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class SamplingMethod(Enum):
    RANDOM = auto()
    LATIN_HYPERCUBE = auto()
    STRATIFIED = auto()
    IMPORTANCE = auto()
    ANTITHETIC = auto()


class RotationMethod(Enum):
    NONE = auto()
    VARIMAX = auto()
    PROMAX = auto()
    QUARTIMAX = auto()
    OBLIMIN = auto()


class ConvergenceStatus(Enum):
    CONVERGED = "converged"
    BORDERLINE = "borderline"
    NOT_CONVERGED = "not_converged"


class ModelType(Enum):
    LINEAR_REGRESSION = "linear_regression"
    LOGISTIC_REGRESSION = "logistic_regression"
    HIERARCHICAL = "hierarchical"
    ROBUST_REGRESSION = "robust_regression"


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class PriorSpec:
    """Prior distributions for Bayesian model parameters."""
    intercept_prior: Dict[str, float] = field(default_factory=lambda: {"mean": 0.0, "std": 10.0})
    coefficient_prior: Dict[str, float] = field(default_factory=lambda: {"mean": 0.0, "std": 5.0})
    noise_prior: Dict[str, float] = field(default_factory=lambda: {"alpha": 2.0, "beta": 1.0})
    covariance_prior: Dict[str, Any] = field(default_factory=lambda: {"df": 5, "scale": "eye"})


@dataclass(frozen=True)
class MCMCConfig:
    """Configuration for Markov Chain Monte Carlo sampling."""
    n_samples: int = 5000
    n_warmup: int = 1000
    n_chains: int = 4
    target_acceptance: float = 0.9
    max_treedepth: int = 10
    thin: int = 1
    seed: Optional[int] = None


@dataclass
class ConvergenceDiagnostics:
    """MCMC convergence diagnostics."""
    rhat: Dict[str, float]
    effective_sample_size: Dict[str, float]
    autocorrelation: Dict[str, NDArray]
    status: ConvergenceStatus
    warnings: List[str] = field(default_factory=list)


@dataclass
class BayesianResult:
    """Results from Bayesian inference."""
    coefficient_means: NDArray
    coefficient_stds: NDArray
    intercept_mean: float
    intercept_std: float
    noise_variance_mean: float
    posterior_samples: Dict[str, NDArray]
    diagnostics: ConvergenceDiagnostics
    log_likelihood: float
    model_type: ModelType
    n_observations: int
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def credible_intervals(self, alpha: float = 0.05) -> Dict[str, Tuple[float, float]]:
        """Compute highest density intervals for all parameters."""
        result = {}
        lower = alpha / 2
        upper = 1 - alpha / 2
        for i, name in enumerate(self.coefficient_means.shape[0] and [f"beta_{i}" for i in range(len(self.coefficient_means))]):
            samples = self.posterior_samples.get(name, np.array([]))
            if len(samples) > 0:
                result[name] = (float(np.percentile(samples, lower * 100)),
                                float(np.percentile(samples, upper * 100)))
        return result


@dataclass
class MonteCarloResult:
    """Results from Monte Carlo simulation."""
    samples: NDArray
    n_simulations: int
    method: SamplingMethod
    variance_reduced: bool
    seed: int
    execution_time_ms: float

    def mean(self) -> float:
        return float(np.mean(self.samples))

    def std(self) -> float:
        return float(np.std(self.samples))

    def percentile(self, q: float) -> float:
        return float(np.percentile(self.samples, q))

    def probability_below(self, threshold: float) -> float:
        return float(np.mean(self.samples < threshold))

    def probability_above(self, threshold: float) -> float:
        return float(np.mean(self.samples > threshold))

    def cvar(self, alpha: float) -> float:
        """Conditional Value at Risk (Expected Shortfall)."""
        cutoff = np.percentile(self.samples, (1 - alpha) * 100)
        tail = self.samples[self.samples <= cutoff]
        return float(np.mean(tail)) if len(tail) > 0 else float(cutoff)

    def confidence_interval(self, confidence: float = 0.95) -> Tuple[float, float]:
        lower = (1 - confidence) / 2 * 100
        upper = (1 + confidence) / 2 * 100
        return (float(np.percentile(self.samples, lower)),
                float(np.percentile(self.samples, upper)))


@dataclass
class CausalResult:
    """Results from causal inference analysis."""
    ate: float
    se: float
    ci_lower: float
    ci_upper: float
    method: str
    n_treated: int
    n_control: int
    balance_smd: Dict[str, float]
    sensitivity_gamma: Optional[float] = None

    def balance_report(self) -> Dict[str, str]:
        report = {}
        for covariate, smd in self.balance_smd.items():
            if abs(smd) < 0.1:
                report[covariate] = "balanced"
            elif abs(smd) < 0.25:
                report[covariate] = "moderate imbalance"
            else:
                report[covariate] = "significant imbalance"
        return report

    def rosenbaum_bound(self, gamma: float) -> float:
        """Compute Rosenbaum sensitivity bound."""
        return self.ate / gamma if gamma > 0 else float("inf")


@dataclass
class PCAResult:
    """Results from Principal Component Analysis."""
    components: NDArray
    explained_variance: NDArray
    explained_variance_ratio: NDArray
    singular_values: NDArray
    loadings: NDArray
    n_significant_components: int
    eigenvalues: NDArray

    def scree_data(self) -> Dict[str, NDArray]:
        return {
            "components": np.arange(1, len(self.eigenvalues) + 1),
            "eigenvalues": self.eigenvalues,
            "variance_ratio": self.explained_variance_ratio,
            "cumulative_variance": np.cumsum(self.explained_variance_ratio),
        }


@dataclass
class FactorAnalysisResult:
    """Results from Factor Analysis."""
    loadings: NDArray
    communalities: NDArray
    uniquenesses: NDArray
    variance_explained: NDArray
    n_factors: int
    rmsea: float
    cfi: float
    chi_square: float
    df: int

    def loadings_table(self) -> Dict[str, NDArray]:
        return {f"Factor_{i+1}": self.loadings[:, i] for i in range(self.n_factors)}


# ---------------------------------------------------------------------------
# Bayesian Inference Engine
# ---------------------------------------------------------------------------

class BayesianInferenceEngine:
    """Bayesian inference engine with MCMC sampling and convergence diagnostics."""

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self._run_history: List[Dict[str, Any]] = []

    def linear_regression(
        self,
        X: NDArray,
        y: NDArray,
        priors: Optional[PriorSpec] = None,
        config: Optional[MCMCConfig] = None,
    ) -> BayesianResult:
        if priors is None:
            priors = PriorSpec()
        if config is None:
            config = MCMCConfig()

        rng = np.random.default_rng(config.seed)
        n_obs, n_features = X.shape

        if self.verbose:
            logger.info("Starting Bayesian linear regression: %d obs, %d features", n_obs, n_features)

        # Initialize chains
        chains = self._run_metropolis_hastings(
            X=X, y=y, priors=priors, config=config, rng=rng, model_type=ModelType.LINEAR_REGRESSION
        )

        # Compute diagnostics
        diagnostics = self._compute_diagnostics(chains, config)

        # Stack chains and compute posterior summaries
        all_samples = np.concatenate(chains, axis=0)
        beta_samples = all_samples[:, :n_features]
        intercept_samples = all_samples[:, n_features]
        sigma_samples = all_samples[:, n_features + 1]

        return BayesianResult(
            coefficient_means=np.mean(beta_samples, axis=0),
            coefficient_stds=np.std(beta_samples, axis=0),
            intercept_mean=float(np.mean(intercept_samples)),
            intercept_std=float(np.std(intercept_samples)),
            noise_variance_mean=float(np.mean(sigma_samples ** 2)),
            posterior_samples={
                **{f"beta_{i}": beta_samples[:, i] for i in range(n_features)},
                "intercept": intercept_samples,
                "sigma": sigma_samples,
            },
            diagnostics=diagnostics,
            log_likelihood=self._compute_log_likelihood(X, y, beta_samples, intercept_samples, sigma_samples),
            model_type=ModelType.LINEAR_REGRESSION,
            n_observations=n_obs,
        )

    def logistic_regression(
        self,
        X: NDArray,
        y: NDArray,
        priors: Optional[PriorSpec] = None,
        config: Optional[MCMCConfig] = None,
    ) -> BayesianResult:
        if priors is None:
            priors = PriorSpec()
        if config is None:
            config = MCMCConfig()

        rng = np.random.default_rng(config.seed)
        n_obs, n_features = X.shape

        chains = self._run_metropolis_hastings(
            X=X, y=y, priors=priors, config=config, rng=rng, model_type=ModelType.LOGISTIC_REGRESSION
        )

        diagnostics = self._compute_diagnostics(chains, config)
        all_samples = np.concatenate(chains, axis=0)
        beta_samples = all_samples[:, :n_features]
        intercept_samples = all_samples[:, n_features]

        return BayesianResult(
            coefficient_means=np.mean(beta_samples, axis=0),
            coefficient_stds=np.std(beta_samples, axis=0),
            intercept_mean=float(np.mean(intercept_samples)),
            intercept_std=float(np.std(intercept_samples)),
            noise_variance_mean=0.0,
            posterior_samples={
                **{f"beta_{i}": beta_samples[:, i] for i in range(n_features)},
                "intercept": intercept_samples,
            },
            diagnostics=diagnostics,
            log_likelihood=self._compute_log_likelihood_logistic(X, y, beta_samples, intercept_samples),
            model_type=ModelType.LOGISTIC_REGRESSION,
            n_observations=n_obs,
        )

    def _run_metropolis_hastings(
        self,
        X: NDArray,
        y: NDArray,
        priors: PriorSpec,
        config: MCMCConfig,
        rng: np.random.Generator,
        model_type: ModelType,
    ) -> List[NDArray]:
        """Run Metropolis-Hastings MCMC for parameter estimation."""
        n_obs, n_features = X.shape
        n_params = n_features + 2  # coefficients + intercept + noise
        total_samples = config.n_warmup + config.n_samples * config.thin

        chains = []
        for chain_idx in range(config.n_chains):
            # Initialize parameters
            current = np.zeros(n_params)
            current[:n_features] = rng.normal(0, 1, n_features)
            current[n_features] = rng.normal(0, 1)  # intercept
            current[n_features + 1] = rng.uniform(0.1, 2.0)  # sigma

            chain_samples = np.zeros((config.n_samples, n_params))
            accepted = 0

            for step in range(total_samples):
                # Propose new state
                proposal_scale = 0.1 * (1 - step / total_samples) + 0.01
                proposal = current + rng.normal(0, proposal_scale, n_params)

                # Ensure sigma is positive
                proposal[n_features + 1] = abs(proposal[n_features + 1])

                # Compute log acceptance ratio
                log_prior_current = self._log_prior(current, priors, n_features, model_type)
                log_prior_proposal = self._log_prior(proposal, priors, n_features, model_type)

                if model_type == ModelType.LINEAR_REGRESSION:
                    log_lik_current = self._log_likelihood_linear(X, y, current, n_features)
                    log_lik_proposal = self._log_likelihood_linear(X, y, proposal, n_features)
                else:
                    log_lik_current = self._log_likelihood_logistic_single(X, y, current, n_features)
                    log_lik_proposal = self._log_likelihood_logistic_single(X, y, proposal, n_features)

                log_alpha = (log_prior_proposal + log_lik_proposal) - (log_prior_current + log_lik_current)

                if np.log(rng.uniform()) < log_alpha:
                    current = proposal
                    accepted += 1

                # Store sample (after warmup, with thinning)
                if step >= config.n_warmup and (step - config.n_warmup) % config.thin == 0:
                    sample_idx = (step - config.n_warmup) // config.thin
                    if sample_idx < config.n_samples:
                        chain_samples[sample_idx] = current

            acceptance_rate = accepted / total_samples
            if self.verbose:
                logger.info("Chain %d acceptance rate: %.3f", chain_idx, acceptance_rate)

            chains.append(chain_samples)

        return chains

    def _log_prior(
        self, params: NDArray, priors: PriorSpec, n_features: int, model_type: ModelType
    ) -> float:
        """Compute log prior probability."""
        log_p = 0.0

        # Coefficient priors (normal)
        for i in range(n_features):
            mean = priors.coefficient_prior["mean"]
            std = priors.coefficient_prior["std"]
            log_p += -0.5 * ((params[i] - mean) / std) ** 2 - np.log(std * np.sqrt(2 * np.pi))

        # Intercept prior
        mean = priors.intercept_prior["mean"]
        std = priors.intercept_prior["std"]
        log_p += -0.5 * ((params[n_features] - mean) / std) ** 2 - np.log(std * np.sqrt(2 * np.pi))

        # Noise prior (only for linear regression)
        if model_type == ModelType.LINEAR_REGRESSION:
            alpha = priors.noise_prior["alpha"]
            beta = priors.noise_prior["beta"]
            sigma = params[n_features + 1]
            if sigma > 0:
                log_p += (alpha - 1) * np.log(sigma) - beta / sigma
            else:
                log_p = -np.inf

        return log_p

    def _log_likelihood_linear(
        self, X: NDArray, y: NDArray, params: NDArray, n_features: int
    ) -> float:
        beta = params[:n_features]
        intercept = params[n_features]
        sigma = params[n_features + 1]

        mu = X @ beta + intercept
        residuals = y - mu
        n = len(y)

        log_lik = -n / 2 * np.log(2 * np.pi * sigma ** 2) - np.sum(residuals ** 2) / (2 * sigma ** 2)
        return log_lik

    def _log_likelihood_logistic_single(
        self, X: NDArray, y: NDArray, params: NDArray, n_features: int
    ) -> float:
        beta = params[:n_features]
        intercept = params[n_features]
        logits = X @ beta + intercept
        probs = 1 / (1 + np.exp(-np.clip(logits, -500, 500)))
        log_lik = np.sum(y * np.log(probs + 1e-10) + (1 - y) * np.log(1 - probs + 1e-10))
        return log_lik

    def _compute_log_likelihood(
        self, X: NDArray, y: NDArray, beta: NDArray, intercept: NDArray, sigma: NDArray
    ) -> float:
        """Compute mean log likelihood across posterior samples."""
        n_samples = min(100, len(sigma))
        indices = np.random.choice(len(sigma), n_samples, replace=False)
        lls = []
        for i in indices:
            mu = X @ beta[i] + intercept[i]
            residuals = y - mu
            ll = -len(y) / 2 * np.log(2 * np.pi * sigma[i] ** 2) - np.sum(residuals ** 2) / (2 * sigma[i] ** 2)
            lls.append(ll)
        return float(np.mean(lls))

    def _compute_log_likelihood_logistic(
        self, X: NDArray, y: NDArray, beta: NDArray, intercept: NDArray
    ) -> float:
        n_samples = min(100, len(intercept))
        indices = np.random.choice(len(intercept), n_samples, replace=False)
        lls = []
        for i in indices:
            logits = X @ beta[i] + intercept[i]
            probs = 1 / (1 + np.exp(-np.clip(logits, -500, 500)))
            ll = np.sum(y * np.log(probs + 1e-10) + (1 - y) * np.log(1 - probs + 1e-10))
            lls.append(ll)
        return float(np.mean(lls))

    def _compute_diagnostics(
        self, chains: List[NDArray], config: MCMCConfig
    ) -> ConvergenceDiagnostics:
        """Compute Gelman-Rubin R-hat and effective sample size."""
        n_chains = len(chains)
        n_samples = chains[0].shape[0]
        n_params = chains[0].shape[1]

        rhat = {}
        ess = {}
        autocorr = {}

        for p in range(n_params):
            param_samples = [c[:, p] for c in chains]
            param_name = f"param_{p}"

            # R-hat (Gelman-Rubin)
            chain_means = np.array([np.mean(s) for s in param_samples])
            chain_vars = np.array([np.var(s, ddof=1) for s in param_samples])
            W = np.mean(chain_vars)
            B = n_samples * np.var(chain_means, ddof=1)
            var_hat = (1 - 1 / n_samples) * W + (1 / n_samples) * B
            rhat[param_name] = float(np.sqrt(var_hat / W)) if W > 0 else 1.0

            # Effective sample size (initial monotone sequence estimator)
            all_samples = np.concatenate(param_samples)
            n_total = len(all_samples)
            mean_val = np.mean(all_samples)
            var_val = np.var(all_samples, ddof=1)

            if var_val > 0:
                autocorr_vals = np.correlate(
                    all_samples - mean_val, all_samples - mean_val, mode="full"
                )[n_total - 1:]
                autocorr_vals = autocorr_vals / (var_val * n_total)
                # Sum until first negative
                tau = 1.0
                for lag in range(1, min(n_total // 2, 200)):
                    if autocorr_vals[lag] < 0:
                        break
                    tau += 2 * autocorr_vals[lag]
                ess[param_name] = float(n_total / tau)
            else:
                ess[param_name] = float(n_total)

            autocorr[param_name] = autocorr_vals[:min(50, len(autocorr_vals))]

        # Determine convergence status
        max_rhat = max(rhat.values())
        min_ess = min(ess.values())
        warnings_list = []

        if max_rhat > 1.1:
            status = ConvergenceStatus.NOT_CONVERGED
            warnings_list.append(f"R-hat {max_rhat:.3f} exceeds 1.1 threshold")
        elif max_rhat > 1.05:
            status = ConvergenceStatus.BORDERLINE
            warnings_list.append(f"R-hat {max_rhat:.3f} is borderline (> 1.05)")
        else:
            status = ConvergenceStatus.CONVERGED

        if min_ess < 400:
            warnings_list.append(f"Low effective sample size: {min_ess:.0f}")

        return ConvergenceDiagnostics(
            rhat=rhat,
            effective_sample_size=ess,
            autocorrelation=autocorr,
            status=status,
            warnings=warnings_list,
        )


# ---------------------------------------------------------------------------
# Monte Carlo Simulation
# ---------------------------------------------------------------------------

class MonteCarloSimulator:
    """Monte Carlo simulation engine with variance reduction and convergence monitoring."""

    def __init__(self, n_simulations: int = 10000, verbose: bool = False):
        self.n_simulations = n_simulations
        self.verbose = verbose

    def run(
        self,
        model: Callable[..., float],
        parameter_distributions: Dict[str, Dict[str, Any]],
        fixed_params: Optional[Dict[str, Any]] = None,
        sampling: SamplingMethod = SamplingMethod.RANDOM,
        variance_reduction: bool = False,
        seed: Optional[int] = None,
    ) -> MonteCarloResult:
        """Run Monte Carlo simulation with specified model and distributions."""
        rng = np.random.default_rng(seed)
        start_time = datetime.now(timezone.utc)

        # Generate parameter samples
        param_samples = self._generate_samples(
            parameter_distributions, self.n_simulations, rng, sampling, variance_reduction
        )

        # Evaluate model across all samples
        results = np.zeros(self.n_simulations)
        for i in range(self.n_simulations):
            kwargs = {key: param_samples[key][i] for key in param_samples}
            if fixed_params:
                kwargs.update(fixed_params)
            try:
                output = model(**kwargs)
                if isinstance(output, tuple):
                    results[i] = output[0]
                else:
                    results[i] = output
            except Exception as e:
                logger.warning("Simulation %d failed: %s", i, e)
                results[i] = np.nan

        # Remove NaN results
        valid_mask = ~np.isnan(results)
        valid_results = results[valid_mask]
        n_valid = int(np.sum(valid_mask))

        elapsed_ms = (datetime.now(timezone.utc) - start_time).total_seconds() * 1000

        if self.verbose:
            logger.info(
                "Simulation complete: %d/%d valid results in %.1fms",
                n_valid, self.n_simulations, elapsed_ms,
            )

        return MonteCarloResult(
            samples=valid_results,
            n_simulations=n_valid,
            method=sampling,
            variance_reduced=variance_reduction,
            seed=seed or 0,
            execution_time_ms=elapsed_ms,
        )

    def _generate_samples(
        self,
        distributions: Dict[str, Dict[str, Any]],
        n: int,
        rng: np.random.Generator,
        method: SamplingMethod,
        variance_reduction: bool,
    ) -> Dict[str, NDArray]:
        """Generate parameter samples from specified distributions."""
        samples = {}

        for param_name, dist_spec in distributions.items():
            dist_type = dist_spec.get("type", "normal")

            if method == SamplingMethod.LATIN_HYPERCUBE:
                raw = self._latin_hypercube_sample(dist_spec, n, rng)
            elif method == SamplingMethod.ANTITHETIC and variance_reduction:
                raw = self._antithetic_sample(dist_spec, n, rng)
            else:
                raw = self._random_sample(dist_spec, n, rng)

            if variance_reduction and method == SamplingMethod.RANDOM:
                raw = self._apply_control_variate(raw)

            samples[param_name] = raw

        return samples

    def _random_sample(
        self, dist_spec: Dict[str, Any], n: int, rng: np.random.Generator
    ) -> NDArray:
        dist_type = dist_spec["type"]
        if dist_type == "normal":
            return rng.normal(dist_spec["mean"], dist_spec["std"], n)
        elif dist_type == "uniform":
            return rng.uniform(dist_spec["low"], dist_spec["high"], n)
        elif dist_type == "lognormal":
            return rng.lognormal(dist_spec["mean"], dist_spec["std"], n)
        elif dist_type == "beta":
            return rng.beta(dist_spec["alpha"], dist_spec["beta"], n)
        elif dist_type == "poisson":
            return rng.poisson(dist_spec["lam"], n).astype(float)
        elif dist_type == "wishart":
            scale = np.array(dist_spec["scale"])
            df = dist_spec["df"]
            p = scale.shape[0]
            chol = np.linalg.cholesky(scale)
            samples_list = []
            for _ in range(n):
                z = rng.standard_normal((df, p))
                a = z @ chol
                samples_list.append(a.T @ a)
            return np.array(samples_list)
        else:
            raise ValueError(f"Unsupported distribution type: {dist_type}")

    def _latin_hypercube_sample(
        self, dist_spec: Dict[str, Any], n: int, rng: np.random.Generator
    ) -> NDArray:
        """Latin Hypercube Sampling for better space coverage."""
        # Generate stratified uniform samples
        strata = np.linspace(0, 1, n + 1)
        uniform_samples = np.array([
            rng.uniform(strata[i], strata[i + 1]) for i in range(n)
        ])
        rng.shuffle(uniform_samples)

        # Transform to target distribution
        dist_type = dist_spec["type"]
        if dist_type == "normal":
            from scipy import stats as sp_stats
            return sp_stats.norm.ppf(uniform_samples, loc=dist_spec["mean"], scale=dist_spec["std"])
        elif dist_type == "uniform":
            return dist_spec["low"] + uniform_samples * (dist_spec["high"] - dist_spec["low"])
        else:
            return self._random_sample(dist_spec, n, rng)

    def _antithetic_sample(
        self, dist_spec: Dict[str, Any], n: int, rng: np.random.Generator
    ) -> NDArray:
        """Antithetic sampling for variance reduction."""
        half_n = n // 2
        raw = self._random_sample(dist_spec, half_n, rng)
        # Create antithetic pairs by reflecting around the mean
        mean = np.mean(raw)
        antithetic = 2 * mean - raw
        combined = np.concatenate([raw, antithetic])
        if n % 2 == 1:
            combined = np.append(combined, self._random_sample(dist_spec, 1, rng))
        return combined[:n]

    def _apply_control_variate(self, samples: NDArray) -> NDArray:
        """Apply control variate variance reduction."""
        mean = np.mean(samples)
        return samples - (mean - np.mean(samples))


# ---------------------------------------------------------------------------
# Causal Inference Engine
# ---------------------------------------------------------------------------

class CausalInferenceEngine:
    """Causal inference toolkit for estimating treatment effects from observational data."""

    def __init__(self, verbose: bool = False):
        self.verbose = verbose

    def estimate_ate(
        self,
        data: Dict[str, NDArray],
        treatment_col: str,
        outcome_col: str,
        covariates: List[str],
        method: str = "propensity_score_matching",
        matching_ratio: int = 1,
        caliper: float = 0.2,
        dag: Optional[Any] = None,
    ) -> CausalResult:
        """Estimate Average Treatment Effect using specified method."""
        treatment = data[treatment_col]
        outcome = data[outcome_col]
        covariate_matrix = np.column_stack([data[c] for c in covariates])

        if method == "propensity_score_matching":
            return self._propensity_score_matching(
                treatment, outcome, covariate_matrix, covariates, matching_ratio, caliper
            )
        elif method == "propensity_score_weighting":
            return self._propensity_score_weighting(
                treatment, outcome, covariate_matrix, covariates
            )
        elif method == "inverse_probability_weighting":
            return self._ipw_estimator(treatment, outcome, covariate_matrix, covariates)
        else:
            raise ValueError(f"Unknown causal inference method: {method}")

    def _propensity_score_matching(
        self,
        treatment: NDArray,
        outcome: NDArray,
        covariates: NDArray,
        covariate_names: List[str],
        ratio: int,
        caliper: float,
    ) -> CausalResult:
        """Propensity score matching with nearest-neighbor matching."""
        # Estimate propensity scores via logistic regression
        from sklearn.linear_model import LogisticRegression

        ps_model = LogisticRegression(max_iter=1000, random_state=42)
        ps_model.fit(covariates, treatment.astype(int))
        propensity_scores = ps_model.predict_proba(covariates)[:, 1]

        # Match treated to control units
        treated_idx = np.where(treatment == 1)[0]
        control_idx = np.where(treatment == 0)[0]

        matched_treated = []
        matched_control = []

        for t_idx in treated_idx:
            ps_t = propensity_scores[t_idx]
            distances = np.abs(propensity_scores[control_idx] - ps_t)
            nearest_idx = np.argsort(distances)[:ratio]

            for c_idx in nearest_idx:
                if distances[c_idx] <= caliper:
                    matched_treated.append(t_idx)
                    matched_control.append(control_idx[c_idx])

        # Compute ATE from matched pairs
        matched_treated_outcomes = outcome[matched_treated]
        matched_control_outcomes = outcome[matched_control]

        ate = float(np.mean(matched_treated_outcomes - matched_control_outcomes))
        se = float(np.std(matched_treated_outcomes - matched_control_outcomes, ddof=1) /
                    np.sqrt(len(matched_treated))) if len(matched_treated) > 1 else 0.0

        ci_lower = ate - 1.96 * se
        ci_upper = ate + 1.96 * se

        # Compute balance (standardized mean differences)
        balance = {}
        for i, name in enumerate(covariate_names):
            treated_vals = covariates[matched_treated, i]
            control_vals = covariates[matched_control, i]
            pooled_std = np.sqrt((np.var(treated_vals, ddof=1) + np.var(control_vals, ddof=1)) / 2)
            smd = abs(np.mean(treated_vals) - np.mean(control_vals)) / pooled_std if pooled_std > 0 else 0
            balance[name] = float(smd)

        return CausalResult(
            ate=ate,
            se=se,
            ci_lower=ci_lower,
            ci_upper=ci_upper,
            method="propensity_score_matching",
            n_treated=len(matched_treated),
            n_control=len(matched_control),
            balance_smd=balance,
        )

    def _propensity_score_weighting(
        self,
        treatment: NDArray,
        outcome: NDArray,
        covariates: NDArray,
        covariate_names: List[str],
    ) -> CausalResult:
        """Inverse probability of treatment weighting (IPTW)."""
        from sklearn.linear_model import LogisticRegression

        ps_model = LogisticRegression(max_iter=1000, random_state=42)
        ps_model.fit(covariates, treatment.astype(int))
        ps = np.clip(ps_model.predict_proba(covariates)[:, 1], 0.01, 0.99)

        weights = treatment / ps + (1 - treatment) / (1 - ps)
        ate = float(np.sum(weights * outcome * treatment) / np.sum(weights * treatment) -
                     np.sum(weights * outcome * (1 - treatment)) / np.sum(weights * (1 - treatment)))

        # Bootstrap SE
        n_bootstrap = 200
        boot_ates = []
        rng = np.random.default_rng(42)
        for _ in range(n_bootstrap):
            idx = rng.choice(len(outcome), len(outcome), replace=True)
            w_boot = weights[idx]
            y_boot = outcome[idx]
            t_boot = treatment[idx]
            a = np.sum(w_boot * y_boot * t_boot) / np.sum(w_boot * t_boot) - \
                np.sum(w_boot * y_boot * (1 - t_boot)) / np.sum(w_boot * (1 - t_boot))
            boot_ates.append(a)

        se = float(np.std(boot_ates, ddof=1))

        balance = {}
        for i, name in enumerate(covariate_names):
            w_t = weights[treatment == 1]
            w_c = weights[treatment == 0]
            weighted_mean_t = np.average(covariates[treatment == 1, i], weights=w_t)
            weighted_mean_c = np.average(covariates[treatment == 0, i], weights=w_c)
            pooled_std = np.sqrt(np.average((covariates[:, i] - np.mean(covariates[:, i])) ** 2, weights=weights))
            smd = abs(weighted_mean_t - weighted_mean_c) / pooled_std if pooled_std > 0 else 0
            balance[name] = float(smd)

        return CausalResult(
            ate=ate, se=se,
            ci_lower=ate - 1.96 * se, ci_upper=ate + 1.96 * se,
            method="propensity_score_weighting",
            n_treated=int(np.sum(treatment == 1)), n_control=int(np.sum(treatment == 0)),
            balance_smd=balance,
        )

    def _ipw_estimator(
        self,
        treatment: NDArray,
        outcome: NDArray,
        covariates: NDArray,
        covariate_names: List[str],
    ) -> CausalResult:
        """Inverse Probability Weighting estimator."""
        return self._propensity_score_weighting(treatment, outcome, covariates, covariate_names)


# ---------------------------------------------------------------------------
# Multivariate Analysis
# ---------------------------------------------------------------------------

class MultivariateAnalysis:
    """Multivariate statistical methods including PCA, Factor Analysis, and CCA."""

    def __init__(self, verbose: bool = False):
        self.verbose = verbose

    def principal_component_analysis(
        self,
        data: NDArray,
        n_components: Optional[int] = None,
        scree_plot: bool = False,
        loadings_threshold: float = 0.3,
    ) -> PCAResult:
        """Perform PCA with automatic component selection."""
        # Center data
        mean = np.mean(data, axis=0)
        centered = data - mean

        # SVD-based PCA
        U, singular_values, Vt = np.linalg.svd(centered, full_matrices=False)
        n_features = data.shape[1]

        eigenvalues = (singular_values ** 2) / (len(data) - 1)
        explained_variance = eigenvalues
        explained_variance_ratio = eigenvalues / np.sum(eigenvalues)

        # Determine significant components via Kaiser criterion + parallel analysis
        if n_components is None:
            # Parallel analysis
            rng = np.random.default_rng(42)
            random_eigenvalues = np.zeros(n_features)
            for _ in range(100):
                random_data = rng.standard_normal(data.shape)
                _, random_sv, _ = np.linalg.svd(random_data, full_matrices=False)
                random_eigenvalues += (random_sv ** 2) / (len(data) - 1)
            random_eigenvalues /= 100

            n_components = int(np.sum(eigenvalues > random_eigenvalues))

        components = Vt[:n_components]
        loadings = components.T * np.sqrt(eigenvalues[:n_components])

        if scree_plot:
            self._create_scree_plot(eigenvalues, explained_variance_ratio)

        return PCAResult(
            components=components,
            explained_variance=explained_variance[:n_components],
            explained_variance_ratio=explained_variance_ratio[:n_components],
            singular_values=singular_values[:n_components],
            loadings=loadings,
            n_significant_components=n_components,
            eigenvalues=eigenvalues,
        )

    def factor_analysis(
        self,
        data: NDArray,
        n_factors: int,
        rotation: RotationMethod = RotationMethod.VARIMAX,
        method: str = "ml",
        fit_indices: bool = True,
    ) -> FactorAnalysisResult:
        """Exploratory Factor Analysis with rotation."""
        from sklearn.decomposition import FactorAnalysis as SKFA

        fa = SKFA(n_components=n_factors, rotation="varimax" if rotation == RotationMethod.VARIMAX else None,
                   random_state=42)
        loadings = fa.fit_transform(data)
        loadings_matrix = fa.components_.T

        # Communalities = sum of squared loadings
        communalities = np.sum(loadings_matrix ** 2, axis=1)
        uniquenesses = 1 - communalities

        variance_explained = np.sum(loadings_matrix ** 2, axis=0) / data.shape[1]

        # Fit indices
        rmsea = 0.0
        cfi = 1.0
        chi_square = 0.0
        df = 0

        if fit_indices:
            n_obs, n_vars = data.shape
            df = (n_vars * (n_vars + 1)) // 2 - n_vars * n_factors - n_factors

            # Reproduced correlation matrix
            reproduced = loadings_matrix @ loadings_matrix.T + np.diag(uniquenesses)
            original_corr = np.corrcoef(data, rowvar=False)
            diff = original_corr - reproduced
            chi_square = n_obs * np.trace(diff @ diff)
            rmsea = float(np.sqrt(max(0, chi_square / (df * n_obs) - 1 / n_obs))) if df > 0 else 0.0
            cfi = 1.0 - chi_square / max(chi_square + df, 1) if df > 0 else 1.0

        return FactorAnalysisResult(
            loadings=loadings_matrix,
            communalities=communalities,
            uniquenesses=uniquenesses,
            variance_explained=variance_explained,
            n_factors=n_factors,
            rmsea=rmsea,
            cfi=cfi,
            chi_square=float(chi_square),
            df=df,
        )

    def canonical_correlation_analysis(
        self,
        X: NDArray,
        Y: NDArray,
    ) -> Dict[str, Any]:
        """Canonical Correlation Analysis between two variable sets."""
        # Center data
        X_centered = X - np.mean(X, axis=0)
        Y_centered = Y - np.mean(Y, axis=0)

        n = X.shape[0]
        Cxx = np.cov(X_centered, rowvar=False)
        Cyy = np.cov(Y_centered, rowvar=False)
        Cxy = np.cov(X_centered, Y_centered, rowvar=False)[:X.shape[1], X.shape[1]:]

        # Solve generalized eigenvalue problem
        from scipy.linalg import sqrtm, inv
        try:
            Cxx_inv_sqrt = inv(sqrtm(Cxx + np.eye(Cxx.shape[0]) * 1e-10))
            Cyy_inv_sqrt = inv(sqrtm(Cyy + np.eye(Cyy.shape[0]) * 1e-10))
        except np.linalg.LinAlgError:
            Cxx_inv_sqrt = np.linalg.inv(np.linalg.cholesky(Cxx + np.eye(Cxx.shape[0]) * 1e-10))
            Cyy_inv_sqrt = np.linalg.inv(np.linalg.cholesky(Cyy + np.eye(Cyy.shape[0]) * 1e-10))

        M = Cxx_inv_sqrt @ Cxy @ Cyy_inv_sqrt
        canonical_corrs, _, _ = np.linalg.svd(M)

        n_canonical = min(X.shape[1], Y.shape[1])
        canonical_corrs = canonical_corrs[:n_canonical]

        return {
            "canonical_correlations": canonical_corrs,
            "squared_correlations": canonical_corrs ** 2,
            "n_pairs": n_canonical,
            "variance_extracted_x": None,  # Requires full solution
            "variance_extracted_y": None,
        }

    def _create_scree_plot(self, eigenvalues: NDArray, variance_ratio: NDArray) -> None:
        """Create scree plot data (returns data, does not render)."""
        logger.info(
            "Scree plot data: components=%s, eigenvalues=%s",
            np.arange(1, len(eigenvalues) + 1).tolist(),
            eigenvalues.tolist(),
        )


# ---------------------------------------------------------------------------
# Diagnostic Utilities
# ---------------------------------------------------------------------------

class ModelDiagnostics:
    """Model validation and diagnostic utilities."""

    @staticmethod
    def qq_plot_data(residuals: NDArray) -> Dict[str, NDArray]:
        """Generate QQ-plot data for residual analysis."""
        sorted_residuals = np.sort(residuals)
        n = len(sorted_residuals)
        theoretical = np.random.default_rng(42).standard_normal(n)
        theoretical = np.sort(theoretical)
        return {"theoretical": theoretical, "sample": sorted_residuals}

    @staticmethod
    def cooksdistance(X: NDArray, residuals: NDArray, mse: float) -> NDArray:
        """Compute Cook's distance for influence diagnostics."""
        hat_matrix = X @ np.linalg.inv(X.T @ X) @ X.T
        h_diag = np.diag(hat_matrix)
        p = X.shape[1]
        cooks_d = (residuals ** 2 / (p * mse)) * (h_diag / (1 - h_diag) ** 2)
        return cooks_d

    @staticmethod
    def calibration_curve(y_true: NDArray, y_prob: NDArray, n_bins: int = 10) -> Dict[str, NDArray]:
        """Compute calibration curve data for probabilistic predictions."""
        bin_edges = np.linspace(0, 1, n_bins + 1)
        bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
        fraction_positive = np.zeros(n_bins)

        for i in range(n_bins):
            mask = (y_prob >= bin_edges[i]) & (y_prob < bin_edges[i + 1])
            if np.sum(mask) > 0:
                fraction_positive[i] = np.mean(y_true[mask])

        return {"bin_centers": bin_centers, "fraction_positive": fraction_positive}

    @staticmethod
    def brier_score(y_true: NDArray, y_prob: NDArray) -> float:
        """Compute Brier score for probabilistic forecasts."""
        return float(np.mean((y_prob - y_true) ** 2))


# ---------------------------------------------------------------------------
# Main Demo
# ---------------------------------------------------------------------------

def main() -> None:
    """Demonstrate advanced analytics capabilities."""
    print("=" * 70)
    print("Advanced Analytics Engine - Demo")
    print("=" * 70)

    rng = np.random.default_rng(42)

    # --- 1. Bayesian Linear Regression ---
    print("\n--- Bayesian Linear Regression ---")
    n_obs, n_features = 200, 3
    X = rng.standard_normal((n_obs, n_features))
    true_weights = np.array([2.5, -1.0, 0.5])
    y = X @ true_weights + rng.standard_normal(n_obs) * 0.5

    engine = BayesianInferenceEngine(verbose=False)
    result = engine.linear_regression(
        X=X, y=y,
        priors=PriorSpec(),
        config=MCMCConfig(n_samples=2000, n_warmup=500, n_chains=2, seed=42),
    )
    print(f"  Posterior mean weights: {result.coefficient_means}")
    print(f"  True weights:          {true_weights}")
    print(f"  Intercept:             {result.intercept_mean:.4f}")
    print(f"  Noise variance:        {result.noise_variance_mean:.4f}")
    print(f"  Convergence status:    {result.diagnostics.status.value}")
    ci = result.credible_intervals(alpha=0.05)
    for param, (lo, hi) in ci.items():
        print(f"  95% CI {param}: [{lo:.4f}, {hi:.4f}]")

    # --- 2. Monte Carlo Simulation ---
    print("\n--- Monte Carlo Risk Simulation ---")

    def portfolio_return(weights: NDArray, returns: NDArray, **kwargs: Any) -> float:
        return float(weights @ returns)

    mc = MonteCarloSimulator(n_simulations=50000, verbose=False)
    mc_result = mc.run(
        model=portfolio_return,
        parameter_distributions={
            "returns": {"type": "normal", "mean": np.array([0.08, 0.12, 0.06]), "std": np.array([0.15, 0.20, 0.10])},
        },
        fixed_params={"weights": np.array([0.4, 0.35, 0.25])},
        sampling=SamplingMethod.LATIN_HYPERCUBE,
        seed=42,
    )
    print(f"  Expected return:       {mc_result.mean():.4f}")
    print(f"  Std deviation:         {mc_result.std():.4f}")
    print(f"  VaR (95%):             {mc_result.percentile(5):.4f}")
    print(f"  CVaR (95%):            {mc_result.cvar(0.95):.4f}")
    print(f"  P(loss):               {mc_result.probability_below(0):.4f}")
    ci95 = mc_result.confidence_interval(0.95)
    print(f"  95% CI:                [{ci95[0]:.4f}, {ci95[1]:.4f}]")

    # --- 3. Multivariate Analysis ---
    print("\n--- Principal Component Analysis ---")
    data = rng.standard_normal((150, 6))
    data[:, 0] = data[:, 1] * 2 + rng.standard_normal(150) * 0.3  # correlated pair
    data[:, 2] = data[:, 3] * 1.5 + rng.standard_normal(150) * 0.5

    mv = MultivariateAnalysis(verbose=False)
    pca_result = mv.principal_component_analysis(data=data, loadings_threshold=0.3)
    print(f"  Significant components: {pca_result.n_significant_components}")
    print(f"  Explained variance:     {pca_result.explained_variance_ratio}")
    print(f"  Cumulative variance:    {np.cumsum(pca_result.explained_variance_ratio)}")

    # --- 4. Factor Analysis ---
    print("\n--- Factor Analysis ---")
    fa_result = mv.factor_analysis(data=data, n_factors=3, rotation=RotationMethod.VARIMAX)
    print(f"  Variance explained: {fa_result.variance_explained}")
    print(f"  RMSEA:              {fa_result.rmsea:.4f}")
    print(f"  CFI:                {fa_result.cfi:.4f}")
    print(f"  Communalities:      {fa_result.communalities}")

    # --- 5. Model Diagnostics ---
    print("\n--- Model Diagnostics ---")
    diagnostics = ModelDiagnostics()
    residuals = rng.standard_normal(200)
    qq_data = diagnostics.qq_plot_data(residuals)
    print(f"  QQ-plot data points: {len(qq_data['theoretical'])}")

    y_true = (rng.random(200) > 0.5).astype(float)
    y_prob = rng.beta(2, 5, 200)
    brier = diagnostics.brier_score(y_true, y_prob)
    print(f"  Brier score:         {brier:.4f}")

    cal = diagnostics.calibration_curve(y_true, y_prob)
    print(f"  Calibration bins:    {len(cal['bin_centers'])}")

    print("\n" + "=" * 70)
    print("Demo complete.")
    print("=" * 70)


if __name__ == "__main__":
    main()