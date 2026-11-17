AI use: I used OpenAI Codex to help write and review the Python app, tests, and documentation.

The analysis and the decision are mine; this is education, not investment advice.

# Video recording guide

These are **outlines**, not transcripts. Record three videos, enable YouTube transcripts, and save or link the actual transcripts here. Each video should begin by speaking the two statements above. Follow the Brightspace student checklist for the required lengths and manifest rows.

## Video 1 — development and checked AI output

Explain how Lab 13's payout reserve and incomplete loss rule changed the design, and how Labs 14–17 added baselines, instability checks, and point-in-time gating. Show one specific Codex output (for example, the proposed 25/0/30/45 mix), manually verify its reserve (25%) and turnover (half the sum of absolute changes from 0/0/40/60 = 25%), and explain why a modeled pass led to a reject recommendation. Show the Locked Changed-Input Record's before/after commits once complete.

## Video 2 — code walkthrough

Start the app from README commands. Show `portfolio.py` CSV validation and annualization, `engine.py` `evaluate`, `grid_weights`, `optimize`, and `stress_table`, then `app.py` tabs and the tests. Change a control and show the live rerun. Explain the five-day liquidity and current-holdings assumptions.

## Video 3 — committee presentation

Open with the app already running live. State the decision and 0% live allocation range, show all three portfolio verdicts and scenario table, then the BAA signal's cutoff and quarantine. End with the stop condition and the evidence needed to revisit a paper pilot.
