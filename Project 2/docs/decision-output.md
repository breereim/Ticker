# Meridian Foundation Reserve - decision output

Data: 60 monthly returns through July 2026; 10 bp annual fee; 10 bp one-way trade cost; benchmark starting-position proxy.
Screen: 6.5% first-year net estimate; 3% reserve minimum; 25% turnover maximum; 5% weight grid.
Weights: BIL / IEF / LQD / SPY.

| Portfolio | Weights | Net estimate | Volatility | Reserve | Turnover | Coded screen |
|---|---:|---:|---:|---:|---:|---|
| Equal weight | 25.00% / 25.00% / 25.00% / 25.00% | 3.52% | 7.49% | 50.00% | 50.00% | FAIL |
| Inverse volatility | 86.10% / 6.17% / 4.80% / 2.93% | 3.07% | 1.45% | 92.27% | 92.27% | FAIL |
| 60/40 benchmark proxy | 0.00% / 0.00% / 40.00% / 60.00% | 7.65% | 12.59% | 0.00% | 0.00% | FAIL |
| Constrained lowest volatility | 25.00% / 0.00% / 30.00% / 45.00% | 6.56% | 9.47% | 25.00% | 25.00% | PASS |

## One-input stress runs

| Scenario | Weights | Net estimate | Volatility | Turnover | Feasible |
|---|---:|---:|---:|---:|---|
| Base: 60 returns | 25.00% / 0.00% / 30.00% / 45.00% | 6.56% | 9.47% | 25.00% | Yes |
| Estimate: SPY -2 pp | 25.00% / 0.00% / 20.00% / 55.00% | 6.85% | 10.24% | 25.00% | Yes |
| Window: last 36 returns | 25.00% / 0.00% / 40.00% / 35.00% | 9.17% | 7.00% | 25.00% | Yes |
| Costs: fee 40 bp, trade 50 bp | 25.00% / 0.00% / 25.00% / 50.00% | 6.85% | 9.85% | 25.00% | Yes |
| Constraint: reserve >= 30% | n/a | n/a | n/a | n/a | No |
| Constraint: turnover <= 10% | 10.00% / 0.00% / 40.00% / 50.00% | 6.66% | 11.06% | 10.00% | Yes |

Committee decision: REJECT live allocation (0%); paper pilot only.
Issuer look-through, actual holdings/turnover, and the CIO annual-loss rule remain unverified.
A coded pass is a planning screen, not verified mandate compliance or a live allocation approval.
