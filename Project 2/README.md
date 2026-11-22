AI use: I used OpenAI Codex to help write and review the Python app, tests, and documentation.

The analysis and the decision are mine; this is education, not investment advice.

# Meridian Foundation Reserve — Project 2

**Committee recommendation: reject live allocation (0%) and retain the app as a pilot for review.** The modeled portfolio passes the coded rules on a benchmark starting-position proxy, but actual holdings, issuer look-through, and the CIO's annual-loss definition are missing. A checkable pass is therefore not an adoption decision.

## Reproduce the decision

From this folder, with Python 3.10 or newer, run one command (no extra packages needed):

```powershell
python decision_report.py
```

The command prints the baseline portfolio, comparators, one-input stress runs, and committee decision. [Read the same output on GitHub](docs/decision-output.md) without running the app. The output is generated from the bundled `prices.csv` through `engine.py`; `docs/decision-memo.md` explains why a coded pass still leads to 0% live allocation. The scenario table is exploratory evidence, not the student's Locked Changed-Input Record.

## Start the app

From this folder, with Python 3.10 or newer:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

On macOS or Linux use `python3 -m venv .venv`, `.venv/bin/python -m pip install -r requirements.txt`, and `.venv/bin/python -m streamlit run app.py`. Open the local URL Streamlit prints. No keys, network fetch, upload, or database are required to operate it. Use the sidebar to change window, expected return, costs, reserve, and turnover. The current-input feasibility verdict and portfolio comparison rerun automatically; select **Reset inputs** to restore the documented base case. The comparison tab shows net return, volatility, and allocation charts. The monitoring tab gives measurable review triggers, and the evidence tab explains the financial design choices. Run `python -m unittest discover -s tests -v` for the checks.

## Mandate and operating rule

The [Lab 13 mandate](docs/source-labs/lab13-mandate.md) sets a seven-year horizon and annual rebalancing for a $100m reserve, CPI + 4% net over rolling five years, four $0.75m quarterly payouts, a 60% global-equity/40% U.S. investment-grade-bond benchmark, long-only holdings, an 8% single-issuer cap with exemptions, turnover at most 25% absent committee approval, and 90% redeemable within five business days. The annual loss statement has no measure or breach rule. We use annualized historical volatility as the provisional risk measure and disclose that it is not the missing loss rule. The 6.5% nominal screening target assumes 2.5% CPI and is not a verified CPI + 4% outcome.

The universe is BIL (Treasury bills), IEF (7–10 year Treasuries), LQD (investment-grade corporate bonds), and SPY (U.S. equities). BIL and IEF count toward the 3% reserve. All four are provisionally treated as five-day liquid. SPY is a U.S. rather than global equity proxy, so the 60/40 benchmark is imperfect. Fund role references: [BIL](https://www.ssga.com/us/en/individual/etfs/state-street-spdr-bloomberg-1-3-month-t-bill-etf-bil), [IEF](https://www.ishares.com/us/products/239456/ishares-7-10-year-treasury-bond-etf), [LQD](https://www.ishares.com/us/products/239566/lqd-ishares-iboxx-investment-grade-corporate-bond-etf), [SPY](https://www.ssga.com/us/en/individual/etfs/state-street-spdr-sp-500-etf-trust-spy).

## Data and calculation

`prices.csv` is the pinned 61-month July 2021–July 2026 adjusted-close extract documented in [Lab 15](docs/source-labs/lab15-portfolio-stability.md), downloaded 2026-10-22 from [this source snapshot](https://github.com/manisahni/marketdata/blob/65a079329e379e104495f459e12e76a8f995585a/daily_adjclose_wide.csv). Its upstream README says yfinance furnished dividend/split-adjusted daily closes. It is a secondary, later-downloaded snapshot, so the portfolio screen is **not** a point-in-time backtest. Recheck prices and fund disclosures before a live decision.

`portfolio.py` validates the CSV, computes simple monthly returns, annualizes their mean and sample standard deviation, and builds correlations. `engine.py` enumerates every long-only 5% mix, applies a first-year net estimate (gross historical mean less assumed annual fee and one-way turnover cost), screens the return proxy and checkable limits, and chooses the mix with least estimated volatility. It assumes the benchmark allocation (0 BIL / 0 IEF / 40 LQD / 60 SPY) as the starting holdings solely to illustrate turnover. Actual Meridian positions were not supplied. Equal weight and inverse volatility are transparent comparators with their own verdicts. ETF underlying issuer look-through is not inferred from fund names.

## Evidence and decision files

- [Decision memo](docs/decision-memo.md): recommendation, allocation range, scenario evidence, monitoring triggers.
- [Decision output](docs/decision-output.md): code-generated baseline and stress numbers readable on GitHub.
- [Validation and AI use](docs/validation-and-ai-use.md): checks, limitations, and the Locked Changed-Input Record status.
- [Submission manifest](Submission-Manifest.md): locations and handoff items.
- [Video preparation](video-transcripts/README.md): opening statements and recording outlines. Actual transcripts must reflect the recorded videos.
- `docs/source-labs/`: copies of Labs 13–17 used as assignment context; the Project 2 app has no runtime dependency on the parent folder.

The Locked Changed-Input Record requires **your own AI-off prediction committed to GitHub before the changed-input run**. No such human-authored commit is represented by this repository yet. Record it using `docs/locked-change-input-record.md`; then execute the documented change and add the observed result in a later commit. Do not present a retrospective prediction as locked.
