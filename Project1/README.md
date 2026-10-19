# JNJ Project 1 — Corporate Finance Application

**Target:** Johnson & Johnson (NYSE: JNJ) common stock.  **Valuation date:** September 10, 2026 market close.  **Currency:** USD millions except per-share data.  **Share basis:** FY2025 diluted weighted-average shares (2,429.4m).

## Decision

Current committee action: **watch/defer, not initiate.** The $372.95 base DCF value is not sufficient to initiate because 87.6% of enterprise value is terminal value, the low case is below market, and the peer cross-checks are near to below market. Reconsider initiation only after a refreshed valuation retains a margin of safety and two consecutive quarters validate the product bridge, normalized FCFF, and bounded litigation/cash needs. Change the action to **do not initiate** if replacement medicines and MedTech miss the bridge for two consecutive quarters, STELARA erosion is at or worse than the bridge, recurring legal/restructuring cash costs emerge, and WACC reaches 7% or more. See `docs/decision-memo.md` for the evidence and monitoring triggers.

## Run

```powershell
& ..\.venv\Scripts\python.exe .\jnj_project1_fcff.py
& ..\.venv\Scripts\python.exe .\jnj_pe_valuation.py
```

### Teammate-operable driver panel

```powershell
& .\Start-JNJ-Dashboard.ps1
```

Or, from this folder:

```powershell
& ..\.venv\Scripts\python.exe .\jnj_valuation_app.py
```

The command opens `http://127.0.0.1:8765` in a browser. Keep its PowerShell
window open while using the app; do not open the HTML file directly. The local-only panel has bounded
driver controls, a Base reset, articulated-statement checks, five-year
pro-forma/FCFF output, valuation bridge, low/base/high cases, sensitivity
views, reverse DCF, comparables policy, and the assumption-challenge record.

### Teammate workflow

1. Adjust only the bounded sliders in the Driver panel.
2. Select **Recalculate**; the app rebuilds the three statements, FCFF DCF,
   bridge, and sensitivity results from the same linked engine.
3. Confirm every visible articulation check passes before using an output.
4. Select **Reset base** to restore the documented case.

This is a semi-adjustable product rather than a notebook that only computes
once: filing-derived opening balances and the share/debt/cash bridge remain
locked, while decision-relevant forecast drivers are adjustable and bounded.

## Validation

```powershell
& ..\.venv\Scripts\python.exe .\validation_suite.py
& ..\.venv\Scripts\python.exe .\cold_run_validation.py
& ..\.venv\Scripts\python.exe .\export_final_report.py
```

See `docs/validation-status.md` for the evidence index. The synthetic known
answer and the Locked Changed-Input Record need course material and the
student's own AI-off, pre-run work; they are deliberately not fabricated.

`docs/model-version-transition.md` identifies the final FCFF model and labels
the earlier weekly FCFE artifacts as historical. The packaged `JNJ-research/`
directory contains the cited DCF, WACC, peer, and source-support files.

`docs/final-model-report.md` is the readable static handoff package; it lets a grader inspect the full five-year income statements, balance sheets, cash-flow statements, revenue bridge, valuation cases, WACC-growth grid, peer calculations, reverse DCF, and checks without launching the dashboard.

The first command produces the linked five-year pro forma, FCFF DCF, enterprise-to-equity bridge, low/base/high cases, WACC–growth sensitivity, reverse DCF, and validation results.  The second produces the reported-GAAP-EPS P/E cross-check.

## Repository map

- `jnj_project1_fcff.py` — final FCFF model and validation checks.
- `JNJ-research/` and `Lab 10 jnj_proforma.md` — filing-based historical evidence and pro-forma driver basis.
- `JNJ-research/lab08_peer_valuation.md`, `jnj_pe_valuation.py`, and `jnj_peer_multiples.py` — peer policy plus P/E and EV/EBIT cross-checks.
- `docs/assumptions-and-challenges.md` — load-bearing driver record and contamination catalog.
- `docs/validation-and-ai-use.md` — validation plan, locked-record template, and AI-use disclosure.
- `docs/decision-memo.md` — draft committee memo.

## Limitations

This is an educational valuation, not investment advice.  Forecasts are judgmental.  The P/E comparison uses two qualified—not identical—peers and reported GAAP EPS.  Before submission, complete the human-authored Locked Changed-Input Record and confirm the final peer EV multiple source fields.
