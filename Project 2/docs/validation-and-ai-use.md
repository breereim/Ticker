AI use: I used OpenAI Codex to help write and review the Python app, tests, and documentation.

The analysis and the decision are mine; this is education, not investment advice.

# Validation and AI use

## Validation performed

`python -m unittest discover -s tests -v` checks reserve and turnover arithmetic, baseline rule failures, the optimizer's modeled feasibility, the infeasible reserve/turnover conflict, and sample-window response. A Streamlit AppTest smoke run checks that the interface renders and its controls recompute. The code and bundled CSV were used locally; no live data call is required. Check these again after any input or code change.

The source snapshot and adjusted-price treatment were carried from [Lab 15](source-labs/lab15-portfolio-stability.md). The BAA point-in-time example was carried from [Lab 17](source-labs/lab17-point-in-time-audit.md): at the 2026-09-30 cutoff, August 2026 BAA 6.32% was knowable; September 2026 BAA 6.47% was published 2026-10-01. This checks one cutoff, not a full point-in-time backtest. The signal remains out of the optimizer.

Known limitations: assumed 2.5% CPI, historical mean as a return estimate, simple annualization, fixed 5% search grid, assumed liquidity, a 60/40 starting-position proxy, no issuer look-through, no defined calendar-year-loss test, and SPY's U.S. rather than global exposure. These limits support the 0% live allocation decision.

## AI assistance and human checks

OpenAI Codex helped translate the Lab 13 mandate and Labs 14–17 into Python and draft these documents. I checked the generated calculations with unit tests and inspected the scenario outputs. One AI output to demonstrate in Video 1 is the initial proposed portfolio; verify its reserve and turnover calculations directly from weights and compare the return margin before treating it as a recommendation. The decision to reject current deployment follows the unverified mandate rules, even though the modeled mix passes its coded checks.

## Locked Changed-Input Record — required human action

The assignment requires an **AI-off prediction written by the student and committed to GitHub before the changed-input run**, followed by the observed result. I cannot truthfully supply or backdate that human prediction. The [record form](locked-change-input-record.md) is ready, but its prediction and commit link are pending. Complete these exact steps in order:

1. Turn off AI assistance. Choose one sidebar input change and write your own directional and approximate numeric prediction in the record form, including why, without running the change.
2. Commit and push the prediction to GitHub. Paste that commit's permanent URL into the form or subsequent result commit.
3. Run the change in the app. Record actual weights, net estimate, risk, checks, and the difference from your prediction.
4. Commit and push the result. Link both commits here and in the submission manifest.

Do not use the automated stress table as the precommit observation: the changed-input run must follow the locked human prediction. Until then this requirement is outstanding.
