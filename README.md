# Dog food calories per cup

Browser-only lookup of kcal per cup and per kg for dry dog food formulas, with cups and grams per day and a calorie-matched switching plan. Built by an AI agent (Claude), maintained by @maxim-k.

- `foods.json`: formulas copied from each maker's product pages, with URL and check date. Rebuild with `build_data.py` from `raw/`.
- `calc.js`: the maths (`node test.js`). RER and life-stage factors: Ohio State University Veterinary Medical Center calorie calculator, Table 1.
- No uploads; visits are counted with cookie-free GoatCounter. MIT license.
