"""Build the 7 notebooks for China: Plan vs Reality.

Each notebook gets a top pip install cell, then markdown and code cells.
Code cells read CSVs from ../data/processed and save charts to ../charts.
Run this file, then execute the notebooks with jupyter nbconvert.
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NBDIR = os.path.join(ROOT, "notebooks")


def md(text):
    return {"cell_type": "markdown", "metadata": {},
            "source": text.splitlines(keepends=True)}


def code(text):
    return {"cell_type": "code", "execution_count": None, "metadata": {},
            "outputs": [], "source": text.splitlines(keepends=True)}


PIP = code("import sys\n!{sys.executable} -m pip install -q pandas matplotlib")


def write_nb(filename, cells):
    all_cells = [PIP] + cells
    for i, cell in enumerate(all_cells):
        cell["id"] = f"c{i}"
    nb = {"cells": all_cells,
          "metadata": {"kernelspec": {"display_name": "China Plan",
                                      "language": "python",
                                      "name": "china-plan"},
                       "language_info": {"name": "python", "version": "3.12"}},
          "nbformat": 4, "nbformat_minor": 5}
    path = os.path.join(NBDIR, filename)
    with open(path, "w") as f:
        json.dump(nb, f, indent=1)
    print("wrote", path, len(cells) + 1, "cells")


SETUP = """import matplotlib.pyplot as plt
import pandas as pd

plt.rcParams["figure.figsize"] = (10, 5.5)
plt.rcParams["axes.titlesize"] = 13
plt.rcParams["axes.labelsize"] = 11
PROC = "../data/processed"
CHARTS = "../charts"
"""

# ================================================================= NB00
NB00 = [
    md("# 00. Setup: what this project is, and how to check it\n\n"
       "Welcome. This project answers one question in plain words: how does China plan its economy in five year blocks, did the last plan hit its targets, how do the provinces differ, who lives where, and what comes next?\n\n"
       "China does not hold competitive presidential elections, so there is no elections chapter here. This is a planning, demographics, and macroeconomics project. If you want elections data, look at the companion projects on the United States and Brazil.\n\n"
       "## How to read this project\n\n"
       "Start at notebook 01 if you know nothing about five year plans. It explains every idea before using it. Notebook 02 tells the long story, from the first plan in 1953 to today, including the failures. Notebook 03 scores the 14th Five Year Plan (2021 to 2025) target by target. Notebook 04 compares the provinces. Notebook 05 covers people and places. Notebook 06 looks at the 15th Five Year Plan (2026 to 2030).\n\n"
       "## Rules this project follows\n\n"
       "- Every number names its source. Official figures are labeled official. Independent figures are labeled independent.\n"
       "- Where sources disagree, both figures are shown and no side is taken.\n"
       "- Where a figure could not be verified, the project says so and does not guess.\n"
       "- No dataset, map, or test is faked. Cuts are listed in BUILD_REPORT.md."),
    code(SETUP + """
import os
print("processed files:")
for fn in sorted(os.listdir(PROC)):
    print(" -", fn)
print("charts folder exists:", os.path.isdir(CHARTS))
"""),
    md("## Data sources at a glance\n\n"
       "- World Bank, World Development Indicators (no key needed). Long run series for GDP, population, urbanization, life expectancy, fertility, poverty, trade, energy, research spending, and age structure. These are the independent cross-check series.\n"
       "- National Bureau of Statistics of China (NBS), 2025 Statistical Communique, February 28, 2026. The official 2025 figures: GDP, income, urbanization, energy, environment, jobs.\n"
       "- Government Work Report, delivered March 5, 2026. The official verdict on the 14th plan and the 15th plan headline targets.\n"
       "- Ministry of Ecology and Environment reporting, via Xinhua, January and March 2026. Air and water figures.\n"
       "- iGDP China Carbon Neutrality Tracker newsletter, January to February 2026 issue. Full period energy and carbon intensity figures.\n"
       "- Seventh National Population Census, 2020, results released May 11, 2021. Population, ethnic composition, and provincial populations.\n"
       "- NBS provincial data via Wikipedia compilations of NBS tables. Provincial GDP for 2024 (revised) and 2025 (preliminary), and mid-2022 provincial populations with urban and rural splits.\n"
       "- Pew Research Center (2023), CIA World Factbook (2021), and China Social Survey (2010) for religion. Three different methods, three different answers, all shown.\n"
       "- Plan documents and secondary summaries for the 15th plan (adopted March 12, 2026), including EIAS analysis and ICBC and Fidelity summary tables. Where those tables disagree, both figures are kept.\n\n"
       "Full citations, file by file, are in data/raw/PROVENANCE.md."),
    code("""
wb = pd.read_csv(f"{PROC}/wb_longrun.csv")
print("World Bank long run table:", wb.shape[0], "rows,", wb.shape[1], "columns")
print("Years covered:", int(wb.year.min()), "to", int(wb.year.max()))
print("Missing values per column (0 is good for core series):")
print(wb.isna().sum()[wb.isna().sum() > 0])
"""),
    md("## Verification checks\n\n"
       "The next cell runs the checks this project promises. It confirms the World Bank series load, the provincial table sums to about the national total (a small gap is normal, see notebook 04), the 14th plan scorecard has 20 rows, and the ethnic shares add to about 100 percent. If any check fails, the build is not finished."),
    code("""
prov = pd.read_csv(f"{PROC}/provinces.csv")
score = pd.read_csv(f"{PROC}/plan_14th_scorecard.csv")
eth = pd.read_csv(f"{PROC}/ethnic_2020.csv")
print("provinces:", len(prov), "(31 mainland divisions expected)")
print("provincial 2024 GDP sum, million CNY:", prov.gdp_2024_m_cny.sum())
print("national 2024 GDP, million CNY: 134806620")
print("gap:", round((1 - prov.gdp_2024_m_cny.sum() / 134806620) * 100, 2), "percent")
print("14th plan scorecard rows:", len(score), "(20 expected)")
print("scorecard status counts:"); print(score.status.value_counts().to_dict())
print("ethnic shares sum:", round(eth.share_pct.sum(), 2), "percent")
print("ALL CHECKS DONE")
"""),
]

# ================================================================= NB01
NB01 = [
    md("# 01. How planning works, in plain words\n\n"
       "## The basic idea\n\n"
       "Every five years, China writes a national development plan. Think of it as a to do list for the whole country, with numbers attached. The plan says what the government wants to build, protect, and improve over the next five years, and how it will know whether it succeeded.\n\n"
       "The system started in 1953, copying the Soviet Union. It has changed a lot since then. Early plans were strict orders: factories were told exactly what to produce. Modern plans are more like guidelines with a few hard promises mixed in. Markets now do most of the day to day deciding. The plan sets the direction.\n\n"
       "## The five year cycle, step by step\n\n"
       "1. Midway through the current plan, work starts on the next one. Drafting takes two to three years.\n"
       "2. The Communist Party Central Committee agrees on general guidelines in the autumn before the plan starts.\n"
       "3. The State Council (the cabinet) writes the detailed plan.\n"
       "4. The National People's Congress (the legislature) approves it the following March.\n"
       "5. Ministries, provinces, and cities write their own detailed action plans to match.\n"
       "6. Progress is reviewed, and the cycle starts again.\n\n"
       "So a plan is not one document written in a week. It is a long coordination exercise across the whole government.\n\n"
       "## Two kinds of targets: binding and indicative\n\n"
       "This distinction matters, and it explains a lot of the scorecard in notebook 03.\n\n"
       "- A binding target is a promise. The government says it must be hit, and local officials are judged on it. Binding targets are used mostly for the environment, resources, and social welfare. Example: cut energy intensity by 13.5 percent.\n"
       "- An indicative target is a goal, not an order. It says where the government wants to go, but missing it is not treated as a broken promise. Example: raise the urbanization rate to 65 percent.\n\n"
       "Since the 11th plan (2006 to 2010), binding targets have been written into how local officials are evaluated. That is why environmental targets get more attention than they used to.\n\n"
       "## What is a five year plan not?\n\n"
       "It is not a budget. It does not list every project and its price. It is not a law that punishes companies for missing a number. And since the 14th plan, it does not even set a number for GDP growth. The 14th plan said growth should stay in a reasonable range, without naming the range. That was a first.\n\n"
       "## The long-range objectives through 2035\n\n"
       "On top of the five year plans, China sets longer goals. The current long-range objectives run to 2035. They describe a country that is much richer per person, more innovative, greener, and with a stronger safety net. The 15th plan (2026 to 2030) is supposed to lay the foundation for doubling GDP per person by 2035 compared with 2020. Notebook 06 explains what that requires.\n\n"
       "## The plans so far\n\n"
       "The chart below shows every plan period from 1953 to 2030. Two gaps are real, not mistakes. No five year plan covered 1963 to 1965, because the economy was too dislocated after the Great Leap Forward to plan. And the 5th plan period (1976 to 1980) started with a ten year outline that was later rewritten when reform began in December 1978."),
    code(SETUP + """
import matplotlib.patches as mpatches

plans = [
    ("1st", 1953, 1957), ("2nd", 1958, 1962), ("3rd", 1966, 1970),
    ("4th", 1971, 1975), ("5th", 1976, 1980), ("6th", 1981, 1985),
    ("7th", 1986, 1990), ("8th", 1991, 1995), ("9th", 1996, 2000),
    ("10th", 2001, 2005), ("11th", 2006, 2010), ("12th", 2011, 2015),
    ("13th", 2016, 2020), ("14th", 2021, 2025), ("15th", 2026, 2030),
]
fig, ax = plt.subplots(figsize=(11, 5))
for i, (name, start, end) in enumerate(plans):
    color = "#2c7fb8" if i < 5 else ("#41b6c4" if i < 10 else "#a1dab4")
    ax.barh(0, end - start + 1, left=start, height=0.5, color=color)
    ax.text((start + end) / 2, 0, name, ha="center", va="center",
            fontsize=8, color="black")
ax.set_xlim(1952, 2031)
ax.set_ylim(-0.6, 0.6)
ax.set_yticks([])
ax.set_xlabel("Year")
ax.set_title("China's five year plans, 1953 to 2030 (no plan covered 1963 to 1965)")
ax.legend(handles=[mpatches.Patch(color="#2c7fb8", label="Mao era plans"),
                   mpatches.Patch(color="#41b6c4", label="Reform era plans"),
                   mpatches.Patch(color="#a1dab4", label="Recent plans")],
          loc="lower center", bbox_to_anchor=(0.5, -0.45), ncol=3, frameon=False)
plt.tight_layout()
plt.savefig(f"{CHARTS}/01_plan_timeline.png", dpi=150, bbox_inches="tight")
print("saved 01_plan_timeline.png")
"""),
    md("## Words you will meet in this project\n\n"
       "- GDP: the total value of everything produced in a country in a year. GDP per person divides that by the population. It is a rough measure of average income, not of happiness or fairness.\n"
       "- Energy intensity: how much energy is used to produce one unit of GDP. If it falls, the economy is getting more output from each ton of coal or kilowatt hour.\n"
       "- Carbon intensity: how much carbon dioxide is emitted per unit of GDP. It can fall even while total emissions rise, if GDP grows faster.\n"
       "- Non-fossil energy: energy from sources other than coal, oil, and gas. That means hydro, nuclear, wind, solar, and others.\n"
       "- Urbanization rate: the share of the population living in cities and towns, counting people who live there permanently, not just people with a city household registration.\n"
       "- Hukou: the household registration system. It ties a person's access to local schools, health care, and pensions to the place they are registered, which is often their birthplace. Migrant workers living in cities without a local hukou are a big policy issue.\n"
       "- Purchasing power parity (PPP): a way to compare economies that adjusts for price differences. A haircut costs less in China than in the United States, so PPP makes China's economy look bigger than market exchange rates do. This project uses market rates unless it says PPP.\n\n"
       "Next: notebook 02 tells the long story, plan by plan, with the numbers."),
]

# ================================================================= NB02
NB02 = [
    md("# 02. Plans through history: what was promised, what happened\n\n"
       "This is the long chapter. It compares planning targets with actual outcomes from the first plan in 1953 to the 14th plan, and it judges the big policies honestly, including the failures.\n\n"
       "Two ways of reading the numbers are used side by side. Official plan targets come from plan documents and government summaries. Actual outcomes come mostly from the World Bank, an independent series, so the reader can check the official story against outside data. Where the two disagree, both are shown.\n\n"
       "## The headline in one paragraph\n\n"
       "From 1978 to 2015, China's economy grew about 9.8 percent a year on World Bank data (the People's Daily cites 9.6 percent for the same period, a small vintage difference). GDP per person rose from 157 dollars in 1978 to 13,293 dollars in 2024. Extreme poverty at the World Bank 2.15 dollar line fell from 97.0 percent in 1981 to 0.0 percent in 2019. Life expectancy rose from 63.1 years in 1978 to 78.0 years in 2024 on the World Bank series (the official figure for 2024 is 79.0 years). Those are the achievements. The failures are real too: a famine that killed tens of millions, a decade of political turmoil that shut universities, severe pollution, a debt pile near 300 percent of GDP, a property crash, and a population now shrinking. Both halves belong in the story."),
    code(SETUP + """
wb = pd.read_csv(f"{PROC}/wb_longrun.csv")
plans = pd.read_csv(f"{PROC}/plan_history.csv")
g = wb.dropna(subset=["gdp_growth_pct"])
periods = [("1st", 1953, 1957), ("2nd", 1958, 1962), ("3rd", 1966, 1970),
           ("4th", 1971, 1975), ("5th", 1976, 1980), ("6th", 1981, 1985),
           ("7th", 1986, 1990), ("8th", 1991, 1995), ("9th", 1996, 2000),
           ("10th", 2001, 2005), ("11th", 2006, 2010), ("12th", 2011, 2015),
           ("13th", 2016, 2020), ("14th", 2021, 2025)]
rows = []
for name, a, b in periods:
    sub = g[(g.year >= a) & (g.year <= b)]
    rows.append([name, f"{a}-{b}", round(sub.gdp_growth_pct.mean(), 2)
                 if len(sub) else None, len(sub)])
era = pd.DataFrame(rows, columns=["plan", "years", "avg_gdp_growth_pct_wb", "years_with_data"])
print(era.to_string(index=False))
print()
print("Note: the World Bank growth series starts in 1961, so the 1st and 2nd plan rows use fewer years.")
"""),
    md("## How to read the era table\n\n"
       "The 2nd plan row is deeply negative, minus 16.4 percent on average, but it only covers 1961 and 1962, because the World Bank growth series starts in 1961. Those were the famine collapse years, so the row shows the disaster, not the whole plan. The 1st plan row is blank for the same reason: no World Bank growth data exists for 1953 to 1957. Averages also hide disasters in the other direction. The 1966 to 1976 period is not one row in the table, but computed separately it averages about 5.9 percent a year, which looks ordinary while hiding school closures and political turmoil.\n\n"
       "From the 6th plan onward, every five year block averaged between about 5.4 and 12.3 percent growth. The reform era is the long boom. It slowed step by step: about 11.3 percent in the 11th plan, 7.9 percent in the 12th, 5.8 percent in the 13th, and 5.4 percent in the 14th."),
    code("""
fig, ax = plt.subplots()
wb2 = wb.dropna(subset=["gdp_usd"])
ax.plot(wb2.year, wb2.gdp_usd / 1e12)
ax.set_yscale("log")
ax.set_ylabel("Trillion US dollars (log scale)")
ax.set_xlabel("Year")
ax.set_title("China GDP, 1960 to 2024 (World Bank, log scale)")
ax.grid(True, which="both", alpha=0.3)
plt.savefig(f"{CHARTS}/02_gdp_log.png", dpi=150, bbox_inches="tight")
print("1960 GDP, billion USD:", round(wb2[wb2.year == 1960].gdp_usd.iloc[0] / 1e9, 1))
print("1978 GDP, billion USD:", round(wb2[wb2.year == 1978].gdp_usd.iloc[0] / 1e9, 1))
print("2024 GDP, billion USD:", round(wb2[wb2.year == 2024].gdp_usd.iloc[0] / 1e9, 1))
print("saved 02_gdp_log.png")
"""),
    code("""
fig, ax = plt.subplots()
wb3 = wb.dropna(subset=["gdp_per_capita_usd"])
ax.plot(wb3.year, wb3.gdp_per_capita_usd)
ax.set_ylabel("US dollars")
ax.set_xlabel("Year")
ax.set_title("GDP per person, 1960 to 2024 (World Bank)")
ax.grid(True, alpha=0.3)
plt.savefig(f"{CHARTS}/02_gdp_per_capita.png", dpi=150, bbox_inches="tight")
print("GDP per person 1978:", round(wb3[wb3.year == 1978].gdp_per_capita_usd.iloc[0], 1))
print("GDP per person 2024:", round(wb3[wb3.year == 2024].gdp_per_capita_usd.iloc[0], 1))
print("saved 02_gdp_per_capita.png")
"""),
    code("""
fig, ax = plt.subplots()
ax.plot(g.year, g.gdp_growth_pct, linewidth=1)
for name, a, b in periods[5:]:
    sub = g[(g.year >= a) & (g.year <= b)]
    ax.hlines(sub.gdp_growth_pct.mean(), a, b, colors="red", linewidth=2)
ax.axhline(0, color="black", linewidth=0.8)
ax.set_ylabel("Percent per year")
ax.set_xlabel("Year (red bars: plan period averages, 6th plan onward)")
ax.set_title("Annual GDP growth and plan period averages (World Bank)")
ax.grid(True, alpha=0.3)
plt.savefig(f"{CHARTS}/02_growth_by_plan.png", dpi=150, bbox_inches="tight")
print("saved 02_growth_by_plan.png")
"""),
    md("## Plan targets versus actuals: the verified table\n\n"
       "The table below lists the plans where a numeric target could be verified against a stated source. Early plans did not publish the kind of numeric targets modern plans do, so they are described in words. The pattern to notice: growth targets were usually beaten in the boom years (the 11th plan targeted 7.5 percent and got about 11.2 to 11.3 percent), then missed when growth slowed (the 13th plan targeted at least 6.5 percent and got about 5.8 percent). Energy targets show the opposite pattern in recent plans: the 11th plan missed its 20 percent energy saving goal by a fraction (19.1 percent), the 12th beat its 16 percent goal (18.2 percent), and the 13th missed its 15 percent goal (about 13.8 percent) while beating its carbon goal (about 22 percent against 18 percent)."),
    code("""
print(plans[["plan", "years", "gdp_growth_target", "energy_intensity_target",
             "carbon_intensity_target"]].to_string(index=False))
"""),
    md("## Poverty: the strongest result, on two different yardsticks\n\n"
       "Two poverty series are often confused. They measure different things, and both are shown.\n\n"
       "- The World Bank line of 2.15 dollars a day (2017 prices) is an international extreme poverty line. On it, China went from 97.0 percent of the population in 1981 to 83.1 percent in 1990, 20.6 percent in 2010, and 0.0 percent in 2019. That is the largest poverty reduction ever recorded on one consistent yardstick.\n"
       "- China's own rural poverty line is a national standard, lower than the World Bank line in income terms for much of the period. On it, the official count of rural poor fell from 770 million at the end of 1978 to 98.99 million in 2012, a rate of 97.5 percent down to 10.2 percent. The targeted campaign then lifted the remaining 98.99 million by the end of 2020, covering 832 counties and 128,000 villages, with about 1.6 trillion yuan in special funds.\n\n"
       "The honest caveat: the national line was low, so clearing it did not mean a comfortable life. And officials themselves set up a transition period after 2020 to stop people sliding back, which shows the result needed defending."),
    code("""
fig, ax = plt.subplots()
pov = wb.dropna(subset=["poverty_215_pct"])
ax.plot(pov.year, pov.poverty_215_pct, marker="o")
ax.set_ylabel("Percent of population")
ax.set_xlabel("Year")
ax.set_title("Extreme poverty at 2.15 dollars a day (World Bank)")
ax.grid(True, alpha=0.3)
plt.savefig(f"{CHARTS}/02_poverty.png", dpi=150, bbox_inches="tight")
print("poverty 1981:", pov[pov.year == 1981].poverty_215_pct.iloc[0])
print("poverty 2019:", pov[pov.year == 2019].poverty_215_pct.iloc[0])
print("saved 02_poverty.png")
"""),
    code("""
fig, ax = plt.subplots()
le = wb.dropna(subset=["life_expectancy"])
ax.plot(le.year, le.life_expectancy)
ax.set_ylabel("Years")
ax.set_xlabel("Year")
ax.set_title("Life expectancy at birth (World Bank)")
ax.grid(True, alpha=0.3)
plt.savefig(f"{CHARTS}/02_life_expectancy.png", dpi=150, bbox_inches="tight")
print("life expectancy 1960:", le[le.year == 1960].life_expectancy.iloc[0])
print("life expectancy 1978:", le[le.year == 1978].life_expectancy.iloc[0])
print("life expectancy 2024:", le[le.year == 2024].life_expectancy.iloc[0])
print("saved 02_life_expectancy.png")
"""),
    md("## Health and cities\n\n"
       "Life expectancy tells a story the GDP chart hides. It collapsed to 33.4 years in 1960 in the famine, then recovered fast, reaching 63.1 years by 1978 and 78.0 years by 2024 on the World Bank series. The official figure for 2024 is 79.0 years. The gap between the two series is a reminder to always ask which series a number comes from.\n\n"
       "Urbanization moved with the economy. The World Bank series puts the urban share at 17.9 percent in 1978, 36.4 percent in 2000, and 65.9 percent in 2024. The NBS permanent resident rate for 2025 is 67.89 percent. Hundreds of millions of people moved to cities, the largest migration in history, and the hukou system still limits many migrants' access to city schools, health care, and pensions.\n\n"
       "The population is now aging fast. The share aged 65 and over rose from 4.2 percent in 1978 to 7.0 percent in 2000 and 14.7 percent in 2024. Fertility fell from 6.09 children per woman in 1970 to 2.72 in 1978, 1.63 in 2000, and about 1.0 in 2023 and 2024."),
    code("""
fig, ax = plt.subplots()
u = wb.dropna(subset=["urban_pct", "pop_65_pct"])
ax.plot(u.year, u.urban_pct, label="Urban share of population")
ax.plot(u.year, u.pop_65_pct, label="Share aged 65 and over")
ax.set_ylabel("Percent")
ax.set_xlabel("Year")
ax.set_title("Urbanization and aging (World Bank)")
ax.legend()
ax.grid(True, alpha=0.3)
plt.savefig(f"{CHARTS}/02_urban_aging.png", dpi=150, bbox_inches="tight")
print("saved 02_urban_aging.png")
"""),
    code("""
fig, ax = plt.subplots()
t = wb.dropna(subset=["exports_pct_gdp", "imports_pct_gdp"])
ax.plot(t.year, t.exports_pct_gdp, label="Exports")
ax.plot(t.year, t.imports_pct_gdp, label="Imports")
ax.set_ylabel("Percent of GDP")
ax.set_xlabel("Year")
ax.set_title("Trade openness: exports and imports as a share of GDP (World Bank)")
ax.legend()
ax.grid(True, alpha=0.3)
plt.savefig(f"{CHARTS}/02_trade.png", dpi=150, bbox_inches="tight")
peak = t.loc[t.exports_pct_gdp.idxmax()]
print("exports peak:", peak.year, round(peak.exports_pct_gdp, 1), "percent of GDP")
print("exports 2024:", round(t[t.year == 2024].exports_pct_gdp.iloc[0], 1))
print("saved 02_trade.png")
"""),
]

NB02 += [
    md("## Policies: what each one aimed at, what the data shows, and the verdict\n\n"
       "Verdict words used here: worked (aim broadly achieved), mixed (real gains with real costs or partial success), missed (aim not achieved), reversed (policy later undone by its own makers), too early (not enough time to judge).\n\n"
       "### Reform and Opening, from December 1978. Aim: grow the economy by letting markets work inside a state led system. Evidence: growth averaged about 9.8 percent a year from 1978 to 2015 (World Bank). Verdict: worked on growth. Costs: inequality rose, corruption grew, and the environment paid a high price.\n\n"
       "### Household responsibility system, 1978 to 1984. Aim: give farm families a reason to produce more by letting them keep output above a quota. Evidence: grain output rose from 304.8 million tons in 1978 to 407.3 million tons in 1984, up 33.6 percent, and farm income more than doubled. Verdict: worked.\n\n"
       "### Special Economic Zones, from 1980. Aim: test markets in small coastal areas before rolling them out. Evidence: the first four zones were Shenzhen, Zhuhai, Shantou, and Xiamen. Shenzhen grew about 54 percent a year from 1980 to 1984, and the four zones took 26 percent of China's foreign investment in 1984. Verdict: worked as an experiment. Cost: coastal regions pulled far ahead of inland ones.\n\n"
       "### Dual-track pricing, from 1984. Aim: move toward market prices without a sudden shock, by keeping a low plan price and letting extra output sell at a market price. Evidence: prices were mostly freed by the 1990s without the output collapse seen in Russia's shock therapy. Cost: the gap between plan and market prices created arbitrage and corruption. Verdict: mixed.\n\n"
       "### Township and village enterprises, 1980s to 1990s. Aim: let rural industry absorb farm labor. Evidence: rural enterprises grew fast through the 1980s and employed well over 100 million people by the mid 1990s on commonly cited figures. Many were later privatized or closed in the late 1990s shakeout. Verdict: mixed. They filled a gap, then faded.\n\n"
       "### State-owned enterprise reform, late 1990s. Aim: make big state firms profitable by cutting losses and shedding workers. Evidence: large state firms became more profitable, but layoffs ran into the tens of millions, often cited at around 30 million. The safety net at the time was thin. Verdict: mixed. Efficiency up, social cost high.\n\n"
       "### WTO accession, December 2001. Aim: lock in export markets and force domestic firms to compete. Evidence: exports rose to a peak of 35.5 percent of GDP in 2006 (World Bank), and China became the world's largest exporter. Verdict: worked on trade. The adjustment costs for workers in import hit sectors, at home and abroad, are still debated.\n\n"
       "### The 2008 stimulus. Aim: protect growth when the global financial crisis crushed exports. Evidence: the government announced a 4 trillion yuan package in November 2008, and growth rebounded to 10.6 percent in 2010 (World Bank). Cost: debt ballooned, and much of the money fed a property and infrastructure boom that later turned into overcapacity and bad loans. Verdict: mixed.\n\n"
       "### Supply-side reform, from 2015. Aim: cut overcapacity in steel and coal, reduce housing inventory, and lower business costs. Evidence: capacity was cut in steel and coal, but debt and property risks stayed high and later got worse. Verdict: mixed. Direction changed, problems persisted.\n\n"
       "### Targeted poverty alleviation, 2013 to 2020. Aim: lift every remaining rural poor person under the national line by the end of 2020. Evidence: 98.99 million people, 832 counties, and 128,000 villages were lifted on official counts, with about 1.6 trillion yuan in special funds. Verdict: worked on its own standard. Caveats: the line was low, and the government set up a five year transition after 2020 to stop people sliding back.\n\n"
       "### One-child policy and its reversals. Aim: slow population growth. Evidence: fertility fell from 6.09 in 1970 to about 1.0 in 2023 and 2024, and the population has shrunk every year since 2022. The policy was replaced by a two-child limit in 2016 and a three-child limit in 2021, yet births kept falling, from 17.86 million in 2016 to 7.92 million in 2025. Verdict: reversed. It achieved slower growth, then overshot so far that the government now pays families to have children.\n\n"
       "### Dual circulation, from 2020. Aim: rely more on domestic demand while staying open to the world, and reduce dependence on foreign technology. Evidence: mixed so far. Final consumption contributed 52 percent of 2025 growth, up 5 points on 2024, but the trade surplus was still about 1 trillion dollars in 2024. Verdict: too early, and the data pulls both ways.\n\n"
       "### Common prosperity, from 2021. Aim: narrow inequality and share growth more widely. Evidence: the urban to rural income ratio narrowed slightly, to 2.31 in 2025, down 0.03 on 2024. A full inequality verdict needs a recent income distribution series, which this build did not fetch, so that part is a documented cut. Verdict: too early.\n\n"
       "### Tech self-reliance, including Made in China 2025. Aim: lead in advanced manufacturing and cut dependence on foreign chips and equipment. Evidence: research spending reached about 3.93 trillion yuan in 2025, 2.80 percent of GDP, above the OECD average of 2.72 percent for the first time, and high-value patents hit 16 per 10,000 people. But the 70 percent chip self-sufficiency goal in Made in China 2025 is described in secondary analysis as largely missed, and the 15th plan drops that goal. Verdict: mixed. Strong in research inputs and some sectors, weak in advanced chips."),
    md("## The failures, stated plainly\n\n"
       "### The Great Leap Forward and the famine, 1958 to 1962\n\n"
       "The 2nd plan aimed to leap ahead in heavy industry. Millions of farm workers were moved into backyard steel furnaces and big projects, officials under pressure to meet quotas reported grain that did not exist, and the state kept taking grain while villages starved. Grain output fell more than 25 percent in 1960 to 1961.\n\n"
       "How many died is contested, and this project does not pick one number. Government statistics imply about 15 million excess deaths. Scholarly estimates range from 15 million to 46 million, with newer estimates concentrated between 30 million and 46 million. Named estimates: about 30 million (Ashton and co-authors, 1984, demographic reconstruction), 32.5 million (Cao Shuji, county records), 36 million (Yang Jisheng, Tombstone, from internal records), and at least 45 million (Frank Dikotter, Mao's Great Famine, from provincial archives, a figure other scholars have questioned). The hardest hit provinces, by share of population dead, were Anhui (18 percent), Chongqing (15 percent), Sichuan (13 percent), Guizhou (11 percent), and Hunan (8 percent).\n\n"
       "### The Cultural Revolution, 1966 to 1976\n\n"
       "A political campaign, not an economic plan, but it wrecked a decade of development. Universities closed, the university entrance exam was suspended from 1966 until it was restored in 1977, and a generation lost schooling. Growth averaged about 5.9 percent a year across 1966 to 1976 on World Bank data, but it swung sharply and the country fell behind its East Asian neighbors.\n\n"
       "### Environmental costs\n\n"
       "Growth was bought with coal. Energy use per person rose from 773 kilograms of oil equivalent in 1990 to 2,947 in 2024 (World Bank). Coal still supplied 51.4 percent of energy consumption in 2025, though that was down 1.8 points on 2024. Air pollution has improved a lot since the worst years: average PM2.5 was 28 micrograms per cubic meter in 2025, down 20 percent over five years. The cleanup is real, but it started from very dirty air, and China is still the world's largest carbon emitter in total, even as its emissions per unit of GDP fall.\n\n"
       "### Overcapacity, debt, and the property crash\n\n"
       "The investment led model produced too much of some things: steel, coal, housing, and now solar panels and electric vehicles. In solar panels, Chinese firms account for nearly 90 percent of global capital investment, per Bruegel analysis. Debt piled up with it. Total non-financial debt reached 296 percent of GDP in the third quarter of 2025 (Congressional Research Service summary of the data), and the IMF put explicit local government debt at 39 percent of GDP plus local financing vehicle debt at 51 percent of GDP in 2025. Property, long about a quarter to a third of GDP including related industries, crashed after 2021: the value of property sales fell 54 percent from 2021, Evergrande defaulted in 2021 on 305 billion dollars of debt, was ordered into liquidation in 2024, and was delisted in August 2025.\n\n"
       "### Demographic headwinds\n\n"
       "The chart below is the other side of the one-child story. Births fell from 17.86 million in 2016 to 7.92 million in 2025, the first year below 8 million since 1949. The population fell for a fourth straight year in 2025, down 3.39 million to 1,404.89 million. The working-age share is shrinking, which makes the 15th plan's growth math harder, as notebook 06 explains."),
    code("""
births = pd.read_csv(f"{PROC}/births.csv")
fig, ax = plt.subplots()
ax.bar(births.year, births.births_million)
ax.set_ylabel("Million births")
ax.set_xlabel("Year")
ax.set_title("Births per year, 2016 to 2025 (NBS)")
ax.grid(True, axis="y", alpha=0.3)
plt.savefig(f"{CHARTS}/02_births.png", dpi=150, bbox_inches="tight")
print("births 2016:", births[births.year == 2016].births_million.iloc[0])
print("births 2025:", births[births.year == 2025].births_million.iloc[0])
print("saved 02_births.png")
"""),
    md("## Bottom line of the history chapter\n\n"
       "Planning did not cause the boom by itself. The boom came when planning loosened: farm families kept their surplus, coastal zones tested markets, and foreign trade was opened. Planning helped most when it set a direction and then let experiment happen, and it failed worst when it set impossible physical targets and punished honest reporting, as in 1958 to 1962. The recent plans are more honest about limits: no GDP number in the 14th plan, binding targets for the environment, and a 15th plan that talks about quality of life as much as speed. Whether that honesty survives slower growth is the question notebook 06 leaves open.\n\n"
       "Next: notebook 03 scores the 14th plan, target by target."),
]

# ================================================================= NB03
NB03 = [
    md("# 03. The 14th Five Year Plan scorecard: 2021 to 2025\n\n"
       "The 14th plan ran from 2021 to 2025. It had 20 quantitative targets: 8 binding (promises) and 12 indicative (goals). It also had a GDP direction with no number, the first time a plan skipped a growth number. This notebook scores each target as met, missed, or not yet reported, and always shows the year of the actual figure, because a 2024 figure is not a 2025 result.\n\n"
       "One important note before the table. The Government Work Report of March 5, 2026 states that all 20 major targets were accomplished. Independent trackers disagree on two of them: carbon intensity (about 12 percent reduction against an 18 percent target) and childcare slots (4.1 against 4.5). This project shows both the official claim and the tracker figures, and takes no position on which characterization is correct. Readers can see the arithmetic for themselves."),
    code(SETUP + """
score = pd.read_csv(f"{PROC}/plan_14th_scorecard.csv")
print("targets:", len(score))
print("binding:", (score.type == "binding").sum())
print("indicative:", (score.type == "indicative").sum())
print(score.status.value_counts().to_dict())
print()
print(score[["indicator", "type", "target", "actual", "actual_year", "status"]].to_string(index=False))
"""),
    code("""
fig, ax = plt.subplots(figsize=(8, 4.5))
counts = score.status.value_counts()
order = ["met", "missed", "not yet reported"]
vals = [counts.get(o, 0) for o in order]
colors = ["#41ab5d", "#e6550d", "#969696"]
ax.bar(order, vals, color=colors)
for i, v in enumerate(vals):
    ax.text(i, v + 0.3, str(v), ha="center")
ax.set_ylabel("Number of targets")
ax.set_title("14th plan scorecard: 20 quantitative targets by outcome")
plt.savefig(f"{CHARTS}/03_scorecard_counts.png", dpi=150, bbox_inches="tight")
print("saved 03_scorecard_counts.png")
"""),
    md("## Reading the scorecard, group by group\n\n"
       "### Environment: mostly met, one clear miss\n\n"
       "Good air days reached 89.3 percent in 2025 against 87.5 percent targeted, a record. Surface water at grade III or better reached 91.4 percent against 85 percent. Forest coverage passed 25 percent against 24.1 percent. Energy intensity fell 15 percent over the full period on the iGDP tracker, beating the 13.5 percent target, though the official interim figure for 2021 to 2024 was minus 11.6 percent. Carbon intensity is the miss: about 12 percent against 18 percent. That miss matters because carbon is the hardest target and the one the world watches.\n\n"
       "### Energy and food security: met, with a wording caution\n\n"
       "Grain output topped 700 million tons for a second straight year in 2025, against a capacity target of over 650 million tons. Energy output reached 5.13 billion tons of coal equivalent against a capacity target of over 4.6 billion. Both are scored met, but output is not capacity, and the notebook keeps that distinction visible.\n\n"
       "### People: mostly met, two to watch\n\n"
       "Urbanization reached 67.89 percent against 65 percent. New urban jobs totaled about 62.42 million against over 55 million. Surveyed urban unemployment averaged 5.2 percent in 2025, inside the 5.5 percent ceiling. Disposable income grew 5.0 percent in real terms in 2025, matching GDP growth of 5.0 percent. Labor productivity grew 6.1 percent in 2025, faster than GDP. Life expectancy reached 79.0 years in 2024 on the official series, above the 78.3 year target, but the World Bank series puts 2024 at 78.0 years, just below target, so the two series disagree on this row. Pension coverage hit 95.0 percent exactly on the 2024 figure. Physicians reached 3.4 per 1,000 against 3.2. Childcare slots missed: 4.1 against 4.5. Working-age education has no verified 2025 actual in the sources checked, so it is scored not yet reported, not guessed.\n\n"
       "### Innovation: met\n\n"
       "Research spending grew about 10 percent a year on average over the plan, above the 7 percent floor, reaching about 3.93 trillion yuan in 2025, or 2.80 percent of GDP, above the OECD average of 2.72 percent for the first time. The core digital economy reached 10.5 percent of GDP in 2024, already above the 10 percent target for 2025. High-value invention patents reached 16 per 10,000 people at the end of 2025, above the target of 12.\n\n"
       "### Growth: no number, but a result anyway\n\n"
       "With no GDP number set, the plan cannot be scored on growth, but the result can still be stated. GDP grew 8.4, 3.0, 5.2, 5.0, and 5.0 percent from 2021 to 2025 on published annual rates. The simple mean of those five rounded rates is 5.32 percent, while the World Bank annual series averages 5.41 percent and the Government Work Report states 5.4 percent. The small gap is a rounding and vintage difference, and all three point to the same story: about 5.4 percent a year. The economy grew from about 101 trillion yuan in 2020 to 140.19 trillion yuan in 2025, an increase of about 39 trillion yuan. Per person GDP reached 99,665 yuan in 2025, or 13,953 dollars, the third straight year above 13,000 dollars."),
    code("""
fig, ax = plt.subplots(figsize=(10, 6))
rows = [
    ("Energy intensity fall", 13.5, 15.0),
    ("Carbon intensity fall", 18.0, 12.0),
    ("Good air days", 87.5, 89.3),
    ("Surface water good", 85.0, 91.4),
    ("Forest coverage", 24.1, 25.0),
    ("Urbanization", 65.0, 67.89),
    ("Non-fossil share", 20.0, 21.7),
    ("Pension coverage", 95.0, 95.0),
]
labels = [r[0] for r in rows]
targets = [r[1] for r in rows]
actuals = [r[2] for r in rows]
y = range(len(rows))
ax.barh([i + 0.2 for i in y], targets, height=0.4, label="Target", color="#969696")
ax.barh([i - 0.2 for i in y], actuals, height=0.4, label="Actual", color="#2c7fb8")
ax.set_yticks(list(y))
ax.set_yticklabels(labels)
ax.set_xlabel("Percent (forest actual is 'past 25', plotted as 25)")
ax.set_title("14th plan: targets vs actuals for comparable percent indicators")
ax.legend()
ax.grid(True, axis="x", alpha=0.3)
plt.savefig(f"{CHARTS}/03_targets_vs_actuals.png", dpi=150, bbox_inches="tight")
print("saved 03_targets_vs_actuals.png")
"""),
    md("## What the scorecard does not prove\n\n"
       "Hitting a target does not prove the policy caused the result. Urbanization would have risen without a target. Missing a target does not prove failure of effort: carbon intensity missed partly because energy demand grew fast and coal stayed cheap and reliable. And the two disputed rows, carbon and childcare, show why attribution matters. The official report says all 20 were accomplished. The figures in this scorecard give 17 met, 2 missed, and 1 not yet reported. This project reports that count, and leaves the official claim alongside it.\n\n"
       "Next: notebook 04 compares the provinces, where the national average hides the real story."),
]

# ================================================================= NB04
NB04 = [
    md("# 04. Provincial scorecard: the same country, very different economies\n\n"
       "The national average hides the real story. Guangdong's economy alone is bigger than most countries. Tibet's is smaller than a single large Chinese city. This notebook compares all 31 mainland provincial divisions on GDP, GDP per person, growth, urbanization, and long-run change, and it is honest about what could not be compared.\n\n"
       "Two labels matter. GDP figures are from NBS data via a Wikipedia compilation: 2024 is revised, 2025 is preliminary. GDP per person here is approximate: 2024 GDP divided by the mid-2022 resident population, because a 2024 provincial population table was not fetched for this build. Populations move, so treat the per person ranking as close, not exact. Urbanization rates are computed from the same mid-2022 NBS table: urban residents divided by total residents."),
    code(SETUP + """
prov = pd.read_csv(f"{PROC}/provinces.csv")
print("provinces:", len(prov))
print()
top = prov.sort_values("gdp_2024_m_cny", ascending=False)
print("Top 10 by 2024 GDP (million CNY):")
print(top[["province", "gdp_2024_m_cny", "share_of_national_2024_pct",
           "real_growth_2025p_pct"]].head(10).to_string(index=False))
print()
print("Bottom 5 by 2024 GDP:")
print(top[["province", "gdp_2024_m_cny", "share_of_national_2024_pct"]].tail(5).to_string(index=False))
print()
print("National 2024 GDP, million CNY: 134806620")
print("Sum of provincial 2024 GDP:", prov.gdp_2024_m_cny.sum())
print("Gap: provincial figures sum to 99.2 percent of the national total.")
print("That gap is normal. National and provincial accounts are compiled")
print("separately and differ by statistical treatment, not by error in this table.")
"""),
    code("""
fig, ax = plt.subplots(figsize=(10, 6))
t10 = prov.sort_values("gdp_2024_m_cny", ascending=True).tail(10)
ax.barh(t10.province, t10.gdp_2024_m_cny / 1e6)
ax.set_xlabel("Trillion CNY, 2024")
ax.set_title("Top 10 provinces by GDP, 2024 (NBS, revised)")
ax.grid(True, axis="x", alpha=0.3)
plt.savefig(f"{CHARTS}/04_top10_gdp.png", dpi=150, bbox_inches="tight")
print("Guangdong plus Jiangsu share of national GDP:",
      round(prov[prov.province.isin(["Guangdong", "Jiangsu"])].share_of_national_2024_pct.sum(), 2), "percent")
print("saved 04_top10_gdp.png")
"""),
    code("""
fig, ax = plt.subplots(figsize=(10, 6))
pc = prov.sort_values("gdp_per_capita_2024_approx_cny", ascending=True)
ax.barh(pc.province, pc.gdp_per_capita_2024_approx_cny)
ax.set_xlabel("CNY per person (approximate: 2024 GDP divided by mid-2022 population)")
ax.set_title("GDP per person by province, approximate (NBS)")
ax.grid(True, axis="x", alpha=0.3)
plt.savefig(f"{CHARTS}/04_gdp_per_capita.png", dpi=150, bbox_inches="tight")
top_pc = pc.iloc[-1]
bot_pc = pc.iloc[0]
print("highest:", top_pc.province, top_pc.gdp_per_capita_2024_approx_cny, "CNY")
print("lowest:", bot_pc.province, bot_pc.gdp_per_capita_2024_approx_cny, "CNY")
print("ratio:", round(top_pc.gdp_per_capita_2024_approx_cny / bot_pc.gdp_per_capita_2024_approx_cny, 2))
print("saved 04_gdp_per_capita.png")
"""),
    md("## Who led and who lagged\n\n"
       "On size, the coast dominates. Guangdong (14.15 trillion yuan in 2024, 10.50 percent of the national total) and Jiangsu (13.67 trillion, 10.14 percent) together are more than a fifth of the economy. Shandong and Zhejiang follow. The bottom five, Qinghai, Ningxia, Hainan, Tibet, and Gansu, together are smaller than Zhejiang alone.\n\n"
       "On GDP per person, the municipalities lead: Beijing (about 227,000 yuan) and Shanghai (about 217,000 yuan), then Jiangsu, Fujian, and Zhejiang. The lowest are Gansu (about 52,000 yuan), Heilongjiang (about 53,000), and Guangxi (about 57,000). The top to bottom ratio is about 4.4 to 1. That gap is the regional inequality problem the plans keep trying to narrow.\n\n"
       "On 2025 growth (preliminary), Tibet grew fastest at 7.0 percent, and Liaoning slowest at 3.7 percent. Fast growth in a small western province and slow growth in the old industrial northeast is a pattern worth watching: the northeast, once the industrial heartland, has lagged for a decade as heavy industry and population loss bite.\n\n"
       "On urbanization (mid-2022), Shanghai (89.3 percent) and Beijing (87.6 percent) are the most urban, and Tibet (37.4 percent) the least, followed by Gansu and Yunnan. Henan, the third most populous province, is only 55.7 percent urban, which is why it still has one of the largest rural populations in the country."),
    code("""
fig, ax = plt.subplots(figsize=(10, 6))
u = prov.sort_values("urban_rate_2022_pct", ascending=True)
ax.barh(u.province, u.urban_rate_2022_pct)
ax.set_xlabel("Percent urban, mid-2022 (NBS)")
ax.set_title("Urbanization rate by province, 2022")
ax.grid(True, axis="x", alpha=0.3)
plt.savefig(f"{CHARTS}/04_urbanization.png", dpi=150, bbox_inches="tight")
print("most urban:", u.iloc[-1].province, u.iloc[-1].urban_rate_2022_pct)
print("least urban:", u.iloc[0].province, u.iloc[0].urban_rate_2022_pct)
print("saved 04_urbanization.png")
"""),
    code("""
fig, ax = plt.subplots(figsize=(10, 6))
m = prov.sort_values("gdp_multiple_2000_to_2024", ascending=True).tail(8)
ax.barh(m.province, m.gdp_multiple_2000_to_2024)
ax.set_xlabel("Times larger, 2024 GDP divided by 2000 GDP (nominal)")
ax.set_title("Fastest growing provinces since 2000 (nominal GDP multiple)")
ax.grid(True, axis="x", alpha=0.3)
plt.savefig(f"{CHARTS}/04_growth_since_2000.png", dpi=150, bbox_inches="tight")
print(m[["province", "gdp_multiple_2000_to_2024"]].to_string(index=False))
print("saved 04_growth_since_2000.png")
"""),
    md("## What this scorecard cannot show: the honest gaps\n\n"
       "- Energy intensity by province: no single public comparable table was found in this build. Provinces had different energy targets in the 11th, 12th, and 13th plans, but a clean current table was not available, so it is not charted.\n"
       "- Research spending by province: same problem. National research spending is known, but a comparable provincial table was not found, so it is not charted.\n"
       "- 2024 provincial populations: not fetched, so per person GDP uses mid-2022 populations and is labeled approximate.\n"
       "- Hong Kong and Macau are not in the provincial table. They are special administrative regions with separate statistical systems. Their 2025 GDP figures (Hong Kong 3.05 trillion yuan, Macau 0.37 trillion yuan on the same compilation) are noted here for completeness, not mixed into the mainland ranking.\n\n"
       "Next: notebook 05 looks at who lives where, and how the population is changing."),
]

# ================================================================= NB05
NB05 = [
    md("# 05. People and places: who lives where, and how that is changing\n\n"
       "China has about 1.4 billion people, but they are not spread evenly. One province, Guangdong, has more people than most countries. The west is vast and empty by comparison. This notebook covers population distribution, aging, urbanization, regional economies, ethnic composition from the 2020 census, and religion, where the numbers depend heavily on who is asking.\n\n"
       "## The national picture\n\n"
       "The 7th National Population Census, conducted in late 2020 and released May 11, 2021, counted 1,411.78 million people on the mainland. By the end of 2025, the NBS put the total at 1,404.89 million, down 3.39 million on the year, the fourth straight annual fall. The urban resident population in 2025 was 953.80 million, an urbanization rate of 67.89 percent, up 0.89 points on 2024. The population aged 16 to 59 was 851.36 million, 60.6 percent of the total.\n\n"
       "Births were 7.92 million in 2025 (a rate of 5.63 per thousand) and deaths were 11.31 million (8.04 per thousand), a natural growth rate of minus 2.41 per thousand. The birth rate is the lowest since 1949, and the death rate is the highest since 1968. Those two facts together explain why the population is shrinking."),
    code(SETUP + """
prov = pd.read_csv(f"{PROC}/provinces.csv")
reg = prov.groupby("region").agg(gdp=("gdp_2024_m_cny", "sum"),
                                  pop=("pop_mid2022", "sum"),
                                  urban=("urban_pop_mid2022", "sum"))
reg["urban_rate"] = (reg["urban"] / reg["pop"] * 100).round(1)
reg = reg.sort_values("gdp", ascending=False)
print(reg.to_string())
print()
print("East region share of provincial GDP:",
      round(reg.loc["East", "gdp"] / reg["gdp"].sum() * 100, 1), "percent")
print("Northeast share:", round(reg.loc["Northeast", "gdp"] / reg["gdp"].sum() * 100, 1), "percent")
"""),
    code("""
fig, ax = plt.subplots(figsize=(10, 5.5))
r = reg.sort_values("gdp")
ax.barh(r.index, r.gdp / 1e6)
ax.set_xlabel("Trillion CNY, 2024 (sum of provincial GDP)")
ax.set_title("Regional GDP: East China is nearly 40 percent of the total")
ax.grid(True, axis="x", alpha=0.3)
plt.savefig(f"{CHARTS}/05_regional_gdp.png", dpi=150, bbox_inches="tight")
print("saved 05_regional_gdp.png")
"""),
    md("## Regions in words\n\n"
       "East China (Shanghai, Jiangsu, Zhejiang, Anhui, Fujian, Jiangxi, Shandong) is the economic core: about 52.1 trillion yuan in 2024, nearly 40 percent of the provincial total. South Central China (Henan, Hubei, Hunan, Guangdong, Guangxi, Hainan) is second at about 35.4 trillion, carried by Guangdong. The North (Beijing, Tianjin, Hebei, Shanxi, Inner Mongolia) and Southwest (Chongqing, Sichuan, Guizhou, Yunnan, Tibet) are each around 15 to 17 trillion. The Northwest is about 7.8 trillion and the Northeast, once the industrial base, is last at about 6.3 trillion, with the slowest growth and a shrinking population.\n\n"
       "The population map tells the same story from the other side. Guangdong had 126.01 million people in the 2020 census, Shandong 101.53 million, Henan 99.37 million. Tibet had 3.65 million, Qinghai 5.92 million, Ningxia 7.20 million. The east is crowded and rich. The west is spacious and poorer. Every plan since the 10th has promised to narrow that gap, and the gap is still there."),
    code("""
eth = pd.read_csv(f"{PROC}/ethnic_2020.csv")
fig, ax = plt.subplots(figsize=(10, 5.5))
e = eth.sort_values("share_pct", ascending=True)
ax.barh(e.group, e.share_pct)
ax.set_xlabel("Percent of mainland population, 2020 census")
ax.set_title("Ethnic composition, 2020 census (Han 91.11 percent)")
ax.grid(True, axis="x", alpha=0.3)
plt.savefig(f"{CHARTS}/05_ethnic.png", dpi=150, bbox_inches="tight")
print(eth.to_string(index=False))
print("shares are the census bulletin's published rounded figures, so they sum to about 100")
print("saved 05_ethnic.png")
"""),
    md("## Ethnic composition: what the census says\n\n"
       "The 2020 census counted 1,286.31 million Han people, 91.11 percent of the mainland population, and 125.47 million people from ethnic minorities, 8.89 percent. The largest minority groups are the Zhuang (19.57 million, 1.39 percent), Uyghur (11.77 million, 0.84 percent), Hui (11.38 million, 0.81 percent), Miao (11.07 million, 0.79 percent), and Manchu (10.42 million, 0.74 percent). The remaining minorities together are 61.26 million people, 4.34 percent.\n\n"
       "Two notes. First, the census asks about ethnicity, and these are self-reported census categories, not estimates. Second, minorities are concentrated in the west and south: Xinjiang, Tibet, Inner Mongolia, Guangxi, Ningxia, and Yunnan have large minority shares, which is part of why regional policy and ethnic policy overlap.\n\n"
       "## Religion: why the numbers disagree so much\n\n"
       "The census does not ask about religion. Every religion figure for China is therefore a survey or administrative estimate, and the estimates differ wildly because they measure different things: belief, practice, affiliation, registered membership, and folk religion overlap. The chart below puts three published estimates side by side. Do not read any one of them as the true figure.\n\n"
       "- Pew Research Center (2023, self-identified affiliation): no religion 93.0 percent, Buddhism 3.7 percent, Christianity 1.4 percent, Islam 1.3 percent, folk beliefs 0.2 percent. This counts people who name a religion when asked.\n"
       "- CIA World Factbook (2021, among people claiming a belief): unaffiliated 52.1 percent, folk beliefs 21.9 percent, Buddhism 18.2 percent, Christianity 5.1 percent, Islam 1.8 percent. This counts folk religion and belief more broadly, so the religious shares look much larger.\n"
       "- China Social Survey (2010): ancestor and god cults 56.2 percent, Buddhism 13.8 percent, Taoist folk religions 12.9 percent, Christianity 2.4 percent, Islam 1.7 percent, Taoism 0.9 percent. This counts practice and folk belief, which overlap heavily.\n\n"
       "The government formally recognizes five religions: Buddhism, Taoism, Islam, Catholicism, and Protestantism. The official Christian count is about 44 million (38 million Protestant plus 6 million Catholic, as of 2018 in secondary summaries), while independent estimates that include unregistered house churches put the total at 70 to 100 million or higher by 2024. The gap between the official and independent counts is itself the story: registration, not belief, is what the official number measures."),
    code("""
rel = pd.read_csv(f"{PROC}/religion_estimates.csv")
fig, ax = plt.subplots(figsize=(10, 6))
groups = ["Buddhism", "Christianity", "Islam", "Folk beliefs"]
sources = ["Pew Research Center 2023, self-identified",
           "CIA World Factbook 2021, among people claiming a belief",
           "China Social Survey 2010"]
import numpy as np
x = np.arange(len(groups))
width = 0.25
for i, src in enumerate(sources):
    vals = []
    for gname in groups:
        hit = rel[(rel.source == src) & (rel.group == gname)]
        vals.append(hit.share_pct.iloc[0] if len(hit) else 0)
    ax.bar(x + (i - 1) * width, vals, width, label=src.split(",")[0])
ax.set_xticks(x)
ax.set_xticklabels(groups)
ax.set_ylabel("Percent (each survey uses a different question)")
ax.set_title("Religion estimates differ because the questions differ")
ax.legend(fontsize=8)
ax.grid(True, axis="y", alpha=0.3)
plt.savefig(f"{CHARTS}/05_religion.png", dpi=150, bbox_inches="tight")
print("saved 05_religion.png")
"""),
    code("""
fig, ax = plt.subplots()
wb = pd.read_csv(f"{PROC}/wb_longrun.csv")
a = wb.dropna(subset=["pop_65_pct", "pop_0_14_pct"])
ax.plot(a.year, a.pop_65_pct, label="Aged 65 and over")
ax.plot(a.year, a.pop_0_14_pct, label="Aged 0 to 14")
ax.set_ylabel("Percent of population")
ax.set_xlabel("Year")
ax.set_title("Aging in one chart: children fall, seniors rise (World Bank)")
ax.legend()
ax.grid(True, alpha=0.3)
plt.savefig(f"{CHARTS}/05_age_structure.png", dpi=150, bbox_inches="tight")
print("65 and over, 2024:", a[a.year == 2024].pop_65_pct.iloc[0])
print("0 to 14, 2024:", a[a.year == 2024].pop_0_14_pct.iloc[0])
print("saved 05_age_structure.png")
"""),
    md("## Aging: the slow change that matters most\n\n"
       "The age chart is the most important chart in this notebook. The share of children falls steadily from the 1970s onward, and the share of seniors rises steadily from the 2000s onward. The two lines are heading toward each other. An economy with fewer young workers and more retirees grows more slowly, spends more on pensions and health care, and needs higher productivity from each worker just to stand still. That is the demographic headwind the 15th plan has to plan around, and it is why the plan puts 7 of its 20 indicators on livelihood and well-being.\n\n"
       "Next: notebook 06 looks at what the 15th plan aims at, and what to watch."),
]

# ================================================================= NB06
NB06 = [
    md("# 06. What is next: the 15th Five Year Plan, 2026 to 2030\n\n"
       "The 15th Five Year Plan was adopted on March 12, 2026, by the National People's Congress, at the closing session of the fourth session of the 14th Congress. It has 20 main indicators across five dimensions (economic development, innovation, livelihood and well-being, green development, and security and resilience), 18 parts, 62 chapters, and 109 major projects. It also comes with a new law on national development planning, setting rules for how future plans are made.\n\n"
       "## The headline goal\n\n"
       "The core objective is to lay a solid foundation for doubling GDP per person by 2035 compared with 2020. That needs average growth of about 4.17 percent a year over the decade, according to EIAS analysis. That is slower than the 14th plan's 5.4 percent, and slower than any plan period since the 1990s, which tells you how much the growth model has changed.\n\n"
       "## The 2026 starting point\n\n"
       "The annual growth target for 2026 is 4.5 to 5.0 percent, described in secondary analysis as the lowest since 1991. Early data, from InsightBridge analysis citing NBS figures, shows GDP up 4.6 percent in the first three quarters of 2026, surveyed urban unemployment at 5.2 percent in September 2026, and youth unemployment (ages 16 to 24, excluding students) at 18.0 percent in September 2026. Per person disposable income in the first three quarters of 2026 was 34,230 yuan, up 5.3 percent nominal and 4.4 percent real. These are secondary analysis figures citing NBS, not primary releases, and they are labeled that way."),
    code(SETUP + """
t15 = pd.read_csv(f"{PROC}/plan_15th_targets.csv")
print(t15[["indicator", "target_2030", "type"]].to_string(index=False))
"""),
    code("""
fig, ax = plt.subplots(figsize=(10, 6))
rows = [
    ("Digital economy share of GDP", 10.5, 12.5),
    ("Patents per 10,000 people", 16, 22),
    ("Working-age education, years", 11.3, 11.7),
    ("Life expectancy, years", 79.0, 80.0),
    ("Forest coverage", 25.0, 25.8),
    ("Non-fossil share of energy", 21.7, 25.0),
]
labels = [r[0] for r in rows]
v2025 = [r[1] for r in rows]
v2030 = [r[2] for r in rows]
y = range(len(rows))
ax.barh([i + 0.2 for i in y], v2025, height=0.4, label="2025 actual (or latest)", color="#969696")
ax.barh([i - 0.2 for i in y], v2030, height=0.4, label="2030 target", color="#2c7fb8")
ax.set_yticks(list(y))
ax.set_yticklabels(labels)
ax.set_title("15th plan: where China starts vs where it aims (different units, one chart)")
ax.legend()
ax.grid(True, axis="x", alpha=0.3)
plt.savefig(f"{CHARTS}/06_targets_2030.png", dpi=150, bbox_inches="tight")
print("saved 06_targets_2030.png")
print("Note: education 2025 value 11.3 is the 14th plan target, used as the start point")
print("because no verified 2025 actual was found. See notebook 03.")
"""),
    md("## The targets, and where the sources disagree\n\n"
       "- Research spending growth is reconfirmed at a minimum of 7 percent a year.\n"
       "- Core digital economy value added is targeted at 12.5 percent of GDP by 2030, up from 10.5 percent in 2024.\n"
       "- High-value invention patents are targeted at over 22 per 10,000 people by 2030, up from 16 in 2025.\n"
       "- Working-age education is targeted at 11.7 years by 2030, binding, up from the 14th plan target of 11.3 years.\n"
       "- Life expectancy is targeted at 80 years by 2030, up from 79.0 years (official, 2024).\n"
       "- Carbon intensity is targeted to fall about 17 percent over the plan, binding. One summary table brackets 17.7 percent. Both figures are shown, not settled.\n"
       "- Non-fossil energy share is targeted at 25 percent by 2030, binding, in the ICBC and Fidelity summaries. The iGDP summary cites about 27 percent from Government Work Report proposals. Both figures are shown, not settled.\n"
       "- PM2.5 is targeted at under 27 micrograms per cubic meter by 2030, binding, down from 28 in 2025.\n"
       "- Forest coverage is targeted at 25.8 percent by 2030, binding, up from past 25 percent in 2025.\n"
       "- Grain production capacity is targeted at 725 million tons by 2030, binding, up from over 650 million tons in the 14th plan.\n"
       "- Energy production capacity is targeted at 5.8 billion tons of coal equivalent by 2030, up from over 4.6 billion tons.\n"
       "- 7 of the 20 indicators cover livelihood and well-being: education, health, elderly care, and childcare. That is the plan's biggest shift in emphasis.\n\n"
       "## What changed in tone\n\n"
       "Two small details say a lot. Artificial intelligence is mentioned 52 times in the 15th plan text, against 11 times in the 14th, according to South China Morning Post analysis cited in secondary summaries. And dual circulation, the slogan of the 14th plan, appears only once. The Made in China 2025 goal of 70 percent chip self-sufficiency, described in secondary analysis as largely missed, is dropped rather than repeated. The plan is more about technology, services, and living standards than about raw speed.\n\n"
       "## What to watch\n\n"
       "1. Growth versus the 4.17 percent decade average. If growth falls below about 4 percent for several years, the 2035 doubling goal slips out of reach.\n"
       "2. Carbon intensity. The 14th plan missed its carbon target. The 15th plan's carbon target is binding, so a second miss would be harder to explain.\n"
       "3. Youth unemployment. At 18.0 percent in September 2026 (excluding students), it is the most politically sensitive number in the plan.\n"
       "4. Births and the population. The population fell for a fourth straight year in 2025. Childcare subsidies started in January 2026 (3,600 yuan a year per child under 3). Watch whether births stabilize.\n"
       "5. Property and debt. Property sales are down 54 percent from 2021, and total non-financial debt is near 296 percent of GDP. The plan's growth math assumes these do not blow up.\n"
       "6. The non-fossil and carbon target discrepancy. If the adopted plan text settles on 27 percent rather than 25 percent for non-fossil energy, or 17.7 percent rather than 17 percent for carbon, this notebook should be updated. Both figures are kept until the plan text is checked.\n\n"
       "## How this project ends\n\n"
       "China's planning story is not a simple success or failure. It is a system that produced the fastest long boom in modern history, caused one of the worst famines in history, cleaned up some of its pollution, missed its carbon target, lifted hundreds of millions out of poverty, and now faces a shrinking population and a heavy debt pile. The plans are worth studying because they show what a government can and cannot do with targets: they can move a whole country in one direction, but they cannot repeal arithmetic. Growth slows, people age, and coal still burns. The next plan will be judged the same way this project judges the last one: target by target, with the year on every figure, and both sides of every disputed number shown."),
]

write_nb("00_setup.ipynb", NB00)
write_nb("01_how_planning_works.ipynb", NB01)
write_nb("02_plans_through_history.ipynb", NB02)
write_nb("03_the_14th_plan_scorecard.ipynb", NB03)
write_nb("04_provincial_scorecard.ipynb", NB04)
write_nb("05_people_and_places.ipynb", NB05)
write_nb("06_whats_next.ipynb", NB06)
print("ALL NOTEBOOKS WRITTEN")
