"""Build processed CSVs for the China: Plan vs Reality project.

Every figure here was verified against a stated public source during the
Nov 2, 2026 research session. Sources are listed in data/raw/PROVENANCE.md.
Nothing in this script is estimated or invented. Where a figure was not
found, the field is left blank and the gap is documented, not filled.
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "data", "raw")
PROC = os.path.join(ROOT, "data", "processed")
os.makedirs(PROC, exist_ok=True)


def wb(name):
    with open(os.path.join(RAW, f"wb_{name}.json")) as f:
        return {r["year"]: r["value"] for r in json.load(f)}


def write_csv(path, header, rows):
    import csv
    with open(path, "w", newline="") as f:
        w = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
        w.writerow(header)
        for row in rows:
            w.writerow(["" if v is None else v for v in row])
    print("wrote", path, len(rows), "rows")


# ---------------------------------------------------------------- World Bank
series = {
    "gdp_usd": wb("gdp_current_usd"),
    "gdp_per_capita_usd": wb("gdp_per_capita_usd"),
    "gdp_growth_pct": wb("gdp_growth_pct"),
    "population": wb("population"),
    "urban_pct": wb("urban_pop_pct"),
    "life_expectancy": wb("life_expectancy"),
    "fertility": wb("fertility"),
    "poverty_215_pct": wb("poverty_215"),
    "exports_pct_gdp": wb("exports_pct_gdp"),
    "imports_pct_gdp": wb("imports_pct_gdp"),
    "energy_use_pc_kg_oil": wb("energy_use_per_capita"),
    "forest_pct": wb("forest_pct"),
    "r_and_d_pct_gdp": wb("r_and_d_pct_gdp"),
    "pop_65_pct": wb("pop_65_pct"),
    "pop_0_14_pct": wb("pop_0_14_pct"),
    "age_dependency": wb("age_dependency"),
}
years = sorted(set().union(*[set(s) for s in series.values()]))
rows = []
for y in years:
    rows.append([y] + [series[k].get(y) for k in series])
write_csv(os.path.join(PROC, "wb_longrun.csv"),
          ["year"] + list(series.keys()), rows)

# ---------------------------------------------------------------- Provinces
# GDP: Wikipedia "List of Chinese administrative divisions by GDP", citing
# NBS data. 2024 is revised, 2025 is preliminary, 2000 is the historical
# column of the same table. Units: million CNY.
# Population and urban population: NBS mid-year 2022 figures from Wikipedia
# "List of Chinese administrative divisions by population".
# Region: the six conventional regions used on that page.
provinces = [
    # name, region, gdp2024, gdp2025p, gdp2000, growth2025p, pop2022, urban2022
    ("Guangdong", "South Central", 14148890, 14584676, 1095840, 3.9, 127060000, 94650000),
    ("Jiangsu", "East", 13669690, 14235150, 863510, 5.3, 85150000, 63370000),
    ("Shandong", "East", 9840690, 10319750, 834850, 5.5, 101630000, 65590000),
    ("Zhejiang", "East", 9000700, 9454500, 621890, 5.5, 65770000, 48260000),
    ("Sichuan", "Southwest", 6453790, 6766534, 397560, 5.5, 83740000, 48860000),
    ("Henan", "South Central", 6355710, 6663279, 509730, 5.6, 101113000, 56330000),
    ("Hubei", "South Central", 5964430, 6266090, 357740, 5.5, 58440000, 37790000),
    ("Fujian", "East", 5747660, 6019945, 380460, 5.0, 41880000, 29370000),
    ("Shanghai", "East", 5375950, 5670871, 488000, 5.4, 24750000, 22110000),
    ("Hunan", "South Central", 5308470, 5530865, 359100, 4.8, 66040000, 39830000),
    ("Anhui", "East", 5064670, 5298900, 316230, 5.5, 61270000, 36860000),
    ("Beijing", "North", 4967020, 5207300, 332800, 5.4, 21840000, 19130000),
    ("Hebei", "North", 4744810, 4930520, 466370, 5.6, 74200000, 45750000),
    ("Shaanxi", "Northwest", 3543710, 3655110, 182330, 5.1, 39560000, 25320000),
    ("Jiangxi", "East", 3422790, 3602000, 202780, 5.2, 45280000, 28110000),
    ("Chongqing", "Southwest", 3204670, 3375793, 184140, 5.3, 32130000, 22800000),
    ("Liaoning", "Northeast", 3254080, 3318290, 470370, 3.7, 41970000, 30640000),
    ("Yunnan", "Southwest", 3142340, 3276578, 205230, 4.1, 46930000, 24270000),
    ("Guangxi", "South Central", 2869410, 2972745, 209670, 5.1, 50470000, 28090000),
    ("Inner Mongolia", "North", 2633700, 2671030, 155130, 4.7, 24010000, 16470000),
    ("Shanxi", "North", 2535350, 2549568, 186190, 4.0, 34810000, 22260000),
    ("Guizhou", "Southwest", 2264570, 2356217, 104040, 4.9, 38560000, 21140000),
    ("Xinjiang", "Northwest", 2049240, 2146200, 137410, 5.5, 25870000, 14980000),
    ("Tianjin", "North", 1793130, 1853982, 160840, 4.8, 13630000, 11600000),
    ("Heilongjiang", "Northeast", 1647810, 1687810, 288190, 4.2, 30990000, 20520000),
    ("Jilin", "Northeast", 1430500, 1497388, 176920, 5.0, 23480000, 14960000),
    ("Gansu", "Northwest", 1302050, 1369750, 106140, 5.8, 24920000, 13510000),
    ("Hainan", "South Central", 797270, 810885, 53200, 4.0, 10270000, 6310000),
    ("Ningxia", "Northwest", 552020, 569649, 29770, 5.3, 7280000, 4830000),
    ("Qinghai", "Northwest", 396550, 412184, 26660, 4.1, 5950000, 3660000),
    ("Tibet", "Southwest", 278910, 303189, 11890, 7.0, 3640000, 1360000),
]
rows = []
for name, region, g24, g25, g00, gr, pop, urb in provinces:
    share = round(g24 / 134806620 * 100, 2)
    pc = round(g24 * 1_000_000 / pop)  # CNY, approximate, see note
    urb_rate = round(urb / pop * 100, 1)
    mult = round(g24 / g00, 1)
    rows.append([name, region, g24, g25, g00, gr, share, pop, urb, urb_rate, pc, mult])
write_csv(os.path.join(PROC, "provinces.csv"),
          ["province", "region", "gdp_2024_m_cny", "gdp_2025p_m_cny",
           "gdp_2000_m_cny", "real_growth_2025p_pct", "share_of_national_2024_pct",
           "pop_mid2022", "urban_pop_mid2022", "urban_rate_2022_pct",
           "gdp_per_capita_2024_approx_cny", "gdp_multiple_2000_to_2024"], rows)

# ------------------------------------------------------- 14th plan scorecard
# Status words: met, missed, not yet reported. Year of actual is always shown.
# Sources are shortened here; full citations are in PROVENANCE.md.
scorecard = [
    # indicator, type, target, actual, actual_year, status, source, note
    ("Energy intensity (energy use per unit of GDP)", "binding", "-13.5%",
     "-15%", "2021-2025", "met", "iGDP tracker (Jan-Feb 2026 issue)",
     "NDRC reported minus 11.6 percent for 2021-2024 only."),
    ("Carbon intensity (CO2 per unit of GDP)", "binding", "-18%",
     "-12%", "2021-2025", "missed", "iGDP tracker (Jan-Feb 2026 issue)",
     "Goldman Sachs (Sep 2025) also expected a miss."),
    ("Good air quality days", "binding", "87.5%",
     "89.3%", "2025", "met", "Ministry of Ecology and Environment / NBS",
     "A record high, up 1.9 points on 2024."),
    ("Surface water at grade III or better", "binding", "85%",
     "91.4%", "2025", "met", "Ministry of Ecology and Environment / NBS",
     "Up 1 point on 2024."),
    ("Forest coverage", "binding", "24.1%",
     "over 25%", "2025", "met", "Government Work Report (Mar 5, 2026)",
     "Stated as past 25 percent, not an exact figure."),
    ("Grain production capacity", "binding", "over 650 million tons",
     "over 700 million tons", "2025", "met", "NBS 2025 Statistical Communique",
     "Actual is output, not capacity. Output topped 700 million tons for a second straight year."),
    ("Energy production capacity", "binding", "over 4.6 billion tons of coal equivalent",
     "5.13 billion tons", "2025", "met", "NBS 2025 Statistical Communique",
     "Actual is output, not capacity."),
    ("Average education, working-age population", "binding", "11.3 years",
     "", "", "not yet reported", "",
     "No 2025 actual figure was found in the sources checked for this build."),
    ("Urbanization rate (permanent residents)", "indicative", "65%",
     "67.89%", "2025", "met", "NBS 2025 Statistical Communique",
     "Up 0.89 points on 2024."),
    ("R and D spending growth", "indicative", "over 7% per year",
     "about 10% per year on average", "2021-2025", "met", "Government Work Report (Mar 5, 2026)",
     "2025 spending about 3.93 trillion yuan, up 8.2 percent, intensity 2.80 percent of GDP."),
    ("Core digital economy share of GDP", "indicative", "10% by 2025",
     "10.5%", "2024", "met", "NBS / MIIT reporting",
     "2025 figure not separately reported in sources found. Met ahead of schedule."),
    ("Non-fossil share of energy consumption", "indicative", "about 20%",
     "21.7%", "2025", "met", "iGDP tracker (Jan-Feb 2026 issue)",
     "Do not confuse with clean energy share of 30.4 percent, which also counts natural gas."),
    ("Surveyed urban unemployment", "indicative", "at or below 5.5%",
     "5.2% average", "2025", "met", "NBS 2025 Statistical Communique",
     "December 2025 was 5.1 percent."),
    ("New urban jobs created", "indicative", "over 55 million cumulative",
     "about 62.42 million", "2021-2025", "met", "NBS annual figures",
     "Annual: 12.69, 12.06, 12.44, 12.56, 12.67 million."),
    ("Life expectancy", "indicative", "plus 1 year (77.3 to 78.3 years)",
     "79.0 years", "2024", "met", "UBP table (Nov 2025)",
     "2025 figure not separately reported in sources found. Cross-check: the World Bank series puts 2024 at 78.0 years, just below the 78.3 target, so official and independent series disagree on this row. Both figures are shown."),
    ("Basic old-age insurance coverage", "indicative", "95%",
     "95.0%", "2024", "met", "UBP table (Nov 2025)",
     "Met exactly, on the 2024 figure in that table."),
    ("Childcare slots per 1,000 children under 3", "indicative", "4.5",
     "4.1", "2024", "missed", "UBP table (Nov 2025)",
     "Also flagged at risk in a Goldman Sachs note."),
    ("Physicians per 1,000 people", "indicative", "3.2",
     "3.4", "2024", "met", "UBP table (Nov 2025)",
     "2025 figure not separately reported in sources found."),
    ("Disposable income growth", "indicative", "in line with GDP growth",
     "5.0% real, GDP 5.0%", "2025", "met", "NBS 2025 Statistical Communique",
     "Per capita disposable income 43,377 yuan."),
    ("Labor productivity growth", "indicative", "faster than GDP growth",
     "6.1%, GDP 5.0%", "2025", "met", "NBS 2025 Statistical Communique",
     "Overall labor productivity 184,413 yuan per person."),
]
write_csv(os.path.join(PROC, "plan_14th_scorecard.csv"),
          ["indicator", "type", "target", "actual", "actual_year", "status",
           "source", "note"], scorecard)

# ------------------------------------------------------------- Plan history
# Targets are the widely reported official plan targets. Actuals for GDP are
# computed in notebook 02 from World Bank data, not typed here.
plans = [
    # plan, years, headline aim, gdp target, energy target, carbon target, outcome note
    ("1st", "1953-1957", "Build heavy industry with Soviet help", "",
     "", "", "Industrial base built. Agricultural output passed prewar levels."),
    ("2nd", "1958-1962", "Great Leap Forward: overtake Britain in steel",
     "", "", "", "Agricultural output target was plus 270 percent. Actual gain was 35 percent. Famine followed."),
    ("3rd", "1966-1970", "Defense and Third Front inland industry", "",
     "", "", "Plan delayed by the aftermath of the Great Leap. Defense became the priority."),
    ("4th", "1971-1975", "Small scale, local, labor intensive projects", "",
     "", "", "Decentralized approach. Growth continued but the economy stayed poor."),
    ("5th", "1976-1980", "Ten year outline, then readjustment and reform", "",
     "", "", "Original steel and oil targets were impossible and were cut. Dec 1978 plenum shifted focus to modernization."),
    ("6th", "1981-1985", "Readjustment and steady growth", "",
     "", "", "First plan to support solar panel manufacturing. Reform era growth took off."),
    ("7th", "1986-1990", "Coastal development first, indirect controls", "",
     "", "", "Coast led, inland supported the coast. Inflation and Tiananmen slowed the end of the period."),
    ("8th", "1991-1995", "Socialist market economy", "",
     "", "", "Deng 1992 southern tour relaunched reform. Growth averaged over 12 percent a year (World Bank)."),
    ("9th", "1996-2000", "Quadruple 1980 GDP by 2000, state firm reform", "",
     "", "", "State firms shed tens of millions of jobs. Asian financial crisis hit 1997 to 1998."),
    ("10th", "2001-2005", "WTO entry, western development, services", "about 7% a year",
     "", "", "China joined the WTO in Dec 2001. Growth averaged about 9.8 percent a year (World Bank)."),
    ("11th", "2006-2010", "First binding targets, energy saving", "7.5% a year",
     "-20%", "", "GDP growth averaged 11.2 percent. Energy intensity fell 19.1 percent, just short of 20 percent."),
    ("12th", "2011-2015", "Rebalance to consumption and services", "7% a year",
     "-16%", "-17%", "GDP growth averaged about 7.8 percent. Energy intensity fell 18.2 percent, beating the target."),
    ("13th", "2016-2020", "Moderately prosperous society, Made in China 2025", "at least 6.5% a year",
     "-15%", "-18%", "GDP growth averaged about 5.7 percent (World Bank), below target, COVID hit 2020. Energy intensity fell about 13.8 percent, missing 15 percent. Carbon intensity fell about 22 percent, beating 18 percent."),
    ("14th", "2021-2025", "Innovation, dual circulation, common prosperity", "no number set",
     "-13.5%", "-18%", "No GDP number was set, a first. See the full scorecard in notebook 03."),
]
write_csv(os.path.join(PROC, "plan_history.csv"),
          ["plan", "years", "headline_aim", "gdp_growth_target",
           "energy_intensity_target", "carbon_intensity_target", "outcome_note"], plans)

# ------------------------------------------------------------- 2020 census
ethnic = [
    ("Han", 1286310000, 91.11),
    ("Zhuang", 19568546, 1.39),
    ("Uyghur", 11774538, 0.84),
    ("Hui", 11377914, 0.81),
    ("Miao", 11067929, 0.79),
    ("Manchu", 10423303, 0.74),
    ("All other minorities combined", 61257770, 4.34),
]
write_csv(os.path.join(PROC, "ethnic_2020.csv"),
          ["group", "population", "share_pct"], ethnic)

# Religion: three published estimates, kept side by side. The census does not
# ask about religion, so every religion figure is a survey or administrative
# estimate, not a census count.
religion = [
    ("Pew Research Center 2023, self-identified", "No religion", 93.0),
    ("Pew Research Center 2023, self-identified", "Buddhism", 3.7),
    ("Pew Research Center 2023, self-identified", "Christianity", 1.4),
    ("Pew Research Center 2023, self-identified", "Islam", 1.3),
    ("Pew Research Center 2023, self-identified", "Folk beliefs", 0.2),
    ("Pew Research Center 2023, self-identified", "Other", 0.3),
    ("CIA World Factbook 2021, among people claiming a belief", "Unaffiliated", 52.1),
    ("CIA World Factbook 2021, among people claiming a belief", "Folk beliefs", 21.9),
    ("CIA World Factbook 2021, among people claiming a belief", "Buddhism", 18.2),
    ("CIA World Factbook 2021, among people claiming a belief", "Christianity", 5.1),
    ("CIA World Factbook 2021, among people claiming a belief", "Islam", 1.8),
    ("CIA World Factbook 2021, among people claiming a belief", "Other (incl. Taoism 0.7)", 0.9),
    ("China Social Survey 2010", "Ancestor and god cults", 56.2),
    ("China Social Survey 2010", "Buddhism", 13.8),
    ("China Social Survey 2010", "Taoist folk religions", 12.9),
    ("China Social Survey 2010", "Christianity", 2.4),
    ("China Social Survey 2010", "Islam", 1.7),
    ("China Social Survey 2010", "Taoism", 0.9),
]
write_csv(os.path.join(PROC, "religion_estimates.csv"),
          ["source", "group", "share_pct"], religion)

# Births, NBS annual communiques.
births = [
    (2016, 17.86), (2017, 17.23), (2018, 15.23), (2019, 14.65), (2020, 12.00),
    (2021, 10.62), (2022, 9.56), (2023, 9.02), (2024, 9.54), (2025, 7.92),
]
write_csv(os.path.join(PROC, "births.csv"), ["year", "births_million"], births)

# 15th plan targets, adopted March 12, 2026. Secondary summaries agree on
# most items; where they differ, both figures are kept and flagged.
plan15 = [
    # indicator, target_2030, type, source, note
    ("GDP growth in 2026 (annual target)", "4.5 to 5.0%", "indicative",
     "Secondary analysis of the 2026 Government Work Report",
     "Described as the lowest annual target since 1991."),
    ("R and D spending growth", "at least 7% per year", "indicative",
     "Plan summaries (ICBC, Fidelity)",
     "Same floor as the 14th plan, reconfirmed."),
    ("Core digital economy share of GDP", "12.5%", "indicative",
     "Plan summaries (ICBC, Fidelity)",
     "14th plan target was 10 percent. Actual reached 10.5 percent in 2024."),
    ("High-value invention patents per 10,000 people", "over 22", "indicative",
     "Plan summaries (ICBC, Fidelity)",
     "2025 actual was 16. 14th plan target was 12."),
    ("Average education, working-age population", "11.7 years", "binding",
     "Plan summaries (ICBC, Fidelity)",
     "14th plan target was 11.3 years."),
    ("Life expectancy", "80 years", "indicative",
     "Plan summaries (ICBC, Fidelity)",
     "Latest verified figure is 79.0 years in 2024."),
    ("Carbon intensity reduction over the plan", "about 17%", "binding",
     "iGDP summary of Government Work Report proposals",
     "Fidelity table brackets 17.7 percent. Both figures are shown, not settled."),
    ("Non-fossil share of energy consumption", "25%", "binding",
     "Plan summaries (ICBC, Fidelity)",
     "iGDP cites about 27 percent from Government Work Report proposals. Both figures are shown, not settled."),
    ("PM2.5 annual average", "under 27 micrograms per cubic meter", "binding",
     "Fidelity plan summary table",
     "2025 actual was 28."),
    ("Forest coverage", "25.8%", "binding",
     "Fidelity plan summary table",
     "2025 actual was past 25 percent."),
    ("Grain production capacity", "725 million tons", "binding",
     "Government Work Report (Mar 2026)",
     "14th plan target was over 650 million tons."),
    ("Energy production capacity", "5.8 billion tons of coal equivalent", "indicative",
     "Government Work Report (Mar 2026) via plan summaries",
     "14th plan target was over 4.6 billion tons."),
    ("Structure", "20 main indicators, 5 dimensions, 109 major projects", "",
     "EIAS analysis; securities firm analysis",
     "7 of the 20 indicators cover livelihood and well-being."),
    ("Long-range goal", "Lay the foundation for doubling per capita GDP by 2035 from 2020", "",
     "EIAS analysis",
     "Needs average growth of about 4.17 percent a year over the decade."),
]
write_csv(os.path.join(PROC, "plan_15th_targets.csv"),
          ["indicator", "target_2030", "type", "source", "note"], plan15)

print("processed data build complete")
