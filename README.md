# China: Plan vs Reality

I started with a simple question. How does a country plan its economy in five year blocks, and does the plan actually work?

I had heard the big claims about China for years. Fast growth. Hundreds of millions lifted out of poverty. A state that sets targets and hits them. I wanted to test those claims myself, with public data I could check, instead of taking anyone's word for it. That is what this project does.

Read it as a story: https://jwavalosq.github.io/china-plan-vs-reality/

## Why this matters

China is the world's second largest economy, and its five year plans shape what gets built, what gets funded, and where people live and work. If you hire, invest, trade, or make policy, you will run into those plans sooner or later. But most writing about them is either praise or alarm, with very little counting in between.

I built this project for people who want the counting. A recruiter, a manager, or a curious reader should be able to follow it with no background in economics and no background in China. Every idea is explained before I use it, and every number names its source.

One thing to know up front: China does not hold competitive presidential elections, so there is no elections chapter here. This is a planning, demographics, and macroeconomics project.

## What I did

I worked through the story in seven notebooks, in order, and I kept each step plain enough to redo.

1. `notebooks/00_setup.ipynb`. I set up the project, loaded the data, and ran checks to prove the data loaded correctly.
2. `notebooks/01_how_planning_works.ipynb`. I mapped the five year cycle, step by step, from research and public consultation to the Party leadership setting direction to the National People's Congress formally adopting the plan. I explain the difference between binding targets, which are promises with accountability, and indicative targets, which are goals to aim for.
3. `notebooks/02_plans_through_history.ipynb`. I traced the long story from the first plan in 1953 to today, charting growth, poverty, health, cities, and trade, and I judged 14 big policies honestly, including the failures.
4. `notebooks/03_the_14th_plan_scorecard.ipynb`. I scored the 14th plan (2021 to 2025) target by target: 17 met, 2 missed, 1 not yet reported.
5. `notebooks/04_provincial_scorecard.ipynb`. I compared all 31 mainland provinces on GDP, GDP per person, growth, urbanization, and change since 2000.
6. `notebooks/05_people_and_places.ipynb`. I looked at who lives where: population distribution, aging, regional economies, ethnic composition from the 2020 census, and religion, where three published estimates disagree and I show all three.
7. `notebooks/06_whats_next.ipynb`. I read the 15th plan (2026 to 2030): what was adopted, its headline targets, where the sources disagree, and what to watch next.

My main sources are World Bank Open Data and China's National Bureau of Statistics, plus the plan documents themselves. The full source list is in `data/raw/PROVENANCE.md`, and `BUILD_REPORT.md` records exactly what I used, what ran, what failed, what I approximated, and what I cut.

## What I found

Growth first. From 1978 to 2015, the economy grew about 9.8 percent a year on World Bank data. GDP rose from 59.8 billion dollars in 1960 to 149.8 billion in 1978 to 18,729.7 billion in 2024. GDP per person rose from 89.7 dollars in 1960 to 156.7 dollars in 1978 to 13,293 dollars in 2024. That is a real transformation, from one of the poorest countries on earth to the world's second largest economy. It came from planning plus markets, not from planning alone.

Poverty fell just as sharply. Extreme poverty at the World Bank 2.15 dollar a day line fell from 97.0 percent in 1981 to 0.0 percent in 2019. On China's own rural line, the official count fell from 770 million people at the end of 1978 to 98.99 million in 2012 to zero in 2020.

Health and cities changed too. Life expectancy rose from 33.4 years in 1960 to 63.1 years in 1978 to 78.0 years in 2024 on the World Bank series. The official figure for 2024 is 79.0 years, and I show both. The urban share rose from 17.9 percent in 1978 to 67.89 percent in 2025 on the national statistics office permanent resident rate.

Then I scored the most recent plan, and the scorecard is more mixed than the official story. Of the 14th plan's 20 quantitative targets, 17 were met, 2 were missed, and 1 is not yet reported. The two misses are carbon intensity, about 12 percent against an 18 percent target, and childcare slots, 4.1 per 1,000 children against a 4.5 target. The unreported one is working-age education, for which I found no verified 2025 actual. The Government Work Report states all 20 were accomplished. I show both claims side by side, and I take no position on which characterization is correct.

The provinces tell a second story: China is not one economy, it is 31 provincial economies of wildly different size and wealth. Guangdong (14.15 trillion yuan in 2024) and Jiangsu (13.67 trillion) together are more than a fifth of the national economy. GDP per person runs from about 227,000 yuan in Beijing to about 52,000 yuan in Gansu, a ratio of about 4.4 to 1.

The people chapter is the one that stayed with me. The 2020 census counted 1,411.78 million people, 91.11 percent Han and 8.89 percent ethnic minorities. By the end of 2025 the total was 1,404.89 million, the fourth straight annual fall. Births fell from 17.86 million in 2016 to 7.92 million in 2025.

Looking ahead, the 15th plan was adopted March 12, 2026. It has 20 indicators across 5 dimensions and 109 major projects. Its core goal is to lay the foundation for doubling GDP per person by 2035 from 2020, which needs about 4.17 percent average growth a year. The 2026 growth target is 4.5 to 5.0 percent.

## The failures, not hidden

I did not hide the failures, because a scorecard that only counts wins is not a scorecard.

A famine during the Great Leap Forward (1958 to 1962) killed tens of millions. The death toll is contested: government statistics imply about 15 million excess deaths, while scholarly estimates range from 15 million to 46 million, with newer estimates concentrated between 30 million and 46 million. I give the named estimates in notebook 02, and I present no single number as settled.

I also cover the Cultural Revolution (1966 to 1976), severe pollution from coal-led growth, overcapacity, debt near 296 percent of GDP in late 2025, a property crash with sales value down 54 percent from 2021, and a shrinking, aging population.

## What it means, and who it helps

Three lessons stand out for me. First, targets work best when they are specific and someone is accountable for them, which is why the binding targets matter more than the slogans. Second, growth targets were usually beaten in the fast years and missed when the economy slowed, while environmental targets were mixed, so a plan is a bet on the future, not a guarantee. Third, the next decade will be decided less by headline growth and more by whether China handles debt, property stress, falling births, and the carbon targets the 14th plan missed.

This project helps anyone who needs to explain China without hype: a hiring manager checking how I think, an analyst who wants a clean starting dataset, or a reader who wants to see the numbers behind the headlines. If you run the notebooks, you can check every claim yourself, and you can reuse the cleaned data for your own questions.

## How to run it yourself

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

## What is in this folder

- `notebooks/`: 7 executed notebooks, zero cell errors.
- `charts/`: 20 charts, saved as PNG files.
- `data/raw/`: World Bank series as fetched, plus `PROVENANCE.md` with every source.
- `data/processed/`: tidy CSVs the notebooks read.
- `scripts/`: `fetch_worldbank.py` (downloads the World Bank series, no key needed), `build_processed.py`, `build_notebooks.py`.
- `BUILD_REPORT.md`: exactly what was used, what ran, what failed, what was approximated, and what was cut.

## The limits, stated honestly

- Where sources disagree, I show both figures and take no side. That applies to the 14th plan completion claim, to life expectancy in 2024 (official 79.0 years versus World Bank 78.0), and to the 15th plan non-fossil and carbon targets, where two figures each are shown.
- The famine toll is an attributed range, 15 million to 46 million, never a single settled number.
- Provincial GDP per person is approximate: 2024 GDP divided by mid-2022 resident population, because a 2024 provincial population table was not fetched. It is labeled approximate everywhere it appears.
- Provincial energy intensity and provincial research spending are not charted, because no single public comparable table was found. I did not guess them.
- The inequality (Gini) series was not fetched, so I judge common prosperity as too early rather than as a number. The urban-rural income ratio of 2.31 in 2025 is shown instead.
- No provincial maps are included. No shapefile was fetched, and none was faked.
- One 15th plan target list found online was rejected because it contradicted verified data, for example it claimed urbanization would reach 60 percent when it was already 67.89 percent in 2025.
- The World Bank carbon dioxide per person series returned no data from the API and was dropped. Carbon is covered instead by plan target figures and the energy series.
- Full-year 2026 results do not exist yet. Figures for 2026 are labeled as first three quarters or September 2026, from secondary analysis citing national statistics.
- Official figures are labeled official. Independent figures are labeled independent. Where a figure could not be verified, I say so and do not guess. Nothing is faked: no invented dataset, map, or test.
