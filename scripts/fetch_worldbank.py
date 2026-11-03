"""Fetch World Bank WDI series for China (no key needed) into data/raw/."""
import json, os, urllib.request

OUT = os.path.join(os.path.dirname(__file__), "..", "data", "raw")
os.makedirs(OUT, exist_ok=True)

INDICATORS = {
    "gdp_current_usd": "NY.GDP.MKTP.CD",
    "gdp_per_capita_usd": "NY.GDP.PCAP.CD",
    "gdp_growth_pct": "NY.GDP.MKTP.KD.ZG",
    "population": "SP.POP.TOTL",
    "urban_pop_pct": "SP.URB.TOTL.IN.ZS",
    "life_expectancy": "SP.DYN.LE00.IN",
    "fertility": "SP.DYN.TFRT.IN",
    "poverty_215": "SI.POV.DDAY",
    "exports_pct_gdp": "NE.EXP.GNFS.ZS",
    "imports_pct_gdp": "NE.IMP.GNFS.ZS",
    "energy_use_per_capita": "EG.USE.PCAP.KG.OE",
    "co2_per_capita": "EN.ATM.CO2E.PC",
    "forest_pct": "AG.LND.FRST.ZS",
    "r_and_d_pct_gdp": "GB.XPD.RSDV.GD.ZS",
    "unemployment": "SL.UEM.TOTL.ZS",
    "school_enrollment_secondary": "SE.SEC.ENRR",
    "age_dependency": "SP.POP.DPND",
    "pop_65_pct": "SP.POP.65UP.TO.ZS",
    "pop_0_14_pct": "SP.POP.0014.TO.ZS",
    "rural_pop_pct": "SP.RUR.TOTL.ZS",
}

def fetch(code):
    url = (f"https://api.worldbank.org/v2/country/CHN/indicator/{code}"
           f"?format=json&per_page=20000&date=1960:2025")
    req = urllib.request.Request(url, headers={"User-Agent": "china-plan-portfolio/1.0"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        data = json.load(resp)
    rows = []
    if isinstance(data, list) and len(data) > 1 and data[1]:
        for r in data[1]:
            rows.append({"year": int(r["date"]), "value": r["value"]})
    return sorted(rows, key=lambda x: x["year"])

summary = {}
for name, code in INDICATORS.items():
    try:
        rows = fetch(code)
        with open(os.path.join(OUT, f"wb_{name}.json"), "w") as f:
            json.dump(rows, f)
        vals = [r for r in rows if r["value"] is not None]
        summary[name] = (len(vals), vals[0]["year"] if vals else None,
                         vals[-1]["year"] if vals else None)
        print(name, "->", len(vals), "points", summary[name][1], "to", summary[name][2])
    except Exception as e:
        print(name, "FAILED:", e)
        summary[name] = ("FAILED", str(e))
with open(os.path.join(OUT, "wb_summary.json"), "w") as f:
    json.dump(summary, f, indent=1)
print("done")
