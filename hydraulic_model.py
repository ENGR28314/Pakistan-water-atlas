"""hydraulic_model.py - simplified hydraulic / risk physics for the Atlas.

These are teaching-grade screening formulas, NOT calibrated engineering models.
"""
from __future__ import annotations

import math

# Simulated "live" weather presets for basin points (illustrative, not a real feed)
WEATHER_STATIONS = {
    "Sialkot (Chenab basin)": {"basin": "Chenab", "base_flow": 2400.0, "temp_c": 31.0, "humidity": 68},
    "Jhelum (Jhelum basin)": {"basin": "Jhelum", "base_flow": 1900.0, "temp_c": 30.0, "humidity": 64},
    "Lahore (Ravi basin)": {"basin": "Ravi", "base_flow": 650.0, "temp_c": 33.0, "humidity": 60},
}

HAZARD_LEVELS = ("Nominal", "Elevated", "Critical Hazard Warning")

# Rational-method peak assumes storm duration >= time of concentration. Real basins
# attenuate this; 0.12 is an illustrative routing factor for a screening model.
ROUTING_ATTENUATION = 0.12


def runoff_flow(base_flow: float, rainfall_mm_hr: float, catchment_km2: float = 5000.0,
                runoff_coeff: float = 0.45) -> float:
    """Rational-method style surge: Q = base + C * i * A / 3.6 (m3/s)."""
    if rainfall_mm_hr < 0:
        raise ValueError("rainfall must be >= 0")
    return base_flow + runoff_coeff * rainfall_mm_hr * catchment_km2 / 3.6 * ROUTING_ATTENUATION


def calculate_basin_stress(inflow_m3s: float, capacity_m3s: float, installed_mw: float,
                           mw_per_m3s: float = 0.35) -> dict:
    """Balance an inflow rate against an operating baseline.

    The operating baseline is the discharge needed to run `installed_mw`
    (installed_mw / mw_per_m3s). Stress index = inflow / capacity, with a
    generation-balance ratio showing how inflow compares with the plant baseline.
    """
    if capacity_m3s <= 0:
        raise ValueError("capacity must be > 0")
    if inflow_m3s < 0 or installed_mw < 0:
        raise ValueError("inflow and MW must be >= 0")
    baseline_flow = installed_mw / mw_per_m3s if mw_per_m3s else 0.0
    stress = inflow_m3s / capacity_m3s
    balance = inflow_m3s / baseline_flow if baseline_flow else math.inf
    if stress >= 1.0:
        status = "Critical Hazard Warning"
    elif stress >= 0.7:
        status = "Elevated"
    else:
        status = "Nominal"
    return {"stress_index": round(stress, 4), "baseline_flow_m3s": round(baseline_flow, 2),
            "generation_balance": round(balance, 4) if math.isfinite(balance) else balance,
            "status": status}


def flash_flood_hazard(base_flow: float, rainfall_mm_hr: float, capacity_m3s: float,
                       catchment_km2: float = 5000.0) -> dict:
    """Connect a 0-100 mm/hr rainfall slider to basin strain and a hazard flag."""
    if not 0 <= rainfall_mm_hr <= 100:
        raise ValueError("rainfall slider range is 0-100 mm/hr")
    q = runoff_flow(base_flow, rainfall_mm_hr, catchment_km2)
    stress = q / capacity_m3s
    if stress >= 1.0 or rainfall_mm_hr >= 70:
        status = "Critical Hazard Warning"
    elif stress >= 0.7 or rainfall_mm_hr >= 35:
        status = "Elevated"
    else:
        status = "Nominal"
    return {"peak_flow_m3s": round(q, 1), "stress_index": round(stress, 4), "status": status}


def water_quality_index(do_mgl: float, ph: float, turbidity_ntu: float, salinity_dsm: float,
                        bod_mgl: float) -> dict:
    """Weighted sub-index WQI (0-100). >=85 Excellent; salinity runoff collapses the score."""
    def clamp(x):
        return max(0.0, min(100.0, x))
    s_do = clamp(do_mgl / 9.0 * 100)
    s_ph = clamp(100 - abs(ph - 7.5) * 25)
    s_turb = clamp(100 - turbidity_ntu * 2)
    s_sal = clamp(100 - salinity_dsm * 25)          # dS/m
    s_bod = clamp(100 - bod_mgl * 10)
    wqi = 0.25 * s_do + 0.15 * s_ph + 0.15 * s_turb + 0.30 * s_sal + 0.15 * s_bod
    if salinity_dsm >= 3.0:
        status = "Ecosystem Collapse Warning"
    elif wqi >= 85:
        status = "Excellent"
    elif wqi >= 70:
        status = "Good"
    elif wqi >= 50:
        status = "Marginal"
    else:
        status = "Poor"
    return {"wqi": round(wqi, 1), "status": status}


def cluster_hazard_flags(flow_m3s: float, rainfall_mm_hr: float, slope_deg: float = 10.0,
                         glacial_melt_index: float = 0.0) -> list[str]:
    """Rule-based hazard clustering. Flash-flood surge > 15,000 m3/s plus intense rain => critical."""
    flags: list[str] = []
    if flow_m3s > 15000 and rainfall_mm_hr >= 50:
        flags.append("CRITICAL: flash-flood surge cluster")
    elif flow_m3s > 15000:
        flags.append("HIGH: riverine flood surge")
    if rainfall_mm_hr >= 80:
        flags.append("HIGH: cloudburst-intensity rainfall")
    if rainfall_mm_hr >= 30 and slope_deg >= 25:
        flags.append("HIGH: landslide / mudflow trigger")
    if glacial_melt_index >= 0.8:
        flags.append("HIGH: GLOF watch")
    return flags


def reservoir_balance(storage_mcm: float, inflow_m3s: float, outflow_m3s: float, hours: float = 24.0,
                      dead_mcm: float = 0.0, max_mcm: float = float("inf")) -> float:
    """Next storage (million m3) after dt hours; clipped to [dead, max]."""
    delta = (inflow_m3s - outflow_m3s) * hours * 3600 / 1e6
    return min(max(storage_mcm + delta, dead_mcm), max_mcm)


def pondage_pressure(live_storage_mcm: float, daily_inflow_m3s: float) -> dict:
    """How many hours of river inflow fit in the pond (indicator used in the IWT pondage dispute)."""
    if daily_inflow_m3s <= 0:
        raise ValueError("inflow must be > 0")
    hours = live_storage_mcm * 1e6 / daily_inflow_m3s / 3600
    return {"hours_of_inflow": round(hours, 2)}
