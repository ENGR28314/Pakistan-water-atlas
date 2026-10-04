"""data_loader.py - dataset loaders and the 12-month telemetry generator."""
from __future__ import annotations

import calendar
from datetime import date

import numpy as np
import pandas as pd

import coordinates as C

# ---------------------------------------------------------------- telemetry
# Monthly seasonal shape (0-1): low Dec-Jan, peak Jun-Aug (monsoon + snowmelt)
_SEASON = np.array([0.08, 0.10, 0.18, 0.30, 0.50, 0.80, 1.00, 0.95, 0.60, 0.30, 0.15, 0.08])
GAUGES = {
    "Indus @ Tarbela": {"low": 1500, "high": 8500, "level_low": 1.5, "level_high": 6.0},
    "Jhelum @ Mangla": {"low": 450, "high": 3200, "level_low": 1.0, "level_high": 5.0},
    "Chenab @ Marala": {"low": 400, "high": 7000, "level_low": 1.0, "level_high": 6.5},
    "Ravi @ Balloki": {"low": 80, "high": 1800, "level_low": 0.5, "level_high": 4.0},
    "Sutlej @ Sulemanki": {"low": 60, "high": 1500, "level_low": 0.5, "level_high": 3.8},
}


def telemetry_12_months(end: date | None = None, seed: int = 42) -> pd.DataFrame:
    """Floating 12-month synthetic gauge record (SIMULATED, not observations).

    Returns long-format DataFrame: month, gauge, discharge_m3s, level_m.
    """
    end = end or date.today()
    rng = np.random.default_rng(seed)
    rows = []
    y, m = end.year, end.month
    months = []
    for _ in range(12):
        months.append((y, m))
        m -= 1
        if m == 0:
            m, y = 12, y - 1
    months.reverse()
    for (yy, mm) in months:
        s = _SEASON[mm - 1]
        for gname, g in GAUGES.items():
            noise = rng.normal(1.0, 0.04)
            q = (g["low"] + (g["high"] - g["low"]) * s) * noise
            lvl = (g["level_low"] + (g["level_high"] - g["level_low"]) * s) * rng.normal(1.0, 0.03)
            rows.append({"month": f"{yy}-{mm:02d}", "label": f"{calendar.month_abbr[mm]} {yy}",
                         "gauge": gname, "discharge_m3s": round(q, 1), "level_m": round(lvl, 2)})
    return pd.DataFrame(rows)


# ---------------------------------------------------------------- reference tables
def provinces_df() -> pd.DataFrame:
    return pd.DataFrame([{"province": k, **v} for k, v in C.PROVINCES.items()])


def structures_df() -> pd.DataFrame:
    return pd.DataFrame([{"name": k, **v} for k, v in C.STRUCTURES.items()])


def confluences_df() -> pd.DataFrame:
    return pd.DataFrame([{"confluence": k, "lat": v[0], "lon": v[1]} for k, v in C.CONFLUENCES.items()])


def peaks_df() -> pd.DataFrame:
    return pd.DataFrame([{"peak": k, **v} for k, v in C.PEAKS.items()])


def lakes_df() -> pd.DataFrame:
    return pd.DataFrame([{"lake": k, **v} for k, v in C.LAKES.items()])


def upstream_downstream(river: str) -> list[str]:
    """Structures on a river ordered upstream -> downstream by latitude along its polyline."""
    pts = C.RIVERS.get(river, [])
    items = [(n, s) for n, s in C.STRUCTURES.items() if s["river"] == river]
    def idx(s):
        return min(range(len(pts)), key=lambda i: (pts[i][0] - s["lat"]) ** 2 + (pts[i][1] - s["lon"]) ** 2) if pts else 0
    return [n for n, s in sorted(items, key=lambda t: idx(t[1]))]


# Mountain range reference (facts are summary-level; verify before expedition use)
RANGES = [
    {"group": "Northern Highlands & Major Ranges", "range": "Karakoram", "highest_peak": "K2", "height_m": 8611,
     "rivers": "Indus, Shyok, Hunza, Shigar, Braldu", "geology": "Collision-zone granite/gneiss, huge glaciers (Baltoro, Siachen, Biafo, Hispar)",
     "climbing": "Technical 8,000 m expeditions; main season Jun-Aug; permits via Alpine Club of Pakistan / GB tourism dept.",
     "tourism": "K2 Base Camp trek, Hunza, Skardu, Khunjerab Pass (Karakoram Highway)"},
    {"group": "Northern Highlands & Major Ranges", "range": "Himalayas", "highest_peak": "Nanga Parbat", "height_m": 8126,
     "rivers": "Indus, Jhelum, Kishanganga/Neelum, Kunhar", "geology": "Young fold mountains; Nanga Parbat-Haramosh massif uplifting rapidly",
     "climbing": "Nanga Parbat 'Killer Mountain', Rupal Face (4,600 m wall); Jun-Aug", "tourism": "Fairy Meadows, Astore, Neelum Valley, Deosai"},
    {"group": "Northern Highlands & Major Ranges", "range": "Hindu Kush", "highest_peak": "Tirich Mir", "height_m": 7708,
     "rivers": "Kabul, Chitral (Kunar), Panjkora, Swat", "geology": "Metamorphic/sedimentary, active tectonics (Hindu Kush deep seismic zone)",
     "climbing": "Tirich Mir first climbed 1950 (Norwegian); Jun-Sep", "tourism": "Chitral, Kalash valleys, Shandur"},
    {"group": "Northern Highlands & Major Ranges", "range": "Hindu Raj", "highest_peak": "Buni Zom", "height_m": 6551,
     "rivers": "Yarkhun, Ghizer, Swat headwaters", "geology": "Fold/thrust belt between Hindu Kush and Karakoram",
     "climbing": "Moderate-to-technical 6,000 m peaks", "tourism": "Broghil, Yarkhun valley, Phandar"},
    {"group": "Western & Southern Border Ranges", "range": "Spin Ghar (Koh-e-Safed)", "highest_peak": "Sikaram (Pak-Afghan border)", "height_m": 4755,
     "rivers": "Kurram, Kabul tributaries", "geology": "Limestone/metamorphic fold range", "climbing": "Trekking; border-zone restrictions apply",
     "tourism": "Kurram / Parachinar area (security-dependent)"},
    {"group": "Western & Southern Border Ranges", "range": "Sulaiman Mountains (Koh-e-Suleman)", "highest_peak": "Takht-e-Sulaiman", "height_m": 3487,
     "rivers": "Gomal, Zhob, hill torrents (rod-kohi)", "geology": "Folded Mesozoic-Cenozoic sedimentary rocks", "climbing": "Trekking / pilgrimage peak",
     "tourism": "Fort Munro, Zhob, Takht-e-Sulaiman"},
    {"group": "Western & Southern Border Ranges", "range": "Kirthar Range", "highest_peak": "Kutte-jo-Kabar (approx.)", "height_m": 2260,
     "rivers": "Seasonal torrents toward Indus plain and Hub", "geology": "Limestone anticlines; fossil-rich", "climbing": "Hiking",
     "tourism": "Kirthar National Park, Ranikot Fort"},
    {"group": "Western & Southern Border Ranges", "range": "Toba Kakar Range", "highest_peak": "approx. 3,000 m summits", "height_m": 3000,
     "rivers": "Zhob, Pishin Lora", "geology": "Folded sedimentary/ophiolitic belt", "climbing": "Hiking", "tourism": "Quetta-Pishin highlands"},
    {"group": "Western & Southern Border Ranges", "range": "Salt Range", "highest_peak": "Sakesar", "height_m": 1522,
     "rivers": "Jhelum (north), Soan", "geology": "Eocambrian salt/gypsum, Paleozoic-Mesozoic strata; Khewra salt mine", "climbing": "Hiking",
     "tourism": "Khewra Salt Mine, Katas Raj, Kallar Kahar, Soon Valley"},
]


def ranges_df() -> pd.DataFrame:
    return pd.DataFrame(RANGES)


CLIMATE_TABLE = [
    {"region": "Polar / glacial", "where": "Karakoram & high Himalaya above ~5,000 m", "feature": "Permanent ice; Siachen, Baltoro, Biafo glaciers"},
    {"region": "Highland", "where": "GB, northern KP, Hindu Kush / Hindu Raj", "feature": "Cold winters, snow-fed rivers"},
    {"region": "Temperate", "where": "Murree, Swat, Neelum, Quetta highlands", "feature": "Mild summers, winter snow, 800-1,500 mm rain in the east"},
    {"region": "Tropical / sub-tropical", "where": "Punjab & Sindh plains, Karachi coast", "feature": "Hot summers, monsoon Jul-Sep"},
    {"region": "Arid", "where": "Balochistan, Thar, Kharan, Cholistan", "feature": "<250 mm/year, extreme temperatures"},
]

# ---------------------------------------------------------------- hazards
HAZARDS = {
    "A. Hydro-meteorological": ["Riverine floods", "Flash floods / hill torrents", "Urban flooding", "Mudflows",
                                "Cloudbursts", "Monsoon variability", "Droughts", "GLOFs", "Heatwaves", "Water stress"],
    "B. Tectonic setting": ["Earthquakes", "Landslides", "Avalanches", "Tsunamis", "Seismic activity & land shifts", "Snow contingencies"],
    "C. Climatological & emerging": ["Accelerated glacier melt", "Sea-level rise & cyclones", "Smog", "Pollution (air, water, soil)",
                                    "Erratic global climate patterns"],
    "D. Anthropogenic": ["Industrial accidents & chemical spills", "Transport & infrastructure risks", "Maritime disasters", "Oil spills",
                         "Fires", "Encroachments", "Food security", "Population bulge", "Biological hazards"],
}

EXPOSURE = {
    "A. Population pressure & diverse terrains": "High density in the Indus plain floodplains alongside remote mountain valleys with poor access.",
    "B. Vulnerable settlements & infrastructure deficits": "Katcha housing, encroached waterways, weak drainage, exposed roads and bridges (e.g. Karakoram Highway).",
    "C. Institutional vulnerabilities": "Delayed decision-making; operational confusion; public distrust; resource misallocation.",
    "D. Socio-economic stratification": "Poverty, income inequality, limited education/health/emergency access, spatial entrapment, unequal mobility, marginalised communities, institutional neglect.",
}

EMERGING = {
    "A. Global Climate Risk Index (CRI) 2025": "Pakistan ranks among the most climate-affected countries in the Germanwatch CRI series. Check the latest edition for the exact rank.",
    "B. Increasing GLOF risks": "Rising temperatures destabilise moraine-dammed lakes; threats to settlements, hydropower and the Karakoram Highway. Past events: Attabad Lake (2010) and recent Ghizer / Taalidass lake events. Needs remote-sensing + in-situ monitoring and early-warning systems.",
    "C. Erratic monsoons & shifting precipitation": "Early onset and extended seasons, 'short-burst' rainfall, localized cloudbursts, hailstorms -> flash floods, mudflows, riverine floods, soil erosion.",
    "D. Sea intrusion & coastal salinization": "1,050 km coastline; Karachi, Gwadar, Thatta exposed to tidal surge and cyclones; saltwater intrusion degrades land and aquaculture. Needs coastal zone management, mangrove restoration, storm-surge warning.",
}

SCENARIOS = pd.DataFrame([
    {"scenario": "Baseline", "description": "Near-historic monsoon and glacier regime; existing infrastructure copes with managed losses.",
     "features": "Seasonal floods in known corridors; localized flash floods; routine GLOF alerts."},
    {"scenario": "Medium", "description": "Erratic monsoon with more short-burst extremes and faster melt.",
     "features": "Repeated flash floods and landslides on northern roads; stressed urban drainage; crop losses in Punjab/Sindh."},
    {"scenario": "Worst-case", "description": "Compound event: extreme monsoon + large GLOF + coastal cyclone + institutional breakdown.",
     "features": "Mass displacement, multi-province riverine flooding (cf. 2022), hydropower and highway loss, food-security shock."},
])

HISTORICAL_EVENTS = pd.DataFrame([
    {"event": "2005 Kashmir earthquake (M7.6)", "year": 2005, "lat": 34.54, "lon": 73.59, "type": "Earthquake"},
    {"event": "2010 Indus super-flood", "year": 2010, "lat": 28.4, "lon": 69.7, "type": "Riverine flood"},
    {"event": "2010 Attabad landslide-dam lake", "year": 2010, "lat": 36.31, "lon": 74.82, "type": "Landslide / GLOF-type"},
    {"event": "2022 monsoon mega-floods (Sindh, Balochistan)", "year": 2022, "lat": 26.5, "lon": 67.8, "type": "Riverine flood"},
    {"event": "1935 Quetta earthquake (M7.7)", "year": 1935, "lat": 29.6, "lon": 66.9, "type": "Earthquake"},
    {"event": "1945 Makran earthquake & tsunami (M8.1)", "year": 1945, "lat": 25.15, "lon": 63.48, "type": "Tsunami"},
    {"event": "2012 Gayari (Siachen) avalanche", "year": 2012, "lat": 35.30, "lon": 77.0, "type": "Avalanche"},
    {"event": "Karachi heatwave (2015)", "year": 2015, "lat": 24.86, "lon": 67.01, "type": "Heatwave"},
    {"event": "Cyclone Phet (Arabian Sea, Sindh coast)", "year": 2010, "lat": 24.5, "lon": 66.5, "type": "Cyclone"},
])

# ---------------------------------------------------------------- dispute tables (as provided in the project brief)
PONDAGE_TABLE = pd.DataFrame([
    {"project": "Kishanganga", "basin": "Jhelum", "india_design_mcm": 7.5, "pakistan_position_mcm": 1.0},
    {"project": "Ratle", "basin": "Chenab", "india_design_mcm": 24.0, "pakistan_position_mcm": 8.0},
])
OTHER_DESIGN_TABLE = pd.DataFrame([
    {"metric": "Spillway level (Ratle)", "pakistan_ask": "Raise by 20 m", "concern": "Low-level gates allow reservoir drawdown"},
    {"metric": "Power intake (Kishanganga)", "pakistan_ask": "Raise by 1.4 m", "concern": "Deep intakes keep drawing at low levels"},
    {"metric": "Power intake (Ratle)", "pakistan_ask": "Raise by up to 8.8 m", "concern": "Operational flexibility vs downstream flow consistency"},
    {"metric": "Freeboard (Ratle)", "pakistan_ask": "1 m (India: 2 m)", "concern": "Possible hidden extra storage"},
])
NEUTRAL_EXPERT_SCHEDULE = [
    ("Nov 2026", "Synthesis Memorandum distributed"),
    ("Feb 2027", "7th meeting & final hydraulic modelling exercise"),
    ("Mar 2027", "Draft Technical Decision circulated"),
    ("Jul 2027", "Final binding determination expected"),
]
