"""agro_economic.py - Agro-Economic Domain content."""
import pandas as pd

OVERVIEW = {
    "World's largest contiguous irrigation (IBIS)": "The Indus Basin Irrigation System: 3 major storage reservoirs, 19 barrages/headworks, 12 inter-river link canals and 45 canal commands (figures per WAPDA/IRSA summaries; verify current counts), irrigating roughly 16+ million ha.",
    "Crop cultivation": "Wheat, rice, cotton, sugarcane and maize dominate; Punjab and Sindh produce the bulk of output.",
    "Rural livelihoods": "Agriculture employs roughly 35-40% of the labour force (PBS Labour Force Survey ranges).",
    "GDP & employment contribution": "Agriculture contributes roughly a fifth of GDP (Economic Survey of Pakistan, recent years).",
}

RABI = pd.DataFrame([
    {"season": "Rabi", "crop": "Wheat", "typical_window": "Sow Oct-Dec; harvest Mar-May", "engineering_water_note": "3-5 canal irrigations; sensitive to late-winter canal closures and tail-end shortages."},
    {"season": "Rabi", "crop": "Barley", "typical_window": "Sow Oct-Nov; harvest Mar-Apr", "engineering_water_note": "Low water demand; suited to marginal/rainfed land."},
    {"season": "Rabi", "crop": "Gram (chickpea)", "typical_window": "Sow Oct-Nov; harvest Mar-Apr", "engineering_water_note": "Mostly rainfed (Thal, Potohar); drought-sensitive."},
    {"season": "Rabi", "crop": "Rapeseed-mustard / canola", "typical_window": "Sow Sep-Nov; harvest Mar-Apr", "engineering_water_note": "1-3 irrigations; efficient oilseed for water-limited areas."},
    {"season": "Rabi", "crop": "Lentil", "typical_window": "Sow Oct-Nov; harvest Mar-Apr", "engineering_water_note": "Limited irrigation; residual moisture."},
    {"season": "Rabi", "crop": "Potato (autumn/spring)", "typical_window": "Sow Sep-Feb; harvest Dec-Jun", "engineering_water_note": "Frequent light irrigations; drip/furrow management matters."},
])

KHARIF = pd.DataFrame([
    {"season": "Kharif", "crop": "Rice (basmati / IRRI)", "typical_window": "Nursery May-Jun; transplant Jun-Jul; harvest Oct-Nov", "engineering_water_note": "Highest water demand (flooded paddy); drives groundwater pumping; DSR/AWD can save water."},
    {"season": "Kharif", "crop": "Cotton", "typical_window": "Sow Apr-Jun; pick Sep-Dec", "engineering_water_note": "Canal + tubewell; heat and pest stress; delayed canal supplies hurt sowing."},
    {"season": "Kharif", "crop": "Sugarcane", "typical_window": "Plant Feb-Mar / Sep-Oct; 10-14 month crop", "engineering_water_note": "Very high consumptive use; major pressure on Sindh/Punjab canal supplies."},
    {"season": "Kharif", "crop": "Maize (autumn/spring)", "typical_window": "Sow Jul-Aug (autumn) / Feb (spring)", "engineering_water_note": "Moderate demand; expanding in KP and Punjab."},
    {"season": "Kharif", "crop": "Sorghum / millets", "typical_window": "Sow Jun-Jul; harvest Oct-Nov", "engineering_water_note": "Drought-tolerant; suited to Thar/Cholistan and rod-kohi areas."},
    {"season": "Kharif", "crop": "Mung bean / mash", "typical_window": "Sow Jul-Aug; harvest Oct-Nov", "engineering_water_note": "Short-duration, low irrigation requirement."},
    {"season": "Kharif", "crop": "Sesame", "typical_window": "Sow Jun-Jul; harvest Oct", "engineering_water_note": "Low-input, rainfed-friendly."},
])

SEASONS = pd.DataFrame([
    {"season": "Kharif", "months": "Apr-Sep (monsoon / summer)", "water_source": "River flows peak (snowmelt + monsoon); canals at full supply"},
    {"season": "Rabi", "months": "Oct-Mar (winter)", "water_source": "Low river flows; reservoir releases + groundwater matter most"},
])

APICULTURE = pd.DataFrame([
    {"indicator": "Managed beehives", "unit": "number", "description": "Count of managed colonies (Apis mellifera and Apis cerana) in a region."},
    {"indicator": "Honey yield per hive", "unit": "kg/hive/year", "description": "Average harvest, depends on flora (sidr/ber, phulai, acacia, mustard, citrus, wild flora)."},
    {"indicator": "Honey production", "unit": "tonnes", "description": "Total annual honey output."},
    {"indicator": "Beekeepers employed", "unit": "persons", "description": "Households with beekeeping as primary or secondary income."},
    {"indicator": "Pollination service benefit", "unit": "PKR million (est.)", "description": "Yield uplift in oilseeds, orchards and vegetables due to managed pollination."},
    {"indicator": "Migratory movement", "unit": "colonies moved/season", "description": "Seasonal movement of hives between plains and hills to follow flowering."},
])

AQUACULTURE = pd.DataFrame([
    {"indicator": "Pond area", "unit": "hectares", "description": "Area under freshwater or brackish aquaculture ponds."},
    {"indicator": "Aquaculture production", "unit": "tonnes", "description": "Farmed fish/shrimp output (rohu, catla, mrigal, tilapia, pangasius, trout in the north)."},
    {"indicator": "Stocking density", "unit": "fish/ha", "description": "Polyculture density; drives feed and aeration needs."},
    {"indicator": "Feed conversion ratio (FCR)", "unit": "kg feed/kg gain", "description": "Efficiency indicator; lower is better."},
    {"indicator": "Water use intensity", "unit": "m3/tonne", "description": "Make-up water per tonne produced; relevant under Indus basin stress."},
    {"indicator": "Salinity tolerance zone", "unit": "dS/m", "description": "Suitable brackish-water culture in coastal Sindh/Balochistan; links to sea intrusion risk."},
    {"indicator": "Employment", "unit": "persons", "description": "Farm, hatchery, feed and processing workers."},
])
