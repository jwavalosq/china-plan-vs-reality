# BUILD REPORT: China, Plan vs Reality

Build date: November 2, 2026. Local build only. Nothing was published,
pushed, posted, or signed into. The parent agent handles publishing.

## What was built

- Folder: `~/workspace/china-plan-vs-reality/`
- 7 notebooks, all executed end to end with zero cell errors (36 code
  cells total):
  - `notebooks/00_setup.ipynb` (4 code cells)
  - `notebooks/01_how_planning_works.ipynb` (2 code cells)
  - `notebooks/02_plans_through_history.ipynb` (11 code cells)
  - `notebooks/03_the_14th_plan_scorecard.ipynb` (4 code cells)
  - `notebooks/04_provincial_scorecard.ipynb` (6 code cells)
  - `notebooks/05_people_and_places.ipynb` (6 code cells)
  - `notebooks/06_whats_next.ipynb` (3 code cells)
- 20 charts in `charts/` (PNG files).
- 8 processed CSVs in `data/processed/`.
- 20 World Bank series JSON files in `data/raw/`.
- `README.md`, this report, `requirements.txt`, `.gitignore`,
  `data/raw/PROVENANCE.md`, and three build scripts in `scripts/`.

## How it was built

1. `scripts/fetch_worldbank.py` downloaded 20 World Bank indicator
   series for China from the public API (no key). 19 returned data. One
   returned zero points (see failures).
2. `scripts/build_processed.py` merged the World Bank series into
   `wb_longrun.csv` and wrote the provincial, scorecard, plan history,
   ethnic, religion, births, and 15th plan tables from verified figures.
3. `scripts/build_notebooks.py` generated the 7 notebooks, each with a
   top pip install cell using the kernel's own Python.
4. Notebooks were executed in place with
   `jupyter nbconvert --to notebook --execute --inplace`, kernel
   `china-plan` (project virtual environment), timeout 300 seconds.
5. Verification: every code cell has an execution count and no error
   output; chart files exist for all 20 saves; a text scan of the whole
   folder (excluding `.venv`) finds zero em-dash characters.

## Key verified findings (exact numbers)

- GDP: 59.8 billion dollars in 1960, 149.8 billion in 1978, 18,729.7
  billion in 2024 (World Bank). GDP per person: 89.7 dollars in 1960,
  156.7 in 1978, 13,293 in 2024.
- Growth averages on World Bank data: 1978 to 2015: 9.76 percent a year
  (People's Daily cites 9.6 percent, a vintage difference); 2006 to
  2010: 11.30 percent; 2011 to 2015: 7.91 percent; 2016 to 2020: 5.77
  percent; 2021 to 2025: 5.41 percent.
- Poverty at 2.15 dollars a day (World Bank): 97.0 percent in 1981,
  83.1 percent in 1990, 20.6 percent in 2010, 0.0 percent in 2019.
  Official rural poor: 770 million at end-1978, 98.99 million in 2012,
  zero in 2020.
- Life expectancy (World Bank): 33.4 years in 1960, 63.1 in 1978, 78.0 in
  2024. Official figure for 2024: 79.0 years. Both are shown.
- Urbanization: 17.9 percent in 1978, 36.4 percent in 2000, 65.9 percent
  in 2024 (World Bank); 67.89 percent in 2025 (NBS permanent resident
  rate).
- Fertility: 6.09 in 1970, 2.72 in 1978, 1.63 in 2000, about 1.0 in 2023
  and 2024 (World Bank).
- Trade: exports peaked at 35.5 percent of GDP in 2006, were 20.4
  percent in 2024 (World Bank).
- 14th plan scorecard: 17 met, 2 missed (carbon intensity about 12
  percent against 18 percent; childcare 4.1 against 4.5), 1 not yet
  reported (working-age education). The Government Work Report states
  all 20 were accomplished. Both claims are shown.
- 2025 official figures (NBS communique): GDP 140,187.9 billion yuan,
  up 5.0 percent; per capita GDP 99,665 yuan (13,953 dollars);
  disposable income 43,377 yuan, up 5.0 percent real; urbanization
  67.89 percent; good air days 89.3 percent; surface water good quality
  91.4 percent; forest past 25 percent; energy output 5.13 billion
  tons of coal equivalent; population 1,404.89 million, down 3.39
  million; births 7.92 million; deaths 11.31 million.
- Provinces (2024, NBS via Wikipedia compilation): Guangdong 14.15
  trillion yuan (10.50 percent of national), Jiangsu 13.67 trillion
  (10.14 percent). GDP per person approximate: Beijing about 227,000
  yuan, Shanghai about 217,000, Gansu about 52,000. Ratio top to
  bottom: about 4.4 to 1. 2025 growth: Tibet fastest at 7.0 percent,
  Liaoning slowest at 3.7 percent.
- Regions (2024, sum of provincial GDP): East 52.12 trillion yuan
  (39.0 percent of the provincial sum), South Central 35.44 trillion,
  North 16.67 trillion, Southwest 15.34 trillion, Northwest 7.84
  trillion, Northeast 6.33 trillion (4.7 percent).
- Census 2020: 1,411.78 million people; Han 91.11 percent; minorities
  8.89 percent (125.47 million); largest minorities Zhuang 19.57
  million, Uyghur 11.77 million, Hui 11.38 million, Miao 11.07 million,
  Manchu 10.42 million.
- Famine deaths: presented as an attributed range, never a single
  number. Government statistics imply about 15 million excess deaths.
  Scholarly estimates range 15 to 46 million, newer estimates
  concentrated 30 to 46 million. Named: Ashton about 30 million, Cao
  32.5 million, Yang 36 million, Dikotter at least 45 million.
- Debt and property: total non-financial debt 296 percent of GDP in
  Q3 2025 (Congressional Research Service summary); property sales
  value down 54 percent since 2021; Evergrande defaulted in 2021 on
  305 billion dollars, ordered into liquidation in 2024, delisted in
  August 2025.
- 15th plan (adopted March 12, 2026): 20 indicators, 5 dimensions, 109
  major projects; doubling per capita GDP by 2035 from 2020 needs about
  4.17 percent average growth; 2026 growth target 4.5 to 5.0 percent;
  digital economy 12.5 percent of GDP by 2030; patents over 22 per
  10,000 by 2030; education 11.7 years by 2030 (binding); life
  expectancy 80 years by 2030; grain capacity 725 million tons by
  2030 (binding); energy capacity 5.8 billion tons of coal equivalent
  by 2030.

## What failed or was approximated

- Direct fetch of the stats.gov.cn 2025 communique page failed in the
  research session. It was not retried for that URL. Communique figures
  in this project come from search-result reporting of that document
  and are labeled as such in PROVENANCE.md.
- The World Bank CO2 per capita series (EN.ATM.CO2E.PC) returned zero
  points from the API. It was dropped. Carbon is covered instead by
  plan target figures and the energy series.
- First CSV write used no quoting, so fields containing commas broke
  parsing (ParserError on the scorecard file). Fixed by rewriting the
  writer with the csv module and proper quoting. All CSVs now parse.
- First notebook run failed in notebook 05 with
  `TypeError: unsupported operand type(s) for /: 'int' and 'method'`
  because `DataFrame.pop` is a method, not the population column.
  Fixed by using bracket access (`reg["pop"]`, `reg["urban"]`).
- First pip install cell used bare `!pip install`, which resolved to
  the system pip under nbconvert and printed an
  externally-managed-environment error into every notebook. Fixed by
  using `!{sys.executable} -m pip install`, which uses the kernel's
  own Python. Pip cells are now clean.
- The era table in notebook 02: the World Bank growth series starts in
  1961, so the 1st plan row is blank and the 2nd plan row covers only
  1961 and 1962 (average minus 16.4 percent, the famine collapse
  years). The notebook text says this plainly.
- Provincial GDP per person is approximate: 2024 GDP divided by
  mid-2022 resident population, because a 2024 provincial population
  table was not fetched. Labeled approximate everywhere it appears.
- Provincial GDP figures sum to 99.2 percent of the national 2024
  total (133.76 trillion vs 134.81 trillion yuan). This is the normal
  gap between separately compiled national and provincial accounts,
  not an error in this table.
- Forest coverage 2025 is stated as "past 25 percent" in the source,
  not an exact figure. It is plotted as 25 in the targets chart and the
  chart label says so.
- The 15th plan chart in notebook 06 uses 11.3 years (the 14th plan
  target) as the 2025 start point for education, because no verified
  2025 actual was found. The chart note and the printed note say this.
- The 14th plan count: the project scores 20 quantitative targets (8
  binding, 12 indicative). GDP growth is listed separately as a
  direction with no number, because the 14th plan set no GDP number.
  Some sources count 20 main indicators including GDP growth, which
  would make 21 items. This project documents the counting choice
  instead of forcing the list to fit.
- The simple mean of the five published rounded 14th plan growth rates
  (8.4, 3.0, 5.2, 5.0, 5.0) is 5.32 percent, while the World Bank series
  averages 5.41 percent and the Government Work Report states 5.4
  percent. The notebook shows all three and notes the rounding and
  vintage difference.

## Cuts (things not included, and why)

- Energy intensity by province: no single public comparable table was
  found. Not charted, not guessed.
- Research spending by province: same reason. Not charted.
- 2024 provincial populations: not fetched. Mid-2022 populations used
  instead, labeled approximate.
- Income inequality (Gini) series: no recent verified series was
  fetched, so the common prosperity verdict is "too early" rather than
  a number. The urban-rural income ratio (2.31 in 2025) is shown
  instead.
- 2020 census age structure from the census bulletin: not re-verified
  in this session, so age structure uses the World Bank 65 and over
  and 0 to 14 series, labeled as such.
- 12th plan carbon intensity actual: not verified in this session, so
  it is not stated. Only the 17 percent target is given.
- 10th plan energy and carbon figures: not verified, not stated.
- Provincial choropleth maps: not built. No shapefile was fetched, and
  a map was never faked. Bar charts carry the provincial comparison.
- 2022 census demographic overlays: not applicable to China; no such
  cut exists here. (The Brazil project's IBGE cut does not apply.)
- 2026 full-year results: do not exist yet. 2026 figures are labeled
  as first three quarters or September 2026, from secondary analysis
  citing NBS.
- The danfetv article listing 15th plan targets (urbanization to 60
  percent, digital economy 40 percent of GDP, renewable energy 50
  percent) was rejected: it contradicts verified data (urbanization
  already 67.89 percent in 2025) and was not used anywhere.
- Fidelity and ICBC secondary tables were used only as leads. Where
  they disagree with each other or with iGDP (non-fossil 25 percent
  versus about 27 percent; carbon about 17 percent versus 17.7
  percent), both figures are kept and the disagreement is flagged.

## Disputed figures handled by attribution, not by picking a side

- Famine deaths: range with named sources (see above).
- 14th plan completion: official "all 20 accomplished" versus tracker
  arithmetic of 17 met, 2 missed, 1 not yet reported.
- Life expectancy 2024: official 79.0 years versus World Bank 78.0
  years. The scorecard scores the row met on the official figure and
  shows the World Bank cross-check.
- 15th plan non-fossil and carbon targets: two figures each, both
  shown, neither settled.
- Religion: three surveys with different questions, all shown, none
  presented as the true share.
- Urbanization: World Bank series runs lower than the NBS permanent
  resident rate. Both are used, each labeled.
