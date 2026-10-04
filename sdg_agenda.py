"""sdg_agenda.py - UN SDGs, MDGs and Vision 2030 (Pakistan) alignment for food, water, environment."""
import pandas as pd

SDGS = pd.DataFrame([
    {"sdg": 1, "goal": "No Poverty", "link": "Poverty alleviation, social protection after floods", "atlas_theme": "Socio-economic"},
    {"sdg": 2, "goal": "Zero Hunger", "link": "Food security, resilient Rabi/Kharif cropping, water-efficient agriculture", "atlas_theme": "Agro-economic"},
    {"sdg": 6, "goal": "Clean Water and Sanitation", "link": "IBIS efficiency, groundwater, water quality, IWT/IRSA governance", "atlas_theme": "Hydraulic & geo-political"},
    {"sdg": 7, "goal": "Affordable and Clean Energy", "link": "Hydropower portfolio (Tarbela, Karot, Suki Kinari, Diamer-Bhasha)", "atlas_theme": "China hydropower"},
    {"sdg": 11, "goal": "Sustainable Cities and Communities", "link": "Urban flooding, smog, encroachment", "atlas_theme": "Disaster risk"},
    {"sdg": 13, "goal": "Climate Action", "link": "GLOF early warning, adaptation, loss and damage", "atlas_theme": "Disaster risk"},
    {"sdg": 14, "goal": "Life Below Water", "link": "Mangroves, coastal salinization, aquaculture", "atlas_theme": "Forests & coast"},
    {"sdg": 15, "goal": "Life on Land", "link": "Forests, national parks, biodiversity", "atlas_theme": "Forests & parks"},
    {"sdg": 16, "goal": "Peace, Justice and Strong Institutions", "link": "Treaty compliance, CCI/IRSA mechanisms", "atlas_theme": "Geo-political"},
    {"sdg": 17, "goal": "Partnerships for the Goals", "link": "CPEC, multilateral finance, transboundary cooperation", "atlas_theme": "Geo-political & finance"},
])

MDGS = pd.DataFrame([
    {"mdg": 1, "goal": "Eradicate extreme poverty and hunger", "note": "2000-2015 framework; succeeded by SDGs in 2015"},
    {"mdg": 7, "goal": "Ensure environmental sustainability", "note": "Included water and sanitation access and forest cover targets"},
    {"mdg": 8, "goal": "Global partnership for development", "note": "Aid, trade and technology partnerships"},
])

VISION_2030 = pd.DataFrame([
    {"pillar": "Food security", "focus": "Raise productivity per unit of water; reduce post-harvest losses"},
    {"pillar": "Water conservation", "focus": "Storage, canal lining, drip/sprinkler, groundwater regulation, National Water Policy"},
    {"pillar": "Environmental protection", "focus": "Forest expansion (e.g. national tree-planting drives), mangrove restoration, pollution control"},
    {"pillar": "Sustainable development", "focus": "Resilient infrastructure, renewable energy, disaster risk reduction"},
    {"pillar": "Zero hunger & poverty alleviation", "focus": "Targeted social protection and rural livelihoods"},
])

NOTE = ("Pakistan's national long-term framework is commonly referred to as Vision 2025 (and its successor planning documents) "
        "alongside SDG localisation by the Planning Commission. This table is a thematic alignment aid, "
        "not an official crosswalk; verify against the Planning Commission's current documents.")

DEFAULT_INDICATORS = {"Irrigation efficiency (%)": 40, "Safely managed drinking water (%)": 36, "Forest cover (% of land)": 5,
                      "Renewable share in power (%)": 55, "Population food-secure (%)": 65}
DEFAULT_TARGETS = {"Irrigation efficiency (%)": 60, "Safely managed drinking water (%)": 100, "Forest cover (% of land)": 6,
                   "Renewable share in power (%)": 60, "Population food-secure (%)": 100}
