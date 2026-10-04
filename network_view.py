"""network_view.py - schematic network diagrams (NOT to scale) built with networkx + Plotly."""
from __future__ import annotations

import networkx as nx

# Hand-laid schematic positions (x east, y north)
IRRIGATION_POS = {
    "Indus (upper)": (0, 10), "Tarbela": (0, 8.5), "Kabul R.": (1.2, 8.5), "Attock": (0.6, 8), "Jinnah": (0.4, 6.8),
    "Chashma": (0.3, 6), "C-J Link": (1.2, 5.6), "Taunsa": (0.2, 4.2), "T-P Link": (1.2, 3.6), "Panjnad": (1.8, 3),
    "Guddu": (0.2, 2), "Sukkur": (0.2, 1.2), "Kotri": (0.2, 0.3), "Arabian Sea": (0.2, -0.6),
    "Jhelum R.": (3.2, 9.2), "Mangla": (3.2, 8.2), "Rasul": (3.0, 7.2), "Chenab R.": (4.6, 9.2), "Marala": (4.6, 8.2),
    "Khanki": (4.4, 7.6), "Qadirabad": (4.2, 7.0), "RQ Link": (3.5, 7.0), "Trimmu": (3.0, 5.6), "Ravi R.": (5.6, 8.2),
    "Balloki": (5.0, 6.6), "Sidhnai": (4.2, 5.0), "Sutlej R.": (6.4, 7.0), "Sulemanki": (6.0, 5.8), "Islam": (5.5, 4.4),
}
IRRIGATION_EDGES = [
    ("Indus (upper)", "Tarbela"), ("Tarbela", "Attock"), ("Kabul R.", "Attock"), ("Attock", "Jinnah"), ("Jinnah", "Chashma"),
    ("Chashma", "Taunsa"), ("Chashma", "C-J Link"), ("C-J Link", "Trimmu"), ("Taunsa", "T-P Link"), ("T-P Link", "Panjnad"),
    ("Taunsa", "Guddu"), ("Guddu", "Sukkur"), ("Sukkur", "Kotri"), ("Kotri", "Arabian Sea"),
    ("Jhelum R.", "Mangla"), ("Mangla", "Rasul"), ("Rasul", "RQ Link"), ("RQ Link", "Qadirabad"), ("Rasul", "Trimmu"),
    ("Chenab R.", "Marala"), ("Marala", "Khanki"), ("Khanki", "Qadirabad"), ("Qadirabad", "Trimmu"),
    ("Qadirabad", "Balloki"), ("Ravi R.", "Balloki"), ("Balloki", "Sidhnai"), ("Trimmu", "Sidhnai"), ("Trimmu", "Panjnad"),
    ("Sutlej R.", "Sulemanki"), ("Balloki", "Sulemanki"), ("Sulemanki", "Islam"), ("Islam", "Panjnad"), ("Panjnad", "Guddu"),
]
HYDRO = {"Tarbela", "Mangla"}
LINKS = {"C-J Link", "T-P Link", "RQ Link"}

CONFLUENCE_POS = {
    "Gilgit R.": (0, 4), "Hunza R.": (1, 5), "Indus (Skardu)": (-1, 5), "Jaglot": (0, 3.2), "Kabul R.": (2.5, 3),
    "Attock": (1.2, 2.2), "Jhelum R.": (4, 3), "Chenab R.": (5, 3), "Ravi R.": (6, 3), "Sutlej R.": (7, 3),
    "Trimmu (Jhelum+Chenab)": (4.5, 2), "Ahmadpur Sial (+Ravi)": (5.3, 1.4), "Panjnad (+Sutlej)": (6.2, 0.7),
    "Mithankot (+Indus)": (4, 0), "Indus (lower)": (4, -1),
}
CONFLUENCE_EDGES = [
    ("Hunza R.", "Jaglot"), ("Gilgit R.", "Jaglot"), ("Indus (Skardu)", "Jaglot"), ("Jaglot", "Attock"), ("Kabul R.", "Attock"),
    ("Jhelum R.", "Trimmu (Jhelum+Chenab)"), ("Chenab R.", "Trimmu (Jhelum+Chenab)"), ("Trimmu (Jhelum+Chenab)", "Ahmadpur Sial (+Ravi)"),
    ("Ravi R.", "Ahmadpur Sial (+Ravi)"), ("Ahmadpur Sial (+Ravi)", "Panjnad (+Sutlej)"), ("Sutlej R.", "Panjnad (+Sutlej)"),
    ("Panjnad (+Sutlej)", "Mithankot (+Indus)"), ("Attock", "Mithankot (+Indus)"), ("Mithankot (+Indus)", "Indus (lower)"),
]


def build_graph(edges, pos) -> nx.DiGraph:
    g = nx.DiGraph()
    for n, p in pos.items():
        g.add_node(n, pos=p)
    g.add_edges_from(edges)
    return g


def irrigation_graph() -> nx.DiGraph:
    return build_graph(IRRIGATION_EDGES, IRRIGATION_POS)


def confluence_graph() -> nx.DiGraph:
    return build_graph(CONFLUENCE_EDGES, CONFLUENCE_POS)


def downstream_of(g: nx.DiGraph, node: str) -> list[str]:
    return sorted(nx.descendants(g, node))


def upstream_of(g: nx.DiGraph, node: str) -> list[str]:
    return sorted(nx.ancestors(g, node))


def to_figure(g: nx.DiGraph, title: str, highlight: str | None = None):
    import plotly.graph_objects as go
    ex, ey = [], []
    for a, b in g.edges():
        (x0, y0), (x1, y1) = g.nodes[a]["pos"], g.nodes[b]["pos"]
        ex += [x0, x1, None]
        ey += [y0, y1, None]
    desc = set(nx.descendants(g, highlight)) if highlight else set()
    asc = set(nx.ancestors(g, highlight)) if highlight else set()
    colors, hover = [], []
    for n in g.nodes():
        if n == highlight:
            colors.append("#d62728")
        elif n in desc:
            colors.append("#ff7f0e")
        elif n in asc:
            colors.append("#2ca02c")
        elif n in HYDRO:
            colors.append("#9467bd")
        elif n in LINKS:
            colors.append("#8c564b")
        else:
            colors.append("#1f77b4")
        hover.append(n)
    nx_, ny_ = zip(*[g.nodes[n]["pos"] for n in g.nodes()])
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=ex, y=ey, mode="lines", line=dict(width=1.5, color="#888"), hoverinfo="none", showlegend=False))
    fig.add_trace(go.Scatter(x=list(nx_), y=list(ny_), mode="markers+text", text=list(g.nodes()), textposition="top center",
                             marker=dict(size=16, color=colors), hovertext=hover, hoverinfo="text", showlegend=False))
    fig.update_layout(title=title + " (schematic, not to scale)", height=620, xaxis=dict(visible=False), yaxis=dict(visible=False),
                      margin=dict(l=10, r=10, t=50, b=10))
    return fig
