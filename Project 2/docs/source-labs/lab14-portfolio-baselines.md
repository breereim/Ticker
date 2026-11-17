# Lab 14 — Meridian portfolio baselines

Run the engine with `python portfolio.py` and the mandate checker with `python mandate.py`.
The inputs in `portfolio.py` are course-authored training values, not market estimates.

| Portfolio | Weights: bills / 10-year / IG / equity (%) | Return (%) | Volatility (%) | Reserve-eligible (%) | Meets 6.5%? |
|---|---|---:|---:|---:|---|
| Benchmark | 0.0 / 0.0 / 40.0 / 60.0 | 6.80 | 10.46 | 0.0 | yes |
| Equal weight | 25.0 / 25.0 / 25.0 / 25.0 | 5.20 | 5.21 | 50.0 | no |
| Inverse volatility | 84.3 / 6.0 / 7.0 / 2.6 | 3.77 | 1.05 | 90.3 | no |

The figures above were checked independently from the supplied inputs. The benchmark's variance is
`0.4² × 0.06² + 0.6² × 0.16² + 2 × 0.4 × 0.6 × 0.06 × 0.16 × 0.25 = 0.010944`.
Its volatility is `sqrt(0.010944) = 10.46%`. Changing both IG–equity correlation
cells from `0.25` to `0.50` raises it to `11.00%`; restore both to `0.25` afterward.

In `portfolio.py`, `covariance_matrix` multiplies each correlation by its two sleeve
volatilities. `portfolio_variance` multiplies every covariance by the matching pair of
weights and adds all pairs. `portfolio_volatility` takes the square root. Cross-sleeve
terms capture diversification: correlation below +1 makes their contribution smaller
than if the sleeves moved together perfectly.

Inverse volatility puts 84.3% in bills because their 0.5% volatility has the largest
reciprocal. I would show the CIO the benchmark first: it clears the assumed 6.5%
expected-return objective, but its 0% eligible reserve fails Meridian's 3% reserve
minimum. Candidate E in `mandate.py` represents this benchmark and should fail that
rule. The expected return is an estimate, not a guarantee of the stated real-return
objective.
