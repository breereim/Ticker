AI use: I used OpenAI Codex to help write and review the Python app, tests, and documentation.

The analysis and the decision are mine; this is education, not investment advice.

# Investment committee decision memo

**Mandate:** Meridian Foundation Reserve, $100m, seven years, annual rebalance. **Decision:** reject live allocation to this process now. **Allocation range:** 0% of reserve capital until the stop conditions clear. The app may be piloted with paper weights and reviewed by the committee. This is a rejection of current deployment, not a claim that the ETFs are categorically unsuitable.

The exact baseline and scenario values are in the [code-generated decision output](decision-output.md), reproduced with `python decision_report.py` from the repository root.

## Why

The 60-month historical estimate, 10 bp annual fee, 10 bp one-way trade cost, and 60/40 starting-position proxy yield a lowest-volatility feasible 5% grid mix of **25% BIL / 0% IEF / 30% LQD / 45% SPY**, with **6.56% first-year net estimated return**, **9.47% annualized historical volatility**, **25% modeled turnover**, and **25% reserve-eligible assets**. It passes the coded weights, long-only, reserve, liquidity assumption, and turnover-proxy checks. Its margin over the 6.5% return screen is only about 0.06 percentage points. This is a historical estimate, not evidence of CPI + 4% net across rolling five-year periods.

The equal-weight baseline is **25/25/25/25**, 3.52% net and 7.49% volatility. It fails the 25% turnover rule against the proxy starting portfolio and the 6.5% return screen. Inverse volatility is about **86.10/6.17/4.80/2.93**, 3.07% net and 1.45% volatility. It also fails turnover and return. The 60/40 benchmark proxy has 7.65% net, 12.59% volatility, and **fails the 3% reserve rule**. The comparison shows that a high estimated return alone does not make a mix mandate-compliant.

Three blockers prevent a live recommendation: the actual holdings are absent, so turnover cannot be certified; ETF look-through is absent, so the 8% nonexempt single-issuer cap cannot be certified; and the CIO has not defined the calendar-year-loss measure or breach response. SPY also leaves a global-equity benchmark mismatch. Historical adjusted prices were downloaded after many sample dates, so the optimizer is not a point-in-time backtest. The BAA diagnostic is properly dated for one decision date but quarantined from weights.

## Stress and stop rule

Rerun the app's scenario table before any committee meeting. It changes SPY's return estimate, uses the last 36 returns, raises costs, raises the reserve minimum, and tightens turnover. The baseline portfolio is at the turnover limit, and the alternate windows and costs change its weights. A 30% reserve minimum is infeasible with the 25% turnover cap from the modeled starting mix. The process **stops** if no feasible mix exists, any checkable mandate rule fails, or the three unresolved items above remain unverified. The screen also fails as a decision basis if the adjusted return estimate falls below 6.5% after costs. Do not override an infeasible result by relaxing a hard rule without committee approval.

## Reconsideration triggers

Reconsider a paper pilot only after the CIO supplies a measurable annual-loss rule, the custodian supplies actual holdings and a turnover calculation, the fund disclosures and holdings support issuer look-through and five-day liquidity, and a global-equity benchmark implementation is chosen. Monitor CPI assumptions, fee and trade estimates, the annual rebalance's turnover, BAA vintage availability, and the return estimate's margin to 6.5% under 36- and 60-month windows. A shift of 10 percentage points or more in any sleeve under a routine input refresh should return to committee review. A live allocation range requires a new decision memo after those gates clear.
