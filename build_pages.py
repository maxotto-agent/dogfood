"""Generate one static page per brand (brands/<slug>.html) and sitemap.xml from foods.json."""
import json, html, re, statistics, os
BASE = "https://maxotto-agent.github.io/dogfood/"
foods = json.load(open("foods.json"))
FOOT = "This application was autonomously scaffolded and deployed using generative software agents. Designed for lightweight, single-purpose utility. Curated and maintained by @maxim-k."
CSS = open("index.html").read().split("<style>")[1].split("</style>")[0]
CSS += "table{margin-top:.5rem}td.n,th.n{text-align:right;white-space:nowrap}"
slug = lambda b: re.sub(r"[^a-z0-9]+", "-", b.lower()).strip("-")
e = html.escape
brands = {}
for f in foods:
    brands.setdefault(f["brand"], []).append(f)

def page(title, desc, path, body):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{BASE}{path}">
<style>{CSS}</style>
</head>
<body>
<main>
{body}
<footer>{FOOT}</footer>
</main>
</body>
</html>
"""

os.makedirs("brands", exist_ok=True)
urls = [""]
for b, fs in sorted(brands.items()):
    fs = sorted(fs, key=lambda f: f["name"])
    cups = [f["kcal_cup"] for f in fs]
    lo, hi, med = min(cups), max(cups), round(statistics.median(cups))
    dates = sorted({f["checked"] for f in fs})
    rows = "\n".join(
        f'<tr><td><a href="{e(f["url"])}">{e(f["name"])}</a></td><td class="n">{f["kcal_cup"]}</td>'
        f'<td class="n">{f["kcal_kg"] if f.get("kcal_kg") else "–"}</td></tr>' for f in fs)
    lo_f = min(fs, key=lambda f: f["kcal_cup"]); hi_f = max(fs, key=lambda f: f["kcal_cup"])
    body = f"""<p class="sub"><a href="../">Dog food calorie calculator</a> › Brands</p>
<h1>{e(b)} dry dog food: calories per cup, {len(fs)} formulas</h1>
<p class="lead">Across {len(fs)} dry {e(b)} formulas, a cup holds {lo} to {hi} kcal (median {med}). The leanest is {e(lo_f["name"])} at {lo}; the richest is {e(hi_f["name"])} at {hi}. A cup of one {e(b)} formula is not a cup of another, so work out the daily amount from the exact formula.</p>
<p><a href="../"><b>Calculate cups per day for a {e(b)} formula →</b></a></p>
<table>
<tr><th>Formula (link: maker's page)</th><th class="n">kcal/cup</th><th class="n">kcal/kg</th></tr>
{rows}
</table>
<p class="sub">Figures are metabolizable energy as fed, copied from each formula's product page on the maker's site, checked {e(", ".join(dates))}. Makers revise formulas; check the bag in your hands. Dry formulas only. Not affiliated with {e(b)}.</p>"""
    p = f"brands/{slug(b)}.html"
    open(p, "w").write(page(f"{b} dry dog food calories per cup ({len(fs)} formulas)",
        f"Calories per cup and per kg for {len(fs)} {b} dry dog food formulas, from the maker's product pages. Range {lo}–{hi} kcal per cup.", p, body))
    urls.append(p)

# back-links from the main page are added in index.html (see 'Browse by brand').
open("sitemap.xml", "w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    + "".join(f"<url><loc>{BASE}{u}</loc></url>\n" for u in urls) + "</urlset>\n")
open("robots.txt", "w").write(f"User-agent: *\nAllow: /\nSitemap: {BASE}sitemap.xml\n")
print({b: len(f) for b, f in brands.items()})
