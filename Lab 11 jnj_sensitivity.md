# Lab 11 — Johnson & Johnson sensitivity analysis

All dollars are USD millions except per-share values. Run `python "Lab 11 jnj_sensitivity.py"` from this folder. The model uses FCFE (cash flow available to equity before dividends) and its existing FCFE equity valuation.

## Independent inputs and ranges

| Driver | Affected years | Lower | Base | Higher | Units | Reason |
|---|---|---|---|---|---|---|
| Revenue growth | FY2026E–FY2030E | 4.0%, 3.0%, 3.0%, 2.5%, 2.0% | 5.0%, 4.0%, 4.0%, 3.5%, 3.0% | 6.0%, 5.0%, 5.0%, 4.5%, 4.0% | % of prior-year revenue | Judgment range: -/+ 1.0 percentage point in each year. It brackets uncertainty in STELARA erosion and replacement-product/MedTech growth; this is not a percent change to the rates. |
| Gross margin | FY2026E–FY2030E | 67.0% | 68.0% | 69.0% | % of revenue | FY2023–FY2025 gross margin was 68.8%, 69.1%, and 67.9%; 67%–69% is a rounded history-informed range. |

## Locked Changed-Input Record

Timestamp: 2026-09-29, America/New_York, before running.

1. Revenue growth: changing every forecast-year rate by -/+1.0 percentage point should decrease/increase final-year EBIT, FCFE, and value/share. The link is revenue → gross profit/costs/working capital → FCFE → equity value.
2. Gross margin: changing the rate from 68.0% to 67.0%/69.0% should decrease/increase final-year EBIT, FCFE, and value/share. The link is gross profit → SG&A and taxes → FCFE → equity value.

## Actual results

| Driver / case | Actual input | FY2030 EBIT | Change from base | FY2030 FCFE | Change from base | Value/share | Change from base |
|---|---|---:|---:|---:|---:|---:|---:|
| Revenue growth — Lower | 4.0%/3.0%/3.0%/2.5%/2.0% | 19,650.0 | -1,325.5 | 19,609.2 | -773.3 | $133.62 | -$4.65 |
| Revenue growth — Base | 5.0%/4.0%/4.0%/3.5%/3.0% | 20,975.5 | 0.0 | 20,382.5 | 0.0 | $138.28 | $0.00 |
| Revenue growth — Higher | 6.0%/5.0%/5.0%/4.5%/4.0% | 22,355.7 | +1,380.2 | 21,178.9 | +796.4 | $143.06 | +$4.79 |
| Gross margin — Lower | 67.0% | 20,257.1 | -718.4 | 19,777.8 | -604.7 | $133.98 | -$4.30 |
| Gross margin — Base | 68.0% | 20,975.5 | 0.0 | 20,382.5 | 0.0 | $138.28 | $0.00 |
| Gross margin — Higher | 69.0% | 21,694.0 | +718.4 | 20,987.2 | +604.7 | $142.57 | +$4.30 |

| Output span (maximum minus minimum) | Revenue growth | Gross margin |
|---|---:|---:|
| FY2030 EBIT | 2,705.7 | 1,436.9 |
| FY2030 FCFE | 1,569.7 | 1,209.4 |
| Value/share | $9.44 | $8.59 |

All usable runs passed annual balance checks and the $10,000.0m minimum-cash check. The restored-base check passed: the before/after values were FY2030 EBIT 20,975.5/20,975.5, FCFE 20,382.5/20,382.5, and value/share $138.28/$138.28.

## Conclusion and reflection

Over these ranges, revenue growth is the larger driver for EBIT, FCFE, and value/share. That conclusion depends on the selected ranges: the revenue shifts compound for five years, while margin changes by one point each year. A sensitivity table is not a forecast probability; it gives conditional outputs for chosen inputs and does not assign likelihoods or capture correlations.

The prediction directions were correct. Revenue growth has a larger-than-roughly-estimated EBIT effect because the annual changes compound. Gross margin does not pass fully to EBIT because the model links SG&A to gross profit.

The tested valuation range ($133.62–$143.06/share) does not change the prior valuation conclusion relative to the cited $269.17 market reference. Revenue replacement remains the higher research priority because it is the largest tested driver.

## Partner exchange

My partner modeled McDonald’s and identified revenue growth as its strongest driver over the ranges tested. I asked whether a consumer-demand shift toward healthier food could stop revenue from growing, since that would weaken the revenue-growth assumption if McDonald’s could not adapt its menu or retain demand. This challenges whether the chosen revenue-growth range includes that business risk, rather than challenging the model arithmetic.

My partner also questioned whether research spending was too expensive. I responded that research expense can reduce near-term operating profit and FCFE, but successful research should eventually support new products and cash flows. The key modeling question is whether the eventual benefit is large enough and arrives soon enough to justify the current expense; it should not simply be assumed without evidence.
