"""coordinates.py - geographic reference data (lat, lon in decimal degrees).

All coordinates are APPROXIMATE (+/- a few km, some more) and intended for
schematic / educational mapping, not for survey or engineering use.
Entries marked conf="approx" should be verified against an official source.
"""

PAKISTAN_CENTER = (30.4, 69.4)

PROVINCES = {
    "Gilgit-Baltistan": {"lat": 35.80, "lon": 74.50, "capital": "Gilgit", "color": "#4C78A8"},
    "Khyber Pakhtunkhwa": {"lat": 34.00, "lon": 71.50, "capital": "Peshawar", "color": "#54A24B"},
    "Punjab": {"lat": 31.00, "lon": 72.50, "capital": "Lahore", "color": "#F58518"},
    "Sindh": {"lat": 26.00, "lon": 68.60, "capital": "Karachi", "color": "#E45756"},
    "Balochistan": {"lat": 28.50, "lon": 65.50, "capital": "Quetta", "color": "#B279A2"},
    "Azad Jammu & Kashmir": {"lat": 33.90, "lon": 73.80, "capital": "Muzaffarabad", "color": "#72B7B2"},
    "Islamabad Capital Territory": {"lat": 33.68, "lon": 73.05, "capital": "Islamabad", "color": "#9D755D"},
}

# Rivers: ordered upstream -> downstream (schematic polylines)
RIVERS = {
    "Indus": [(35.30, 75.63), (35.65, 74.63), (35.53, 73.80), (34.09, 72.69), (33.91, 72.25),
              (32.96, 71.55), (32.43, 71.37), (30.51, 70.85), (28.95, 70.37), (28.42, 69.71),
              (27.69, 68.86), (25.37, 68.31), (24.00, 67.40)],
    "Kabul": [(34.50, 70.40), (34.15, 71.30), (33.91, 72.25)],
    "Gilgit": [(36.60, 73.60), (35.92, 74.31), (35.72, 74.62)],
    "Jhelum": [(34.10, 74.80), (33.90, 73.75), (33.15, 73.64), (32.68, 73.52), (31.15, 72.15)],
    "Chenab": [(32.90, 75.20), (32.67, 74.46), (32.40, 73.98), (32.33, 73.69), (31.15, 72.15), (29.35, 71.02)],
    "Ravi": [(32.60, 75.40), (31.22, 73.87), (30.80, 72.00), (30.00, 71.40)],
    "Sutlej": [(31.00, 74.60), (30.38, 73.85), (29.83, 72.55), (29.35, 71.02)],
    "Panjnad": [(29.35, 71.02), (28.95, 70.37)],
}

# kind: barrage | dam | headwork
STRUCTURES = {
    "Tarbela Dam": {"lat": 34.09, "lon": 72.69, "kind": "dam", "river": "Indus", "province": "Khyber Pakhtunkhwa"},
    "Mangla Dam": {"lat": 33.15, "lon": 73.64, "kind": "dam", "river": "Jhelum", "province": "Azad Jammu & Kashmir"},
    "Warsak Dam": {"lat": 34.15, "lon": 71.30, "kind": "dam", "river": "Kabul", "province": "Khyber Pakhtunkhwa"},
    "Diamer-Bhasha Dam (under construction)": {"lat": 35.53, "lon": 73.80, "kind": "dam", "river": "Indus", "province": "Gilgit-Baltistan"},
    "Dasu HPP (under construction)": {"lat": 35.29, "lon": 73.20, "kind": "dam", "river": "Indus", "province": "Khyber Pakhtunkhwa"},
    "Rawal Dam": {"lat": 33.70, "lon": 73.12, "kind": "dam", "river": "Korang", "province": "Islamabad Capital Territory"},
    "Jinnah Barrage": {"lat": 32.92, "lon": 71.52, "kind": "barrage", "river": "Indus", "province": "Punjab"},
    "Chashma Barrage": {"lat": 32.43, "lon": 71.37, "kind": "barrage", "river": "Indus", "province": "Punjab"},
    "Taunsa Barrage": {"lat": 30.51, "lon": 70.85, "kind": "barrage", "river": "Indus", "province": "Punjab"},
    "Guddu Barrage": {"lat": 28.42, "lon": 69.71, "kind": "barrage", "river": "Indus", "province": "Sindh"},
    "Sukkur Barrage": {"lat": 27.68, "lon": 68.84, "kind": "barrage", "river": "Indus", "province": "Sindh"},
    "Kotri Barrage": {"lat": 25.43, "lon": 68.31, "kind": "barrage", "river": "Indus", "province": "Sindh"},
    "Marala Headworks": {"lat": 32.67, "lon": 74.46, "kind": "headwork", "river": "Chenab", "province": "Punjab"},
    "Khanki Headworks": {"lat": 32.40, "lon": 73.98, "kind": "headwork", "river": "Chenab", "province": "Punjab"},
    "Qadirabad Barrage": {"lat": 32.33, "lon": 73.69, "kind": "barrage", "river": "Chenab", "province": "Punjab"},
    "Trimmu Barrage": {"lat": 31.15, "lon": 72.15, "kind": "barrage", "river": "Chenab", "province": "Punjab"},
    "Panjnad Headworks": {"lat": 29.35, "lon": 71.02, "kind": "headwork", "river": "Panjnad", "province": "Punjab"},
    "Rasul Barrage": {"lat": 32.68, "lon": 73.52, "kind": "barrage", "river": "Jhelum", "province": "Punjab"},
    "Balloki Headworks": {"lat": 31.22, "lon": 73.87, "kind": "headwork", "river": "Ravi", "province": "Punjab"},
    "Sidhnai Barrage": {"lat": 30.55, "lon": 72.00, "kind": "barrage", "river": "Ravi", "province": "Punjab"},
    "Sulemanki Headworks": {"lat": 30.38, "lon": 73.85, "kind": "headwork", "river": "Sutlej", "province": "Punjab"},
    "Islam Headworks": {"lat": 29.83, "lon": 72.55, "kind": "headwork", "river": "Sutlej", "province": "Punjab"},
}

# Link canals: (from_structure, to_structure)
LINK_CANALS = {
    "Upper Jhelum Canal": ("Mangla Dam", "Rasul Barrage"),
    "Marala-Ravi (MR) Link": ("Marala Headworks", "Balloki Headworks"),
    "Rasul-Qadirabad (RQ) Link": ("Rasul Barrage", "Qadirabad Barrage"),
    "Qadirabad-Balloki (QB) Link": ("Qadirabad Barrage", "Balloki Headworks"),
    "Trimmu-Sidhnai (TS) Link": ("Trimmu Barrage", "Sidhnai Barrage"),
    "Balloki-Sulemanki (BS) Link": ("Balloki Headworks", "Sulemanki Headworks"),
    "Chashma-Jhelum (CJ) Link": ("Chashma Barrage", "Trimmu Barrage"),
    "Taunsa-Panjnad (TP) Link": ("Taunsa Barrage", "Panjnad Headworks"),
}

CONFLUENCES = {
    "Gilgit-Hunza / Gilgit-Indus (Jaglot)": (35.72, 74.62),
    "Kabul-Indus (Attock/Khairabad)": (33.91, 72.25),
    "Jhelum-Chenab (Trimmu)": (31.15, 72.15),
    "Ravi-Chenab (near Ahmadpur Sial, approx)": (30.95, 71.90),
    "Sutlej-Chenab = Panjnad (Uch, approx)": (29.35, 71.02),
    "Panjnad-Indus (Mithankot)": (28.95, 70.37),
}

# Mountain peaks
PEAKS = {
    "K2": {"lat": 35.8825, "lon": 76.5133, "m": 8611, "range": "Karakoram"},
    "Gasherbrum I": {"lat": 35.7244, "lon": 76.6962, "m": 8080, "range": "Karakoram"},
    "Broad Peak": {"lat": 35.8111, "lon": 76.5656, "m": 8051, "range": "Karakoram"},
    "Gasherbrum II": {"lat": 35.7580, "lon": 76.6530, "m": 8035, "range": "Karakoram"},
    "Nanga Parbat": {"lat": 35.2375, "lon": 74.5892, "m": 8126, "range": "Himalaya"},
    "Rakaposhi": {"lat": 36.1430, "lon": 74.4890, "m": 7788, "range": "Karakoram"},
    "Tirich Mir": {"lat": 36.2553, "lon": 71.8428, "m": 7708, "range": "Hindu Kush"},
    "Buni Zom": {"lat": 36.2000, "lon": 72.2800, "m": 6551, "range": "Hindu Raj"},
    "Sakesar": {"lat": 32.5200, "lon": 72.0200, "m": 1522, "range": "Salt Range"},
}

# Lakes (approx)
LAKES = {
    "Saif-ul-Malook": {"lat": 34.88, "lon": 73.69, "province": "Khyber Pakhtunkhwa"},
    "Lulusar Lake": {"lat": 35.00, "lon": 73.95, "province": "Khyber Pakhtunkhwa"},
    "Satpara Lake": {"lat": 35.20, "lon": 75.60, "province": "Gilgit-Baltistan"},
    "Sheosar Lake (Deosai)": {"lat": 35.03, "lon": 75.40, "province": "Gilgit-Baltistan"},
    "Attabad Lake": {"lat": 36.31, "lon": 74.82, "province": "Gilgit-Baltistan"},
    "Manchar Lake": {"lat": 26.40, "lon": 67.65, "province": "Sindh"},
    "Keenjhar Lake": {"lat": 24.95, "lon": 68.05, "province": "Sindh"},
    "Haleji Lake": {"lat": 24.80, "lon": 67.77, "province": "Sindh"},
    "Hanna Lake": {"lat": 30.25, "lon": 67.12, "province": "Balochistan"},
    "Rawal Lake": {"lat": 33.70, "lon": 73.12, "province": "Islamabad Capital Territory"},
    "Mangla Lake": {"lat": 33.15, "lon": 73.64, "province": "Azad Jammu & Kashmir"},
    "Tarbela Reservoir": {"lat": 34.09, "lon": 72.69, "province": "Khyber Pakhtunkhwa"},
    "Kallar Kahar Lake": {"lat": 32.78, "lon": 72.70, "province": "Punjab"},
}

# Climatic regions: coarse schematic polygons [(lat, lon), ...]
CLIMATE_REGIONS = {
    "Polar / glacial (Karakoram high ice)": {
        "color": "#9ecae1",
        "poly": [(36.9, 75.0), (36.9, 77.0), (35.4, 77.0), (35.4, 75.0)]},
    "Highland": {
        "color": "#8c6d31",
        "poly": [(37.0, 71.5), (37.0, 75.0), (35.4, 75.0), (35.4, 77.0), (34.8, 76.0),
                 (34.8, 72.0), (35.8, 71.0)]},
    "Temperate": {
        "color": "#74c476",
        "poly": [(34.8, 72.0), (34.8, 74.5), (33.5, 74.2), (33.2, 72.5), (33.9, 71.2)]},
    "Tropical / sub-tropical (monsoonal plains)": {
        "color": "#fd8d3c",
        "poly": [(33.0, 71.0), (33.0, 74.5), (30.5, 75.0), (28.0, 72.0), (25.0, 70.0), (24.2, 68.0),
                 (25.5, 67.2), (27.5, 68.0), (30.0, 69.5)]},
    "Arid / hyper-arid": {
        "color": "#e6c36a",
        "poly": [(32.0, 66.0), (30.0, 69.5), (27.5, 68.0), (25.5, 67.2), (25.1, 62.5),
                 (27.0, 62.5), (29.5, 61.0), (30.5, 63.5)]},
}

MOUNTAIN_RANGES = {
    "Karakoram": (36.0, 76.0), "Himalayas": (34.8, 74.8), "Hindu Kush": (36.3, 71.8),
    "Hindu Raj": (36.3, 72.6), "Spin Ghar (Koh-e-Safed)": (33.9, 70.0),
    "Sulaiman Mountains": (30.5, 70.0), "Kirthar Range": (26.5, 67.2),
    "Toba Kakar Range": (31.2, 67.9), "Salt Range": (32.7, 72.4),
}

# Dams / hydropower for hydro-politics maps
CHINA_HYDRO = {
    "Karot HPP (720 MW)": {"lat": 33.0, "lon": 73.5, "mw": 720, "river": "Jhelum", "province": "Punjab / AJK border"},
    "Suki Kinari HPP (884 MW)": {"lat": 34.95, "lon": 73.40, "mw": 884, "river": "Kunhar", "province": "Khyber Pakhtunkhwa"},
    "Kohala HPP (1,124 MW, proposed)": {"lat": 34.10, "lon": 73.50, "mw": 1124, "river": "Jhelum", "province": "Azad Jammu & Kashmir"},
    "Azad Pattan HPP (700.7 MW, proposed)": {"lat": 33.70, "lon": 73.60, "mw": 700.7, "river": "Jhelum", "province": "Azad Jammu & Kashmir"},
}

# Indian-administered Kashmir / Jammu projects (location approx) for IWT dispute maps
INDIAN_PROJECTS = {
    "Pakal Dul (1,000 MW)": {"lat": 33.45, "lon": 75.75, "mw": 1000, "river": "Marusudar (Chenab)"},
    "Ratle (850 MW)": {"lat": 33.17, "lon": 75.32, "mw": 850, "river": "Chenab"},
    "Kiru (624 MW)": {"lat": 33.20, "lon": 75.80, "mw": 624, "river": "Chenab"},
    "Kwar (540 MW)": {"lat": 33.22, "lon": 75.77, "mw": 540, "river": "Chenab"},
    "Kishanganga (330 MW)": {"lat": 34.60, "lon": 74.80, "mw": 330, "river": "Kishanganga/Neelum"},
    "Baglihar (900 MW)": {"lat": 33.17, "lon": 75.10, "mw": 900, "river": "Chenab"},
    "Salal (690 MW)": {"lat": 33.10, "lon": 74.80, "mw": 690, "river": "Chenab"},
}

FORESTS = {
    "Changa Manga": (31.08, 73.95), "Ziarat Juniper": (30.38, 67.73), "Ushu": (35.57, 72.62),
    "Dir": (35.20, 71.88), "Soon Valley": (32.55, 72.00), "Mukshpuri": (34.00, 73.38),
    "Rama Meadows": (35.30, 74.80), "Kalam": (35.49, 72.58), "Chitral": (35.85, 71.78),
    "Margalla Hills": (33.74, 73.05),
}

PARKS = {
    "Ayub National Park": (33.62, 73.07), "Jallo Park, Lahore": (31.61, 74.47),
    "Lulusar-Dudipatsar National Park": (35.00, 73.95), "Lal Suhanra National Park": (29.42, 71.98),
    "Kirthar National Park": (26.00, 67.50), "Khunjerab National Park": (36.60, 75.20),
    "City Park Multan": (30.20, 71.47), "Kashmir Park, DHA Multan": (30.18, 71.52),
    "Chitral Gol National Park": (35.90, 71.75), "Chaman Zar-e-Askari Park, Multan": (30.19, 71.50),
    "Jinnah Park": (33.60, 73.05), "Hingol National Park": (25.50, 65.50),
    "Shakarparian National Park": (33.69, 73.08), "Faisal Park, Mumtazabad": (30.25, 71.45),
    "Pir Lasura National Park": (33.00, 73.00), "Hazarganji-Chiltan National Park": (30.00, 66.90),
    "Pakistan Park": (33.69, 73.07), "Machiara National Park": (34.40, 73.55),
    "Rajana Forest Bhagat Wildlife Park": (30.87, 72.32), "Margalla Hills National Park": (33.75, 73.05),
}
