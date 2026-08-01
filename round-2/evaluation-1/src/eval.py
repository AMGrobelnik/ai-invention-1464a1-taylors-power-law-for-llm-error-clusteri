#!/usr/bin/env python3
"""Validate whether Taylor exponent b predicts voting gain across model/benchmark/difficulty combos."""

from __future__ import annotations

import gc
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from loguru import logger
from scipy import stats
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add("logs/run.log", rotation="30 MB", level="DEBUG")

WORKDIR = Path(__file__).resolve().parent
EXPERIMENT_DIR = WORKDIR.parent / "gen_art_experiment_1"
RNG_SEED = 20260801
N_BOOTSTRAP = 10_000
K_PRIMARY = 5
K_SECONDARY = (3, 10)


def majority_vote_gain(correctness_samples: list[int], m_p: float, k: int) -> float:
    """Real per-problem voting gain at k: majority-vote accuracy over the first
    min(k, n_samples) repeated draws, minus single-draw accuracy m_p. When fewer
    than k raw samples exist (as here, samples_per_problem=5 < k=10), the largest
    available draw set is reused (matching the EXPERIMENT artifact's own
    convention of reusing the k=5 figure for k=10 in this budget-scaled run)."""
    n_use = min(k, len(correctness_samples))
    if n_use == 0:
        return float("nan")
    votes = correctness_samples[:n_use]
    majority = 1.0 if sum(votes) > n_use / 2 else 0.0
    return majority - m_p


def load_experiment_data(path: Path) -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    """Load the real EXPERIMENT artifact output (method_out.json).

    Returns (problem_df, combo_df, noise_floor) where:
    - problem_df: one row per real (model, benchmark, problem) triple, with the
      per-problem overdispersion ratio od_p = v_p_empirical / (m_p*(1-m_p)) used
      as the finest-grained real analog of the Taylor exponent b (true per-problem
      b is not defined -- b is only fit at the (model, benchmark) level from the
      set of problems' (m_p, v_p) pairs), and real per-problem voting gains
      recomputed from the raw correctness_samples.
    - combo_df: one row per real (model, benchmark) combo with the literal fitted
      b from the EXPERIMENT artifact and its aggregate voting gains -- this is the
      exact granularity the artifact plan's metric 1 describes.
    - noise_floor: the real b_null_p_value per (model, benchmark) combo from the
      EXPERIMENT artifact's own null-simulation gate.
    """
    payload = json.loads(path.read_text())
    meta = payload["metadata"]
    taylor = meta.get("taylor_exponents", {})
    voting = meta.get("voting_gains", {})
    noise_floor = meta.get("noise_floor_validation", {})

    problem_rows = []
    for ds in payload.get("datasets", []):
        combo_name = ds["dataset"]
        model, benchmark = combo_name.split("__", 1)
        for ex in ds["examples"]:
            m_p = ex.get("metadata_m_p")
            v_p = ex.get("metadata_v_p_empirical")
            samples = ex.get("metadata_correctness_samples") or []
            if m_p is None or v_p is None:
                continue
            denom = m_p * (1.0 - m_p)
            od_p = (v_p / denom) if denom > 0 else float("nan")
            row = {
                "benchmark": benchmark,
                "model": model,
                "combo": combo_name,
                "problem_id": ex.get("metadata_problem_id"),
                "m_p": float(m_p),
                "od_p": float(od_p),
            }
            for k in (K_PRIMARY, *K_SECONDARY):
                row[f"delta_{k}"] = majority_vote_gain(samples, float(m_p), k)
            problem_rows.append(row)
    problem_df = pd.DataFrame(problem_rows)

    combo_rows = []
    for combo_name, texp in taylor.items():
        model, benchmark = combo_name.split("__", 1)
        vg = voting.get(combo_name, {})
        combo_rows.append(
            {
                "combo": combo_name,
                "model": model,
                "benchmark": benchmark,
                "b": texp.get("exponent_b"),
                "r_squared": texp.get("r_squared"),
                "n_problems_fit": texp.get("n_problems"),
                "delta_3": vg.get("k_3_gain"),
                "delta_5": vg.get("k_5_gain"),
                "delta_10": vg.get("k_10_gain"),
            }
        )
    combo_df = pd.DataFrame(combo_rows)
    return problem_df, combo_df, noise_floor


def spearman_with_bootstrap_ci(
    x: np.ndarray, y: np.ndarray, rng: np.random.Generator, n_boot: int = N_BOOTSTRAP
) -> dict:
    rho, p = stats.spearmanr(x, y)
    n = len(x)
    if n < 3:
        return {"rho": float(rho), "p_value": float(p), "ci_low": None, "ci_high": None, "n": n}
    idx = rng.integers(0, n, size=(n_boot, n))
    boot_rhos = np.empty(n_boot)
    for i in range(n_boot):
        bx, by = x[idx[i]], y[idx[i]]
        if np.std(bx) == 0 or np.std(by) == 0:
            boot_rhos[i] = np.nan
        else:
            boot_rhos[i] = stats.spearmanr(bx, by)[0]
    boot_rhos = boot_rhos[~np.isnan(boot_rhos)]
    ci_low, ci_high = np.percentile(boot_rhos, [2.5, 97.5]) if len(boot_rhos) else (np.nan, np.nan)
    return {
        "rho": float(rho),
        "p_value": float(p),
        "ci_low": float(ci_low),
        "ci_high": float(ci_high),
        "n": int(n),
    }


def holm_bonferroni(p_values: list[float]) -> list[float]:
    """Return Holm-Bonferroni adjusted p-values, order matching input."""
    p_arr = np.asarray(p_values)
    order = np.argsort(p_arr)
    m = len(p_arr)
    adjusted = np.empty(m)
    running_max = 0.0
    for rank, idx in enumerate(order):
        adj = (m - rank) * p_arr[idx]
        running_max = max(running_max, adj)
        adjusted[idx] = min(running_max, 1.0)
    return adjusted.tolist()


def fisher_z(rho: float) -> float:
    rho_c = np.clip(rho, -0.999999, 0.999999)
    return 0.5 * np.log((1 + rho_c) / (1 - rho_c))


def fisher_z_inv(z: float) -> float:
    return (np.exp(2 * z) - 1) / (np.exp(2 * z) + 1)


def dersimonian_laird(rhos: list[float], ns: list[int]) -> dict:
    """DerSimonian-Laird random-effects meta-analysis on Fisher-z transformed correlations."""
    zs = np.array([fisher_z(r) for r in rhos])
    variances = np.array([1.0 / (n - 3) if n > 3 else np.nan for n in ns])
    valid = ~np.isnan(variances) & ~np.isnan(zs)
    zs, variances = zs[valid], variances[valid]
    if len(zs) == 0:
        return {
            "pooled_rho": None,
            "ci_low": None,
            "ci_high": None,
            "tau2": None,
            "i2": None,
            "q_statistic": None,
            "k_studies": 0,
        }
    weights_fixed = 1.0 / variances
    z_fixed = np.sum(weights_fixed * zs) / np.sum(weights_fixed)
    q = float(np.sum(weights_fixed * (zs - z_fixed) ** 2))
    df = len(zs) - 1
    c = np.sum(weights_fixed) - np.sum(weights_fixed**2) / np.sum(weights_fixed)
    tau2 = max(0.0, (q - df) / c) if df > 0 and c > 0 else 0.0
    weights_re = 1.0 / (variances + tau2)
    z_pooled = np.sum(weights_re * zs) / np.sum(weights_re)
    se_pooled = np.sqrt(1.0 / np.sum(weights_re))
    ci_low_z, ci_high_z = z_pooled - 1.96 * se_pooled, z_pooled + 1.96 * se_pooled
    i2 = max(0.0, (q - df) / q * 100) if q > 0 and df >= 0 else 0.0
    return {
        "pooled_rho": float(fisher_z_inv(z_pooled)),
        "ci_low": float(fisher_z_inv(ci_low_z)),
        "ci_high": float(fisher_z_inv(ci_high_z)),
        "tau2": float(tau2),
        "i2": float(i2),
        "q_statistic": float(q),
        "k_studies": int(len(zs)),
    }


def cohens_d(top_q: np.ndarray, bottom_q: np.ndarray) -> float:
    n1, n2 = len(top_q), len(bottom_q)
    if n1 < 2 or n2 < 2:
        return float("nan")
    pooled_std = np.sqrt(
        ((n1 - 1) * np.var(top_q, ddof=1) + (n2 - 1) * np.var(bottom_q, ddof=1)) / (n1 + n2 - 2)
    )
    if pooled_std == 0:
        return float("nan")
    return float((np.mean(top_q) - np.mean(bottom_q)) / pooled_std)


def stratify(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    def _bucket(s: pd.Series) -> pd.Series:
        try:
            return pd.qcut(s, q=3, labels=["low", "medium", "high"], duplicates="drop")
        except ValueError:
            return pd.Series(["medium"] * len(s), index=s.index)

    df["stratum"] = df.groupby("benchmark")["m_p"].transform(_bucket)
    return df


@logger.catch(reraise=True)
def main() -> None:
    rng = np.random.default_rng(RNG_SEED)
    exp_path = EXPERIMENT_DIR / "method_out.json"
    if not exp_path.exists() or exp_path.stat().st_size == 0:
        raise FileNotFoundError(
            f"EXPERIMENT artifact output not found at {exp_path}; this evaluation "
            "requires gen_art_experiment_1's method_out.json to exist."
        )
    logger.info(f"Loading real experiment predictions from {exp_path}")
    problem_df, combo_df, noise_floor_raw = load_experiment_data(exp_path)
    problem_df = stratify(problem_df)
    benchmarks = sorted(problem_df["benchmark"].unique().tolist())
    logger.info(
        f"Real data: {len(problem_df)} problems across benchmarks {benchmarks}, "
        f"{len(combo_df)} (model, benchmark) combos"
    )

    metrics_agg: dict[str, float] = {}
    datasets_out = []
    primary = problem_df.dropna(subset=["od_p", "delta_5"]).copy()
    logger.info(f"Per-problem rows usable for od_p analysis (k={K_PRIMARY}): {len(primary)}")

    # --- 1a. LITERAL plan-specified test: real fitted b vs aggregate voting gain,
    # at the only granularity where b is actually defined -- (model, benchmark) combos.
    combo_valid = combo_df.dropna(subset=["b", "delta_5"])
    combo_level_result = None
    if len(combo_valid) >= 3:
        combo_level_result = spearman_with_bootstrap_ci(
            combo_valid["b"].to_numpy(), combo_valid["delta_5"].to_numpy(), rng
        )
        metrics_agg["combo_level_spearman_rho_k5"] = combo_level_result["rho"]
        metrics_agg["combo_level_spearman_p_k5"] = combo_level_result["p_value"]
        metrics_agg["combo_level_n_combos"] = float(len(combo_valid))
        logger.info(
            f"[combo-level, literal b, n={len(combo_valid)}/{len(combo_df)}] "
            f"rho={combo_level_result['rho']:.3f} p={combo_level_result['p_value']:.3f} "
            "-- NOTE: severely underpowered (n<10); interpret only as directional signal"
        )
    else:
        logger.warning(
            f"Only {len(combo_valid)} (model,benchmark) combos have a non-null fitted b "
            "-- too few for any combo-level correlation test."
        )

    # --- 1b. Per-problem analysis using od_p = v_p/(m_p(1-m_p)), the real per-problem
    # overdispersion ratio (Taylor's law implies od_p relates monotonically to local b),
    # used because true per-problem b is not defined in the EXPERIMENT's output. This
    # is the analysis granularity that makes stratified/holdout/transfer/meta-analysis
    # metrics meaningful with the available real sample size.
    within_benchmark = {}
    for bench in benchmarks:
        sub = primary[primary["benchmark"] == bench]
        if len(sub) < 3:
            continue
        res = spearman_with_bootstrap_ci(sub["od_p"].to_numpy(), sub["delta_5"].to_numpy(), rng)
        within_benchmark[bench] = res
        metrics_agg[f"within_benchmark_spearman_rho_k{K_PRIMARY}_{bench}"] = res["rho"]
        metrics_agg[f"within_benchmark_spearman_p_k{K_PRIMARY}_{bench}"] = res["p_value"]
        logger.info(f"[within-benchmark, od_p proxy, k={K_PRIMARY}] {bench}: rho={res['rho']:.3f} p={res['p_value']:.3f} n={res['n']}")

    secondary_k_correlations = {}
    for k_sec in K_SECONDARY:
        sub_k = problem_df.dropna(subset=["od_p", f"delta_{k_sec}"])
        for bench in benchmarks:
            sb = sub_k[sub_k["benchmark"] == bench]
            if len(sb) < 3:
                continue
            res = spearman_with_bootstrap_ci(sb["od_p"].to_numpy(), sb[f"delta_{k_sec}"].to_numpy(), rng)
            secondary_k_correlations[f"{bench}_k{k_sec}"] = res
            metrics_agg[f"within_benchmark_spearman_rho_k{k_sec}_{bench}"] = res["rho"]

    # --- 2 & 3. Calibration / held-out transfer split (60/40 stratified by model, benchmark, stratum) ---
    strat_key = primary["model"].astype(str) + "|" + primary["benchmark"] + "|" + primary["stratum"].astype(str)
    primary = primary.assign(_strat_key=strat_key)
    train_idx, test_idx = [], []
    for _, group in primary.groupby("_strat_key"):
        shuffled = group.sample(frac=1.0, random_state=RNG_SEED)
        n_train = max(1, int(round(0.6 * len(shuffled))))
        train_idx.extend(shuffled.index[:n_train].tolist())
        test_idx.extend(shuffled.index[n_train:].tolist())
    train_df = primary.loc[train_idx]
    test_df = primary.loc[test_idx]
    logger.info(f"Calibration split: train={len(train_df)} test={len(test_df)}")

    calib_rho = calib_r2 = calib_rmse = attenuation = float("nan")
    test_res = {"rho": float("nan"), "p_value": float("nan"), "n": 0}
    if len(train_df) >= 3 and len(test_df) >= 3:
        reg = LinearRegression()
        reg.fit(train_df[["od_p"]].to_numpy(), train_df["delta_5"].to_numpy())
        train_pred = reg.predict(train_df[["od_p"]].to_numpy())
        calib_rho, _ = stats.spearmanr(train_pred, train_df["delta_5"])
        calib_r2 = r2_score(train_df["delta_5"], train_pred)
        calib_rmse = float(np.sqrt(mean_squared_error(train_df["delta_5"], train_pred)))
        logger.info(f"Calibration: rho={calib_rho:.3f} R2={calib_r2:.3f} RMSE={calib_rmse:.4f}")

        test_pred = reg.predict(test_df[["od_p"]].to_numpy())
        test_res = spearman_with_bootstrap_ci(test_pred, test_df["delta_5"].to_numpy(), rng)
        attenuation = test_res["rho"] / calib_rho if calib_rho not in (0, None) and not np.isnan(calib_rho) else float("nan")
        logger.info(f"Held-out transfer: rho={test_res['rho']:.3f} attenuation={attenuation:.3f}")
    else:
        logger.warning("Calibration/holdout split has too few rows per side; skipping regression metrics.")
    metrics_agg["calibration_spearman_rho"] = float(calib_rho)
    metrics_agg["calibration_r2"] = float(calib_r2)
    metrics_agg["calibration_rmse"] = float(calib_rmse)
    metrics_agg["holdout_transfer_spearman_rho"] = float(test_res["rho"])
    metrics_agg["holdout_transfer_spearman_p"] = float(test_res["p_value"])
    metrics_agg["holdout_transfer_attenuation_factor"] = float(attenuation)

    # --- 4. Cross-benchmark transfer: train on GSM8K-family combo, test on the others ---
    gsm8k_key = next((b for b in benchmarks if "gsm8k" in b.lower()), None)
    cross_bench_results = {}
    if gsm8k_key is not None:
        gsm8k_df = primary[primary["benchmark"] == gsm8k_key]
        if len(gsm8k_df) >= 5:
            cross_reg = LinearRegression()
            cross_reg.fit(gsm8k_df[["od_p"]].to_numpy(), gsm8k_df["delta_5"].to_numpy())
            for bench in [b for b in benchmarks if b != gsm8k_key]:
                held = primary[primary["benchmark"] == bench]
                if len(held) < 3:
                    continue
                preds = cross_reg.predict(held[["od_p"]].to_numpy())
                res = spearman_with_bootstrap_ci(preds, held["delta_5"].to_numpy(), rng)
                cross_bench_results[bench] = res
                metrics_agg[f"cross_benchmark_transfer_rho_{bench}"] = res["rho"]
                metrics_agg[f"cross_benchmark_transfer_p_{bench}"] = res["p_value"]
                logger.info(f"Cross-benchmark {gsm8k_key}->{bench}: rho={res['rho']:.3f}")
        else:
            logger.warning(f"Too few rows ({len(gsm8k_df)}) in {gsm8k_key} to fit a cross-benchmark transfer model.")

    # --- 5. Stratified sub-group correlations with Holm-Bonferroni correction ---
    stratified_results = {}
    for bench in benchmarks:
        strata_p, strata_names, strata_rho, strata_n = [], [], [], []
        for stratum in ("low", "medium", "high"):
            sub = primary[(primary["benchmark"] == bench) & (primary["stratum"] == stratum)]
            if len(sub) < 3:
                continue
            res = spearman_with_bootstrap_ci(sub["od_p"].to_numpy(), sub["delta_5"].to_numpy(), rng)
            strata_p.append(res["p_value"])
            strata_names.append(stratum)
            strata_rho.append(res["rho"])
            strata_n.append(res["n"])
        if not strata_p:
            continue
        adj_p = holm_bonferroni(strata_p)
        for name, rho, p_raw, p_adj, n in zip(strata_names, strata_rho, strata_p, adj_p, strata_n):
            stratified_results[f"{bench}_{name}"] = {
                "rho": rho,
                "p_value_raw": p_raw,
                "p_value_holm_bonferroni": p_adj,
                "n": n,
                "significant_fwer_0.05": bool(p_adj < 0.05),
            }
            metrics_agg[f"stratified_rho_{bench}_{name}"] = rho
            metrics_agg[f"stratified_p_holm_{bench}_{name}"] = p_adj
    logger.info(f"Holm-Bonferroni testing plan: {len(stratified_results)} stratum tests, FWER target <= 0.05")

    # --- 6. Noise-floor validation (real b_null_p per combo from EXPERIMENT artifact) ---
    combo_p_values = [
        v["p_value_reject_null"] for v in noise_floor_raw.values() if v.get("p_value_reject_null") is not None
    ]
    n_rejected = sum(1 for p in combo_p_values if p < 0.05)
    min_p = float(min(combo_p_values)) if combo_p_values else float("nan")
    noise_floor_pass = n_rejected > 0
    metrics_agg["noise_floor_n_combos_tested"] = float(len(combo_p_values))
    metrics_agg["noise_floor_n_combos_rejected_at_p05"] = float(n_rejected)
    metrics_agg["noise_floor_min_p_value"] = min_p
    metrics_agg["noise_floor_any_rejected"] = float(noise_floor_pass)
    logger.info(
        f"Noise floor (real, per-combo b_null gate): {n_rejected}/{len(combo_p_values)} combos reject the "
        f"i.i.d.-Bernoulli null at p<0.05 (min p={min_p:.3f}). Per the plan's own logic, if none reject, "
        "the exponent-based diagnostic is not established as distinguishable from sampling noise."
    )

    # --- 7. Pooled meta-analytic correlation (DerSimonian-Laird over benchmark x stratum x k) ---
    pooled_rhos, pooled_ns = [], []
    for res in within_benchmark.values():
        pooled_rhos.append(res["rho"])
        pooled_ns.append(res["n"])
    for res in stratified_results.values():
        pooled_rhos.append(res["rho"])
        pooled_ns.append(res["n"])
    for res in secondary_k_correlations.values():
        pooled_rhos.append(res["rho"])
        pooled_ns.append(res["n"])
    meta = dersimonian_laird(pooled_rhos, pooled_ns)
    metrics_agg["meta_pooled_rho"] = meta["pooled_rho"] if meta["pooled_rho"] is not None else float("nan")
    metrics_agg["meta_pooled_ci_low"] = meta["ci_low"] if meta["ci_low"] is not None else float("nan")
    metrics_agg["meta_pooled_ci_high"] = meta["ci_high"] if meta["ci_high"] is not None else float("nan")
    metrics_agg["meta_tau2"] = meta["tau2"] if meta["tau2"] is not None else float("nan")
    metrics_agg["meta_i2"] = meta["i2"] if meta["i2"] is not None else float("nan")
    metrics_agg["meta_q_statistic"] = meta["q_statistic"] if meta["q_statistic"] is not None else float("nan")
    metrics_agg["meta_k_studies"] = float(meta["k_studies"])
    logger.info(f"Meta-analytic pooled rho={meta['pooled_rho']} tau2={meta['tau2']} I2={meta['i2']}")

    # --- 8. Effect size summary (Cohen's d, top vs bottom quartile of od_p) ---
    effect_sizes = {}
    for bench in benchmarks:
        sub = primary[primary["benchmark"] == bench]
        if len(sub) < 8:
            continue
        q_low, q_high = sub["od_p"].quantile([0.25, 0.75])
        top_q = sub[sub["od_p"] >= q_high]["delta_5"].to_numpy()
        bottom_q = sub[sub["od_p"] <= q_low]["delta_5"].to_numpy()
        d = cohens_d(bottom_q, top_q)
        effect_sizes[bench] = {"cohens_d_low_minus_high_od_p": d, "n_top_quartile": len(top_q), "n_bottom_quartile": len(bottom_q)}
        metrics_agg[f"cohens_d_{bench}"] = float(d)
    logger.info(f"Effect sizes (Cohen's d, low-od_p minus high-od_p quartile): {effect_sizes}")

    # --- 9. Visualization ---
    figures_dir = WORKDIR / "figures"
    figures_dir.mkdir(exist_ok=True)
    make_visualizations(primary, benchmarks, figures_dir)

    # --- Assemble output following exp_eval_sol_out schema ---
    metrics_agg["n_total_problems"] = float(len(primary))
    metrics_agg["n_combos_with_fitted_b"] = float(len(combo_valid))
    metrics_agg["n_combos_total"] = float(len(combo_df))

    for bench in benchmarks:
        sub = primary[primary["benchmark"] == bench]
        examples = []
        for _, row in sub.iterrows():
            examples.append(
                {
                    "input": f"model={row['model']} problem={row['problem_id']}",
                    "output": f"delta_{K_PRIMARY}={row['delta_5']:.4f}",
                    "metadata_model": row["model"],
                    "metadata_stratum": str(row["stratum"]),
                    "metadata_m_p": float(row["m_p"]),
                    "predict_od_p_local_b_proxy": f"{row['od_p']:.4f}",
                    "eval_delta_k_actual": float(row["delta_5"]),
                }
            )
        if examples:
            datasets_out.append({"dataset": bench, "examples": examples})

    output = {
        "metadata": {
            "evaluation_name": "taylor_exponent_predicts_vote_gain",
            "description": (
                "Validates whether Taylor power-law exponent b reliably predicts voting "
                "gains across held-out model/benchmark/difficulty combinations, using the "
                "real EXPERIMENT artifact output (gen_art_experiment_1/method_out.json)."
            ),
            "data_granularity_note": (
                "The EXPERIMENT artifact fits b only at the (model, benchmark) level "
                "(9 combos, 3 with a null fit due to degenerate m_p in the small budget-"
                "scaled sample). combo_level_spearman_* uses that literal b. All other "
                "correlation/stratification/transfer/meta-analysis metrics use od_p = "
                "v_p_empirical/(m_p*(1-m_p)), the real per-problem overdispersion ratio, "
                "as the finest-grained per-problem analog of b, since true per-problem b "
                "does not exist in the artifact's output."
            ),
            "primary_k": K_PRIMARY,
            "secondary_k": list(K_SECONDARY),
            "combo_level_literal_b_result": combo_level_result,
            "within_benchmark_spearman_od_p": within_benchmark,
            "secondary_k_correlations": secondary_k_correlations,
            "stratified_results_holm_bonferroni": stratified_results,
            "cross_benchmark_transfer": cross_bench_results,
            "meta_analysis": meta,
            "effect_sizes": effect_sizes,
            "noise_floor": {
                "per_combo_p_values": combo_p_values,
                "n_combos_tested": len(combo_p_values),
                "n_combos_rejected_at_0.05": n_rejected,
                "min_p_value": min_p,
                "any_rejected": noise_floor_pass,
            },
        },
        "metrics_agg": metrics_agg,
        "datasets": datasets_out,
    }

    def _sanitize(obj):
        if isinstance(obj, float):
            return obj if np.isfinite(obj) else None
        if isinstance(obj, dict):
            return {k: _sanitize(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [_sanitize(v) for v in obj]
        return obj

    output = _sanitize(output)
    # exp_eval_sol_out schema requires every metrics_agg value to be a finite number;
    # metrics that came out NaN (insufficient real data for that specific test) are
    # dropped from metrics_agg but remain visible, with None, in the metadata detail blocks.
    output["metrics_agg"] = {k: v for k, v in output["metrics_agg"].items() if v is not None}

    out_path = WORKDIR / "eval_out.json"
    out_path.write_text(json.dumps(output, indent=2, allow_nan=False, default=str))
    logger.info(f"Wrote {out_path} ({out_path.stat().st_size / 1024:.1f} KB)")

    del problem_df, combo_df, primary, train_df, test_df
    gc.collect()


def make_visualizations(primary: pd.DataFrame, benchmarks: list[str], figures_dir: Path) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    strata = ["low", "medium", "high"]
    colors = {"low": "#4c72b0", "medium": "#dd8452", "high": "#55a868"}
    fig, axes = plt.subplots(1, len(benchmarks), figsize=(6 * len(benchmarks), 5), sharey=True)
    axes = np.atleast_1d(axes)
    for ax, bench in zip(axes, benchmarks):
        sub_bench = primary[primary["benchmark"] == bench]
        for stratum in strata:
            sub = sub_bench[sub_bench["stratum"] == stratum]
            if sub.empty:
                continue
            ax.scatter(sub["od_p"], sub["delta_5"], s=14, alpha=0.6, color=colors[stratum], label=f"{stratum} (n={len(sub)})")
        if len(sub_bench) >= 3 and np.ptp(sub_bench["od_p"].to_numpy()) > 1e-6:
            coeffs = np.polyfit(sub_bench["od_p"], sub_bench["delta_5"], 1)
            xs = np.linspace(sub_bench["od_p"].min(), sub_bench["od_p"].max(), 100)
            ys = np.polyval(coeffs, xs)
            resid_std = np.std(sub_bench["delta_5"] - np.polyval(coeffs, sub_bench["od_p"]))
            ax.plot(xs, ys, color="black", linewidth=1.5)
            ax.fill_between(xs, ys - 1.96 * resid_std, ys + 1.96 * resid_std, color="gray", alpha=0.2)
        ax.set_title(f"{bench} (n={len(sub_bench)})")
        ax.set_xlabel("Per-problem overdispersion od_p (local b proxy)")
        ax.legend(fontsize=7)
    axes[0].set_ylabel(f"Voting gain Delta_{K_PRIMARY}")
    fig.suptitle("Per-problem overdispersion (local Taylor-exponent proxy) vs. voting gain")
    fig.tight_layout()
    fig.savefig(figures_dir / "b_vs_delta_scatter.png", dpi=150)
    plt.close(fig)

    def _safe_hist(ax, values: pd.Series, color: str, title: str) -> None:
        vals = values.dropna().to_numpy()
        n_bins = min(20, max(3, len(vals) // 3)) if len(vals) else 1
        if len(vals) == 0 or np.ptp(vals) < 1e-9 * max(1.0, abs(np.mean(vals))):
            ax.bar([0], [len(vals)], color=color, alpha=0.8)
        else:
            ax.hist(vals, bins=n_bins, color=color, alpha=0.8)
        ax.set_title(title)

    fig2, (ax_b, ax_d) = plt.subplots(1, 2, figsize=(10, 4))
    _safe_hist(ax_b, primary["od_p"], "#4c72b0", "Distribution of od_p (local b proxy)")
    _safe_hist(ax_d, primary["delta_5"], "#dd8452", f"Distribution of Delta_{K_PRIMARY}")
    fig2.tight_layout()
    fig2.savefig(figures_dir / "marginal_histograms.png", dpi=150)
    plt.close(fig2)


if __name__ == "__main__":
    main()
