# Lab 13 — Meridian Foundation Reserve

## S1–S10: statement types

| Statement | Type | Reason |
|---|---|---|
| S1: Horizon seven years; annual rebalancing. | Hard constraint | It fixes the planning horizon and a portfolio-management operating rule. |
| S2: CPI + 4% a year, net of costs, over rolling five-year periods. | Objective | This states the desired investment outcome, not an absolute guarantee. |
| S3: Pays $0.75m quarterly; twelve months of payouts held in cash or daily-liquid government securities. | Hard constraint | It specifies both the required liquidity reserve and eligible assets. |
| S4: 60% global equities, 40% U.S. investment-grade bonds. | Preference | It is a benchmark for comparison, not stated as a required allocation. |
| S5: Long-only: no borrowing, short sales or derivatives. | Hard constraint | These are explicit prohibitions. |
| S6: No single issuer above 8%. | Hard constraint | This is a measurable concentration limit, with stated exemptions. |
| S7: Annual turnover at most 25% without committee approval. | Hard constraint | It is a measurable limit unless the committee grants approval. |
| S8: At least 90% redeemable within five business days. | Hard constraint | It provides a measurable liquidity threshold and time window. |
| S9: No calendar-year loss greater than 10%. | Unverifiable promise | The CIO has not supplied a measure or a breach rule, so it cannot responsibly be coded as a test. |
| S10: No sector, ESG, tax or home-bias preference; nobody has said what the pilot should optimize. | Missing | The optimization objective/risk criterion is absent even though several non-preferences are stated. |

## Checker

The checker is in `mandate.py`. Run it with:

```powershell
python mandate.py
```

It computes the reserve minimum as `4 × 0.75 ÷ 100 = 3.0%`. Its results for the assigned candidates are:

| Rule | A | B | C |
|---|---|---|---|
| Weights sum to 100 | 100.0 pass | 100.0 pass | 100.0 pass |
| Long-only (lowest weight) | 0.0 pass | 0.0 pass | 0.0 pass |
| Reserve ≥ 3.0% | 14.0 pass | 1.0 FAIL | 2.0 FAIL |
| Redeemable in 5 days ≥ 90% | 100.0 pass | 85.0 FAIL | 100.0 pass |
| Largest single company ≤ 8% | 0.0 pass | 9.0 FAIL | 8.0 pass |
| Calendar-year loss | requires CIO clarification | requires CIO clarification | requires CIO clarification |
| Verdict | passes every checkable rule | fails 3 rule(s) | fails 1 rule(s) |

For the required probe, temporarily change candidate A's Cash weight from `2` to `-2` and its Global equity index fund weight from `60` to `64`. The output should show a lowest weight of `-2.0 FAIL`; its reserve is still `10.0 pass`, and the other checks still pass. Restore the two original values afterward.

## Attack portfolio D

Candidate D is 3% Cash and 97% Treasury 10-year notes. It passes every rule that `mandate.py` can measure: it sums to 100%, is long-only, has a 100% eligible reserve, is 100% redeemable within five days, and holds no non-exempt company issuer.

The objection holds. D may reasonably be rejected because S2 calls for CPI + 4% net over rolling five-year periods, while this nearly all-duration-government-bond portfolio is not designed around that objective; S10 exposes that there is still no selected return/risk objective for optimization.

If checking a partner's D, I would cite S2 against a portfolio whose construction makes the stated real-return objective implausible, while recognizing that S2 is an objective rather than a guaranteed outcome.

## One question for the CIO

**What risk criterion should govern optimization and the S9 loss limit—maximum acceptable probability of a calendar-year loss beyond 10%, a drawdown limit, or something else—and over what measurement convention?**

The answer changes the portfolio: a strict probability-based annual-loss limit would call for a more defensive allocation and potentially cash/Treasuries or bonds, whereas a tolerance for interim losses in pursuit of CPI + 4% would support more global equity exposure.

## Investment policy statement

An investment policy statement (IPS) is the client-and-manager agreement that translates mission, return needs, risk tolerance, liquidity, time horizon, governance, and restrictions into a decision framework. It guides portfolio construction, implementation, monitoring, and review; objectives state what success aims to achieve, while constraints bound what may be held or done.

Meridian's IPS mapping is: S1 gives time horizon and rebalancing governance; S2 the return objective; S3 cash-flow and reserve-liquidity need; S4 the performance benchmark; S5 investment-method restrictions; S6 concentration control; S7 turnover/governance control; S8 general liquidity requirement; S9 an intended risk restriction that is incomplete until measured; and S10 explicitly rules out several preferences but leaves the core optimization criterion unspecified.

## Reflection

A portfolio can pass every coded rule yet still be wrong because code only evaluates explicit, measurable constraints. It cannot decide whether the portfolio has a credible chance of meeting the real return objective, fits the foundation's risk tolerance, or reflects an as-yet-unstated optimization preference. Candidate D illustrates that gap.

I was least certain about S1. I classified it as a hard constraint because the seven-year horizon and annual rebalancing govern how the mandate is managed, although the horizon also supplies contextual information rather than a simple pass/fail holdings test.
