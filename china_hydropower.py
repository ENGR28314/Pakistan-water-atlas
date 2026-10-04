"""china_hydropower.py - Financial footprint of China's investments in Pakistan's hydropower.

Capacities per project brief (CPEC pages). Capex/CF values below are ILLUSTRATIVE inputs for the
LCOE engine; replace with figures from PPIB / CPEC Authority / sponsor disclosures.
"""
import pandas as pd

SUMMARY = ("Chinese investors hold a dominant share of foreign direct investment in Pakistan's power sector under CPEC; "
           "hydropower projects are financed through a mix of sponsor equity and Chinese bank debt.")

PORTFOLIO = pd.DataFrame([
    {"project": "Karot Hydropower Project", "mw": 720, "river": "Jhelum", "status": "Operational (per CPEC page; verify)", "illus_capex_usd_m": 1700, "illus_cf": 0.55},
    {"project": "Suki Kinari (SK) Hydropower Station", "mw": 884, "river": "Kunhar", "status": "Operational (per CPEC page; verify)", "illus_capex_usd_m": 1960, "illus_cf": 0.50},
    {"project": "Kohala Hydropower Project", "mw": 1124, "river": "Jhelum", "status": "Under development (verify)", "illus_capex_usd_m": 2400, "illus_cf": 0.55},
    {"project": "Azad Pattan Hydropower Project", "mw": 700.7, "river": "Jhelum", "status": "Under development (verify)", "illus_capex_usd_m": 1600, "illus_cf": 0.55},
])
