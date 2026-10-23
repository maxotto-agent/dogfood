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
<script data-goatcounter="https://maxotto-agent.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script></head>
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
        f'<tr><td><a href="../formulas/{slug(b+" "+f["name"])}.html">{e(f["name"])}</a> (<a href="{e(f["url"])}">maker</a>)</td><td class="n">{f["kcal_cup"]}</td>'
        f'<td class="n">{f["kcal_kg"] if f.get("kcal_kg") else "–"}</td></tr>' for f in fs)
    lo_f = min(fs, key=lambda f: f["kcal_cup"]); hi_f = max(fs, key=lambda f: f["kcal_cup"])
    body = f"""<p class="sub"><a href="../">Dog food calorie calculator</a> › Brands</p>
<h1>{e(b)} dry dog food: calories per cup, {len(fs)} formulas</h1>
<p class="lead">Across {len(fs)} dry {e(b)} formulas, a cup holds {lo} to {hi} kcal (median {med}). The leanest is {e(lo_f["name"])} at {lo}; the richest is {e(hi_f["name"])} at {hi}. A cup of one {e(b)} formula is not a cup of another, so work out the daily amount from the exact formula.</p>
<p><a href="../"><b>Calculate cups per day for a {e(b)} formula →</b></a></p>
<table>
<tr><th>Formula</th><th class="n">kcal/cup</th><th class="n">kcal/kg</th></tr>
{rows}
</table>
<p class="sub">Figures are metabolizable energy as fed, copied from each formula's product page on the maker's site, checked {e(", ".join(dates))}. Makers revise formulas; check the bag in your hands. Dry formulas only. Not affiliated with {e(b)}.</p>"""
    p = f"brands/{slug(b)}.html"
    open(p, "w").write(page(f"{b} dry dog food calories per cup ({len(fs)} formulas)",
        f"Calories per cup and per kg for {len(fs)} {b} dry dog food formulas, from the maker's product pages. Range {lo}–{hi} kcal per cup.", p, body))
    urls.append(p)


# one page per formula (long-tail "<formula> calories per cup")
os.makedirs("formulas", exist_ok=True)
for b, fs in brands.items():
    med_b = round(statistics.median([f["kcal_cup"] for f in fs]))
    for f in fs:
        fslug = slug(b + " " + f["name"])
        if any(u.endswith("/" + fslug + ".html") for u in urls[-3:]): fslug += "-2"
        f["_slug"] = fslug
        kc = f["kcal_cup"]; g = round(kc and f["kcal_kg"] and 1000 * kc / f["kcal_kg"]) if f.get("kcal_kg") else None
        wrows = ""
        for kg in (5, 10, 20, 30, 40):
            kcal = 1.6 * 70 * kg ** 0.75
            wrows += f'<tr><td class="n">{kg} kg ({round(kg*2.2046)} lb)</td><td class="n">{round(kcal)}</td><td class="n">{kcal/kc:.2f}</td></tr>'
        diff = kc - med_b
        cmp_ = (f"{abs(diff)} kcal per cup {'above' if diff > 0 else 'below'} the {e(b)} median of {med_b}" if diff else f"equal to the {e(b)} median of {med_b}")
        kgtxt = f", {f['kcal_kg']} kcal per kg" if f.get("kcal_kg") else ""
        gtxt = f" A cup weighs about {g} g." if g else ""
        body = f"""<p class="sub"><a href="../">Dog food calorie calculator</a> › <a href="../brands/{slug(b)}.html">{e(b)}</a> › Formula</p>
<h1>{e(b)} {e(f["name"])}: calories per cup</h1>
<p class="lead">{e(b)} {e(f["name"])} dry dog food has {kc} kcal per cup{kgtxt}, according to the maker's product page. That is {cmp_}.{gtxt}</p>
<p><a href="../"><b>Work out cups per day for your dog →</b></a></p>
<h2>Rough daily amount, neutered adult dog at a healthy weight</h2>
<table>
<tr><th class="n">Dog weight</th><th class="n">kcal/day</th><th class="n">Cups/day</th></tr>
{wrows}
</table>
<p class="sub">Estimate: resting energy 70 × kg^0.75 times 1.6 (typical neutered adult factor). Active, intact, young, old or overweight dogs differ; ask your vet. Figure copied from <a href="{e(f["url"])}">the maker's page</a>, checked {e(f["checked"])}. Makers revise formulas; check the bag in your hands. Not affiliated with {e(b)}.</p>"""
        p = f"formulas/{fslug}.html"
        open(p, "w").write(page(f"{b} {f['name']} calories per cup ({kc} kcal)",
            f"{b} {f['name']} dry dog food: {kc} kcal per cup{kgtxt}. Daily cups by dog weight.", p, body))
        urls.append(p)

# back-links from the main page are added in index.html (see 'Browse by brand').
open("sitemap.xml", "w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    + "".join(f"<url><loc>{BASE}{u}</loc></url>\n" for u in urls) + "</urlset>\n")
open("robots.txt", "w").write(f"User-agent: *\nAllow: /\nSitemap: {BASE}sitemap.xml\n")
print({b: len(f) for b, f in brands.items()})
