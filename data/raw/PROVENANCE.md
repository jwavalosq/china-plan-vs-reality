# PROVENANCE: every source used, and what was taken from it

All research and fetching was done on November 2, 2026. Where a page could
not be fetched directly, the figures come from search-result reporting of
that document and are labeled that way in the notebooks.

## World Bank, World Development Indicators (API, no key)

Fetched by `scripts/fetch_worldbank.py` into `data/raw/wb_*.json`, then
merged into `data/processed/wb_longrun.csv`.

Series used: GDP current USD (NY.GDP.MKTP.CD), GDP per capita USD
(NY.GDP.PCAP.CD), GDP growth percent (NY.GDP.MKTP.KD.ZG), population
(SP.POP.TOTL), urban population share (SP.URB.TOTL.IN.ZS), life expectancy
(SP.DYN.LE00.IN), fertility (SP.DYN.TFRT.IN), poverty at 2.15 dollars a day
(SI.POV.DDAY), exports and imports as percent of GDP (NE.EXP.GNFS.ZS,
NE.IMP.GNFS.ZS), energy use per capita (EG.USE.PCAP.KG.OE), forest area
share (AG.LND.FRST.ZS), research spending share (GB.XPD.RSDV.GD.ZS),
age dependency (SP.POP.DPND), population 65 and over (SP.POP.65UP.TO.ZS),
population 0 to 14 (SP.POP.0014.TO.ZS), rural population share
(SP.RUR.TOTL.ZS).

Coverage: most series 1960 to 2025, poverty 1981 to 2022, research spending
1996 to 2023. The CO2 per capita series (EN.ATM.CO2E.PC) returned zero
points from the API and was dropped; see BUILD_REPORT.md.

## National Bureau of Statistics, 2025 Statistical Communique (Feb 28, 2026)

Figures as reported in search results of the communique (a direct fetch of
the stats.gov.cn page failed in the research session and was not retried
for that URL). Used for: GDP 140,187.9 billion yuan, up 5.0 percent;
quarterly growth 5.4, 5.2, 4.8, 4.5 percent; per capita GDP 99,665 yuan
(13,953 dollars); per capita disposable income 43,377 yuan, up 5.0 percent
real; urban disposable income 56,502 yuan; rural 24,456 yuan; urban-rural
ratio 2.31; total population 1,404.89 million, down 3.39 million; urban
resident population 953.80 million; urbanization 67.89 percent, up 0.89
points; births 7.92 million; deaths 11.31 million; natural growth minus
2.41 per thousand; population aged 16 to 59: 851.36 million (60.6 percent);
energy output 5.13 billion tons of coal equivalent; energy consumption
6.17 billion tons; coal share 51.4 percent; clean energy share 30.4
percent (a broader definition than non-fossil, and labeled as such);
grain output above 700 million tons for a second straight year; urban
jobs 12.67 million in 2025; surveyed urban unemployment 5.2 percent
average (December 5.1 percent); labor productivity 184,413 yuan per
person, up 6.1 percent.

## Government Work Report, delivered March 5, 2026

Used for: the statement that all 20 major 14th plan targets were
accomplished; average growth of 5.4 percent over the plan period; research
spending up about 10 percent a year on average; forest coverage past 25
percent in 2025; grain capacity target of 725 million tons and energy
capacity of 5.8 billion tons of coal equivalent for the 15th plan.

## Ministry of Ecology and Environment, via Xinhua (Jan and Mar 2026)

Used for: good air quality days 89.3 percent in 2025 (record, up 1.9
points); PM2.5 average 28 micrograms per cubic meter in 2025, down 4.4
percent on the year and 20 percent over five years; surface water good
quality share 91.4 percent in 2025, up 1 point; coastal waters good
quality 84.9 percent.

## iGDP China Carbon Neutrality Tracker newsletter (Jan-Feb 2026 issue)

Used for: full-period 14th plan energy intensity reduction of 15 percent
against a 13.5 percent target, carbon intensity reduction of about 12
percent against an 18 percent target, and non-fossil energy share of 21.7
percent in 2025 against about 20 percent. These are tracker figures, not
official releases, and are labeled that way.

## NDRC / State Council Information Office (Aug 12, 2025)

Used for: energy intensity reduction of 11.6 percent for 2021 to 2024
only. Shown next to the full-period tracker figure so the two are not
confused.

## UBP macroeconomics table (Nov 2025)

Used for: life expectancy 79.0 years, physicians 3.4 per 1,000, pension
coverage 95.0 percent, childcare slots 4.1 per 1,000. This table appears
to use 2024 actuals, published before final 2025 data, so every figure
from it is labeled with the year 2024 in the scorecard.

## CNIPA via Xinhua

Used for: high-value invention patents per 10,000 people, 16 at end-2025
(2.29 million high-value patents held; valid invention patents 6.318
million, up 11.1 percent), against a target of 12.

## InsightBridge analysis (Oct 22, 2026, citing NBS)

Used for: 2025 research spending about 3.93 trillion yuan, up 8.2
percent, intensity 2.80 percent of GDP, above the OECD average of 2.72
percent; 2026 first three quarters GDP up 4.6 percent; September 2026
surveyed urban unemployment 5.2 percent; youth unemployment 18.0
percent in September 2026; first three quarters 2026 disposable income
34,230 yuan and consumption spending 22,354 yuan. Labeled as secondary
analysis citing NBS, not as primary releases.

## EIAS analysis (15th plan)

Used for: 20 main indicators across five dimensions; 18 parts and 62
chapters; core objective of laying the foundation for doubling per
capita GDP by 2035 from 2020, needing about 4.17 percent average annual
growth; 7 of 20 indicators on livelihood and well-being.

## ICBC and Fidelity secondary 15th plan tables

Used as leads for: digital economy core 12.5 percent of GDP by 2030;
patents over 22 per 10,000 by 2030; working-age education 11.7 years by
2030 (binding); life expectancy 80 years by 2030; carbon intensity
reduction about 17 percent (Fidelity brackets 17.7 percent); non-fossil
share 25 percent by 2030; PM2.5 under 27 micrograms per cubic meter by
2030 (binding); forest coverage 25.8 percent by 2030 (binding). Where
these tables disagree with the iGDP summary (non-fossil 27 percent,
carbon 17.7 percent), both figures are kept and the disagreement is
flagged. These tables contain known inconsistencies elsewhere (for
example a surface water baseline that does not match the Ministry
figure), so no figure from them is used without a second check or a
flag.

## Wikipedia: Five-year plans of China

Used for: plan history narrative, including the 2nd plan agricultural
target of plus 270 percent against an actual gain of 35 percent, the
3rd plan defense shift, the 5th plan impossible steel and oil targets,
the 6th plan first solar support, the 11th plan introduction of binding
targets (22 targets, 8 binding), and the absence of any plan covering
1963 to 1965.

## Wikipedia: List of Chinese administrative divisions by GDP

Used for: provincial GDP in million CNY for 2025 (preliminary), 2024
(revised), and 2000, plus 2025 real growth rates, citing NBS data. The
national 2025 total on this table (140,187,920 million CNY) matches the
NBS communique exactly, which cross-checks the table.

## Wikipedia: List of Chinese administrative divisions by population

Used for: mid-year 2022 provincial populations with urban and rural
splits (NBS figures), the six conventional regions, and the 2020 census
provincial populations. Note: this page shows two slightly different
2022 totals for Guangdong (127.06 million in the main table, 126.57
million in the regional table). This project uses the main table
consistently.

## Seventh National Population Census (2020, released May 11, 2021)

Used for: mainland population 1,411.78 million; Han 1,286,310,000 (91.11
percent); ethnic minorities 125.47 million (8.89 percent); Zhuang
19,568,546; Uyghur 11,774,538; Hui 11,377,914; Miao 11,067,929; Manchu
10,423,303; male 723.34 million; female 685.32 million; urbanization
63.89 percent in 2020.

## Religion sources

Pew Research Center (2023, self-identified affiliation); CIA World
Factbook (2021 estimates among people claiming a belief); China Social
Survey (2010). Official Christian count of about 44 million (38 million
Protestant plus 6 million Catholic, as of 2018) from secondary summaries
of official figures; independent estimates of 70 to 100 million or
higher by 2024 from secondary summaries. The census does not ask about
religion, so all religion figures are survey or administrative
estimates.

## Great Leap Forward famine estimates

Government statistics: about 15 million excess deaths. Ashton, Hill,
Piazza, and Zeitz (1984): about 30 million premature deaths. Cao Shuji:
32.5 million. Yang Jisheng, Tombstone: 36 million. Frank Dikotter, Mao's
Great Famine (2010): at least 45 million, from provincial archives, a
figure other scholars have questioned. Current Wikipedia summary of the
range: 15 to 46 million, with newer estimates concentrated between 30
million and 46 million. Hardest hit provinces by share dead: Anhui 18
percent, Chongqing 15 percent, Sichuan 13 percent, Guizhou 11 percent,
Hunan 8 percent.

## Plan target history sources

US-China Economic and Security Review Commission backgrounder on the
12th plan (2011), Appendix II: 11th plan GDP target 7.5 percent, actual
11.2 percent; 12th plan GDP target 7 percent. YaleGlobal / Stephen Roach
(Nov 2015): 13th plan GDP target around 6.5 percent, 12th plan actual
average about 7.8 percent. People's Daily (Mar 2016): 13th plan minimum
6.5 percent a year; 1978 to 2015 average growth 9.6 percent. NRDC issue
brief (Nov 2017): 12th plan energy intensity target minus 16 percent,
actual minus 18.2 percent. Korea-Europe Review and PLOS ONE papers:
11th plan energy intensity target minus 20 percent, actual minus 19.1
percent; 13th plan energy intensity target minus 15 percent, actual
about minus 13.8 percent, carbon target minus 18 percent, actual about
minus 22 percent, total energy cap 5.0 billion tons, actual about 4.97
billion tons.

## Policy history sources

Household responsibility system: grain output 304.8 million tons in
1978 to 407.3 million tons in 1984 (academic paper via S3, citing NBS;
also China Agricultural University summary). Special Economic Zones:
four zones in 1980 (Shenzhen, Zhuhai, Shantou, Xiamen); Shenzhen growth
about 54 percent a year 1980 to 1984; four zones took 26 percent of
China's foreign investment in 1984 (same paper). Targeted poverty
alleviation: 98.99 million people, 832 counties, 128,000 villages, about
1.6 trillion yuan in special funds (State Council Information Office
briefing, Mar 2020; State Council white paper, 2021). Births: NBS annual
communiques, 2016 to 2025 series as reported in 2026 coverage of the
2025 communique. Debt and property: Congressional Research Service
report (2026): total non-financial debt 296 percent of GDP in Q3 2025;
IMF local government debt 39 percent of GDP and financing vehicle debt
51 percent of GDP in 2025; property sales value down 54 percent since
2021; Evergrande default 2021 on 305 billion dollars, liquidation
ordered 2024, delisted August 2025. Bruegel (2026): public debt about
100 percent of GDP; trade surplus about 1 trillion dollars in 2024;
real estate about a third of growth and fixed-asset investment before
the crash; solar panel capital investment share near 90 percent.
