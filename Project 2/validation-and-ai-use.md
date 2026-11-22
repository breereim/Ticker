AI use: I used OpenAI Codex to help write and review the Python app, tests, and documentation. On 2026-11-19, Codex reproduced the changed-input figures and updated this validation record. The pre-run prediction in the linked commit was written by the student with AI assistance off.

The analysis and the decision are mine; this is education, not investment advice.

# Validation and AI use

## Validation performed

| Date (America/New_York) | Check | Result |
|---|---|---|
| 2026-11-19 | `python -m unittest discover -s tests -v` | **5 tests passed.** They cover reserve and turnover arithmetic, baseline rule failures, optimized feasibility, an infeasible reserve/turnover conflict, sample-window response, and the stress table. |
| 2026-11-19 | Streamlit `AppTest`, default inputs and annual fund fee changed from 10 to 20 bp | **0 app exceptions** in both runs. The selected portfolio's displayed net estimate and volatility changed from 6.56% / 9.47% to 7.15% / 9.85%; live allocation remained 0%. The first smoke attempt hit AppTest's 3-second startup timeout; the repeat with a 30-second timeout passed. |
| 2026-11-19 | `python decision_report.py` compared with [decision-output.md](decision-output.md) | The generated baseline and six stress rows match the Markdown output, including the 10 bp base case: constrained weights 25/0/30/45, 6.56% net, 9.47% volatility, coded PASS. |
| 2026-11-19 | `run_case(fee_bps=10)` and `run_case(fee_bps=20)` | Reproduced the exact weights, net estimates, volatility, and coded PASS/FAIL verdicts in the [Locked Changed-Input Record](locked-change-input-record.md). |

The source snapshot and adjusted-price treatment were carried from [Lab 15](source-labs/lab15-portfolio-stability.md). The BAA point-in-time example was carried from [Lab 17](source-labs/lab17-point-in-time-audit.md): at the 2026-09-30 cutoff, August 2026 BAA 6.32% was knowable; September 2026 BAA 6.47% was published 2026-10-01. This checks one cutoff, not a full point-in-time backtest. The signal remains out of the optimizer.

Known limitations: assumed 2.5% CPI, historical mean as a return estimate, simple annualization, fixed 5% search grid, assumed liquidity, a 60/40 starting-position proxy, no issuer look-through, no defined calendar-year-loss test, and SPY's U.S. rather than global exposure. These limits support the 0% live allocation decision. The reproduced 10/20 bp figures use the current local code; a separate timestamped capture of the student's 1:54 p.m. app screen is not in the local files.

## AI assistance and human checks

| Tool and model/version | Interaction dates | Use and verification |
|---|---|---|
| OpenAI Codex, GPT-6 in the current session; exact model snapshot and Codex app build are not exposed here | 2026-11-18 and 2026-11-19 | Helped set up and run the app, inspect project requirements, rerun calculations and tests, and update this record and the changed-input result table. The numeric results above were checked against the local deterministic code and Streamlit AppTest. |
| OpenAI Codex, model/version and dates of earlier drafting not independently recorded in the local files | Earlier project work, dates to confirm from chat history | The existing README credits Codex for drafting and reviewing the app, tests, and documentation. The student should supply any additional AI tools, model versions, and dates used in that earlier work before submission. |
| OpenAI Codex with faster-whisper 1.2.1, small.en speech model | 2026-11-22 | Generated timestamped drafts from all three recorded videos and corrected clear project terms. Two uncertain phrases remain marked in the transcripts; the student must listen to the recordings and verify every transcript before submission. |

The student-authored AI-off prediction remains unchanged in the [Locked Changed-Input Record](locked-change-input-record.md). The AI-assisted additions on 2026-11-19 are the reproducible numeric result table and this validation update. One AI output suitable for Video 1 is the proposed 25/0/30/45 portfolio: its reserve is 25%, and its turnover from the 0/0/40/60 benchmark proxy is 25%. Its 6.56% modeled net estimate clears the 6.5% screen by only 0.06 percentage points. The decision is still to reject live allocation because actual holdings, issuer look-through, and the CIO annual-loss rule remain unverified.

## Locked Changed-Input Record

The student reports writing the prediction with AI off at 1:26 p.m. on 2026-11-19, before changing the annual fund fee from 10 to 20 basis points at 1:54 p.m. The [prediction commit](https://github.com/breereim/Ticker/commit/d482c5721a609deaa2c0e8d889161dadc3b7d8e5) is recorded in the form. The original prediction was directional and did not give approximate numeric values; that limitation is preserved rather than retroactively revised.

The local code reproduction gives the constrained portfolio 25/0/30/45, 6.56% net, 9.47% volatility, PASS before the change and 25/0/25/50, 7.15% net, 9.85% volatility, PASS after it. All four portfolio comparisons, including baseline PASS/FAIL results, appear in the record. The modeled verdicts and committee decision did not change. The result commit permalink is not present in the local files yet; insert the post-run GitHub commit URL in the record and submission manifest, and verify the two commit timestamps on GitHub before submission.
