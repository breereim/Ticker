AI use: I used OpenAI Codex to help write and review the Python app, tests, and documentation.

The analysis and the decision are mine; this is education, not investment advice.

# Meridian Foundation Reserve — Project 2

**Committee recommendation: reject live allocation (0%) and retain the app as a pilot for review.** The modeled portfolio passes the coded rules on a benchmark starting-position proxy, but actual holdings, issuer look-through, and the CIO's annual-loss definition are missing. A checkable pass is therefore not an adoption decision.

## Reproduce the decision

From the `Project 2` folder in a clone of [Ticker](https://github.com/breereim/Ticker), with Python 3.10 or newer, run one command (no extra packages needed):

```powershell
python decision_report.py
```

The command prints the baseline portfolio, comparators, one-input stress runs, and committee decision. [Read the same output on GitHub](https://github.com/breereim/Ticker/blob/main/Project%202/decision-output.md) without running the app. The output is generated from the bundled `prices.csv` through `engine.py`; the [decision memo](https://github.com/breereim/Ticker/blob/main/Project%202/decision-memo.md) explains why a coded pass still leads to 0% live allocation. The scenario table is exploratory evidence, not the student's Locked Changed-Input Record.

## Start the app

From the `Project 2` folder in a clone of the GitHub repository, with Python 3.10 or newer, use these PowerShell commands. The dependency file is one level up, at `Ticker/requirements.txt`:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r ..\requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

On macOS or Linux use `python3 -m venv .venv`, `.venv/bin/python -m pip install -r ../requirements.txt`, and `.venv/bin/python -m streamlit run app.py`. If you have only the standalone local `Project 2` folder, use its own `requirements.txt` instead of `../requirements.txt`. Open the local URL Streamlit prints. No keys, network fetch, upload, or database are required to operate it. Use the sidebar to change window, expected return, costs, reserve, and turnover. The current-input feasibility verdict and portfolio comparison rerun automatically; select **Reset inputs** to restore the documented base case. The comparison tab shows net return, volatility, and allocation charts. The monitoring tab gives measurable review triggers, and the evidence tab explains the financial design choices. In the GitHub checkout, run `python -m unittest test_engine -v` for the checks; in the standalone local folder, run `python -m unittest discover -s tests -v`.

## Mandate and operating rule

The [Lab 13 mandate](https://github.com/breereim/Ticker/blob/main/mandate.md.md) sets a seven-year horizon and annual rebalancing for a $100m reserve, CPI + 4% net over rolling five years, four $0.75m quarterly payouts, a 60% global-equity/40% U.S. investment-grade-bond benchmark, long-only holdings, an 8% single-issuer cap with exemptions, turnover at most 25% absent committee approval, and 90% redeemable within five business days. The annual loss statement has no measure or breach rule. We use annualized historical volatility as the provisional risk measure and disclose that it is not the missing loss rule. The 6.5% nominal screening target assumes 2.5% CPI and is not a verified CPI + 4% outcome.

The universe is BIL (Treasury bills), IEF (7–10 year Treasuries), LQD (investment-grade corporate bonds), and SPY (U.S. equities). BIL and IEF count toward the 3% reserve. All four are provisionally treated as five-day liquid. SPY is a U.S. rather than global equity proxy, so the 60/40 benchmark is imperfect. Fund role references: [BIL](https://www.ssga.com/us/en/individual/etfs/state-street-spdr-bloomberg-1-3-month-t-bill-etf-bil), [IEF](https://www.ishares.com/us/products/239456/ishares-7-10-year-treasury-bond-etf), [LQD](https://www.ishares.com/us/products/239566/lqd-ishares-iboxx-investment-grade-corporate-bond-etf), [SPY](https://www.ssga.com/us/en/individual/etfs/state-street-spdr-sp-500-etf-trust-spy).

## Data and calculation

`prices.csv` is the pinned 61-month July 2021–July 2026 adjusted-close extract documented in [Lab 15](https://github.com/breereim/Ticker/blob/main/lab15_portfolio_stability.md), downloaded 2026-10-22 from [this source snapshot](https://github.com/manisahni/marketdata/blob/65a079329e379e104495f459e12e76a8f995585a/daily_adjclose_wide.csv). Its upstream README says yfinance furnished dividend/split-adjusted daily closes. It is a secondary, later-downloaded snapshot, so the portfolio screen is **not** a point-in-time backtest. Recheck prices and fund disclosures before a live decision.

`portfolio.py` validates the CSV, computes simple monthly returns, annualizes their mean and sample standard deviation, and builds correlations. `engine.py` enumerates every long-only 5% mix, applies a first-year net estimate (gross historical mean less assumed annual fee and one-way turnover cost), screens the return proxy and checkable limits, and chooses the mix with least estimated volatility. It assumes the benchmark allocation (0 BIL / 0 IEF / 40 LQD / 60 SPY) as the starting holdings solely to illustrate turnover. Actual Meridian positions were not supplied. Equal weight and inverse volatility are transparent comparators with their own verdicts. ETF underlying issuer look-through is not inferred from fund names.

## Evidence and decision files

- [Decision memo](https://github.com/breereim/Ticker/blob/main/Project%202/decision-memo.md): recommendation, allocation range, scenario evidence, monitoring triggers.
- [Decision output](https://github.com/breereim/Ticker/blob/main/Project%202/decision-output.md): code-generated baseline and stress numbers readable on GitHub.
- [Validation and AI use](https://github.com/breereim/Ticker/blob/main/Project%202/validation-and-ai-use.md): checks, limitations, and the Locked Changed-Input Record status.
- [Locked Changed-Input Record](https://github.com/breereim/Ticker/blob/main/Project%202/locked-change-input-record.md): prediction, observed result, and reconciliation.
- [Submission manifest](https://github.com/breereim/Ticker/blob/main/Project%202/Submission-Manifest.md): locations and handoff items.
- Corrected transcripts: [Video 1](https://github.com/breereim/Ticker/blob/main/Project%202/transcript-video-1.txt), [Video 2](https://github.com/breereim/Ticker/blob/main/Project%202/transcript-video-2.txt), and [Video 3](https://github.com/breereim/Ticker/blob/main/Project%202/transcript-video-3.txt).
- [Labs 14–17](https://github.com/breereim/Ticker): assignment context in the repository root; the Project 2 app does not import those files.

The student's AI-off prediction is preserved in the [pre-run commit](https://github.com/breereim/Ticker/commit/d482c5721a609deaa2c0e8d889161dadc3b7d8e5); the observed result was added in a [later commit](https://github.com/breereim/Ticker/commit/d00029308f34be1fc4383d45222ae6ebe4d48676). The [current record](https://github.com/breereim/Ticker/blob/main/Project%202/locked-change-input-record.md) preserves the directional prediction and qualitative reconciliation. See the [validation writeup](https://github.com/breereim/Ticker/blob/main/Project%202/validation-and-ai-use.md) for the reproduced numeric comparison and its limitations.
