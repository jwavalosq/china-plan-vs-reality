# China: Plan vs Reality

How does a country plan its economy in five year blocks? Did the last plan hit its targets? How do the provinces differ? Who lives where? And what comes next?

This project answers those questions in plain words, with numbers you can check. It is written for a beginner. Every idea is explained before it is used, and every number names its source.

China does not hold competitive presidential elections, so there is no elections chapter here. This is a planning, demographics, and macroeconomics project.

## Start here

Read the notebooks in order. Each one ends by pointing to the next.

1. `notebooks/00_setup.ipynb`. What the project is, where the data comes from, and the checks that prove the data loaded correctly.
2. `notebooks/01_how_planning_works.ipynb`. The five year cycle, step by step. Binding targets (promises) versus indicative targets (goals). The long-range objectives through 2035. A timeline of all 15 plans.
3. `notebooks/02_plans_through_history.ipynb`. The long story, from the first plan in 1953 to today. Plan targets versus actual outcomes, long-run charts for growth, poverty, health, cities, and trade, and an honest judgment of 14 big policies, including the failures.
4. `notebooks/03_the_14th_plan_scorecard.ipynb`. The 14th plan (2021 to 2025), scored target by target: 17 met, 2 missed, 1 not yet reported.
5. `notebooks/04_provincial_scorecard.ipynb`. All 31 mainland provinces compared on GDP, GDP per person, growth, urbanization, and change since 2000.
6. `notebooks/05_people_and_places.ipynb`. Population distribution, aging, regional economies, ethnic composition from the 2020 census, and religion, where three published estimates disagree and all three are shown.
7. `notebooks/06_whats_next.ipynb`. The 15th plan (2026 to 2030): what was adopted, its headline targets, where the sources disagree, and what to watch.

## The headline findings

- Growth: from 1978 to 2015, the economy grew about 9.8 percent a year on World Bank data. GDP per person rose from 157 dollars in 1978 to 13,293 dollars in 2024.
- Poverty: extreme poverty at the World Bank 2.15 dollar line fell from 97.0 percent in 1981 to 0.0 percent in 2019. On China's own rural line, the official count fell from 770 million in 1978 to zero in 2020.
- Health: life expectancy rose from 63.1 years in 1978 to 78.0 years in 2024 on the World Bank series. The official figure for 2024 is 79.0 years. Both are shown.
- Cities: the urban share rose from 17.9 percent in 1978 to 67.89 percent in 2025 (NBS permanent resident rate).
- The 14th plan: 17 of 20 quantitative targets met, 2 missed (carbon intensity, about 12 percent against 18 percent; childcare slots, 4.1 against 4.5), and 1 not yet reported (working-age education, no verified 2025 actual found). The Government Work Report states all 20 were accomplished. Both claims are shown, side by side, and the project takes no position on which characterization is correct.
- Provinces: Guangdong (14.15 trillion yuan in 2024) and Jiangsu (13.67 trillion) together are more than a fifth of the economy. GDP per person runs from about 227,000 yuan in Beijing to about 52,000 yuan in Gansu, a ratio of about 4.4 to 1.
- People: the 2020 census counted 1,411.78 million people, 91.11 percent Han and 8.89 percent ethnic minorities. By the end of 2025 the total was 1,404.89 million, the fourth straight annual fall. Births fell from 17.86 million in 2016 to 7.92 million in 2025.
- The 15th plan: adopted March 12, 2026. Its core goal is to lay the foundation for doubling GDP per person by 2035 from 2020, which needs about 4.17 percent average growth a year. The 2026 growth target is 4.5 to 5.0 percent.

## The failures, not hidden

A famine during the Great Leap Forward (1958 to 1962) killed tens of millions. The death toll is contested: government statistics imply about 15 million excess deaths, while scholarly estimates range from 15 million to 46 million, with newer estimates concentrated between 30 million and 46 million. Named estimates are given in notebook 02, and no single number is presented as settled.

Other failures covered honestly: the Cultural Revolution (1966 to 1976), severe pollution from coal-led growth, overcapacity, debt near 296 percent of GDP in late 2025, a property crash (sales value down 54 percent from 2021), and a shrinking, aging population.

## How to run it

You need Python 3.12 and the packages in `requirements.txt`. Each notebook starts with a pip install cell, so it also runs in Google Colab.

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/jupyter nbconvert --to notebook --execute --inplace notebooks/*.ipynb
```

To rebuild the processed data from the raw files, run:

```bash
python3 scripts/build_processed.py
python3 scripts/build_notebooks.py
```

## Files

- `notebooks/`: 7 executed notebooks, zero cell errors.
- `charts/`: 20 charts, saved as PNG files.
- `data/raw/`: World Bank series as fetched, plus `PROVENANCE.md` with every source.
- `data/processed/`: tidy CSVs the notebooks read.
- `scripts/`: `fetch_worldbank.py` (downloads the World Bank series, no key needed), `build_processed.py`, `build_notebooks.py`.
- `BUILD_REPORT.md`: exactly what was used, what ran, what failed, what was approximated, and what was cut.

## Rules this project follows

- Official figures are labeled official. Independent figures are labeled independent.
- Where sources disagree, both figures are shown and no side is taken.
- Where a figure could not be verified, the project says so and does not guess.
- Nothing is faked: no invented dataset, map, or test.
