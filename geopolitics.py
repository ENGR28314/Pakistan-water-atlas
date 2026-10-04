"""geopolitics.py - Geo-Political & Strategic Domain content.

Content for 2026 items (PCA August 2026 order, Neutral Expert calendar, Ministry clarification)
was SUPPLIED IN THE PROJECT BRIEF and is beyond the author's independent verification.
Check the Sources tab links before relying on any date or figure. India disputes the Court of
Arbitration's competence and has held the IWT 'in abeyance' since April 2025; both positions are shown.
"""
import pandas as pd

HYDRO_POLITICS_KASHMIR = (
    "The Indus system's three western rivers (Indus, Jhelum, Chenab) flow from Indian-administered Jammu & Kashmir "
    "or through it into Pakistan. Under the 1960 Indus Waters Treaty (IWT), the western rivers were allocated to Pakistan "
    "with limited Indian rights (run-of-river hydropower, restricted storage); the eastern rivers (Ravi, Beas, Sutlej) went to India.")

IWT_CRISIS = [
    "April 2025: India announced the IWT would be held in abeyance; Pakistan rejects unilateral suspension as not provided for in the treaty.",
    "Pakistan relies on Court of Arbitration (PCA) proceedings and the Neutral Expert process under the treaty's dispute mechanisms.",
    "India's position: the Court of Arbitration is 'illegally constituted' and it does not recognise its rulings.",
    "Risk for lower riparian Pakistan: data-sharing, flood warnings and flow regulation at Marala and other headworks.",
]
MARITIME = ("Maritime trade infrastructure: Karachi Port, Port Qasim and Gwadar handle most of Pakistan's seaborne trade; Indus Delta health, "
            "freshwater flows below Kotri and sea intrusion link water policy to port and coastal resilience.")

PCA_TIMELINE = pd.DataFrame([
    {"date": "2016", "event": "Pakistan requests a Court of Arbitration over Kishanganga/Ratle designs; India seeks a Neutral Expert."},
    {"date": "2022", "event": "World Bank appoints both a Neutral Expert (Michel Lino) and Court of Arbitration members (parallel processes)."},
    {"date": "Jun 2025", "event": "PCA issues a Supplemental Award on Competence (see Sources)."},
    {"date": "31 Aug 2026", "event": "Interim enforcement order reported: concrete freeze on Ratle dam wall and power intake above specified elevations (per project brief)."},
    {"date": "Nov 2026", "event": "Neutral Expert: Synthesis Memorandum distributed."},
    {"date": "Feb 2027", "event": "Neutral Expert: 7th meeting & final hydraulic modelling exercise."},
    {"date": "Mar 2027", "event": "Neutral Expert: Draft Technical Decision circulated."},
    {"date": "Jul 2027", "event": "Neutral Expert: final binding determination expected."},
    {"date": "~Oct 2027", "event": "Freeze runs until 90 days after the Neutral Expert's final decision (per project brief)."},
])

COA_VALIDITY = (
    "Validity of the Court of Arbitration: Pakistan actively participates in the PCA process. It argues the Court is a legally sound "
    "dispute-resolution body properly constituted under Article IX of the IWT.")

INTER_BASIN_TRANSFER = (
    "India proposes inter-basin water transfers: feasibility studies are to begin immediately for a 113 km canal redirecting surplus "
    "Indus-system flows to Punjab, Haryana and Rajasthan.")

# ----- Tab: "Indian atrocities" (title as requested). Content is attributed, Pakistan-position framing.
INDIAN_ACTIONS_1A = [
    "Two new canal systems are proposed in India.",
    "A canal linking the Chenab with the Ravi-Beas-Sutlej would enable full use of the eastern rivers and help India use its entire allocated share of the western rivers under the IWT.",
    "The project is proposed to be completed in three years.",
]
INDIAN_ACTIONS_1B = [
    "A Ravi-Beas link is proposed to tap water flowing beyond treaty limits into Pakistan.",
    "Expediting under-construction hydropower: Pakal Dul (1,000 MW), Ratle (850 MW), Kiru (624 MW) and Kwar (540 MW) to utilise Indus-system waters.",
    "Substantive limits on water control: Pakistan asserts that Kishanganga and Ratle designs exceed run-of-river permissions via excessive pondage, giving structural capacity to manipulate flows.",
    "Enforcement of interim measures: Pakistan maintains India must comply with court-ordered temporary restrictions at Ratle while a parallel technical review proceeds.",
]
DISPUTED_SPECS = [
    ("🌊 Pondage Capacity (Live Storage)",
     "Pondage handles daily demand fluctuations. Kishanganga: India 7.5 MCM vs Pakistan 1 MCM. Ratle: India 24 MCM vs Pakistan 8 MCM. "
     "Concern: ability to store water in sowing seasons or release sudden surges (man-made drought or flood)."),
    ("📐 Orifice Spillways & Gate Placements",
     "India uses deep, low-level gated orifice spillways to flush silt. Pakistan asks for higher, ungated or minimal spillways; at Ratle, raised by 20 m. "
     "Concern: low-level gates can drain a reservoir quickly."),
    ("🔌 Intake Submergence Levels",
     "Pakistan asks to raise intakes by 1.4 m (Kishanganga) and up to 8.8 m (Ratle). Concern: deep intakes allow generation and draw at very low reservoir levels."),
    ("🧗 Freeboard Heights",
     "Ratle: India 2 m freeboard vs Pakistan 1 m. Concern: inflated freeboard could hide extra storage capacity."),
]
INDIA_POSITION_NOTE = (
    "India's stated position: the Court of Arbitration is illegally constituted and its rulings are not recognised; India says its projects comply with "
    "the IWT's run-of-river provisions and its Environment Ministry reportedly extended the Ratle environmental clearance to 2030 (per project brief).")
RUNTIME_RISK = [
    "Concrete freeze: no concrete on Ratle's dam wall and power intake above specified elevations until 90 days after the Neutral Expert's decision.",
    "Engineering risk: if the Neutral Expert rules against India's pondage/spillway design, poured concrete may need costly modification.",
    "India's defiance: New Delhi has publicly dismissed the freeze and continues construction on its domestic timeline.",
]

PAKAL_DUL_RATLE = pd.DataFrame([
    {"issue": "Pondage capacity", "pakistan_view": "Excess pondage exceeds run-of-river allowances; structural control of flows."},
    {"issue": "Freeboard & dam elevation", "pakistan_view": "Freeboard should be minimal (hydro-meteorologically justified); excess hides storage."},
    {"issue": "Deep-level outlets & gated spillways", "pakistan_view": "Low-level outlets enable full drawdown; spillways should be higher/ungated."},
    {"issue": "Court of Arbitration interventions", "pakistan_view": "Interim enforcement should bind construction while technical review proceeds."},
])

# ----- Internal disputes
CHENAB_IMPACT = {
    "Flow reductions at Head Marala": "Pakistan reports concern about reduced/irregular Chenab flows at Head Marala, especially in sowing seasons.",
    "Devastating crop impacts": "Late or reduced canal supplies affect wheat (Rabi) and rice/cotton (Kharif) in central Punjab.",
}
DIAMER_BHASHA = {
    "Joint engineering and progress": "Diamer-Bhasha Dam on the Indus (Gilgit-Baltistan/KP boundary) is a major WAPDA storage and hydropower project with Chinese-linked contractors and Pakistani partners.",
    "Strategic storage and economic injection": "Planned live storage of roughly 6.4 MAF to supplement Tarbela and regulate flows; construction creates jobs and local spending.",
    "The power postponement": "Power generation timelines have been revised/postponed; see WAPDA and the Ministry of Economic Affairs clarification in Sources.",
}
PUNJAB_SINDH = {
    "Sindh's grievances (lower riparian)": "Reduced downstream flows below Kotri, delta degradation, sea intrusion, perceived unfair apportionment, objection to new canals.",
    "Punjab's counter-claims (upper riparian)": "Existing apportionment (1991 Accord), need for flood storage and agriculture, accusations of overstated Sindh shares.",
    "Structural gridlock / deadlock": "Provincial vetoes and mistrust stall projects (e.g. Kalabagh, Cholistan canals).",
}
IRSA_LEGAL = [
    ("IRSA technocratic vote deadlock", "IRSA's provincial members vote on allocations; ties/dissents block decisions."),
    ("Council of Common Interests (CCI) appeal", "A province may appeal an IRSA decision to the CCI under Article 155 of the Constitution."),
    ("Constitutional review (Supreme Court)", "Final disputes may reach the Supreme Court."),
    ("The 2024-2026 restructuring crisis", "Debate over IRSA's structure, canal proposals and representation (verify current status)."),
    ("The veto power and conciliation", "Consensus-based CCI decisions create de facto provincial veto power."),
    ("Judicial intervention", "Courts have been asked to resolve water-sharing and project disputes."),
]
