# Lab 19 — Buffett, Cathie Wood, and Burry panel

This Lab 19 panel follows the professor's in-class instruction to use Cathie Wood in place of Graham. The handout's Graham-specific COST table is superseded for this version. The Lab 18 app remains a separate Buffett-only app.

The [Lab 19 app](app.py) shows the shared five-year SEC EDGAR facts, all eight coded checks, screen verdicts, and three editable memos side by side. It flags any memo number absent from the script's printed report. Missing facts display as `not found`; dependent checks remain `not known`.

Run with your own SEC contact identity:

```powershell
$env:SEC_USER_AGENT = 'Your Name your.email@example.edu'
& .\.venv\Scripts\python.exe .\lab19\validate.py
& .\.venv\Scripts\python.exe .\.agents\skills\buffett-edgar\scripts\edgar_buffett.py COST
& .\.venv\Scripts\python.exe .\.agents\skills\buffett-edgar\scripts\edgar_buffett.py AAPL
& .\.venv\Scripts\python.exe .\lab19\verify_memos.py
& .\.venv\Scripts\python.exe -m streamlit run .\lab19\app.py
```

Cathie Wood's classroom checks are in [cathie_wood_checks.py](../.agents/skills/cathie-wood-edgar/scripts/cathie_wood_checks.py). They test revenue growth, R&D expense growth, and latest R&D expense as a share of revenue against a configurable 5.0% threshold. A live AAPL probe at 10.0% flipped the final check to fail; the baseline was restored to 5.0%. These figures are limited proxies. [ARK's investment process](https://www.ark-invest.com/investment-process) also studies technology cost curves, adoption, market opportunity, and valuation, none of which this panel can establish.

The Project 2 workspace includes SPY, whose [largest holding was Apple as of 2026-11-04](https://www.ssga.com/us/en/intermediary/etfs/state-street-spdr-sp-500-etf-trust-spy). Results, bull and bear cases, and the decision are in [checkout.md](checkout.md).
