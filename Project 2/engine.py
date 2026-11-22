"""Meridian committee model. Annualized estimates are not forecasts."""

from itertools import combinations
from math import isfinite
from pathlib import Path

from portfolio import (
    covariance_matrix, equal_weights, estimate_from_prices,
    expected_return, inverse_volatility_weights, portfolio_volatility,
)

ASSETS = ("BIL", "IEF", "LQD", "SPY")
CURRENT = (0.0, 0.0, 0.40, 0.60)  # benchmark proxy; actual holdings not supplied
RESERVE = (0, 1)
OBJECTIVE = 0.065  # CPI assumption 2.5% + 4%; only a planning proxy
MIN_RESERVE = 0.03
MIN_LIQUID = 0.90
MAX_TURNOVER = 0.25
GRID = 20


def estimates(last_36=False, path=None):
    source = path or Path(__file__).with_name("prices.csv")
    names, means, vols, corr = estimate_from_prices(source, last_36=last_36)
    if names != ASSETS:
        raise ValueError("Expected date,BIL,IEF,LQD,SPY columns in that order")
    return means, vols, corr


def turnover(weights, current=CURRENT):
    return sum(abs(a - b) for a, b in zip(weights, current)) / 2


def evaluate(weights, means, vols, corr, *, fee_bps=10, trade_bps=10,
             current=CURRENT, reserve_min=MIN_RESERVE,
             turnover_limit=MAX_TURNOVER, liquid=(True, True, True, True)):
    if len(weights) != 4 or len(means) != 4 or len(vols) != 4:
        raise ValueError("Four weights, returns, and volatilities are required")
    if not all(isfinite(x) for x in (*weights, *means, *vols)):
        raise ValueError("Inputs must be finite")
    if fee_bps < 0 or trade_bps < 0 or not 0 <= reserve_min <= 1 or not 0 <= turnover_limit <= 1:
        raise ValueError("Costs and limits must be nonnegative and shares within 0 to 1")
    traded = turnover(weights, current)
    gross = expected_return(weights, means)
    # First-year planning estimate: annual fund fee plus one rebalance cost.
    net = gross - fee_bps / 10000 - traded * trade_bps / 10000
    vol = portfolio_volatility(weights, covariance_matrix(vols, corr))
    reserve = sum(weights[i] for i in RESERVE)
    liquid_share = sum(w for w, ok in zip(weights, liquid) if ok)
    checks = {
        "Weights total 100%": abs(sum(weights) - 1) < 1e-9,
        "Long only": min(weights) >= -1e-9,
        f"Reserve at least {reserve_min:.0%}": reserve + 1e-9 >= reserve_min,
        "Five day liquidity at least 90%": liquid_share + 1e-9 >= MIN_LIQUID,
        f"Turnover at most {turnover_limit:.0%}": traded <= turnover_limit + 1e-9,
    }
    return dict(weights=weights, gross=gross, net=net, volatility=vol,
                reserve=reserve, liquid=liquid_share, turnover=traded,
                objective=net >= OBJECTIVE, checks=checks,
                failures=[name for name, passed in checks.items() if not passed],
                # ETF underlying issuer exposures and CIO loss rule remain unresolved.
                unknowns=["Underlying issuer look-through <= 8% not verified",
                          "Calendar-year loss rule has no CIO definition",
                          "Actual current holdings and turnover not verified"])


def grid_weights():
    for bars in combinations(range(GRID + 3), 3):
        boundaries = (-1,) + bars + (GRID + 3,)
        yield tuple((boundaries[i + 1] - boundaries[i] - 1) / GRID for i in range(4))


def optimize(means, vols, corr, *, fee_bps=10, trade_bps=10,
             current=CURRENT, reserve_min=MIN_RESERVE,
             turnover_limit=MAX_TURNOVER, liquid=(True, True, True, True)):
    best = None
    for weights in grid_weights():
        row = evaluate(weights, means, vols, corr, fee_bps=fee_bps,
                       trade_bps=trade_bps, current=current,
                       reserve_min=reserve_min, turnover_limit=turnover_limit,
                       liquid=liquid)
        if row["failures"] or not row["objective"]:
            continue
        if best is None or row["volatility"] < best["volatility"] - 1e-12:
            best = row
    return best


def run_case(*, last_36=False, equity_delta=0.0, fee_bps=10,
             trade_bps=10, reserve_min=MIN_RESERVE,
             turnover_limit=MAX_TURNOVER, liquid=(True, True, True, True)):
    means, vols, corr = estimates(last_36)
    means = (*means[:3], means[3] + equity_delta)
    options = dict(fee_bps=fee_bps, trade_bps=trade_bps,
                   reserve_min=reserve_min, turnover_limit=turnover_limit,
                   liquid=liquid)
    return {
        "equal": evaluate(equal_weights(ASSETS), means, vols, corr, **options),
        "inverse_vol": evaluate(inverse_volatility_weights(vols), means, vols, corr, **options),
        "benchmark": evaluate(CURRENT, means, vols, corr, **options),
        "portfolio": optimize(means, vols, corr, **options),
        "means": means, "vols": vols,
    }


def stress_table():
    scenarios = (
        ("Base: 60 returns", {}),
        ("Estimate: SPY -2 pp", {"equity_delta": -0.02}),
        ("Window: last 36 returns", {"last_36": True}),
        ("Costs: fee 40 bp, trade 50 bp", {"fee_bps": 40, "trade_bps": 50}),
        ("Constraint: reserve >= 30%", {"reserve_min": 0.30}),
        ("Constraint: turnover <= 10%", {"turnover_limit": 0.10}),
    )
    result = []
    for label, kwargs in scenarios:
        case = run_case(**kwargs)
        row = case["portfolio"]
        result.append(dict(scenario=label, feasible=row is not None,
                           weights=None if row is None else row["weights"],
                           net=None if row is None else row["net"],
                           volatility=None if row is None else row["volatility"],
                           turnover=None if row is None else row["turnover"]))
    return result
