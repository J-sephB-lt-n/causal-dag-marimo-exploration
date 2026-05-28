"""
Simulate data from the education-income causal DAG using ancestral sampling
with numpy/scipy.

All monetary values are in ZAR (South African Rand).
Income is monthly. Family wealth is total household net worth (stock).

Usage
-----
    from data_gen_func import simulate_dag

    # Observational sample
    df = simulate_dag(n=5_000)

    # Interventional: do(education_level='3-tertiary-undergrad')
    df_do = simulate_dag(n=5_000, education_level='3-tertiary-undergrad')
"""

import numpy as np
import polars as pl
from scipy.special import softmax
from scipy.stats import truncnorm

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

PROVINCES = [
    "Gauteng",
    "KwaZulu-Natal",
    "Western Cape",
    "Eastern Cape",
    "Limpopo",
    "Mpumalanga",
    "North West",
    "Free State",
    "Northern Cape",
]

PROVINCE_WEIGHTS = np.array([0.26, 0.20, 0.12, 0.11, 0.10, 0.08, 0.07, 0.05, 0.02])
PROVINCE_WEIGHTS = PROVINCE_WEIGHTS / PROVINCE_WEIGHTS.sum()

PROVINCE_WAGE_SCALAR = np.array([
    1.35,  # Gauteng
    0.95,  # KwaZulu-Natal
    1.25,  # Western Cape
    0.80,  # Eastern Cape
    0.75,  # Limpopo
    0.85,  # Mpumalanga
    0.82,  # North West
    0.83,  # Free State
    0.88,  # Northern Cape
])

# 1 = rural, 0 = urban
PROVINCE_IS_RURAL = np.array([0, 0, 0, 1, 1, 1, 1, 0, 1], dtype=float)

EDUCATION_LEVELS = [
    "0-no-formal-education",
    "1-primary",
    "2-secondary",
    "3-tertiary-undergrad",
    "4-tertiary-masters",
    "5-tertiary-phd",
]

INSTITUTION_LEVELS = ["none", "community_college", "university", "elite_university"]

OCCUPATIONS = ["unemployed", "manual", "service", "professional", "executive"]

PARENTS_EDU_PROBS = np.array([0.08, 0.17, 0.45, 0.22, 0.06, 0.02])

# LogNormal (mu, sigma) for family wealth by parents_education index
WEALTH_MU    = np.array([8.8,  9.5, 10.3, 11.5, 12.4, 13.0])
WEALTH_SIGMA = np.array([1.2,  1.1,  1.0,  0.9,  0.8,  0.7])

# Monthly income log-means by occupation index
OCCUPATION_LOG_MU = np.log(np.array([3_000, 10_000, 15_000, 30_000, 100_000], dtype=float))


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _sigmoid(x: np.ndarray) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-np.clip(x, -30, 30)))


def _categorical(rng: np.random.Generator, probs: np.ndarray) -> np.ndarray:
    """Row-wise categorical draw from a (n, k) probability matrix."""
    cumulative = probs.cumsum(axis=1)
    u = rng.random((len(probs), 1))
    return (u > cumulative).sum(axis=1).astype(int)


# ---------------------------------------------------------------------------
# Main simulation function
# ---------------------------------------------------------------------------

def simulate_dag(
    n: int,
    education_level: str | None = None,
    seed: int = 42,
) -> pl.DataFrame:
    """
    Simulate n observations from the education-income causal DAG via
    ancestral sampling.

    Parameters
    ----------
    n : int
        Number of samples to generate.
    education_level : str or None
        Causal intervention do(education_level=e). Must be one of
        EDUCATION_LEVELS. When set, education_level is fixed for all
        observations rather than sampled from its observational distribution.
    seed : int
        Random seed for reproducibility.

    Returns
    -------
    pl.DataFrame
    """
    if education_level is not None and education_level not in EDUCATION_LEVELS:
        raise ValueError(
            f"education_level must be one of {EDUCATION_LEVELS}, got '{education_level}'"
        )

    rng = np.random.default_rng(seed)

    # ------------------------------------------------------------------
    # 1. ability_motivation  ~  N(0, 1)
    # ------------------------------------------------------------------
    ability = rng.standard_normal(n)

    # ------------------------------------------------------------------
    # 2. location  ~  Categorical(province_weights)
    # ------------------------------------------------------------------
    location_idx = rng.choice(len(PROVINCES), size=n, p=PROVINCE_WEIGHTS)
    is_rural     = PROVINCE_IS_RURAL[location_idx]
    wage_scalar  = PROVINCE_WAGE_SCALAR[location_idx]

    # ------------------------------------------------------------------
    # 3. parents_education  ~  Categorical(SA marginals)
    # ------------------------------------------------------------------
    parents_edu_idx = rng.choice(len(EDUCATION_LEVELS), size=n, p=PARENTS_EDU_PROBS)

    # ------------------------------------------------------------------
    # 4. family_wealth  ~  LogNormal(mu[parents_edu], sigma[parents_edu])
    # ------------------------------------------------------------------
    wealth_mu_vec    = WEALTH_MU[parents_edu_idx]
    wealth_sigma_vec = WEALTH_SIGMA[parents_edu_idx]
    family_wealth    = rng.lognormal(mean=wealth_mu_vec, sigma=wealth_sigma_vec)

    log_wealth        = np.log(family_wealth)
    log_wealth_scaled = (log_wealth - log_wealth.mean()) / (log_wealth.std() + 1e-8)

    # ------------------------------------------------------------------
    # 5. test_scores  ~  TruncatedNormal(50 + 15*ability, 15) in [0, 100]
    # ------------------------------------------------------------------
    ts_mu    = 50.0 + 15.0 * ability
    ts_sigma = 15.0
    a_clip   = (0.0   - ts_mu) / ts_sigma
    b_clip   = (100.0 - ts_mu) / ts_sigma
    test_scores = truncnorm.rvs(
        a_clip, b_clip,
        loc=ts_mu, scale=ts_sigma,
        random_state=rng.integers(2**31),
    )

    # ------------------------------------------------------------------
    # 6. scholarship  ~  Bernoulli(sigmoid(logit))
    # ------------------------------------------------------------------
    test_scores_scaled = (test_scores - 50.0) / 15.0
    scholarship_logit  = (
        -3.8
        - 0.8 * log_wealth_scaled
        + 0.6 * ability
        + 0.8 * test_scores_scaled
    )
    scholarship = (rng.random(n) < _sigmoid(scholarship_logit)).astype(float)

    # ------------------------------------------------------------------
    # 7. education_institution  ~  Categorical(softmax(logits))
    #    0=none, 1=community_college, 2=university, 3=elite_university
    # ------------------------------------------------------------------
    parents_edu_f = parents_edu_idx.astype(float)

    inst_logits = np.column_stack([
        np.zeros(n),
        1.5 + 0.3 * ability + 0.2 * parents_edu_f + 0.3 * log_wealth_scaled - 0.5 * is_rural,
       -0.5 + 0.8 * ability + 0.6 * parents_edu_f + 0.6 * log_wealth_scaled - 0.8 * is_rural,
       -3.0 + 1.2 * ability + 0.8 * parents_edu_f + 1.0 * log_wealth_scaled - 1.2 * is_rural,
    ])
    inst_probs = softmax(inst_logits, axis=1)
    inst_idx   = _categorical(rng, inst_probs)

    # ------------------------------------------------------------------
    # 8. education_level  ~  Categorical(softmax(logits))  OR  do()
    # ------------------------------------------------------------------
    inst_f           = inst_idx.astype(float)
    is_univ_or_elite = (inst_idx >= 2).astype(float)
    is_elite         = (inst_idx == 3).astype(float)

    if education_level is not None:
        edu_idx = np.full(n, EDUCATION_LEVELS.index(education_level), dtype=int)
    else:
        edu_logits = np.column_stack([
            np.zeros(n),
            0.5  + 0.2 * parents_edu_f + 0.1 * ability,
            2.0  + 0.4 * parents_edu_f + 0.3 * ability + 0.3 * log_wealth_scaled - 0.3 * is_rural,
            0.0  + 0.7 * parents_edu_f + 0.8 * ability + 0.7 * log_wealth_scaled - 0.5 * is_rural + 1.5 * is_univ_or_elite + 0.8 * scholarship,
           -2.0  + 0.6 * parents_edu_f + 0.9 * ability + 0.6 * log_wealth_scaled - 0.6 * is_rural + 1.2 * is_elite          + 0.5 * scholarship,
           -4.0  + 0.5 * parents_edu_f + 1.0 * ability + 0.5 * log_wealth_scaled - 0.8 * is_rural + 1.0 * is_elite          + 0.4 * scholarship,
        ])
        edu_probs = softmax(edu_logits, axis=1)
        edu_idx   = _categorical(rng, edu_probs)

    # ------------------------------------------------------------------
    # 9. profess_network  ~  Beta(alpha, beta)
    #    mu = sigmoid(-3 + 0.7*edu + 0.6*inst), kappa=6
    # ------------------------------------------------------------------
    edu_f      = edu_idx.astype(float)
    network_mu = _sigmoid(-3.0 + 0.7 * edu_f + 0.6 * inst_f)
    kappa      = 6.0
    net_alpha  = np.clip(network_mu * kappa,         0.01, None)
    net_beta   = np.clip((1.0 - network_mu) * kappa, 0.01, None)
    profess_network = rng.beta(net_alpha, net_beta)

    # ------------------------------------------------------------------
    # 10. occupation  ~  Categorical(softmax(logits))
    # ------------------------------------------------------------------
    occ_logits = np.column_stack([
        np.zeros(n),
        1.5  + 0.2 * edu_f - 0.3 * profess_network + 0.3 * is_rural,
        1.0  + 0.4 * edu_f + 0.4 * profess_network - 0.2 * is_rural,
       -2.0  + 1.0 * edu_f + 0.8 * profess_network + 0.6 * inst_f - 0.4 * is_rural,
       -5.0  + 0.8 * edu_f + 1.2 * profess_network + 1.0 * inst_f - 0.3 * is_rural,
    ])
    occ_probs = softmax(occ_logits, axis=1)
    occ_idx   = _categorical(rng, occ_probs)

    # ------------------------------------------------------------------
    # 11. income  ~  LogNormal(log_mu, sigma=0.6)  monthly ZAR
    # ------------------------------------------------------------------
    occ_base     = OCCUPATION_LOG_MU[occ_idx]
    income_log_mu = (
        occ_base
        + 0.15 * edu_f
        + 0.10 * inst_f
        + 0.20 * profess_network
        + 0.05 * log_wealth_scaled
        + 0.10 * ability
        + np.log(wage_scalar)
    )
    income = rng.lognormal(mean=income_log_mu, sigma=0.6)

    # ------------------------------------------------------------------
    # 12. survey_participation  ~  Bernoulli(sigmoid(logit))
    # ------------------------------------------------------------------
    log_income        = np.log(income)
    log_income_scaled = (log_income - log_income.mean()) / (log_income.std() + 1e-8)
    survey_logit      = (
        -1.5
        + 0.3 * edu_f
        + 0.2 * log_income_scaled
        - 0.4 * is_rural
    )
    survey_participation = rng.random(n) < _sigmoid(survey_logit)

    # ------------------------------------------------------------------
    # Assemble Polars DataFrame
    # ------------------------------------------------------------------
    df = pl.DataFrame({
        "ability_motivation":    ability,
        "location":              [PROVINCES[i]         for i in location_idx],
        "parents_education":     [EDUCATION_LEVELS[i]  for i in parents_edu_idx],
        "family_wealth":         family_wealth,
        "test_scores":           test_scores,
        "scholarship":           scholarship.astype(bool),
        "education_institution": [INSTITUTION_LEVELS[i] for i in inst_idx],
        "education_level":       [EDUCATION_LEVELS[i]  for i in edu_idx],
        "profess_network":       profess_network,
        "occupation":            [OCCUPATIONS[i]       for i in occ_idx],
        "income":                income,
        "survey_participation":  survey_participation,
    })

    df = df.with_columns([
        pl.col("location").cast(pl.Enum(PROVINCES)),
        pl.col("parents_education").cast(pl.Enum(EDUCATION_LEVELS)),
        pl.col("education_institution").cast(pl.Enum(INSTITUTION_LEVELS)),
        pl.col("education_level").cast(pl.Enum(EDUCATION_LEVELS)),
        pl.col("occupation").cast(pl.Enum(OCCUPATIONS)),
    ])

    return df


# ---------------------------------------------------------------------------
# Quick smoke-test
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import time

    t0 = time.perf_counter()
    df = simulate_dag(n=5_000, seed=42)
    print(f"Simulated 5,000 rows in {time.perf_counter() - t0:.3f}s\n")

    print(df.head())
    print("\nSchema:")
    print(df.schema)

    print("\nMarginal distributions:")
    for col in [
        "location", "parents_education", "education_institution",
        "education_level", "occupation", "scholarship", "survey_participation",
    ]:
        print(f"\n--- {col} ---")
        vc = df[col].value_counts(sort=True)
        total = len(df)
        print(vc.with_columns((pl.col("count") / total * 100).round(1).alias("%")))

    print("\n--- income (monthly ZAR) by occupation ---")
    print(
        df.group_by("occupation")
        .agg([
            pl.col("income").median().round(0).alias("median"),
            pl.col("income").quantile(0.1).round(0).alias("p10"),
            pl.col("income").quantile(0.9).round(0).alias("p90"),
        ])
        .sort("median")
    )

    print("\n--- family_wealth by parents_education ---")
    print(
        df.group_by("parents_education")
        .agg(pl.col("family_wealth").median().round(0).alias("median_wealth"))
        .sort("median_wealth")
    )

    print("\n--- do(education_level='3-tertiary-undergrad') income vs observational ---")
    df_do = simulate_dag(n=5_000, education_level="3-tertiary-undergrad", seed=42)
    print("Observational median income:   ", round(df["income"].median(), 0))
    print("Interventional median income:  ", round(df_do["income"].median(), 0))
