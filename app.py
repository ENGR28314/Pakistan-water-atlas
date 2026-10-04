"""Pakistan Water, Hazard & Hydro-Politics Atlas - Streamlit app.

Run:  streamlit run app.py
Created and Designed by Engr. Syed Hassan Iqbal Shah
"""
import pandas as pd
import streamlit as st

import agro_economic as AG
import china_hydropower as CH
import coordinates as C
import data_loader as D
import forests_parks as FP
import geopolitics as G
import hydraulic_model as H
import input_driven as I
import map_view as M
import network_view as N
import sdg_agenda as SDG
import simulation_engines as S
import socio_economic as SE
import sources as SRC

st.set_page_config(page_title="Pakistan Water & Hazard Atlas", page_icon="🌊", layout="wide")


def show(fig, key):
    st.plotly_chart(fig, use_container_width=True, key=key)


st.title("🌊 Pakistan Water, Hazard & Hydro-Politics Atlas")
st.caption(SRC.CREDIT)
st.info(SRC.DISCLAIMER)

TABS = ["🗺️ Provinces & Water System", "🌡️ Climate", "⛰️ Mountains", "⚠️ Disaster Risk", "🏞️ Lakes",
        "🌲 Forests", "🦌 Parks", "📈 Socio-Economic", "🌾 Agro-Economic", "🌍 Geo-Political",
        "🇮🇳 Indian Atrocities", "🏗️ China Hydropower", "📐 Pakal Dul & Ratle", "🧪 Hydraulic & Risk Models",
        "🎯 SDGs / Vision", "📚 Sources"]
tabs = st.tabs(TABS)

# ------------------------------------------------------------------ Provinces & water
with tabs[0]:
    st.subheader("Provinces and territories")
    show(M.province_map(), "prov")
    st.dataframe(D.provinces_df()[["province", "capital"]], hide_index=True)
    st.subheader("Rivers, dams, barrages, link canals, confluences")
    rivers = st.multiselect("Rivers", list(C.RIVERS), default=list(C.RIVERS))
    links = st.checkbox("Show link canals", True)
    show(M.water_system_map(links, rivers), "water")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Structures**")
        st.dataframe(D.structures_df(), hide_index=True)
    with c2:
        st.markdown("**Confluences**")
        st.dataframe(D.confluences_df(), hide_index=True)
    r = st.selectbox("Upstream → downstream order on river", [x for x in C.RIVERS if D.upstream_downstream(x)])
    st.write(" → ".join(D.upstream_downstream(r)))
    st.subheader("Link canals — Indus Basin Irrigation System (IBIS)")
    show(M.link_canal_map(), "links")
    st.dataframe(pd.DataFrame([{"link canal": k, "from": a, "to": b} for k, (a, b) in C.LINK_CANALS.items()]), hide_index=True)
    st.subheader("Irrigation & hydropower network (schematic)")
    g = N.irrigation_graph()
    node = st.selectbox("Highlight node (red) — downstream orange, upstream green", ["(none)"] + list(g.nodes()))
    show(N.to_figure(g, "Irrigation & hydropower network", None if node == "(none)" else node), "irr_net")
    st.subheader("River confluence network (schematic)")
    show(N.to_figure(N.confluence_graph(), "River confluence network"), "conf_net")

# ------------------------------------------------------------------ Climate
with tabs[1]:
    st.subheader("Climatic regions of Pakistan")
    show(M.climate_map(), "climate")
    st.dataframe(pd.DataFrame(D.CLIMATE_TABLE), hide_index=True)
    st.caption("Region polygons are coarse schematic shapes, not climate-classification boundaries.")

# ------------------------------------------------------------------ Mountains
with tabs[2]:
    st.subheader("Mountain ranges")
    show(M.ranges_map(), "ranges")
    rdf = D.ranges_df()
    sel = st.selectbox("Range", rdf["range"])
    row = rdf[rdf["range"] == sel].iloc[0]
    st.markdown(f"**{row['group']}** — highest peak: **{row['highest_peak']}** ({row['height_m']} m)")
    for k in ("rivers", "geology", "climbing", "tourism"):
        st.markdown(f"- **{k.title()}:** {row[k]}")
    st.dataframe(rdf, hide_index=True)
    st.caption("Heights for lesser ranges are approximate; verify before expedition planning.")

# ------------------------------------------------------------------ Disaster risk
with tabs[3]:
    st.subheader("National Disaster Risk Context")
    t1, t2, t3, t4, t5 = st.tabs(["1. Hazard profile", "2. Exposure & vulnerability", "3. Emerging risks", "4. Risk scenarios", "Historical events map"])
    with t1:
        for grp, items in D.HAZARDS.items():
            with st.expander(grp, expanded=False):
                for i in items:
                    st.markdown(f"- {i}")
    with t2:
        for k, v in D.EXPOSURE.items():
            st.markdown(f"**{k}** — {v}")
    with t3:
        for k, v in D.EMERGING.items():
            st.markdown(f"**{k}** — {v}")
    with t4:
        st.dataframe(D.SCENARIOS, hide_index=True)
        eng = S.ClimateScenarioEngine()
        peak = st.number_input("Base peak flow (m³/s)", 1000, 50000, 10000, 500)
        rain = st.slider("Base rainfall (mm/hr)", 0, 100, 30)
        st.dataframe(eng.project(peak, rain), hide_index=True)
    with t5:
        show(M.hazards_map(D.HISTORICAL_EVENTS), "hazmap")
        st.dataframe(D.HISTORICAL_EVENTS, hide_index=True)

# ------------------------------------------------------------------ Lakes
with tabs[4]:
    st.subheader("Lakes of Pakistan by province (selected)")
    show(M.lakes_map(), "lakes")
    st.dataframe(D.lakes_df(), hide_index=True)
    st.caption("A selection, not a complete inventory of all lakes.")

# ------------------------------------------------------------------ Forests
with tabs[5]:
    st.subheader("Main forest types")
    st.dataframe(FP.FOREST_TYPES, hide_index=True)
    st.subheader("Notable forests")
    name = st.selectbox("Select a forest", FP.NOTABLE_FORESTS["forest"])
    f = FP.NOTABLE_FORESTS[FP.NOTABLE_FORESTS["forest"] == name].iloc[0]
    for k in ("province", "type", "area", "history", "wildlife", "attractions"):
        st.markdown(f"- **{k.title()}:** {f[k]}")
    st.dataframe(FP.NOTABLE_FORESTS, hide_index=True)
    show(M.forests_parks_map(), "forestmap")
    st.caption("'verify' marks figures I could not confirm; locations are approximate.")

# ------------------------------------------------------------------ Parks
with tabs[6]:
    st.subheader("National parks and urban parks")
    pn = st.selectbox("Select a park for details", FP.NATIONAL_PARKS["park"])
    p = FP.NATIONAL_PARKS[FP.NATIONAL_PARKS["park"] == pn].iloc[0]
    left, right = st.columns([1, 1.4])
    with left:
        for k in ("province", "category", "area", "history", "wildlife", "attractions"):
            st.markdown(f"**{k.title()}:** {p[k]}")
        st.caption("Coordinates approximate. Entries with 'verify' need checking against official sources.")
    with right:
        show(M.park_map(pn), "parkmap")
    st.dataframe(FP.NATIONAL_PARKS.drop(columns=["lat", "lon"]), hide_index=True)

# ------------------------------------------------------------------ Socio / Agro shared panel
def input_panel(key):
    st.markdown("#### Input-driven socio/agro data")
    st.caption("Defaults are illustrative placeholders. Edit the table or upload a CSV with the same columns.")
    up = st.file_uploader("Upload CSV (optional)", type="csv", key=f"{key}_up")
    base = I.default_data()
    if up is not None:
        try:
            base = I.validate(pd.read_csv(up))
        except Exception as e:
            st.error(f"Could not use the CSV: {e}")
    df = I.validate(st.data_editor(base, num_rows="dynamic", key=f"{key}_ed", hide_index=True))
    c1, c2 = st.columns(2)
    metric = c1.selectbox("Metric", list(I.METRICS), key=f"{key}_m")
    gtype = c2.selectbox("Graph type", I.GRAPH_TYPES, key=f"{key}_g")
    if df.empty:
        st.warning("No rows to plot.")
        return
    show(I.build_chart(df, metric, gtype), f"{key}_chart")
    s = I.summary(df, metric)
    st.write(f"Total: **{s['total']:,.0f}** — largest: **{s['top']}** ({s['share_top_pct']}%)")


with tabs[7]:
    st.subheader("Socio-Economic Domain")
    for k, v in SE.DOMAINS.items():
        st.markdown(f"**{k}** — {v}")
    input_panel("socio")

with tabs[8]:
    st.subheader("Agro-Economic Domain")
    for k, v in AG.OVERVIEW.items():
        st.markdown(f"**{k}** — {v}")
    st.markdown("#### Major crop seasons")
    st.dataframe(AG.SEASONS, hide_index=True)
    a, b = st.columns(2)
    with a:
        st.markdown("**Rabi**")
        st.dataframe(AG.RABI, hide_index=True)
    with b:
        st.markdown("**Kharif**")
        st.dataframe(AG.KHARIF, hide_index=True)
    st.markdown("#### Apiculture")
    st.dataframe(AG.APICULTURE, hide_index=True)
    st.markdown("#### Aquaculture")
    st.dataframe(AG.AQUACULTURE, hide_index=True)
    input_panel("agro")

# ------------------------------------------------------------------ Geo-political
with tabs[9]:
    st.subheader("Geo-Political & Strategic Domains")
    show(M.geopolitics_map(), "geo")
    st.markdown("**Hydro-politics of Kashmir** — " + G.HYDRO_POLITICS_KASHMIR)
    st.markdown("**IWT crisis**")
    for x in G.IWT_CRISIS:
        st.markdown(f"- {x}")
    st.markdown("**Maritime trade infrastructure** — " + G.MARITIME)
    st.markdown("#### Court of Arbitration (PCA) timeline")
    st.dataframe(G.PCA_TIMELINE, hide_index=True)
    st.success(G.COA_VALIDITY)
    st.warning(G.INTER_BASIN_TRANSFER)
    st.markdown("#### Chenab projects and Punjab's crops")
    for k, v in G.CHENAB_IMPACT.items():
        st.markdown(f"**{k}** — {v}")
    st.markdown("#### CPEC: Diamer-Bhasha Dam")
    for k, v in G.DIAMER_BHASHA.items():
        st.markdown(f"**{k}** — {v}")
    st.markdown("#### Punjab vs Sindh")
    for k, v in G.PUNJAB_SINDH.items():
        st.markdown(f"**{k}** — {v}")
    eng = S.WaterShareEngine()
    avail = st.slider("Available water (MAF) — illustrative", 40, 120, 80)
    pun = st.number_input("Punjab claim (MAF)", 1.0, 100.0, 55.0)
    sin = st.number_input("Sindh claim (MAF)", 1.0, 100.0, 48.0)
    st.dataframe(eng.share(avail, {"Punjab": pun, "Sindh": sin}), hide_index=True)
    st.markdown("#### Legal mechanisms (IRSA inter-provincial)")
    for k, v in G.IRSA_LEGAL:
        st.markdown(f"- **{k}:** {v}")

# ------------------------------------------------------------------ Indian atrocities (tab name as requested)
with tabs[10]:
    st.subheader("🇮🇳 Chenab Projects, Flow Concerns and the Indus Waters Treaty")
    st.caption("This tab presents Pakistan's position as supplied in the project brief. See India's stated position at the end.")
    show(M.pakal_ratle_map(), "ind_map")
    st.markdown("### 1(A). Two new canal systems to be created in India")
    for x in G.INDIAN_ACTIONS_1A:
        st.markdown(f"- {x}")
    st.markdown("### 1(B). Ravi-Beas link and expedited hydropower")
    for x in G.INDIAN_ACTIONS_1B:
        st.markdown(f"- {x}")
    st.markdown("### 2(A). The disputed engineering specifications")
    st.write("Pakistan argues India's designs go beyond the 'run-of-the-river' permissions of the IWT and amount to "
             "'imagined capacity' giving structural control over transboundary flows.")
    for t, body in G.DISPUTED_SPECS:
        with st.expander(t):
            st.write(body)
    st.dataframe(D.PONDAGE_TABLE, hide_index=True)
    st.dataframe(D.OTHER_DESIGN_TABLE, hide_index=True)
    st.markdown("### 2(B). The July 2027 Neutral Expert timeline")
    for d, e in D.NEUTRAL_EXPERT_SCHEDULE:
        st.markdown(f"**{d}** — {e}")
    st.markdown("**The incompatible reality on the ground**")
    for x in G.RUNTIME_RISK:
        st.markdown(f"- {x}")
    st.info(G.INDIA_POSITION_NOTE)

# ------------------------------------------------------------------ China hydropower
with tabs[11]:
    st.subheader("The Financial Footprint of China's Investments in Pakistan's Hydropower")
    st.write(CH.SUMMARY)
    show(M.china_map(), "china")
    st.dataframe(CH.PORTFOLIO, hide_index=True)
    st.markdown("#### Illustrative energy & cost engine")
    eco = S.HydropowerEconomics()
    pr = st.selectbox("Project", CH.PORTFOLIO["project"])
    row = CH.PORTFOLIO[CH.PORTFOLIO["project"] == pr].iloc[0]
    capex = st.number_input("Capex (USD million) — illustrative", 100, 10000, int(row["illus_capex_usd_m"]), 50)
    cf = st.slider("Capacity factor", 0.2, 0.8, float(row["illus_cf"]), 0.01)
    disc = st.slider("Discount rate", 0.03, 0.15, 0.08, 0.005)
    st.metric("Annual energy (GWh)", f"{eco.annual_gwh(row['mw'], cf):,.0f}")
    st.metric("LCOE (USD/MWh)", f"{eco.lcoe_usd_mwh(capex, row['mw'], cf, disc):,.1f}")
    st.caption("Capex and capacity factors are placeholders, not published project financials.")

# ------------------------------------------------------------------ Pakal Dul & Ratle
with tabs[12]:
    st.subheader("Objectionable Technical Designs of India's Pakal Dul (1,000 MW) and Ratle (850 MW)")
    show(M.pakal_ratle_map(), "pr_map")
    st.dataframe(G.PAKAL_DUL_RATLE, hide_index=True)
    st.markdown("#### Pondage engine")
    proj = st.selectbox("Project", D.PONDAGE_TABLE["project"])
    pr_row = D.PONDAGE_TABLE[D.PONDAGE_TABLE["project"] == proj].iloc[0]
    q = st.number_input("Mean inflow (m³/s)", 50, 5000, 600, 50)
    mins = st.slider("Emptying time (minutes)", 5, 240, 30)
    te = S.TreatyDisputeEngine()
    gap = te.pondage_gap(pr_row["india_design_mcm"], pr_row["pakistan_position_mcm"], q)
    st.write(gap)
    st.metric("Surge if India's pond emptied (m³/s)", f"{te.downstream_surge(pr_row['india_design_mcm'], mins):,.0f}")
    st.caption("Illustrative arithmetic only; real releases are limited by gate and outlet capacity.")

# ------------------------------------------------------------------ Hydraulic & risk models
with tabs[13]:
    st.subheader("Interactive Hydraulic & Risk Models")
    st.caption("Weather and telemetry are SIMULATED, not live feeds.")
    sub1, sub2, sub3, sub4 = st.tabs(["Flash-flood synthesizer", "Water quality", "12-month telemetry analytics", "Monte-Carlo & reservoir"])
    with sub1:
        stn = st.selectbox("Region / basin point", list(H.WEATHER_STATIONS))
        w = H.WEATHER_STATIONS[stn]
        rain = st.slider("Rainfall intensity (mm/hr)", 0, 100, 20)
        cap = st.number_input("Channel capacity (m³/s)", 500, 50000, 12000, 500)
        res = H.flash_flood_hazard(w["base_flow"], rain, cap)
        st.metric("Peak flow (m³/s)", f"{res['peak_flow_m3s']:,}")
        st.metric("Stress index", res["stress_index"])
        {"Nominal": st.success, "Elevated": st.warning}.get(res["status"], st.error)(res["status"])
        coords = {"Sialkot (Chenab basin)": (32.50, 74.53), "Jhelum (Jhelum basin)": (32.93, 73.73), "Lahore (Ravi basin)": (31.55, 74.34)}
        statuses = {n: H.flash_flood_hazard(v["base_flow"], rain, cap)["status"] for n, v in H.WEATHER_STATIONS.items()}
        show(M.hydraulic_map(coords, statuses), "hyd_map")
        inst = st.number_input("Installed MW for stress calc", 0, 5000, 1000, 50)
        st.write(H.calculate_basin_stress(res["peak_flow_m3s"], cap, inst))
        st.write(H.cluster_hazard_flags(res["peak_flow_m3s"], rain))
    with sub2:
        c = st.columns(5)
        do = c[0].number_input("DO mg/L", 0.0, 14.0, 8.5)
        ph = c[1].number_input("pH", 4.0, 10.0, 7.5)
        tu = c[2].number_input("Turbidity NTU", 0.0, 200.0, 2.0)
        sa = c[3].number_input("Salinity dS/m", 0.0, 20.0, 0.3)
        bo = c[4].number_input("BOD mg/L", 0.0, 30.0, 1.0)
        st.write(H.water_quality_index(do, ph, tu, sa, bo))
    with sub3:
        import plotly.express as px
        tel = D.telemetry_12_months()
        metric = st.radio("Variable", ["level_m", "discharge_m3s"], horizontal=True)
        fig = px.area(tel, x="label", y=metric, color="gauge", title="12-month simulated gauge record")
        fig.update_xaxes(categoryorder="array", categoryarray=list(dict.fromkeys(tel["label"])))
        show(fig, "tele")
    with sub4:
        med = st.number_input("Median annual peak (m³/s)", 1000, 40000, 9000, 500)
        mc = S.FloodMonteCarlo(med).run(5000)
        st.metric("P(peak > 15,000 m³/s)", f"{mc['p_exceed']:.1%}")
        import plotly.express as px
        show(px.histogram(x=mc["peaks"], nbins=60, labels={"x": "Annual peak (m³/s)"}), "mc")
        days = 60
        inflow = [1500 + 80 * i for i in range(days)]
        rel = [2000] * days
        sim = S.ReservoirSimulator(live_capacity_mcm=6000, dead_mcm=2000).run(inflow, rel)
        show(px.line(sim, x="day", y="storage_mcm", title="Illustrative reservoir routing"), "res")

# ------------------------------------------------------------------ SDGs
with tabs[14]:
    st.subheader("UN SDGs, MDGs and Vision agenda")
    st.dataframe(SDG.SDGS, hide_index=True)
    st.markdown("**MDGs (2000–2015)**")
    st.dataframe(SDG.MDGS, hide_index=True)
    st.markdown("**Vision / national agenda themes**")
    st.dataframe(SDG.VISION_2030, hide_index=True)
    st.caption(SDG.NOTE)
    ind = {}
    for k, v in SDG.DEFAULT_INDICATORS.items():
        ind[k] = st.number_input(k, 0.0, 1000.0, float(v), key=f"sdg_{k}")
    st.dataframe(S.sdg_score(ind, SDG.DEFAULT_TARGETS), hide_index=True)
    st.caption("Default indicator values are placeholders; enter official figures.")

# ------------------------------------------------------------------ Sources
with tabs[15]:
    st.subheader("📚 Sources")
    for t, u in SRC.SOURCES:
        st.markdown(f"- [{t}]({u})")
    st.caption("Links were supplied in the project brief; check them directly, especially the 2026 items.")

st.divider()
st.caption(SRC.CREDIT)
