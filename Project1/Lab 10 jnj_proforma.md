# DRIVE submission — Johnson & Johnson (NYSE: JNJ)

> Historical weekly FCFE teaching-model artifact. Retained for course evidence; do not use its $138.28/share output, 8.0% cost of equity, 2.5% terminal growth, or 2,407.939m share count in the final FCFF conclusion. See `docs/model-version-transition.md`.

All dollars are USD millions unless stated otherwise. Historical fiscal years end December 31, 2023; December 29, 2024; and December 28, 2025.

## D — the line that makes JNJ different

**JNJ is a patent-portfolio company, not a store-growth company: the key near-term model line is STELARA’s biosimilar-driven erosion.** The FY2025 10-K says the STELARA decline reduced worldwide operational sales growth by about 6.2 percentage points. I therefore use 5.0%, 4.0%, 4.0%, 3.5%, and 3.0% revenue growth—below the FY2025 6.0% reported growth—and do not use a store/floor-plan driver.

Partner question: *Why not grow sales at JNJ’s five-year 6.7% CAGR?*  
Answer: The historical CAGR includes product launches, acquisitions, and a pre-biosimilar STELARA base. The disclosed 2025 STELARA headwind and the fact that 1.1 percentage points of 2025 growth came from acquisitions make it a poor forward run rate.

## R — three-year history

### History grid

| Item | FY2023 | FY2024 | FY2025 |
|---|---:|---:|---:|
| Revenue | 85,159 — [FY2023 10-K, p. 45](https://www.sec.gov/Archives/edgar/data/200406/000020040624000013/jnj-20231231.htm) | 88,821 — [FY2024 10-K, p. 45](https://www.sec.gov/Archives/edgar/data/200406/000020040625000038/jnj-20241229.htm) | 94,193 — [FY2025 10-K, p. 44](https://www.sec.gov/Archives/edgar/data/200406/000020040626000016/jnj-20251228.htm) |
| Gross profit | 58,606 — FY2023 10-K, p. 45 | 61,350 — FY2024 10-K, p. 45 | 63,937 — FY2025 10-K, p. 44 |
| SG&A | 21,512 — FY2023 10-K, p. 45 | 22,869 — FY2024 10-K, p. 45 | 23,676 — FY2025 10-K, p. 44 |
| Net income | 35,153 — FY2023 10-K, p. 45 | 14,066 — FY2024 10-K, p. 45 | 26,804 — FY2025 10-K, p. 44 |
| Inventory | 11,181 — [FY2023 10-K, p. 44](https://www.sec.gov/Archives/edgar/data/200406/000020040624000013/jnj-20231231.htm) | 12,444 — [FY2024 10-K, p. 44](https://www.sec.gov/Archives/edgar/data/200406/000020040625000038/jnj-20241229.htm) | 14,191 — [FY2025 10-K, p. 43](https://www.sec.gov/Archives/edgar/data/200406/000020040626000016/jnj-20251228.htm) |
| PP&E, net | 19,898 — FY2023 10-K, p. 44 | 20,518 — FY2024 10-K, p. 44 | 23,169 — FY2025 10-K, p. 43 |
| Shareholders’ equity | 68,774 — FY2023 10-K, p. 44 | 71,490 — FY2024 10-K, p. 44 | 81,544 — FY2025 10-K, p. 43 |

I manually checked two primary-statement items in the filings: FY2023 inventory and PP&E on the FY2023 balance sheet, and FY2025 revenue and gross profit on the FY2025 earnings statement. No requested historical items are unresolved.

### Ratio and growth table

| Ratio / growth | FY2023 | FY2024 | FY2025 | Method / filing source |
|---|---:|---:|---:|---|
| Gross margin | 68.82% | 69.07% | 67.88% | Gross profit ÷ revenue from earnings statements above |
| SG&A ÷ gross profit | 36.70% | 37.28% | 37.03% | SG&A ÷ gross profit |
| Inventory days | 153.7 | 165.3 | 171.3 | Ending inventory ÷ cost of products sold × 365 |
| D&A ÷ PP&E | 37.62% | 35.77% | 32.38% | Cash-flow D&A ÷ ending PP&E; D&A: [FY2025 10-K, p. 47](https://www.sec.gov/Archives/edgar/data/200406/000020040626000016/jnj-20251228.htm) |
| Capital spending, filing | 4,543 | 4,424 | 4,832 | Cash-flow “additions to PP&E,” FY2025 10-K p. 47 (data-provider comparison: **unresolved**; no provider field used) |
| Effective tax rate | 11.53% | 15.71% | 17.73% | Tax provision ÷ pretax income from earnings statements |
| Reported revenue growth | 6.46% | 4.30% | 6.05% | Calculated from revenue history |
| Operational growth (constant currency) | 7.4% | 5.9% | 5.3% | FY2024 10-K MD&A p. 23; [FY2025 10-K MD&A p. 23](https://www.sec.gov/Archives/edgar/data/200406/000020040626000016/jnj-20251228.htm) |
| Acquisitions/divestitures contribution | +1.5 pts | +0.5 pts | +1.1 pts | FY2024 10-K MD&A p. 23; FY2025 10-K MD&A p. 23 |

JNJ does **not** disclose same-store sales, and it does not label a company-wide “organic growth” metric in these filings. It calls constant-currency growth “operational” growth; it excludes currency but still includes acquisition/divestiture effects. A rough underlying growth proxy after removing both disclosed effects is 5.9%, 5.4%, and 4.2%, respectively. That proxy is my calculation, not a JNJ metric.

### Assumption set

| Assumption | Value | Label | Reason |
|---|---:|---|---|
| Opening revenue | 94,193 | history | FY2025 reported revenue, 10-K p. 44. |
| Revenue growth | 5.0%, 4.0%, 4.0%, 3.5%, 3.0% | judgment | Below FY2025 reported growth because STELARA reduced 2025 operational growth by ~6.2 points and acquisition contribution was 1.1 points. I assume replacement products and MedTech partly offset erosion, but not immediately. |
| Gross margin | 68.0% | judgment | Three-year range is 67.9%–69.1%; I use near the low end because price was a 3.1-point drag in FY2025. |
| SG&A ÷ gross profit | 37.0% | history | Near the 36.7%–37.3% historical range. |
| R&D ÷ revenue | 15.5% | history | Near FY2025 R&D ÷ revenue (15.6%); innovation is core to patent replacement. |
| D&A ÷ opening PP&E | 32.4% | history | FY2025 total cash-flow D&A ÷ ending PP&E. |
| PP&E depreciation rate | 12.0% | judgment | Total D&A includes material intangible amortization, so applying the full 32.4% to PP&E would misstate the PP&E roll-forward. 12% leaves the residual as intangible amortization. |
| Inventory days | 171.3 | history | FY2025 ending inventory ÷ COGS × 365. |
| Capex ÷ revenue | 5.0% | judgment | FY2025 capex was 5.13% of revenue; I round slightly down but retain substantial manufacturing investment. |
| Other working-capital investment | 1.0% of incremental revenue | judgment | JNJ’s other assets/liabilities include large acquisition, tax, and legal balances, so a simple historic percent of sales would be misleading. This is a deliberately modest recurring operating investment. |
| Net interest rate | 2.0% of debt | judgment | 2025 net interest expense ÷ year-end debt is about 2.0%; debt is held flat rather than assuming refinancing gains. |
| Tax rate | 18.0% | judgment | Close to FY2025’s 17.73%, without assuming its low 2023 rate repeats. |
| Cash dividend | 12,750 in 2026; +3% yearly | judgment | FY2025 cash dividends paid were 12,381; modest growth preserves cash while recognizing JNJ’s dividend practice. |
| Debt / revolver | 47,933 / 0 | history / judgment | FY2025 debt is 8,495 current loans/notes plus 39,438 long-term debt. No revolver is required in the projection. |
| Floor plan | none (0) | none | JNJ is not an auto dealer/retailer and reports no floor-plan financing. |
| Minimum cash | 10,000 | judgment | A conservative liquidity floor below FY2025 cash of 19,709, retaining flexibility for a global healthcare business. |
| Cost of equity | 8.0% | judgment | A transparent required return for an established healthcare equity; changing risk-free rates, beta, or the equity risk premium would change it. |
| Terminal growth | 2.5% | judgment | Long-run nominal growth below the explicit early-years path; it avoids treating patent-driven above-trend growth as perpetual. |
| Shares outstanding | 2,407.939 | history | FY2025 issued shares less treasury shares, 10-K p. 43; the same count is used for model and market price comparison. |

### Opening balance sheet supplied to the engine

| FY2025 opening balance sheet | Amount |
|---|---:|
| Cash | 19,709 |
| Inventory | 14,191 |
| PP&E | 23,169 |
| Other operating assets (balancing aggregation) | 142,141 |
| **Total assets** | **199,210** |
| Debt | 47,933 |
| Other liabilities | 69,733 |
| Shareholders’ equity | 81,544 |
| **Liabilities + equity** | **199,210** |

The aggregation preserves the audited opening balance sheet while keeping the teaching model legible. “Other operating assets” is total assets less cash, inventory, and PP&E; “other liabilities” is total liabilities less debt.

## I and V — engine, checks, and price

Run `python jnj_drive_model.py`. It produces five income statements, balance sheets, FCFE cash flows, a live annual balance check, and value per share. It does not silence a check. Cash is generated from FCFE less the dividend; with the assumptions above, no year needs a revolver draw because cash remains above the $10.0bn floor.

The latest completed-market close available when this file was prepared was **$269.17 on September 23, 2026** ([StockAnalysis historical data](https://stockanalysis.com/stocks/jnj/history/)); September 24 was still trading. The model output uses 2,407.939 million shares, the same share count used for that market comparison: **the model says $138.28 per share; the market said $269.17—what growth, margin, or required-return assumption explains the gap?** This is a valuation question, not a recommendation.

## E — fresh-eyes attack and answer

Partner attack: Why is 8.0% a defensible cost of equity when JNJ is a mature and diversified healthcare company? What would change it?
Answer: I use 8.0% as a conservative estimated required return because the cash flows face patent cliffs, legal uncertainty, and acquisition integration risk even though the company is diversified. I would lower it if a current CAPM build with a lower beta/risk-free rate supports it, or raise it if STELARA replacement, litigation, leverage, or market risk worsens.

### My attack on my Oracle partner

Your Oracle model assumes that free cash flow recovers after the AI-cloud buildout. Why is that defensible when Oracle reported $55.7 billion of 2026 fiscal year capital expenditures—up 162% year over year—and says that capital expenditures should rise further in the 2027 fiscal year?

 It won’t generate strong cash flow right away and if it runs short of cash the model shows how that shortage is funded. Once the new investments start making money, cash flow improves, but the company still has ongoing maintenance costs.
## Organic growth learning and reflection

Organic growth generally means revenue growth from the existing business after stripping out acquisitions/divestitures and, often, currency. JNJ’s MD&A instead reports **operational growth**, which excludes currency; it separately states the acquisition/divestiture contribution. It does not report same-store sales because it does not operate a store base. The ABG video’s 1.8% versus 4.7% distinction makes the same point: reported growth can include new stores, acquisitions, or other non-comparable expansion; the forecast should use the growth of the comparable economic base when that is the question.

The label I would defend longest is **history** for FY2025 capex: it is directly shown as “additions to property, plant and equipment” in the cash-flow statement, not inferred from a vendor field. The surprising filing number was the stated approximate **6.2-point** FY2025 drag on worldwide operational growth from STELARA’s decline—large enough to overwhelm a casual extrapolation of headline sales growth.

## Primary filing links

- [FY2023 Form 10-K, filed February 16, 2024](https://www.sec.gov/Archives/edgar/data/200406/000020040624000013/jnj-20231231.htm)
- [FY2024 Form 10-K, filed February 13, 2025](https://www.sec.gov/Archives/edgar/data/200406/000020040625000038/jnj-20241229.htm)
- [FY2025 Form 10-K, filed February 11, 2026](https://www.sec.gov/Archives/edgar/data/200406/000020040626000016/jnj-20251228.htm)

## Lab 10 — one-at-a-time sensitivity

Run `python jnj_lab10_sensitivity.py`. It uses immutable base inputs and a fresh forecast for every lower/base/higher case. Output dollars are USD millions, except per-share values. The cash-flow measure is **FCFE**, consistently defined as cash flow available to equity before dividends; the equity valuation is valid under the existing FCFE model.

### R — independent inputs and reproducible ranges

| Independent operating driver | Affected years | Lower | Base | Higher | Units | Range reason |
|---|---|---|---|---|---|---|
| Revenue growth path | FY2026E–FY2030E | 4.0%, 3.0%, 3.0%, 2.5%, 2.0% | 5.0%, 4.0%, 4.0%, 3.5%, 3.0% | 6.0%, 5.0%, 5.0%, 4.5%, 4.0% | % of prior-year revenue | Judgment: exactly -/+ 1.0 **percentage point** in every forecast year around the base path. It brackets the uncertain speed of STELARA erosion and replacement-product/MedTech offset; it is not a percent change to the rates. |
| Gross margin | FY2026E–FY2030E | 67.0% | 68.0% | 69.0% | % of revenue | FY2023–FY2025 history is 68.8%, 69.1%, and 67.9%. The 67%–69% interval is a rounded history-informed range; 68% base reflects the FY2025 pricing drag. These are percentage-point changes. |

### Locked Changed-Input Record — 2026-09-29, America/New_York, before run

1. Revenue growth: base 5.0%/4.0%/4.0%/3.5%/3.0% → each year -/+1.0 percentage point. Prediction: lower/higher growth lowers/raises FY2030 EBIT, FCFE, and value/share; a roughly 5% different FY2030 revenue base should produce several-hundred-million-dollar FCFE and several-dollar value/share movement because revenue flows through gross profit, expenses, working capital, and FCFE.
2. Gross margin: base 68.0% → 67.0%/69.0% for each forecast year. Prediction: lower/higher margin lowers/raises EBIT, FCFE, and value/share; one percentage point of FY2030 revenue is roughly $1.1bn of gross profit before linked SG&A, tax, reinvestment, and valuation effects.

### I and V — actual output (all checks passed)

| Driver / case | Actual changed input | FY2030 operating profit (EBIT) | Change from base | FY2030 FCFE | Change from base | Value/share | Change from base |
|---|---|---:|---:|---:|---:|---:|---:|
| Revenue growth — Lower | 4.0%/3.0%/3.0%/2.5%/2.0% | 19,650.0 | -1,325.5 | 19,609.2 | -773.3 | $133.62 | -$4.65 |
| Revenue growth — Base | 5.0%/4.0%/4.0%/3.5%/3.0% | 20,975.5 | 0.0 | 20,382.5 | 0.0 | $138.28 | $0.00 |
| Revenue growth — Higher | 6.0%/5.0%/5.0%/4.5%/4.0% | 22,355.7 | +1,380.2 | 21,178.9 | +796.4 | $143.06 | +$4.79 |
| Gross margin — Lower | 67.0% | 20,257.1 | -718.4 | 19,777.8 | -604.7 | $133.98 | -$4.30 |
| Gross margin — Base | 68.0% | 20,975.5 | 0.0 | 20,382.5 | 0.0 | $138.28 | $0.00 |
| Gross margin — Higher | 69.0% | 21,694.0 | +718.4 | 20,987.2 | +604.7 | $142.57 | +$4.30 |

| Output span over lower/base/higher | Revenue-growth range | Gross-margin range |
|---|---:|---:|
| FY2030 EBIT | 2,705.7 | 1,436.9 |
| FY2030 FCFE | 1,569.7 | 1,209.4 |
| Value/share | $9.44 | $8.59 |

Each usable case had annual balance check = 0.0 within display rounding and cash above the $10,000.0m floor. Trace detail for selected FY2030 cases is retained in terminal output: lower/base/higher revenue cases have revenue of 108,655.2 / 114,038.7 / 119,633.5 and FCFE of 19,609.2 / 20,382.5 / 21,178.9; the gross-margin cases retain the same base revenue of 114,038.7 while gross profit changes to 76,405.9 / 77,546.3 / 78,686.7.

The final restored-base rerun **passed**: FY2030 EBIT 20,975.5 / 20,975.5, FCFE 20,382.5 / 20,382.5, and value/share $138.28 / $138.28 before/after, with tolerance $0.0001m and $0.0001 per share.

### E — result explanation and learning

Over these stated ranges, revenue growth is the larger driver: its spans are $2,705.7m EBIT, $1,569.7m FCFE, and $9.44/share, versus $1,436.9m, $1,209.4m, and $8.59/share for gross margin. The ranking is conditional on the selected ranges; the five annual revenue shifts compound, while the margin test is a one-point constant path, so it does not establish an inherently more important driver.

The revenue link is revenue → gross profit and R&D/capex/inventory needs → net income and FCFE → FCFE equity value. The margin link is gross profit → SG&A (37% of gross profit in this model) → EBIT → after-tax FCFE. The latter coupling explains why a one-point gross-margin change moves FY2030 EBIT by $718.4m rather than the full $1,140.4m of FY2030 revenue.

The directions matched both locked predictions. The revenue output magnitude was larger than the initial rough “several hundred” shorthand for EBIT because the annual percentage-point changes compound through the full five-year revenue base. The margin result confirms the linked-SG&A effect omitted from the rough gross-profit-to-EBIT wording. This analysis does not by itself change the valuation conclusion: the base $138.28/share remains far below the cited $269.17 market reference, while the tested $133.62–$143.06 range does not bridge that gap. It raises the research priority of the revenue replacement path because it is the largest tested driver.

One-at-a-time sensitivity changes one independent assumption while holding the others at base, then allows the linked statements to recalculate. A sensitivity table is not a forecast probability: it shows conditional outcomes for chosen inputs, not the likelihood of those inputs or correlations among them.

### Partner exchange evidence

My partner modeled McDonald’s and identified revenue growth as its strongest driver over the ranges tested. I asked whether a consumer-demand shift toward healthier food could stop revenue from growing, since that would weaken the revenue-growth assumption if McDonald’s could not adapt its menu or retain demand. This was a range-and-business-risk challenge, not a claim that the model’s arithmetic was wrong.

I checked that the partner’s conclusion was stated over the selected ranges and that the reported driver was revenue growth. The question I raised was whether the assumed revenue-growth range incorporated the potential demand shift toward healthier food. My partner should retain the specific base-versus-changed output and arithmetic reconciliation from the live exchange with their McDonald’s model.
