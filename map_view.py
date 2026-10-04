"""map_view.py - interactive Plotly maps (OpenStreetMap tiles, no API token needed).

Needs internet access in the browser to load tiles. Plotly is imported lazily.
"""
from __future__ import annotations

import coordinates as C

KIND_COLOR = {"dam": "#d62728", "barrage": "#1f77b4", "headwork": "#2ca02c"}
RIVER_COLOR = {"Indus": "#08519c", "Kabul": "#3182bd", "Gilgit": "#6baed6", "Jhelum": "#2171b5",
               "Chenab": "#2b8cbe", "Ravi": "#4292c6", "Sutlej": "#6baed6", "Panjnad": "#084594"}


def _go():
    import plotly.graph_objects as go
    return go


def _map_cls(go):
    return getattr(go, "Scattermap", None) or go.Scattermapbox


def new_fig(center=C.PAKISTAN_CENTER, zoom=4.6, height=560, title=None):
    go = _go()
    fig = go.Figure()
    layout = dict(height=height, margin=dict(l=0, r=0, t=40 if title else 0, b=0),
                  legend=dict(orientation="h", y=-0.02), title=title)
    center_d = dict(lat=center[0], lon=center[1])
    if hasattr(go, "Scattermap"):
        layout["map"] = dict(style="open-street-map", center=center_d, zoom=zoom)
    else:
        layout["mapbox"] = dict(style="open-street-map", center=center_d, zoom=zoom)
    fig.update_layout(**layout)
    return fig


def add_points(fig, names, lats, lons, color="#d62728", size=11, group=None, text=None, symbol=None):
    go = _go()
    fig.add_trace(_map_cls(go)(lat=list(lats), lon=list(lons), mode="markers+text" if text is not None else "markers",
                               marker=dict(size=size, color=color), text=text if text is not None else None,
                               textposition="top right", hovertext=list(names), hoverinfo="text",
                               name=group or "points"))


def add_line(fig, pts, name, color="#08519c", width=3, dash=False):
    go = _go()
    fig.add_trace(_map_cls(go)(lat=[p[0] for p in pts], lon=[p[1] for p in pts], mode="lines",
                               line=dict(width=width, color=color), name=name, hoverinfo="name"))


def add_polygon(fig, poly, name, color):
    pts = list(poly) + [poly[0]]
    go = _go()
    fig.add_trace(_map_cls(go)(lat=[p[0] for p in pts], lon=[p[1] for p in pts], mode="lines", fill="toself",
                               fillcolor=color, opacity=0.35, line=dict(width=1, color=color), name=name, hoverinfo="name"))


# ---------------------------------------------------------------- map builders
def province_map():
    fig = new_fig(title="Provinces and territories")
    for n, p in C.PROVINCES.items():
        add_points(fig, [f"{n} — capital: {p['capital']}"], [p["lat"]], [p["lon"]], p["color"], 16, n, text=[n])
    return fig


def water_system_map(show_links=True, rivers=None):
    fig = new_fig(title="Rivers, dams, barrages, link canals and confluences")
    for r, pts in C.RIVERS.items():
        if rivers and r not in rivers:
            continue
        add_line(fig, pts, r, RIVER_COLOR.get(r, "#08519c"))
    for kind, col in KIND_COLOR.items():
        items = [(n, s) for n, s in C.STRUCTURES.items() if s["kind"] == kind]
        add_points(fig, [f"{n} ({s['river']}, {s['province']})" for n, s in items],
                   [s["lat"] for _, s in items], [s["lon"] for _, s in items], col, 11, kind.title())
    if show_links:
        for ln, (a, b) in C.LINK_CANALS.items():
            A, B = C.STRUCTURES[a], C.STRUCTURES[b]
            add_line(fig, [(A["lat"], A["lon"]), (B["lat"], B["lon"])], ln, "#ff7f0e", 2)
    add_points(fig, list(C.CONFLUENCES), [v[0] for v in C.CONFLUENCES.values()], [v[1] for v in C.CONFLUENCES.values()],
               "#9467bd", 13, "Confluences")
    return fig


def link_canal_map():
    fig = new_fig(center=(31.0, 72.8), zoom=5.6, title="Link canals — Indus Basin Irrigation System (IBIS)")
    for r in ("Indus", "Jhelum", "Chenab", "Ravi", "Sutlej"):
        add_line(fig, C.RIVERS[r], r, RIVER_COLOR[r], 2)
    for ln, (a, b) in C.LINK_CANALS.items():
        A, B = C.STRUCTURES[a], C.STRUCTURES[b]
        add_line(fig, [(A["lat"], A["lon"]), (B["lat"], B["lon"])], ln, "#ff7f0e", 4)
    names = list(C.STRUCTURES)
    add_points(fig, names, [C.STRUCTURES[n]["lat"] for n in names], [C.STRUCTURES[n]["lon"] for n in names], "#333", 8, "Structures")
    return fig


def climate_map():
    fig = new_fig(title="Climatic regions (schematic)")
    for n, r in C.CLIMATE_REGIONS.items():
        add_polygon(fig, r["poly"], n, r["color"])
    return fig


def ranges_map():
    fig = new_fig(zoom=4.8, title="Mountain ranges and highest peaks")
    add_points(fig, list(C.MOUNTAIN_RANGES), [v[0] for v in C.MOUNTAIN_RANGES.values()], [v[1] for v in C.MOUNTAIN_RANGES.values()],
               "#8c564b", 12, "Range centres (approx.)", text=list(C.MOUNTAIN_RANGES))
    add_points(fig, [f"{n} — {p['m']} m ({p['range']})" for n, p in C.PEAKS.items()],
               [p["lat"] for p in C.PEAKS.values()], [p["lon"] for p in C.PEAKS.values()], "#000", 9, "Peaks")
    return fig


def lakes_map():
    fig = new_fig(title="Lakes of Pakistan")
    for prov, col in [(k, v["color"]) for k, v in C.PROVINCES.items()]:
        items = [(n, v) for n, v in C.LAKES.items() if v["province"] == prov]
        if items:
            add_points(fig, [n for n, _ in items], [v["lat"] for _, v in items], [v["lon"] for _, v in items], col, 12, prov)
    return fig


def hazards_map(events_df):
    fig = new_fig(title="Historical events & hazards")
    palette = ["#d62728", "#1f77b4", "#2ca02c", "#9467bd", "#ff7f0e", "#8c564b", "#e377c2"]
    for i, (t, g) in enumerate(events_df.groupby("type")):
        add_points(fig, [f"{r.event} ({r.year})" for r in g.itertuples()], g["lat"], g["lon"], palette[i % len(palette)], 13, t)
    return fig


def geopolitics_map():
    fig = new_fig(center=(33.6, 74.0), zoom=5.2, title="Geo-political & strategic: Western rivers, Indian projects, Pakistani storage")
    for r in ("Indus", "Jhelum", "Chenab", "Ravi", "Sutlej"):
        add_line(fig, C.RIVERS[r], r, RIVER_COLOR[r], 3)
    add_points(fig, [f"{n} — {p['mw']} MW ({p['river']})" for n, p in C.INDIAN_PROJECTS.items()],
               [p["lat"] for p in C.INDIAN_PROJECTS.values()], [p["lon"] for p in C.INDIAN_PROJECTS.values()], "#ff7f0e", 12,
               "Indian-administered J&K projects (approx.)")
    pk = {n: s for n, s in C.STRUCTURES.items() if s["kind"] == "dam" or n in ("Marala Headworks",)}
    add_points(fig, list(pk), [s["lat"] for s in pk.values()], [s["lon"] for s in pk.values()], "#d62728", 12, "Pakistani dams / Marala")
    return fig


def pakal_ratle_map():
    fig = new_fig(center=(33.3, 75.5), zoom=7.3, title="Chenab basin: Pakal Dul, Ratle, Kiru, Kwar and downstream Marala")
    add_line(fig, C.RIVERS["Chenab"], "Chenab", RIVER_COLOR["Chenab"], 4)
    sel = {k: v for k, v in C.INDIAN_PROJECTS.items() if k.split(" ")[0] in ("Pakal", "Ratle", "Kiru", "Kwar", "Baglihar", "Salal")}
    add_points(fig, [f"{n} — {p['mw']} MW" for n, p in sel.items()], [p["lat"] for p in sel.values()], [p["lon"] for p in sel.values()],
               "#ff7f0e", 14, "Projects (approx.)", text=list(sel))
    m = C.STRUCTURES["Marala Headworks"]
    add_points(fig, ["Marala Headworks"], [m["lat"]], [m["lon"]], "#2ca02c", 14, "Marala (downstream, Pakistan)", text=["Marala"])
    return fig


def china_map():
    fig = new_fig(center=(34.0, 73.4), zoom=6.4, title="China-financed hydropower portfolio")
    for r in ("Indus", "Jhelum", "Kabul"):
        add_line(fig, C.RIVERS[r], r, RIVER_COLOR[r], 3)
    add_points(fig, [f"{n} — {p['river']}, {p['province']}" for n, p in C.CHINA_HYDRO.items()],
               [p["lat"] for p in C.CHINA_HYDRO.values()], [p["lon"] for p in C.CHINA_HYDRO.values()], "#d62728", 15,
               "Projects (approx.)", text=list(C.CHINA_HYDRO))
    d = C.STRUCTURES["Diamer-Bhasha Dam (under construction)"]
    add_points(fig, ["Diamer-Bhasha Dam"], [d["lat"]], [d["lon"]], "#1f77b4", 14, "Diamer-Bhasha", text=["Diamer-Bhasha"])
    return fig


def hydraulic_map(stations: dict, results: dict):
    """stations: name -> (lat, lon); results: name -> status string."""
    fig = new_fig(center=(32.2, 73.6), zoom=6.0, title="Interactive hydraulic & risk model: basin hazard status")
    col = {"Nominal": "#2ca02c", "Elevated": "#ff7f0e", "Critical Hazard Warning": "#d62728"}
    for n, (la, lo) in stations.items():
        s = results.get(n, "Nominal")
        add_points(fig, [f"{n}: {s}"], [la], [lo], col.get(s, "#555"), 18, n, text=[n])
    for r in ("Chenab", "Jhelum", "Ravi"):
        add_line(fig, C.RIVERS[r], r, RIVER_COLOR[r], 2)
    return fig


def forests_parks_map(selected=None):
    fig = new_fig(zoom=4.6, title="Notable forests and parks (approx. locations)")
    add_points(fig, list(C.FORESTS), [v[0] for v in C.FORESTS.values()], [v[1] for v in C.FORESTS.values()], "#2ca02c", 11, "Forests")
    add_points(fig, list(C.PARKS), [v[0] for v in C.PARKS.values()], [v[1] for v in C.PARKS.values()], "#1f77b4", 10, "Parks")
    return fig


def park_map(park_name: str, zoom=9.5):
    """Map centred on one park, with all other parks as faint context."""
    if park_name not in C.PARKS:
        raise KeyError(park_name)
    la, lo = C.PARKS[park_name]
    fig = new_fig(center=(la, lo), zoom=zoom, height=420, title=f"{park_name} (approx. location)")
    others = {n: v for n, v in C.PARKS.items() if n != park_name}
    add_points(fig, list(others), [v[0] for v in others.values()], [v[1] for v in others.values()], "#9ecae1", 8, "Other parks")
    add_points(fig, [park_name], [la], [lo], "#d62728", 18, "Selected park", text=[park_name])
    return fig
