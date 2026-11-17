# Lab 16 — Provenance Gate

Run `& .\.venv\Scripts\python.exe .\asof.py` from the Course/Work Folder. If `python` is on your PATH, `python asof.py` also works. Change `DECISION_DATE` at the top of the file to test another trading day.

## Known-answer check

On 2026-03-31, the funnel removes row 11 for its missing ticker, row 7 as an exact duplicate, rows 3, 8, and 10 because they were published later, and row 2 because row 4 is AAA's newer February publication. The as-of panel is rows **1, 4, 5, 6, 9, 12**.

| Ticker | As-of signal | Naive signal |
|---|---:|---:|
| AAA | +1.98% (February) | +5.83% (March) |
| BBB | −1.02% (February) | −5.15% (March) |
| CCC | +0.91% (February) | +1.82% (February, revised) |

For the later-date check, setting the decision date to `2026-04-15` makes every as-of signal equal its naive signal: AAA +5.83%, BBB −5.15%, and CCC +1.82%. The file remains set to `2026-03-31`.

## Explain and reflect

The measured month tells which period the index describes. The publication date tells when a trader could first use that particular value. A revision can replace an earlier value for the same measured month. Rule 4 groups rows by ticker and month and keeps the most recent publication left after the decision-date filter. For AAA, that is row 4's February value of 103, rather than row 2's 104.

Look-ahead bias occurs when a historical decision uses information published later. On March 31, AAA's March value of 109 had not been published. Its naive +5.83% February-to-March change could not have been a March 31 signal; the knowable January-to-February change was +1.98%. A backtest using the naive column would attribute decisions to data that was unavailable at the time. The post-date rule has the largest effect on the latest month for AAA and BBB; the revision rule also matters because keeping AAA row 2 would incorrectly give +2.97%.

Partner code explanation, swap, and quiz answer: complete in person. Do not record the solo later-date check as the partner swap.
