"""
Statistical Analysis Toolkit

Comprehensive statistical analysis framework providing hypothesis testing, regression
modeling, survival analysis, Bayesian estimation, and resampling methods for rigorous
empirical research and data-driven decision making.
"""

from __future__ import annotations

import logging
import warnings
from abc import ABC, abstractmethod
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

class TestType(Enum):
    ONE_SAMPLE = "one_sample"
    TWO_SAMPLE_INDEPENDENT = "two_sample_independent"
    TWO_SAMPLE_PAIRED = "two_sample_paired"
    ONE_WAY_ANOVA = "one_way_anova"
    TWO_WAY_ANOVA = "two_way_anova"
    CHI_SQUARE = "chi_square"
    FISHER_EXACT = "fisher_exact"


class Alternative(Enum):
    TWO_SIDED = "two-sided"
    LESS = "less"
    GREATER = "greater"


class EffectSize(Enum):
    COHENS_D = "cohens_d"
    HEDGES_G = "hedges_g"
    ETA_SQUARED = "eta_squared"
    OMEGA_SQUARED = "omega_squared"
    GLASSS_DELTA = "glass_delta"
    CLIFFS_DELTA = "cliffs_delta"
    ODDS_RATIO = "odds_ratio"
    RISK_RATIO = "risk_ratio"
    NNT = "number_needed_to_treat"


class CorrectionMethod(Enum):
    NONE = "none"
    BONFERRONI = "bonferroni"
    HOLM = "holm"
    BENJAMINI_HOCHBERG = "benjamini_hochberg"
    BENJAMINI_YEKUTIELI = "benjamini_yekutieli"


class Family(Enum):
    GAUSSIAN = "gaussian"
    BINOMIAL = "binomial"
    POISSON = "poisson"
    GAMMA = "gamma"
    INVERSE_GAUSSIAN = "inverse_gaussian"


class Link(Enum):
    IDENTITY = "identity"
    LOG = "log"
    LOGIT = "logit"
    INVERSE = "inverse"
    PROBIT = "probit"


class ConfidenceLevel(Enum):
    PERCENTILE = "percentile"
    BCA = "bca"
    STUDENTIZED = "studentized"
    BASIC = "basic"


class SurvivalTest(Enum):
    LOG_RANK = "log_rank"
    WILCOXON = "wilcoxon"
    TARONE_WARE = "tarone_ware"
    PETO = "peto"
    LOG_RANK_SECOND = "log_rank_second"


# ---------------------------------------------------------------------------
# Dataclasses — Results
# ---------------------------------------------------------------------------

@dataclass
class TestResult:
    """Result of a hypothesis test."""
    test_name: str
    statistic: float
    p_value: float
    effect_size: Optional[float] = None
    effect_size_type: Optional[EffectSize] = None
    ci_lower: Optional[float] = None
    ci_upper: Optional[float] = None
    power: Optional[float] = None
    sample_size_1: int = 0
    sample_size_2: int = 0
    df: Optional[float] = None
    alternative: Alternative = Alternative.TWO_SIDED
    alpha: float = 0.05

    def significant(self, alpha: Optional[float] = None) -> bool:
        a = alpha if alpha is not None else self.alpha
        return self.p_value < a

    @property
    def effect_size_interpretation(self) -> str:
        if self.effect_size is None:
            return "N/A"
        d = abs(self.effect_size)
        if self.effect_size_type in (EffectSize.COHENS_D, EffectSize.HEDGES_G, EffectSize.GLASSS_DELTA):
            if d < 0.2:
                return "negligible"
            elif d < 0.5:
                return "small"
            elif d < 0.8:
                return "medium"
            else:
                return "large"
        elif self.effect_size_type == EffectSize.CLIFFS_DELTA:
            if d < 0.147:
                return "negligible"
            elif d < 0.33:
                return "small"
            elif d < 0.474:
                return "medium"
            else:
                return "large"
        return ""


@dataclass
class RegressionResult:
    """Result of a regression model."""
    coefficients: NDArray
    standard_errors: NDArray
    t_values: Optional[NDArray] = None
    p_values: Optional[NDArray] = None
    feature_names: Optional[List[str]] = None
    intercept: float = 0.0
    intercept_se: float = 0.0
    intercept_p: float = 0.0
    r_squared: float = 0.0
    adj_r_squared: float = 0.0
    aic: float = 0.0
    bic: float = 0.0
    deviance: float = 0.0
    residual_df: int = 0
    dispersion_estimate: float = 1.0
    residual_std_error: float = 0.0
    f_statistic: Optional[float] = None
    f_p_value: Optional[float] = None
    n_observations: int = 0
    model_type: str = "linear"
    family: Optional[Family] = None

    def summary(self) -> List[Tuple[str, float, float, float, float]]:
        """Return list of (name, coef, se, t/z, p) for all coefficients."""
        result = []
        names = self.feature_names or [f"x{i}" for i in range(len(self.coefficients))]
        for i, name in enumerate(names):
            tv = self.t_values[i] if self.t_values is not None else 0.0
            pv = self.p_values[i] if self.p_values is not None else 0.0
            result.append((name, self.coefficients[i], self.standard_errors[i], tv, pv))
        return result


@dataclass
class BootstrapResult:
    """Result from bootstrap resampling."""
    point_estimate: float
    ci_lower: float
    ci_upper: float
    std_error: float
    bias: float
    level: ConfidenceLevel
    alpha: float
    n_resamples: int
    bootstrap_distribution: Optional[NDArray] = None
    acceleration: Optional[float] = None


@dataclass
class PermutationTestResult:
    """Result from permutation test."""
    observed_statistic: float
    p_value: float
    n_permutations: int
    permutation_distribution: Optional[NDArray] = None


@dataclass
class PowerAnalysisResult:
    """Result from power analysis."""
    power: float
    sample_size: Optional[int] = None
    effect_size: float = 0.0
    alpha: float = 0.05
    analysis_type: str = "post_hoc"


@dataclass
class KMResult:
    """Kaplan-Meier survival estimate result."""
    times: NDArray
    survival: NDArray
    standard_errors: NDArray
    confidence_intervals: Optional[Tuple[NDArray, NDArray]] = None
    at_risk: Optional[NDArray] = None
    events: Optional[NDArray] = None
    censored: Optional[NDArray] = None
    n_subjects: int = 0

    def survival_at(self, time_point: float) -> float:
        idx = np.searchsorted(self.times, time_point, side="right") - 1
        idx = max(0, min(idx, len(self.survival) - 1))
        return float(self.survival[idx])

    @property
    def median_survival(self) -> float:
        idx = np.searchsorted(self.survival, 0.5, side="right") - 1
        idx = max(0, min(idx, len(self.times) - 1))
        return float(self.times[idx])


@dataclass
class CoxResult:
    """Cox proportional hazards regression result."""
    hazard_ratios: NDArray
    coefficients: NDArray
    standard_errors: NDArray
    z_values: NDArray
    p_values: NDArray
    confidence_intervals: Tuple[NDArray, NDArray]
    feature_names: List[str]
    log_likelihood: float
    aic: float
    concordance: float
    n_events: int
    n_subjects: int
    ph_test_p: Optional[float] = None  # proportional hazards test

    def summary(self) -> List[Tuple[str, float, float, float, float]]:
        result = []
        for i, name in enumerate(self.feature_names):
            result.append((
                name,
                float(self.hazard_ratios[i]),
                float(self.confidence_intervals[0][i]),
                float(self.confidence_intervals[1][i]),
                float(self.p_values[i]),
            ))
        return result


# ---------------------------------------------------------------------------
# Effect Size Calculator
# ---------------------------------------------------------------------------

class EffectSizeCalculator:
    """Compute various effect size measures."""

    @staticmethod
    def cohens_d(group1: NDArray, group2: NDArray, pooled: bool = True) -> float:
        n1, n2 = len(group1), len(group2)
        var1, var2 = np.var(group1, ddof=1), np.var(group2, ddof=1)
        if pooled:
            sp = np.sqrt(((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2))
        else:
            sp = np.sqrt((var1 + var2) / 2)
        return float((np.mean(group1) - np.mean(group2)) / sp) if sp > 0 else 0.0

    @staticmethod
    def hedges_g(group1: NDArray, group2: NDArray) -> float:
        d = EffectSizeCalculator.cohens_d(group1, group2)
        n1, n2 = len(group1), len(group2)
        correction = 1 - 3 / (4 * (n1 + n2) - 9)
        return float(d * correction)

    @staticmethod
    def glass_delta(group1: NDArray, group2: NDArray) -> float:
        std_control = np.std(group2, ddof=1)
        return float((np.mean(group1) - np.mean(group2)) / std_control) if std_control > 0 else 0.0

    @staticmethod
    def cliffs_delta(group1: NDArray, group2: NDArray) -> float:
        n1, n2 = len(group1), len(group2)
        dominance = 0.0
        for x in group1:
            dominance += np.sum(x > group2) - np.sum(x < group2)
        return float(dominance / (n1 * n2))

    @staticmethod
    def eta_squared(ss_between: float, ss_total: float) -> float:
        return float(ss_between / ss_total) if ss_total > 0 else 0.0

    @staticmethod
    def omega_squared(ss_between: float, ss_total: float, ms_within: float, n: int, k: int) -> float:
        num = ss_between - (k - 1) * ms_within
        den = ss_total + ms_within
        return float(num / den) if den > 0 else 0.0

    @staticmethod
    def odds_ratio(table: NDArray) -> float:
        a, b, c, d = table[0, 0], table[0, 1], table[1, 0], table[1, 1]
        return float((a * d) / (b * c)) if (b * c) > 0 else float("inf")


# ---------------------------------------------------------------------------
# Hypothesis Testing
# ---------------------------------------------------------------------------

class HypothesisTesting:
    """Comprehensive hypothesis testing framework."""

    def __init__(self, random_state: Optional[int] = None):
        self.rng = np.random.default_rng(random_state)

    def t_test_ind(
        self,
        group1: NDArray,
        group2: NDArray,
        alternative: Alternative = Alternative.TWO_SIDED,
        equal_var: bool = False,
        effect_size: EffectSize = EffectSize.COHENS_D,
        power_analysis: bool = True,
    ) -> TestResult:
        """Independent two-sample t-test (Welch's or Student's)."""
        n1, n2 = len(group1), len(group2)
        m1, m2 = np.mean(group1), np.mean(group2)
        v1, v2 = np.var(group1, ddof=1), np.var(group2, ddof=1)

        if equal_var:
            sp = np.sqrt(((n1 - 1) * v1 + (n2 - 1) * v2) / (n1 + n2 - 2))
            se = sp * np.sqrt(1 / n1 + 1 / n2)
            df = n1 + n2 - 2
        else:
            se = np.sqrt(v1 / n1 + v2 / n2)
            df = (v1 / n1 + v2 / n2) ** 2 / (
                (v1 / n1) ** 2 / (n1 - 1) + (v2 / n2) ** 2 / (n2 - 1)
            )

        t_stat = (m1 - m2) / se if se > 0 else 0.0

        if alternative == Alternative.TWO_SIDED:
            p_value = 2 * (1 - self._t_cdf(abs(t_stat), df))
        elif alternative == Alternative.GREATER:
            p_value = 1 - self._t_cdf(t_stat, df)
        else:
            p_value = self._t_cdf(t_stat, df)

        # Compute effect size
        es_val = self._compute_effect_size(group1, group2, effect_size)

        # Confidence interval for difference
        t_crit = self._t_ppf(1 - 0.025, df)
        diff = m1 - m2
        ci_lower = diff - t_crit * se
        ci_upper = diff + t_crit * se

        # Power analysis
        power = None
        if power_analysis:
            power = self._t_test_power(t_stat, df, n1, n2, alpha=0.05)

        return TestResult(
            test_name="Welch's t-test" if not equal_var else "Student's t-test",
            statistic=float(t_stat),
            p_value=float(p_value),
            effect_size=es_val,
            effect_size_type=effect_size,
            ci_lower=float(ci_lower),
            ci_upper=float(ci_upper),
            power=power,
            sample_size_1=n1,
            sample_size_2=n2,
            df=float(df),
            alternative=alternative,
        )

    def t_test_paired(
        self,
        before: NDArray,
        after: NDArray,
        alternative: Alternative = Alternative.TWO_SIDED,
        effect_size: EffectSize = EffectSize.COHENS_D,
    ) -> TestResult:
        """Paired sample t-test."""
        differences = after - before
        n = len(differences)
        mean_d = np.mean(differences)
        std_d = np.std(differences, ddof=1)
        se = std_d / np.sqrt(n)
        t_stat = mean_d / se if se > 0 else 0.0
        df = n - 1

        if alternative == Alternative.TWO_SIDED:
            p_value = 2 * (1 - self._t_cdf(abs(t_stat), df))
        elif alternative == Alternative.GREATER:
            p_value = 1 - self._t_cdf(t_stat, df)
        else:
            p_value = self._t_cdf(t_stat, df)

        t_crit = self._t_ppf(1 - 0.025, df)
        ci_lower = mean_d - t_crit * se
        ci_upper = mean_d + t_crit * se

        es_val = EffectSizeCalculator.cohens_d(differences, np.zeros_like(differences)) if np.std(differences) > 0 else 0.0

        return TestResult(
            test_name="Paired t-test",
            statistic=float(t_stat),
            p_value=float(p_value),
            effect_size=es_val,
            effect_size_type=EffectSize.COHENS_D,
            ci_lower=float(ci_lower),
            ci_upper=float(ci_upper),
            sample_size_1=n,
            df=float(df),
            alternative=alternative,
        )

    def mann_whitney_u(
        self,
        group1: NDArray,
        group2: NDArray,
        alternative: Alternative = Alternative.TWO_SIDED,
    ) -> TestResult:
        """Mann-Whitney U test (non-parametric two-sample test)."""
        n1, n2 = len(group1), len(group2)
        combined = np.concatenate([group1, group2])
        ranks = self._rankdata(combined)
        r1 = ranks[:n1]

        u1 = np.sum(r1) - n1 * (n1 + 1) / 2
        u2 = n1 * n2 - u1
        u_stat = min(u1, u2)

        # Normal approximation
        mean_u = n1 * n2 / 2
        std_u = np.sqrt(n1 * n2 * (n1 + n2 + 1) / 12)
        z_stat = (u_stat - mean_u) / std_u if std_u > 0 else 0.0

        if alternative == Alternative.TWO_SIDED:
            p_value = 2 * (1 - self._normal_cdf(abs(z_stat)))
        elif alternative == Alternative.LESS:
            p_value = self._normal_cdf(z_stat)
        else:
            p_value = 1 - self._normal_cdf(z_stat)

        # Cliff's delta as effect size
        es_val = EffectSizeCalculator.cliffs_delta(group1, group2)

        return TestResult(
            test_name="Mann-Whitney U",
            statistic=float(u_stat),
            p_value=float(p_value),
            effect_size=es_val,
            effect_size_type=EffectSize.CLIFFS_DELTA,
            sample_size_1=n1,
            sample_size_2=n2,
            alternative=alternative,
        )

    def wilcoxon_signed_rank(
        self,
        sample1: NDArray,
        sample2: NDArray,
        alternative: Alternative = Alternative.TWO_SIDED,
    ) -> TestResult:
        """Wilcoxon signed-rank test for paired samples."""
        differences = sample1 - sample2
        non_zero = differences[differences != 0]
        n = len(non_zero)

        abs_diff = np.abs(non_zero)
        ranks = self._rankdata(abs_diff)
        signed_ranks = ranks * np.sign(non_zero)

        w_pos = np.sum(signed_ranks[signed_ranks > 0])
        w_neg = np.sum(np.abs(signed_ranks[signed_ranks < 0]))
        w_stat = min(w_pos, w_neg)

        # Normal approximation
        mean_w = n * (n + 1) / 4
        std_w = np.sqrt(n * (n + 1) * (2 * n + 1) / 24)
        z_stat = (w_stat - mean_w) / std_w if std_w > 0 else 0.0

        if alternative == Alternative.TWO_SIDED:
            p_value = 2 * (1 - self._normal_cdf(abs(z_stat)))
        elif alternative == Alternative.LESS:
            p_value = self._normal_cdf(z_stat)
        else:
            p_value = 1 - self._normal_cdf(z_stat)

        return TestResult(
            test_name="Wilcoxon signed-rank",
            statistic=float(w_stat),
            p_value=float(p_value),
            sample_size_1=n,
            alternative=alternative,
        )

    def one_way_anova(
        self,
        groups: List[NDArray],
        effect_size: EffectSize = EffectSize.ETA_SQUARED,
    ) -> TestResult:
        """One-way ANOVA for comparing multiple group means."""
        k = len(groups)
        all_data = np.concatenate(groups)
        n_total = len(all_data)
        grand_mean = np.mean(all_data)

        ss_between = sum(len(g) * (np.mean(g) - grand_mean) ** 2 for g in groups)
        ss_within = sum(np.sum((g - np.mean(g)) ** 2) for g in groups)
        ss_total = ss_between + ss_within

        df_between = k - 1
        df_within = n_total - k

        ms_between = ss_between / df_between if df_between > 0 else 0
        ms_within = ss_within / df_within if df_within > 0 else 1e-10

        f_stat = ms_between / ms_within if ms_within > 0 else 0
        p_value = 1 - self._f_cdf(f_stat, df_between, df_within)

        if effect_size == EffectSize.ETA_SQUARED:
            es_val = EffectSizeCalculator.eta_squared(ss_between, ss_total)
        elif effect_size == EffectSize.OMEGA_SQUARED:
            es_val = EffectSizeCalculator.omega_squared(ss_between, ss_total, ms_within, n_total, k)
        else:
            es_val = None

        return TestResult(
            test_name="One-way ANOVA",
            statistic=float(f_stat),
            p_value=float(p_value),
            effect_size=es_val,
            effect_size_type=effect_size,
            df=float(df_within),
            sample_size_1=n_total,
            alpha=0.05,
        )

    def chi_square_test(
        self,
        observed: NDArray,
        expected: Optional[NDArray] = None,
    ) -> TestResult:
        """Chi-square goodness-of-fit or independence test."""
        if expected is None:
            expected = np.full_like(observed, np.sum(observed) / observed.size, dtype=float)

        chi2 = float(np.sum((observed - expected) ** 2 / expected))
        df = observed.size - 1
        p_value = 1 - self._chi2_cdf(chi2, df)

        return TestResult(
            test_name="Chi-square test",
            statistic=chi2,
            p_value=float(p_value),
            df=float(df),
        )

    def permutation_test(
        self,
        group1: NDArray,
        group2: NDArray,
        statistic: Callable[[NDArray, NDArray], float] = lambda a, b: np.mean(a) - np.mean(b),
        n_permutations: int = 10000,
    ) -> PermutationTestResult:
        """Non-parametric permutation test."""
        observed = statistic(group1, group2)
        combined = np.concatenate([group1, group2])
        n1 = len(group1)

        perm_stats = np.zeros(n_permutations)
        for i in range(n_permutations):
            perm = self.rng.permutation(combined)
            perm_stats[i] = statistic(perm[:n1], perm[n1:])

        p_value = float(np.mean(np.abs(perm_stats) >= np.abs(observed)))

        return PermutationTestResult(
            observed_statistic=float(observed),
            p_value=p_value,
            n_permutations=n_permutations,
            permutation_distribution=perm_stats,
        )

    def batch_test(
        self,
        groups: List[NDArray],
        control: NDArray,
    ) -> List[TestResult]:
        """Run pairwise tests between control and each treatment group."""
        results = []
        for i, group in enumerate(groups):
            result = self.t_test_ind(control, group, effect_size=EffectSize.COHENS_D)
            result.test_name = f"Group {i + 1} vs Control"
            results.append(result)
        return results

    def multiple_comparison_correction(
        self,
        results: List[TestResult],
        method: CorrectionMethod = CorrectionMethod.BENJAMINI_HOCHBERG,
    ) -> List[TestResult]:
        """Apply multiple comparison correction to batch test results."""
        p_values = [r.p_value for r in results]
        n = len(p_values)

        if method == CorrectionMethod.NONE:
            adjusted = p_values
        elif method == CorrectionMethod.BONFERRONI:
            adjusted = [min(p * n, 1.0) for p in p_values]
        elif method == CorrectionMethod.HOLM:
            indexed = sorted(enumerate(p_values), key=lambda x: x[1])
            adjusted_arr = np.zeros(n)
            for rank, (orig_idx, p) in enumerate(indexed):
                adjusted_arr[orig_idx] = min(p * (n - rank), 1.0)
            adjusted = adjusted_arr.tolist()
        elif method == CorrectionMethod.BENJAMINI_HOCHBERG:
            indexed = sorted(enumerate(p_values), key=lambda x: x[1], reverse=True)
            adjusted_arr = np.zeros(n)
            cumulative_min = 1.0
            for rank, (orig_idx, p) in enumerate(indexed):
                adjusted_val = min(p * n / (n - rank), 1.0)
                cumulative_min = min(cumulative_min, adjusted_val)
                adjusted_arr[orig_idx] = cumulative_min
            adjusted = adjusted_arr.tolist()
        else:
            adjusted = p_values

        corrected_results = []
        for result, adj_p in zip(results, adjusted):
            corrected = TestResult(
                test_name=result.test_name,
                statistic=result.statistic,
                p_value=adj_p,
                effect_size=result.effect_size,
                effect_size_type=result.effect_size_type,
                ci_lower=result.ci_lower,
                ci_upper=result.ci_upper,
                power=result.power,
                sample_size_1=result.sample_size_1,
                sample_size_2=result.sample_size_2,
                df=result.df,
                alternative=result.alternative,
                alpha=result.alpha,
            )
            corrected_results.append(corrected)
        return corrected_results

    # -- Distribution helpers (minimal, avoid scipy dependency) --
    def _t_cdf(self, t: float, df: float) -> float:
        """Approximate Student's t CDF via normal for large df."""
        if df > 30:
            return self._normal_cdf(t)
        # Rough approximation using normal with correction
        z = t * (1 - 1 / (4 * df)) / np.sqrt(1 + t ** 2 / (2 * df))
        return self._normal_cdf(z)

    def _t_ppf(self, p: float, df: float) -> float:
        """Approximate Student's t PPF."""
        if df > 30:
            return self._normal_ppf(p)
        # Rough approximation
        z = self._normal_ppf(p)
        return z + (z ** 3 + z) / (4 * df)

    def _normal_cdf(self, z: float) -> float:
        return 0.5 * (1 + np.math.erf(z / np.sqrt(2)))

    def _normal_ppf(self, p: float) -> float:
        """Rational approximation to inverse normal CDF."""
        if p <= 0 or p >= 1:
            return 0.0
        if p < 0.5:
            return -self._normal_ppf(1 - p)
        t = np.sqrt(-2 * np.log(1 - p))
        c0, c1, c2 = 2.515517, 0.802853, 0.010328
        d1, d2, d3 = 1.432788, 0.189269, 0.001308
        return t - (c0 + c1 * t + c2 * t ** 2) / (1 + d1 * t + d2 * t ** 2 + d3 * t ** 3)

    def _f_cdf(self, f: float, df1: float, df2: float) -> float:
        """Approximate F-distribution CDF."""
        if df1 <= 0 or df2 <= 0 or f <= 0:
            return 0.0
        x = df2 / (df2 + df1 * f)
        # Use beta regularized approximation
        return 1.0 - self._beta_incomplete(df1 / 2, df2 / 2, x)

    def _chi2_cdf(self, x: float, df: float) -> float:
        """Approximate chi-squared CDF."""
        if x <= 0:
            return 0.0
        return self._gamma_lower(df / 2, x / 2) / self._gamma_func(df / 2)

    def _gamma_func(self, z: float) -> float:
        """Lanczos approximation for gamma function."""
        g = 7
        coeffs = [0.99999999999980993, 676.5203681218851, -1259.1392167224028,
                  771.32342877765313, -176.61502916214059, 12.507343278686905,
                  -0.13857109526572012, 9.9843695780195716e-6, 1.5056327351493116e-7]
        if z < 0.5:
            return np.pi / (np.sin(np.pi * z) * self._gamma_func(1 - z))
        z -= 1
        x = coeffs[0]
        for i in range(1, g + 2):
            x += coeffs[i] / (z + i)
        t = z + g + 0.5
        return np.sqrt(2 * np.pi) * (t ** (z + 0.5)) * np.exp(-t) * x

    def _beta_incomplete(self, a: float, b: float, x: float) -> float:
        """Incomplete beta function approximation."""
        if x <= 0:
            return 0.0
        if x >= 1:
            return 1.0
        # Continued fraction approximation
        max_iter = 200
        eps = 1e-14
        qab = a + b
        qap = a + 1
        qam = a - 1
        c = 1.0
        d = 1.0 - qab * x / qap
        if abs(d) < 1e-30:
            d = 1e-30
        d = 1.0 / d
        h = d
        for m in range(1, max_iter + 1):
            m2 = 2 * m
            aa = m * (b - m) * x / ((qam + m2) * (a + m2))
            d = 1.0 + aa * d
            if abs(d) < 1e-30:
                d = 1e-30
            c = 1.0 + aa / c
            if abs(c) < 1e-30:
                c = 1e-30
            d = 1.0 / d
            h *= d * c
            aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
            d = 1.0 + aa * d
            if abs(d) < 1e-30:
                d = 1e-30
            c = 1.0 + aa / c
            if abs(c) < 1e-30:
                c = 1e-30
            d = 1.0 / d
            del_val = d * c
            h *= del_val
            if abs(del_val - 1.0) < eps:
                break
        return np.exp(a * np.log(x) + b * np.log(1 - x) - np.log(a)) * h / a

    def _gamma_lower(self, a: float, x: float) -> float:
        """Lower incomplete gamma function."""
        if x <= 0:
            return 0.0
        if x < a + 1:
            # Series expansion
            total = 1.0 / a
            term = 1.0 / a
            for n in range(1, 200):
                term *= x / (a + n)
                total += term
                if abs(term) < 1e-14 * abs(total):
                    break
            return total * np.exp(-x + a * np.log(x) - np.log(self._gamma_func(a)))
        else:
            # Continued fraction
            f = 1e-30
            c = f
            d = 0.0
            for i in range(1, 201):
                if i % 2 == 1:
                    an = (i + 1) // 2
                    b = x + 2 * an - 1
                else:
                    an = i // 2
                    b = x + 2 * an - 1
                    a_coeff = an * (a - an)
                    b_coeff = x + 2 * an - 1
                    # Use Lentz's algorithm
                if i == 1:
                    d = (x + 1 - a) if (x + 1 - a) != 0 else 1e-30
                    d = 1.0 / d
                    c = d
                    f = d
                    continue
                # Simplified continued fraction
                if i % 2 == 1:
                    b_val = x + 2 * ((i + 1) // 2) - 1
                    a_val = -((i - 1) // 2 + 1) * (((i - 1) // 2 + 1) - 1 - a + a)
                else:
                    b_val = x + 2 * (i // 2) - 1
                    a_val = -(i // 2) * (i // 2 - a)
                d = b_val + a_val * d
                if abs(d) < 1e-30:
                    d = 1e-30
                c = b_val + a_val / c
                if abs(c) < 1e-30:
                    c = 1e-30
                d = 1.0 / d
                delta = c * d
                f *= delta
                if abs(delta - 1.0) < 1e-14:
                    break
        result = f * np.exp(-x + a * np.log(x) - np.log(self._gamma_func(a)))
        return self._gamma_func(a) - result

    def _rankdata(self, arr: NDArray) -> NDArray:
        """Rank data with average tie-breaking."""
        sorted_idx = np.argsort(arr)
        ranks = np.empty_like(arr, dtype=float)
        ranks[sorted_idx] = np.arange(1, len(arr) + 1, dtype=float)

        # Handle ties
        unique_vals, counts = np.unique(arr, return_counts=True)
        for val, count in zip(unique_vals, counts):
            if count > 1:
                mask = arr == val
                avg_rank = np.mean(ranks[mask])
                ranks[mask] = avg_rank
        return ranks

    def _compute_effect_size(
        self, group1: NDArray, group2: NDArray, es_type: EffectSize
    ) -> float:
        if es_type == EffectSize.COHENS_D:
            return EffectSizeCalculator.cohens_d(group1, group2)
        elif es_type == EffectSize.HEDGES_G:
            return EffectSizeCalculator.hedges_g(group1, group2)
        elif es_type == EffectSize.GLASSS_DELTA:
            return EffectSizeCalculator.glass_delta(group1, group2)
        elif es_type == EffectSize.CLIFFS_DELTA:
            return EffectSizeCalculator.cliffs_delta(group1, group2)
        return 0.0

    def _t_test_power(self, t_stat: float, df: float, n1: int, n2: int, alpha: float) -> float:
        """Post-hoc power for t-test."""
        ncp = abs(t_stat) * np.sqrt((n1 * n2) / (n1 + n2))
        t_crit = self._t_ppf(1 - alpha / 2, df)
        power = 1 - self._t_cdf(t_crit - ncp, df) + self._t_cdf(-t_crit - ncp, df)
        return float(power)


# ---------------------------------------------------------------------------
# Bootstrap Resampling
# ---------------------------------------------------------------------------

class Bootstrap:
    """Bootstrap confidence interval estimation."""

    def __init__(self, n_resamples: int = 10000, random_state: Optional[int] = None):
        self.n_resamples = n_resamples
        self.rng = np.random.default_rng(random_state)

    def confidence_interval(
        self,
        data: NDArray,
        statistic: Callable[[NDArray], float] = np.mean,
        level: ConfidenceLevel = ConfidenceLevel.PERCENTILE,
        alpha: float = 0.05,
    ) -> BootstrapResult:
        """Compute bootstrap confidence interval."""
        point_estimate = statistic(data)
        n = len(data)

        # Bootstrap resamples
        boot_stats = np.zeros(self.n_resamples)
        for i in range(self.n_resamples):
            sample = data[self.rng.choice(n, n, replace=True)]
            boot_stats[i] = statistic(sample)

        std_error = float(np.std(boot_stats, ddof=1))
        bias = float(np.mean(boot_stats) - point_estimate)

        if level == ConfidenceLevel.PERCENTILE:
            ci_lower = float(np.percentile(boot_stats, alpha / 2 * 100))
            ci_upper = float(np.percentile(boot_stats, (1 - alpha / 2) * 100))
            acceleration = None
        elif level == ConfidenceLevel.BCA:
            # Bias-corrected and accelerated
            z0 = self._normal_ppf_inner(np.mean(boot_stats < point_estimate))
            # Acceleration via jackknife
            jack_stats = np.zeros(n)
            for j in range(n):
                jack_sample = np.delete(data, j)
                jack_stats[j] = statistic(jack_sample)
            jack_mean = np.mean(jack_stats)
            num = np.sum((jack_mean - jack_stats) ** 3)
            den = 6 * (np.sum((jack_mean - jack_stats) ** 2)) ** 1.5
            acceleration = float(num / den) if den > 0 else 0.0

            z_alpha = self._normal_ppf_inner(alpha / 2)
            z_1_alpha = self._normal_ppf_inner(1 - alpha / 2)
            lower_p = self._normal_cdf_inner(z0 + (z0 + z_alpha) / (1 - acceleration * (z0 + z_alpha)))
            upper_p = self._normal_cdf_inner(z0 + (z0 + z_1_alpha) / (1 - acceleration * (z0 + z_1_alpha)))

            ci_lower = float(np.percentile(boot_stats, lower_p * 100))
            ci_upper = float(np.percentile(boot_stats, upper_p * 100))
        else:
            ci_lower = float(np.percentile(boot_stats, alpha / 2 * 100))
            ci_upper = float(np.percentile(boot_stats, (1 - alpha / 2) * 100))
            acceleration = None

        return BootstrapResult(
            point_estimate=float(point_estimate),
            ci_lower=ci_lower,
            ci_upper=ci_upper,
            std_error=std_error,
            bias=bias,
            level=level,
            alpha=alpha,
            n_resamples=self.n_resamples,
            bootstrap_distribution=boot_stats,
            acceleration=acceleration,
        )

    def _normal_ppf_inner(self, p: float) -> float:
        if p <= 0 or p >= 1:
            return 0.0
        if p < 0.5:
            return -self._normal_ppf_inner(1 - p)
        t = np.sqrt(-2 * np.log(1 - p))
        c0, c1, c2 = 2.515517, 0.802853, 0.010328
        d1, d2, d3 = 1.432788, 0.189269, 0.001308
        return t - (c0 + c1 * t + c2 * t ** 2) / (1 + d1 * t + d2 * t ** 2 + d3 * t ** 3)

    def _normal_cdf_inner(self, z: float) -> float:
        return 0.5 * (1 + np.math.erf(z / np.sqrt(2)))


# ---------------------------------------------------------------------------
# BootstrapResult (re-declare for clarity)
# ---------------------------------------------------------------------------

# Already declared above.

# ---------------------------------------------------------------------------
# Survival Analysis
# ---------------------------------------------------------------------------

class SurvivalAnalysis:
    """Survival analysis with Kaplan-Meier and Cox proportional hazards."""

    def __init__(self, random_state: Optional[int] = None):
        self.rng = np.random.default_rng(random_state)

    def kaplan_meier(
        self,
        times: NDArray,
        events: NDArray,
        groups: Optional[NDArray] = None,
        confidence_level: float = 0.95,
    ) -> KMResult:
        """Kaplan-Meier survival estimation."""
        sorted_idx = np.argsort(times)
        times_sorted = times[sorted_idx]
        events_sorted = events[sorted_idx]

        unique_times = np.unique(times_sorted)
        n_at_risk = len(times)
        survival = np.ones(len(unique_times))
        se = np.zeros(len(unique_times))
        at_risk_counts = np.zeros(len(unique_times))
        event_counts = np.zeros(len(unique_times))
        censor_counts = np.zeros(len(unique_times))

        for i, t in enumerate(unique_times):
            at_risk_counts[i] = n_at_risk
            mask_t = times_sorted == t
            d_i = np.sum(events_sorted[mask_t] == 1)
            c_i = np.sum(events_sorted[mask_t] == 0)
            event_counts[i] = d_i
            censor_counts[i] = c_i

            if n_at_risk > 0 and d_i > 0:
                survival[i] = (1 - d_i / n_at_risk) ** (1 if i == 0 else 1)
                if i > 0:
                    survival[i] = survival[i - 1] * (1 - d_i / n_at_risk)
                # Greenwood's formula
                if d_i > 0 and n_at_risk > d_i:
                    se[i] = survival[i] * np.sqrt(d_i / (n_at_risk * (n_at_risk - d_i))) if i == 0 else \
                        survival[i] * np.sqrt(np.sum(event_counts[:i + 1] / (at_risk_counts[:i + 1] * (at_risk_counts[:i + 1] - event_counts[:i + 1]))))
            else:
                if i > 0:
                    survival[i] = survival[i - 1]

            n_at_risk -= (d_i + c_i)

        # Confidence intervals
        z = 1.96
        ci_lower = np.maximum(0, survival - z * se)
        ci_upper = np.minimum(1, survival + z * se)

        return KMResult(
            times=unique_times,
            survival=survival,
            standard_errors=se,
            confidence_intervals=(ci_lower, ci_upper),
            at_risk=at_risk_counts,
            events=event_counts,
            censored=censor_counts,
            n_subjects=len(times),
        )

    def log_rank_test(
        self,
        km_result_a: KMResult,
        km_result_b: KMResult,
        group_a: str = "A",
        group_b: str = "B",
    ) -> TestResult:
        """Log-rank test comparing two survival curves."""
        # Simplified log-rank using observed vs expected events
        events_a = np.sum(km_result_a.events)
        events_b = np.sum(km_result_b.events)
        n_a = km_result_a.n_subjects
        n_b = km_result_b.n_subjects
        total_events = events_a + events_b
        total_n = n_a + n_b

        expected_a = total_events * n_a / total_n if total_n > 0 else 0
        observed_minus_expected = events_a - expected_a

        # Variance (simplified)
        variance = total_events * (n_a / total_n) * (n_b / total_n) * (total_n - total_events) / (total_n - 1) if total_n > 1 else 1

        chi2 = (observed_minus_expected ** 2 / variance) if variance > 0 else 0
        p_value = 1 - 0.5 * (1 + np.math.erf(np.sqrt(chi2 / 2)))

        return TestResult(
            test_name="Log-rank test",
            statistic=float(chi2),
            p_value=float(p_value),
            sample_size_1=n_a,
            sample_size_2=n_b,
        )

    def cox_ph(
        self,
        times: NDArray,
        events: NDArray,
        covariates: NDArray,
        covariate_names: Optional[List[str]] = None,
    ) -> CoxResult:
        """Cox proportional hazards regression (Breslow approximation)."""
        n = len(times)
        p = covariates.shape[1]
        if covariate_names is None:
            covariate_names = [f"x{i}" for i in range(p)]

        # Sort by time
        sorted_idx = np.argsort(times)
        times_s = times[sorted_idx]
        events_s = events[sorted_idx]
        cov_s = covariates[sorted_idx]

        # Initialize coefficients
        beta = np.zeros(p)
        max_iter = 50
        tol = 1e-6

        for iteration in range(max_iter):
            # Risk set and linear predictor
            eta = cov_s @ beta
            exp_eta = np.exp(eta)

            # Score function and Hessian (partial likelihood)
            score = np.zeros(p)
            hessian = np.zeros((p, p))

            event_times = np.unique(times_s[events_s == 1])

            for t_event in event_times:
                at_risk = times_s >= t_event
                d = np.sum((times_s == t_event) & (events_s == 1))
                risk_exp = exp_eta[at_risk]
                risk_cov = cov_s[at_risk]

                weighted_sum = np.sum(risk_exp)
                weighted_cov_sum = risk_cov @ risk_exp if risk_cov.ndim > 1 else risk_cov * risk_exp

                if weighted_sum > 0:
                    mean_cov = weighted_cov_sum / weighted_sum
                    if risk_cov.ndim > 1:
                        weighted_sq_sum = (risk_cov ** 2).T @ risk_exp
                        var_cov = weighted_sq_sum / weighted_sum - mean_cov ** 2
                    else:
                        var_cov = np.var(risk_cov) * np.mean(risk_exp) / weighted_sum

                    score += d * (cov_s[times_s == t_event].mean(axis=0) - mean_cov)
                    if risk_cov.ndim > 1:
                        outer = np.outer(mean_cov, mean_cov)
                        hessian -= d * (var_cov - outer) if isinstance(var_cov, np.ndarray) else d * np.diag(var_cov - outer.diagonal())

            # Newton-Raphson update
            try:
                step = np.linalg.solve(hessian, score)
            except np.linalg.LinAlgError:
                step = np.linalg.lstsq(hessian, score, rcond=None)[0]

            beta += step

            if np.max(np.abs(step)) < tol:
                break

        # Standard errors from observed information
        eta_final = cov_s @ beta
        exp_eta_final = np.exp(eta_final)
        var_matrix = np.zeros((p, p))

        event_times = np.unique(times_s[events_s == 1])
        for t_event in event_times:
            at_risk = times_s >= t_event
            risk_exp = exp_eta_final[at_risk]
            risk_cov = cov_s[at_risk]
            weighted_sum = np.sum(risk_exp)

            if weighted_sum > 0 and risk_cov.ndim > 1:
                mean_cov = (risk_cov.T @ risk_exp) / weighted_sum
                weighted_sq = (risk_cov ** 2).T @ risk_exp / weighted_sum
                var_matrix += weighted_sq - np.outer(mean_cov, mean_cov)

        try:
            var_beta = np.linalg.inv(-var_matrix)
        except np.linalg.LinAlgError:
            var_beta = np.eye(p) * 1e6

        se = np.sqrt(np.diag(var_beta))
        hr = np.exp(beta)
        z = beta / se
        p_values = 2 * (1 - 0.5 * (1 + np.math.erf(np.abs(z) / np.sqrt(2))))
        ci_lower = np.exp(beta - 1.96 * se)
        ci_upper = np.exp(beta + 1.96 * se)

        # Log-likelihood
        ll = np.sum(eta_final * events_s - np.log(np.cumsum(exp_eta_final[::-1])[::-1] + 1e-300) * events_s)
        aic = -2 * ll + 2 * (p + 1)

        # Concordance index (simplified)
        concordant = 0
        total_pairs = 0
        for i in range(n):
            for j in range(i + 1, n):
                if times_s[i] != times_s[j]:
                    total_pairs += 1
                    if times_s[i] < times_s[j] and events_s[i] == 1:
                        if eta_final[i] > eta_final[j]:
                            concordant += 1
                    elif times_s[j] < times_s[i] and events_s[j] == 1:
                        if eta_final[j] > eta_final[i]:
                            concordant += 1
        concordance = concordant / total_pairs if total_pairs > 0 else 0.5

        return CoxResult(
            hazard_ratios=hr,
            coefficients=beta,
            standard_errors=se,
            z_values=z,
            p_values=p_values,
            confidence_intervals=(ci_lower, ci_upper),
            feature_names=covariate_names,
            log_likelihood=float(ll),
            aic=float(aic),
            concordance=float(concordance),
            n_events=int(np.sum(events)),
            n_subjects=n,
        )


# ---------------------------------------------------------------------------
# Main Demo
# ---------------------------------------------------------------------------

def main() -> None:
    """Demonstrate statistical analysis capabilities."""
    print("=" * 70)
    print("Statistical Analysis Toolkit - Demo")
    print("=" * 70)

    rng = np.random.default_rng(42)

    # --- 1. Hypothesis Testing ---
    print("\n--- Hypothesis Testing ---")
    treatment = rng.normal(105, 15, 50)
    control = rng.normal(100, 15, 50)

    ht = HypothesisTesting(random_state=42)
    result = ht.t_test_ind(treatment, control, effect_size=EffectSize.COHENS_D)
    print(f"  {result.test_name}")
    print(f"  t-statistic: {result.statistic:.4f}")
    print(f"  p-value:     {result.p_value:.6f}")
    print(f"  Cohen's d:   {result.effect_size:.4f} ({result.effect_size_interpretation})")
    print(f"  95% CI:      [{result.ci_lower:.4f}, {result.ci_upper:.4f}]")
    print(f"  Significant: {result.significant()}")

    # --- 2. Mann-Whitney U ---
    print("\n--- Mann-Whitney U Test ---")
    non_param_result = ht.mann_whitney_u(treatment, control)
    print(f"  U-statistic: {non_param_result.statistic:.4f}")
    print(f"  p-value:     {non_param_result.p_value:.6f}")
    print(f"  Cliff's delta: {non_param_result.effect_size:.4f}")

    # --- 3. One-way ANOVA ---
    print("\n--- One-way ANOVA ---")
    group_a = rng.normal(100, 15, 30)
    group_b = rng.normal(110, 15, 30)
    group_c = rng.normal(105, 15, 30)
    anova_result = ht.one_way_anova([group_a, group_b, group_c])
    print(f"  F-statistic: {anova_result.statistic:.4f}")
    print(f"  p-value:     {anova_result.p_value:.6f}")
    print(f"  Eta-squared: {anova_result.effect_size:.4f}")

    # --- 4. Bootstrap ---
    print("\n--- Bootstrap Confidence Interval ---")
    boot = Bootstrap(n_resamples=5000, random_state=42)
    boot_result = boot.confidence_interval(
        data=treatment, statistic=np.median, level=ConfidenceLevel.BCA
    )
    print(f"  Point estimate:  {boot_result.point_estimate:.4f}")
    print(f"  BCa 95% CI:      [{boot_result.ci_lower:.4f}, {boot_result.ci_upper:.4f}]")
    print(f"  Bootstrap SE:    {boot_result.std_error:.4f}")
    print(f"  Bias:            {boot_result.bias:.4f}")

    # --- 5. Survival Analysis ---
    print("\n--- Survival Analysis ---")
    sa = SurvivalAnalysis(random_state=42)
    times = rng.exponential(12, 100)
    events = rng.binomial(1, 0.7, 100).astype(float)

    km = sa.kaplan_meier(times, events)
    print(f"  Median survival: {km.median_survival:.2f}")
    print(f"  Survival at 12 months: {km.survival_at(12):.3f}")
    print(f"  Subjects: {km.n_subjects}")

    print("\n" + "=" * 70)
    print("Demo complete.")
    print("=" * 70)


if __name__ == "__main__":
    main()