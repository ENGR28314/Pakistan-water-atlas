"""input_driven.py - editable socio/agro data and chart builder shared by the
Agro-Economic and Socio-Economic domains.

DEFAULT VALUES ARE ILLUSTRATIVE PLACEHOLDERS (order-of-magnitude), not official statistics.
Edit them in the app or load your own CSV (PBS, Agriculture Census, provincial departments).
"""
from __future__ import annotations

import pandas as pd

METRICS = {
    "Cultivated area (ha)": "cultivated_area_ha",
    "Crop production (tonnes)": "crop_production_t",
    "Employment (persons)": "employment_persons",
    "Honey production (tonnes)": "honey_production_t",
    "Aquaculture production (tonnes)": "aquaculture_production_t",
}
GRAPH_TYPES = ["Bar chart", "Pie chart", "Scatter plot", "Line chart"]

COLUMNS = ["province_region", "cultivated_area_ha", "crop_production_t", "employment_persons",
           "honey_production_t", "aquaculture_production_t"]


def default_data() -> pd.DataFrame:
    return pd.DataFrame([
        ["Punjab", 13_000_000, 90_000_000, 12_000_000, 6_000, 120_000],
        ["Sindh", 3_200_000, 40_000_000, 4_500_000, 900, 90_000],
        ["Khyber Pakhtunkhwa", 1_800_000, 12_000_000, 2_800_000, 2_500, 12_000],
        ["Balochistan", 2_300_000, 7_000_000, 1_400_000, 600, 6_000],
        ["Gilgit-Baltistan", 120_000, 800_000, 150_000, 150, 800],
        ["Azad Jammu & Kashmir", 250_000, 900_000, 220_000, 400, 1_500],
        ["Islamabad Capital Territory", 25_000, 90_000, 30_000, 20, 100],
    ], columns=COLUMNS)


def validate(df: pd.DataFrame) -> pd.DataFrame:
    missing = [c for c in COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"missing columns: {missing}")
    out = df[COLUMNS].copy()
    for c in COLUMNS[1:]:
        out[c] = pd.to_numeric(out[c], errors="coerce").fillna(0).clip(lower=0)
    return out


def build_chart(df: pd.DataFrame, metric_label: str, graph_type: str):
    """Return a Plotly figure for the chosen metric / graph type."""
    import plotly.express as px  # lazy so non-UI tests need no plotly
    if metric_label not in METRICS:
        raise ValueError(f"unknown metric {metric_label}")
    if graph_type not in GRAPH_TYPES:
        raise ValueError(f"unknown graph type {graph_type}")
    col = METRICS[metric_label]
    x = "province_region"
    title = f"{metric_label} by province / region"
    if graph_type == "Bar chart":
        return px.bar(df, x=x, y=col, color=x, title=title, labels={col: metric_label})
    if graph_type == "Pie chart":
        return px.pie(df, names=x, values=col, title=title)
    if graph_type == "Scatter plot":
        other = "cultivated_area_ha" if col != "cultivated_area_ha" else "crop_production_t"
        return px.scatter(df, x=other, y=col, color=x, text=x, title=f"{metric_label} vs {other}")
    return px.line(df, x=x, y=col, markers=True, title=title, labels={col: metric_label})


def summary(df: pd.DataFrame, metric_label: str) -> dict:
    col = METRICS[metric_label]
    total = float(df[col].sum())
    top = df.loc[df[col].idxmax(), "province_region"] if len(df) else None
    return {"total": total, "top": top, "share_top_pct": round(100 * df[col].max() / total, 1) if total else 0.0}
