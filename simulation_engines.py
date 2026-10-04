"""simulation_engines.py - Monte-Carlo, scenario, reservoir and dispute engines.

Pure numpy/pandas. All engines are deterministic given a seed so results are testable.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

import hydraulic_model as H


class FloodMonteCarlo:
    """Monte-Carlo exceedance of a flow threshold given lognormal annual-peak flow."""

    def __init__(self, median_peak_m3s: float, sigma: float = 0.5, seed: int = 7):
        self.median, self.sigma, self.seed = median_peak_m3s, sigma, seed

    def run(self, n: int = 5000, threshold_m3s: float = 15000.0) -> dict:
        rng = np.random.default_rng(self.seed)
        peaks = rng.lognormal(mean=np.log(self.median), sigma=self.sigma, size=n)
        return {"n": n, "p_exceed": float((peaks > threshold_m3s).mean()),
                "p95_m3s": float(np.percentile(peaks, 95)), "mean_m3s": float(peaks.mean()), "peaks": peaks}


class ReservoirSimulator:
    """Daily mass-balance routing for a reservoir (Tarbela/Mangla style)."""

    def __init__(self, live_capacity_mcm: float, dead_mcm: float = 0.0, start_mcm: float | None = None):
        self.cap, self.dead = live_capacity_mcm + dead_mcm, dead_mcm
        self.start = start_mcm if start_mcm is not None else self.dead + live_capacity_mcm * 0.5

    def run(self, inflow_m3s, release_m3s) -> pd.DataFrame:
        s = self.start
        rows = []
        for d, (qi, qo) in enumerate(zip(inflow_m3s, release_m3s)):
            s = H.reservoir_balance(s, qi, qo, 24.0, self.dead, self.cap)
            rows.append({"day": d + 1, "storage_mcm": s, "inflow": qi, "release": qo,
                         "spill": max(0.0, (s - self.cap)) if s > self.cap else 0.0})
        return pd.DataFrame(rows)


class ClimateScenarioEngine:
    """Baseline / Medium / Worst-case multipliers applied to hazard drivers."""

    FACTORS = {
        "Baseline": {"rain": 1.00, "melt": 1.00, "sea_level_cm": 0},
        "Medium": {"rain": 1.25, "melt": 1.35, "sea_level_cm": 20},
        "Worst-case": {"rain": 1.60, "melt": 1.80, "sea_level_cm": 50},
    }

    def project(self, base_peak_m3s: float, base_rain_mm_hr: float) -> pd.DataFrame:
        rows = []
        for name, f in self.FACTORS.items():
            peak = base_peak_m3s * (0.6 * f["rain"] + 0.4 * f["melt"])
            rain = min(100.0, base_rain_mm_hr * f["rain"])
            flags = H.cluster_hazard_flags(peak, rain, glacial_melt_index=min(1.0, 0.4 * f["melt"]))
            rows.append({"scenario": name, "peak_flow_m3s": round(peak), "rain_mm_hr": round(rain, 1),
                         "sea_level_rise_cm": f["sea_level_cm"], "flags": "; ".join(flags) or "none"})
        return pd.DataFrame(rows)


class WaterShareEngine:
    """Illustrative inter-provincial apportionment (Punjab vs Sindh) under shortage.

    Pro-rata sharing of a shortage is a *teaching device*, not the 1991 Water Apportionment Accord.
    """

    def share(self, available_maf: float, claims_maf: dict[str, float]) -> pd.DataFrame:
        total = sum(claims_maf.values())
        if total <= 0:
            raise ValueError("claims must be positive")
        ratio = min(1.0, available_maf / total)
        return pd.DataFrame([{"province": p, "claim_maf": c, "allocated_maf": round(c * ratio, 3),
                              "shortage_pct": round((1 - ratio) * 100, 1)} for p, c in claims_maf.items()])


class TreatyDisputeEngine:
    """Quantifies pondage / freeboard / intake gaps between India's design and Pakistan's position."""

    def pondage_gap(self, india_mcm: float, pakistan_mcm: float, daily_inflow_m3s: float) -> dict:
        a = H.pondage_pressure(india_mcm, daily_inflow_m3s)["hours_of_inflow"]
        b = H.pondage_pressure(pakistan_mcm, daily_inflow_m3s)["hours_of_inflow"]
        return {"india_hours": a, "pakistan_hours": b, "excess_mcm": round(india_mcm - pakistan_mcm, 2),
                "ratio": round(india_mcm / pakistan_mcm, 2)}

    def downstream_surge(self, pond_mcm: float, release_minutes: float) -> float:
        """Average surge (m3/s) if a full pond is emptied in `release_minutes`."""
        if release_minutes <= 0:
            raise ValueError("minutes must be > 0")
        return pond_mcm * 1e6 / (release_minutes * 60)


class HydropowerEconomics:
    """Simple LCOE / annual-energy engine for the China-financed hydropower portfolio."""

    def annual_gwh(self, mw: float, capacity_factor: float) -> float:
        return mw * capacity_factor * 8760 / 1000

    def lcoe_usd_mwh(self, capex_usd_m: float, mw: float, capacity_factor: float,
                     discount: float = 0.08, years: int = 30, om_pct: float = 0.02) -> float:
        crf = discount * (1 + discount) ** years / ((1 + discount) ** years - 1)
        annual_cost = capex_usd_m * 1e6 * (crf + om_pct)
        mwh = mw * capacity_factor * 8760
        return annual_cost / mwh


def sdg_score(indicators: dict[str, float], targets: dict[str, float]) -> pd.DataFrame:
    """Percent-of-target progress per indicator (capped at 100)."""
    rows = []
    for k, t in targets.items():
        v = indicators.get(k, 0.0)
        rows.append({"indicator": k, "value": v, "target": t, "progress_pct": round(min(100.0, 100 * v / t), 1) if t else 0.0})
    return pd.DataFrame(rows)
