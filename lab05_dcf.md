# Lab 05 — Johnson & Johnson DCF

**Company:** Johnson & Johnson (NYSE: JNJ)  
**Model date:** September 10, 2026  
**Currency:** USD millions, except per-share values

## Inputs

| Input | Value | Unit | As-of date | Exact locator / source | Treatment |
|---|---:|---|---|---|---|
| Operating cash flow | 24,530 | USD millions | Dec. 28, 2025 | FY2025 Form 10-K, Consolidated Statements of Cash Flows, p. 47 / HTML lines 1598–1619 | Sourced |
| Interest paid | 1,977 | USD millions | FY ended Dec. 28, 2025 | FY2025 Form 10-K, Consolidated Statements of Cash Flows, supplemental cash-flow data, p. 47 / HTML lines 1661–1663 | Sourced |
| Effective tax rate | 17.7% | percent | FY ended Dec. 28, 2025 | FY2025 Form 10-K, Note 8 Income taxes, p. 68 / HTML lines 2356–2404 | Sourced |
| Capital expenditure | 4,832 | USD millions | FY ended Dec. 28, 2025 | FY2025 Form 10-K, Consolidated Statements of Cash Flows, p. 47 / HTML lines 1620–1623 | Sourced |
| Starting FCFF | 21,325.1 | USD millions | FY ended Dec. 28, 2025 | 24,530 + 1,977 × (1 − 17.7%) − 4,832 | Calculated |
| Growth, Years 1–5 | 6%, 5%, 4%, 3%, 3% | percent | Sep. 10, 2026 | Declining forecast based on Item 7/MD&A history and recent outlook; not company guidance | Estimate |
| WACC | 5.88% | percent | Sep. 10, 2026 | Estimated from a 4.844% risk-free rate, 0.24 beta, 5% equity-risk premium, a 4.50% debt-note rate after tax, and market-value weights | Estimate |
| Terminal growth | 3.0% | percent | Sep. 10, 2026 | Long-run economic-growth assumption | Estimate |
| Cash and cash equivalents | 19,709 | USD millions | Dec. 28, 2025 | FY2025 Form 10-K, Consolidated Balance Sheets, p. 43 / HTML lines 1405–1413 | Sourced |
| Total debt | 47,933 | USD millions | Dec. 28, 2025 | $8,495 loans and notes payable + $39,438 long-term debt; 10-K p. 43 / HTML lines 1427–1438 | Calculated from sourced lines |
| Diluted weighted-average shares | 2,429.4 | millions of shares | FY ended Dec. 28, 2025 | FY2025 Form 10-K, Note 15 Earnings per share, p. 79 / HTML lines 2835–2845 | Sourced |
| Share price | 267.08 | USD/share | Sep. 9, 2026, 4:00 PM EDT | [StockAnalysis JNJ historical price](https://stockanalysis.com/stocks/jnj/history/) | Sourced market quote |

Primary source: [Johnson & Johnson FY2025 Form 10-K](https://www.sec.gov/Archives/edgar/data/200406/000020040626000016/jnj-20251228.htm).

## Valuation and reasonableness

- Value per diluted share: **$320.59**
- Share price: **$267.08**
- Price/value: **0.83×**, within the 0.5×–2× reasonableness band.

## Sensitivity grid: value per diluted share

| WACC \ terminal growth | 2% | 3% | 4% |
|---|---:|---:|---:|
| 5.00% | $319.10 | $466.90 | $910.32 |
| 5.88% | $243.83 | $320.59 | $479.00 |
| 7.00% | $186.36 | $227.48 | $296.01 |

## Reverse DCF

At the $267.08 target price, the model solves for a **−3.8032 percentage-point** uniform shift to all explicit FCFF-growth rates. The implied annual path is approximately **2.20%, 1.20%, 0.20%, −0.80%, and −0.80%**.

Held fixed: starting FCFF, WACC, terminal growth, cash, debt, and diluted shares. This is one set of assumptions consistent with the market price, not proof of mispricing.

## Conditional call

**Watch-defer. Initiate if** the price-implied growth requirement remains at or below the base forecast path and a credible product-level bridge supports replacement of STELARA erosion; **otherwise defer.** Monitor next quarter’s Innovative Medicine operating growth, particularly STELARA erosion versus DARZALEX, CARVYKTI, and TREMFYA growth.
