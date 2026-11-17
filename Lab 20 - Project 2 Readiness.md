# Lab 20 — Project 2 readiness checkout

**Status:** Preparation only. Complete the partner and AI-off sections during the lab, then commit and push this file. Do not describe a local test as the partner's cold run.

## Repository handoff

- GitHub repository URL: `ADD LINK`
- App entrypoint: [`app.py`](app.py)
- README command that produces the decision: `python decision_report.py`
- Visible decision numbers: [`docs/decision-output.md`](docs/decision-output.md)
- Decision memo: [`docs/decision-memo.md`](docs/decision-memo.md)
- Validation and AI use: [`docs/validation-and-ai-use.md`](docs/validation-and-ai-use.md)
- Locked Changed-Input Record: [`docs/locked-change-input-record.md`](docs/locked-change-input-record.md)
- Video 1 link and transcript: `ADD LINKS`
- Video 2 link and transcript: `ADD LINKS`
- Video 3 link and transcript: `ADD LINKS`
- Week 12 studio must-fix list carried into this checkout: `ADD YOUR LIST OR LINK`

## I — partner cold run

Send only the repository URL. Ask your partner to use a fresh folder and follow only the README. Have the partner write this note without coaching.

- Partner name or initials: `PARTNER FILLS IN`
- Date and start/end times: `PARTNER FILLS IN`
- Exact command followed: `PARTNER FILLS IN`
- First failure, or “none”: `PARTNER FILLS IN`
- Elapsed time to result: `PARTNER FILLS IN`
- Where the partner found the decision numbers and verdict: `PARTNER FILLS IN`
- Control moved and mandate verdict observed: `PARTNER FILLS IN`
- Partner's question or confusing README line: `PARTNER FILLS IN`

## V — changed input, predicted before the run

Complete the [Locked Changed-Input Record](docs/locked-change-input-record.md) **with AI closed**. Record the old and new input with units, the expected direction of the decision numbers, the expected decision effect, and the reason. Commit and push that prediction **before** running the change. Then run it and add the actual before/after outputs, decision effect, and explanation in a later commit.

- Prediction commit permalink: `ADD AFTER PRE-RUN PUSH`
- Result commit permalink: `ADD AFTER POST-RUN PUSH`
- Link to before and after output evidence: `ADD LINK OR FILE PATH`

The app's built-in stress scenarios and the generated [decision output](docs/decision-output.md) are useful comparisons, but they do not replace the required pre-run, human-authored prediction.

## Explain the code — no AI during the exchange

Open [`engine.py`](engine.py) at `evaluate` and `optimize`. Explain how the first-year net estimate, hard-limit checks, and lowest-volatility feasible mix produce the decision numbers. Then swap roles.

- Code lines explained to partner: `FILL IN DURING LAB`
- Partner's question: `FILL IN DURING LAB`
- My answer from the code: `FILL IN DURING LAB`
- Line I could not explain, if any: `FILL IN DURING LAB`

## E — fix one thing

- First cold-run failure or confusion selected for repair: `FILL IN AFTER COLD RUN`
- File and exact change made, or “clean cold run; no fix needed”: `FILL IN`
- Fix commit permalink, if changed: `ADD LINK`
- Partner rerun result: `FILL IN AFTER RERUN`

## Decision line

**Reject live allocation (0%); reconsider a paper pilot after actual holdings and turnover, ETF issuer look-through, and the CIO's calendar-year-loss rule are verified.**

This line matches the [decision memo](docs/decision-memo.md). Edit it if the changed-input run changes the committee decision, and keep the memo and visible output consistent.

## Reflect with partner

1. What the cold run found that I could not see: `FILL IN AFTER DISCUSSION`
2. What I will not touch before the deadline: `FILL IN AFTER DISCUSSION`

## Individual checkout — GitHub links

- This completed Lab 20 `.md` file: `ADD GITHUB LINK`
- README and decision-producing `.py` file: `ADD GITHUB LINKS`
- Partner cold-run note: `LINK THIS FILE AFTER PUSH`
- Prediction commit: `ADD LINK`
- Fix commit or clean-run record: `ADD LINK TO COMMIT OR THIS FILE`
- Decision memo and visible output: `ADD GITHUB LINKS`

The Project 2 deadline and submission items are in the Brightspace assignment header. This Lab 20 checkout records readiness and unresolved items; it does not approve Project 2.
