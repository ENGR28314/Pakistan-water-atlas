"""forests_parks.py - forest types, notable forests and national / urban parks.

Areas are approximate and sources differ; entries marked 'verify' have uncertain
figures or locations and should be checked against provincial forest / wildlife departments.
"""
import pandas as pd
import coordinates as C

FOREST_TYPES = pd.DataFrame([
    {"type": "Coniferous forests", "where": "Northern mountains, ~1,000-4,000 m (KP, Gilgit-Baltistan, AJK)",
     "species": "Pine, fir, spruce, deodar", "role": "Watershed protection, timber, carbon storage"},
    {"type": "Mangrove forests", "where": "Indus Delta, Karachi coast and Balochistan coast (Arabian Sea)",
     "species": "Avicennia marina (dominant), Rhizophora, Ceriops", "role": "Storm-surge buffer, fisheries nursery, blue carbon"},
    {"type": "Riverain (Bela) forests", "where": "Narrow strips along the Indus and other river banks",
     "species": "Shisham, babul, tamarisk, poplar", "role": "Bank stabilisation, fuelwood, floodplain habitat"},
    {"type": "Tropical thorn (scrub) forests", "where": "Low plains and semi-arid flatlands of Punjab and Sindh",
     "species": "Acacia, prosopis, jand, ber, phulai", "role": "Fodder, fuelwood, desertification control"},
    {"type": "Irrigated / planted forests", "where": "Canal-irrigated plantations, e.g. Changa Manga near Lahore",
     "species": "Shisham, mulberry, eucalyptus, poplar", "role": "Timber supply, recreation, microclimate"},
])

NOTABLE_FORESTS = pd.DataFrame([
    {"forest": "Changa Manga", "province": "Punjab", "type": "Irrigated / planted", "area": "~12,000 acres (approx.)",
     "history": "Planted in the 1860s during British rule to supply timber/fuel for railways; one of the largest hand-planted forests.",
     "wildlife": "Birds, nilgai/deer in places, reptiles; plantation fauna.", "attractions": "Forest park, mini train, boating, picnic spots."},
    {"forest": "Ziarat Juniper Forest", "province": "Balochistan", "type": "Coniferous (juniper)", "area": "~100,000+ ha (sources vary)",
     "history": "Ancient juniper stands, some trees reported to be thousands of years old; UNESCO Biosphere Reserve area.",
     "wildlife": "Markhor, black bear, wolves, migratory birds.", "attractions": "Ziarat Residency (Quaid's last residence), Sandeman hills, hiking."},
    {"forest": "Ushu Forest", "province": "Khyber Pakhtunkhwa (Swat Kohistan)", "type": "Coniferous", "area": "verify",
     "history": "Part of the Ushu valley's old-growth conifer belt above Kalam.", "wildlife": "Himalayan ibex and brown bear in higher reaches (reported), birds.",
     "attractions": "Ushu Valley, Mahodand Lake road, trekking."},
    {"forest": "Dir Forest", "province": "Khyber Pakhtunkhwa", "type": "Coniferous", "area": "verify",
     "history": "Dir Kohistan forests have long supplied timber; subject to logging pressure.", "wildlife": "Musk deer, leopard (reported), pheasants.",
     "attractions": "Kumrat Valley, Jahaz Banda, Shahi Masjid area."},
    {"forest": "Soon Valley Forest", "province": "Punjab (Khushab)", "type": "Tropical thorn / dry subtropical", "area": "verify",
     "history": "Salt Range valley with scrub forest of phulai, wild olive.", "wildlife": "Urial, chinkara, partridges, migratory birds.",
     "attractions": "Uchhali, Khabeki and Jahlar lakes, Neela Wahn, Sakesar."},
    {"forest": "Mukshpuri Forest", "province": "Punjab / KP (Galiyat)", "type": "Coniferous (blue pine, fir)", "area": "verify",
     "history": "Galiyat forests managed as reserved forests since the colonial period.", "wildlife": "Leopard (reported), Kalij pheasant, langur.",
     "attractions": "Mukshpuri Top hike, Nathia Gali, Ayubia."},
    {"forest": "Rama Meadows Forest", "province": "Gilgit-Baltistan (Astore)", "type": "Coniferous & alpine", "area": "verify",
     "history": "Alpine pasture on the approach to Nanga Parbat.", "wildlife": "Himalayan ibex, snow leopard (rare), marmots.",
     "attractions": "Rama Lake, Rama Meadows camping, Nanga Parbat views."},
    {"forest": "Kalam Forest", "province": "Khyber Pakhtunkhwa (Swat)", "type": "Coniferous", "area": "verify",
     "history": "Deodar, pine and fir stands around the Swat River headwaters.", "wildlife": "Birds, small mammals; ibex in higher areas.",
     "attractions": "Mahodand Lake, Kalam bazaar, Ushu Valley."},
    {"forest": "Chitral Forests", "province": "Khyber Pakhtunkhwa", "type": "Coniferous / chilgoza pine", "area": "verify",
     "history": "Chilgoza pine, deodar and juniper woodlands in Hindu Kush valleys.", "wildlife": "Markhor, snow leopard, ibex (Chitral Gol).",
     "attractions": "Kalash valleys, Chitral Gol, Shandur."},
    {"forest": "Margalla Hills Scrub Forests", "province": "Islamabad Capital Territory", "type": "Subtropical scrub / pine", "area": "17,386 ha (Margalla Hills NP)",
     "history": "Protected as a national park in 1980; periodic fire and encroachment pressure.", "wildlife": "Leopard, barking deer, jackal, rhesus monkey, many birds.",
     "attractions": "Trail 3/5, Monal, Daman-e-Koh, Pir Sohawa."},
])

# name -> details; coordinates are pulled from coordinates.PARKS
_P = [
    ("Ayub National Park", "Punjab (Rawalpindi)", "Urban national park", "approx. 1,000+ acres (verify)", "Old Rawalpindi park established in the 20th century.", "Birds, small mammals", "Lake, zoo, rides, jogging"),
    ("Jallo Park, Lahore", "Punjab (Lahore)", "Urban wildlife park", "verify", "Developed as a recreational forest park near the Lahore canal.", "Deer, waterfowl, introduced species", "Safari, boating, trails"),
    ("Lulusar-Dudipatsar National Park", "Khyber Pakhtunkhwa (Kaghan)", "Alpine national park", "~750 km2 (approx.)", "Established in 2003 to protect high-altitude lakes and ecosystems.", "Himalayan brown bear, snow leopard, ibex, golden marmot", "Lulusar Lake, Dudipatsar Lake, Babusar Pass"),
    ("Lal Suhanra National Park", "Punjab (Bahawalpur)", "Desert / riverine national park", "~1,250 km2 (approx.)", "Declared a Biosphere Reserve; spans desert, riverine and irrigated plantation zones.", "Blackbuck, chinkara, nilgai, desert birds", "Safari, Patisar Lake, Cholistan access"),
    ("Kirthar National Park", "Sindh", "Arid mountain national park", "~3,000 km2 (approx.)", "Established 1974 to protect Sindh ibex and urial.", "Sindh ibex, urial, chinkara, leopard (rare)", "Hiking, Ranikot, wildlife viewing"),
    ("Khunjerab National Park", "Gilgit-Baltistan", "High-altitude national park", "~2,270 km2 (approx.)", "Established 1975, partly to protect the Marco Polo sheep.", "Marco Polo sheep, snow leopard, ibex, brown bear", "Khunjerab Pass, KKH drive"),
    ("City Park Multan", "Punjab (Multan)", "Urban park", "verify", "Municipal recreational green space.", "Birds", "Walking, family recreation"),
    ("Kashmir Park, DHA Multan", "Punjab (Multan)", "Urban park", "verify", "Neighbourhood park in DHA Multan.", "Birds", "Walking, children's play"),
    ("Chitral Gol National Park", "Khyber Pakhtunkhwa", "Mountain national park", "~77 km2 (approx.)", "Established 1984, a key markhor conservation site.", "Markhor, snow leopard, ibex", "Wildlife viewing near Chitral town"),
    ("Chaman Zar-e-Askari Park, Multan", "Punjab (Multan)", "Urban park", "verify", "Cantonment recreational park.", "Birds", "Walking, family recreation"),
    ("Jinnah Park", "Punjab (Rawalpindi) - verify", "Urban park", "verify", "Urban public park named after the founder of Pakistan.", "Birds", "Walking, recreation"),
    ("Hingol National Park", "Balochistan", "Coastal / desert national park", "~1,650 km2 (approx.)", "Established 1988; Pakistan's largest national park by area (commonly cited).", "Sindh ibex, urial, marsh crocodile, Indus dolphins (nearby)", "Princess of Hope rock, Hinglaj, mud volcanoes"),
    ("Shakarparian National Park", "Islamabad Capital Territory", "Urban national park", "verify", "Hill park with national monument.", "Birds", "Pakistan Monument, Lok Virsa, viewpoints"),
    ("Faisal Park, Mumtazabad", "Punjab (Multan) - verify", "Urban park", "verify", "Urban recreational park.", "Birds", "Walking, recreation"),
    ("Pir Lasura National Park", "verify (Punjab / AJK)", "National park", "verify", "Listed among Pakistan's national parks; verify province and status.", "verify", "verify"),
    ("Hazarganji-Chiltan National Park", "Balochistan (near Quetta)", "Mountain national park", "~275 km2 (approx.)", "Established 1980 for markhor conservation.", "Chiltan markhor, urial, chinkara", "Hiking near Quetta"),
    ("Pakistan Park", "verify", "Park", "verify", "Name is ambiguous in public sources; verify which park is meant.", "verify", "verify"),
    ("Machiara National Park", "Azad Jammu & Kashmir", "Mountain national park", "~135 km2 (approx.)", "Established 1996 near Muzaffarabad.", "Himalayan musk deer, black bear, leopard, monal pheasant", "Alpine forest trails"),
    ("Rajana Forest Bhagat Wildlife Park", "Punjab (Toba Tek Singh) - verify", "Wildlife park", "verify", "Punjab wildlife/forest recreation area (verify details).", "verify", "verify"),
    ("Margalla Hills National Park", "Islamabad Capital Territory", "Mountain national park", "17,386 ha", "Established 1980.", "Leopard, barking deer, jackal, rhesus monkey, many birds", "Hiking trails, Monal, Daman-e-Koh"),
]
NATIONAL_PARKS = pd.DataFrame(
    [{"park": n, "province": p, "category": c, "area": a, "history": h, "wildlife": w, "attractions": at,
      "lat": C.PARKS[n][0], "lon": C.PARKS[n][1], "coords": "approx."} for (n, p, c, a, h, w, at) in _P])
