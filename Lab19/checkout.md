# Lab 19 checkout — Cathie Wood variant

The three lenses use the same SEC EDGAR annual rows. This panel follows the professor's in-class instruction to replace Graham with Cathie Wood. The Cathie Wood checks are classroom growth and research-spending proxies, not ARK's actual selection rules. Live reports were run for COST and AAPL on 2026-11-05.

## COST panel

| Investor | Check | Result |
|---|---|---|
| Buffett | ROE of 15% or more every year | pass |
| Buffett | Owner earnings positive every year | pass |
| Buffett | Owner earnings grew, first year to last | pass |
| Cathie Wood | Revenue grew, first year to last | pass |
| Cathie Wood | R&D expense grew, first year to last | not known |
| Cathie Wood | Latest R&D expense at least 5.0% of revenue | not known |
| Burry | Operating cash flow at least net income every year | pass |
| Burry | Liabilities no more than twice equity, latest year (1.49) | pass |

Screen counts: Buffett 3 of 3; Cathie Wood 1 of 3 with 2 unknown; Burry 2 of 2. COST's selected R&D expense tag is `not found`, so neither R&D check is guessed. The five COST current ratios and liabilities-to-equity ratios still match the supplied handout, though the current-ratio check is no longer part of this panel. See the [COST memos](memos/COST).

## Project 2 company: AAPL

The workspace includes SPY in the Project 2 fund universe. [State Street lists Apple as SPY's largest holding as of 2026-11-04](https://www.ssga.com/us/en/intermediary/etfs/state-street-spdr-sp-500-etf-trust-spy). Apple files a 10-K, so no substitution was needed.

| Investor | Check | Result |
|---|---|---|
| Buffett | ROE of 15% or more every year | pass |
| Buffett | Owner earnings positive every year | pass |
| Buffett | Owner earnings grew, first year to last | pass |
| Cathie Wood | Revenue grew, first year to last | pass |
| Cathie Wood | R&D expense grew, first year to last | pass |
| Cathie Wood | Latest R&D expense at least 5.0% of revenue (9.6%) | pass |
| Burry | Operating cash flow at least net income every year | fail |
| Burry | Liabilities no more than twice equity, latest year (2.61) | fail |

Screen counts: Buffett 3 of 3; Cathie Wood 3 of 3; Burry 0 of 2. The [three AAPL memos](memos/AAPL) appear side by side in the app. Raising Cathie Wood's classroom R&D-intensity threshold to 10.0% made AAPL's last check fail; I restored 5.0% because it is a modest prompt for further research rather than proof of disruption.

**Bull case, two sentences.** Buffett's owner-earnings and ROE checks pass, while Cathie Wood's proxies show revenue and reported research spending rose from the first year to the last. Together those figures support further research into the company's growth opportunities.

**Bear case, two sentences.** Burry's cash-conversion check fails because operating cash flow was below net income in one year. Latest liabilities to equity of 2.61 also exceeds his ceiling, and none of the printed figures proves that research spending will produce successful new technology.

**Decision:** Use the panel for Project 2 screening only if missing facts stay unknown and an analyst reviews the filings, innovation thesis, and valuation before investing.

**Reflection:** Buffett and Cathie Wood's coded checks agree on AAPL's historical financial strength and growth, while Burry's two checks raise concerns. The threshold probe shows that a screen verdict can change without any company fact changing.

**What the panel of agents is:** Three separate investor lenses apply fixed code checks to the same EDGAR rows and write their own memos. They disagree because they ask different questions about returns, growth and research spending, and cash support. The Cathie Wood function returns `not known` for each check whose required input is missing; if the five-year history is incomplete, all its checks are `not known`.

`lab19/validate.py` checks the adapted live panel and missing-data behavior. `lab19/verify_memos.py` audits every number across all six memos. The separate Lab 18 app still shows only Buffett's checks and memo.
