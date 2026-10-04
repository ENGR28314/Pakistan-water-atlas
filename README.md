# Pakistan Water, Hazard & Hydro-Politics Atlas

Streamlit app covering provinces, rivers, dams/barrages, link canals, confluences, climate regions, mountain ranges,
national disaster risk, lakes, forests, parks, socio-economic and agro-economic domains, geo-political/IWT issues,
China-financed hydropower, Pakal Dul/Ratle designs, SDG alignment, simulation engines and sources.

*Created and Designed by Engr. Syed Hassan Iqbal Shah*

## Run

```bash
pip install -r requirements.txt
streamlit run app.py
python -m unittest test_suite.py -v
```

Maps use OpenStreetMap tiles, so the browser needs internet access. No API token is needed.

## Files

| File | Purpose |
|---|---|
| `app.py` | Streamlit UI (16 tabs) |
| `coordinates.py` | Approximate lat/lon for provinces, rivers, structures, peaks, lakes, forests, parks, projects |
| `data_loader.py` | Reference tables, hazards, dispute tables, 12-month simulated telemetry engine |
| `hydraulic_model.py` | Basin stress, flash-flood synthesizer, water-quality index, hazard clustering |
| `simulation_engines.py` | Monte-Carlo flood, reservoir routing, climate scenarios, water-share, treaty-dispute and hydropower-economics engines |
| `map_view.py` | All interactive maps (including per-park maps) |
| `network_view.py` | Schematic irrigation/hydropower and confluence networks |
| `input_driven.py` | Editable socio/agro dataset + Bar/Pie/Scatter/Line chart builder |
| `agro_economic.py`, `socio_economic.py` | Domain content (Rabi/Kharif, apiculture, aquaculture, etc.) |
| `geopolitics.py`, `china_hydropower.py` | IWT/PCA/Neutral Expert, Indian projects, Punjab-Sindh, China hydropower |
| `forests_parks.py` | Forest types, notable forests, national and urban parks |
| `sdg_agenda.py` | SDG / MDG / Vision alignment |
| `sources.py` | References and credit |
| `test_suite.py` | Unit tests |

## Important caveats

- Coordinates are approximate and schematic. Network diagrams are not to scale.
- Weather and 12-month gauge telemetry are **simulated**, not live data.
- Default socio/agro values, hydropower capex and capacity factors are **illustrative placeholders**.
- Entries marked "verify" (some forest areas, park details) could not be confirmed.
- 2026 items (PCA 31 Aug 2026 order, Neutral Expert calendar, Ministry clarification) came from the project brief; check them against the Sources tab.
- The "Indian Atrocities" tab presents Pakistan's position and notes India's stated position.
