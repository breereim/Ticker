"""Price Meridian's three portfolio baselines using course training inputs.

Run: python portfolio.py
Returns, volatilities, correlations, and weights use decimal units internally.
"""

import csv
from datetime import date
from itertools import combinations
from math import sqrt
from pathlib import Path
import re


# Editable inputs. The order is shared by every table and weight vector below.
SLEEVES = (
    "Treasury bills",
    "Treasury 10-year note",
    "Investment-grade bond fund",
    "Global equity index fund",
)
EXPECTED_RETURNS = (0.035, 0.043, 0.050, 0.080)
VOLATILITIES = (0.005, 0.070, 0.060, 0.160)
CORRELATIONS = (
    (1.00, 0.10, 0.05, 0.00),
    (0.10, 1.00, 0.80, -0.10),
    (0.05, 0.80, 1.00, 0.25),
    (0.00, -0.10, 0.25, 1.00),
)
OBJECTIVE_RETURN = 0.065
RESERVE_ELIGIBLE = ("Treasury bills", "Treasury 10-year note")


def validate_inputs(sleeves, expected_returns, volatilities, correlations):
    """Reject incomplete, asymmetric, or out-of-range input tables."""
    count = len(sleeves)
    if not count or len(expected_returns) != count or len(volatilities) != count:
        raise ValueError("Sleeves, returns, and volatilities must have equal nonzero lengths.")
    if len(set(sleeves)) != count:
        raise ValueError("Sleeve names must be unique.")
    if len(correlations) != count or any(len(row) != count for row in correlations):
        raise ValueError("Correlation table must be square and match the sleeves.")
    if any(volatility <= 0 for volatility in volatilities):
        raise ValueError("Every volatility must be positive.")
    for i in range(count):
        for j in range(count):
            value = correlations[i][j]
            if not -1 <= value <= 1:
                raise ValueError(
                    f"Correlation for {sleeves[i]} / {sleeves[j]} must be between -1 and 1."
                )
            if abs(value - correlations[j][i]) > 1e-12:
                raise ValueError(
                    f"Correlation table is not symmetric: {sleeves[i]} / {sleeves[j]}."
                )
        if abs(correlations[i][i] - 1) > 1e-12:
            raise ValueError(f"Self-correlation for {sleeves[i]} must be 1.")


def covariance_matrix(volatilities, correlations):
    """Covariance[i][j] = correlation[i][j] * volatility[i] * volatility[j]."""
    return tuple(
        tuple(correlations[i][j] * vol_i * vol_j for j, vol_j in enumerate(volatilities))
        for i, vol_i in enumerate(volatilities)
    )


def benchmark_weights(sleeves):
    """Return 40% IG bonds and 60% global equity, in sleeve order."""
    allocations = {
        "Investment-grade bond fund": 0.40,
        "Global equity index fund": 0.60,
    }
    return tuple(allocations.get(sleeve, 0.0) for sleeve in sleeves)


def equal_weights(sleeves):
    """Spread 100% equally over all sleeves."""
    return tuple(1 / len(sleeves) for _ in sleeves)


def inverse_volatility_weights(volatilities):
    """Normalize each reciprocal volatility so the weights total 100%."""
    reciprocals = tuple(1 / volatility for volatility in volatilities)
    total = sum(reciprocals)
    return tuple(value / total for value in reciprocals)


def expected_return(weights, expected_returns):
    """Sum each sleeve's weight times its expected return."""
    return sum(weight * sleeve_return for weight, sleeve_return in zip(weights, expected_returns))


def portfolio_variance(weights, covariances):
    """Include every weighted covariance, including cross-sleeve terms."""
    return sum(
        weights[i] * weights[j] * covariances[i][j]
        for i in range(len(weights))
        for j in range(len(weights))
    )


def portfolio_volatility(weights, covariances):
    """Convert portfolio variance to standard deviation."""
    return sqrt(portfolio_variance(weights, covariances))


def reserve_eligible_weight(weights, sleeves, eligible_sleeves):
    """Sum weights in the reserve-eligible sleeves."""
    return sum(weight for sleeve, weight in zip(sleeves, weights) if sleeve in eligible_sleeves)


def meets_objective(portfolio_return, objective_return):
    """Check the expected-return objective."""
    return portfolio_return >= objective_return


def lowest_risk_mix(
    sleeves, expected_returns, volatilities, correlations,
    objective_return, eligible_sleeves, reserve_minimum,
):
    """Find the lowest-volatility feasible long-only mix on a 5-point grid.

    Returns (weights, expected return, volatility, eligible weight), or None.
    """
    validate_inputs(sleeves, expected_returns, volatilities, correlations)
    if not 0 <= reserve_minimum <= 1:
        raise ValueError("Reserve minimum must be between 0 and 100%.")
    if not set(eligible_sleeves).issubset(sleeves):
        raise ValueError("Eligible assets must appear in the asset list.")

    covariances = covariance_matrix(volatilities, correlations)
    best = None
    # Twenty 5-point units total. Bar positions give every allocation exactly once.
    for bars in combinations(range(20 + len(sleeves) - 1), len(sleeves) - 1):
        boundaries = (-1,) + bars + (20 + len(sleeves) - 1,)
        weights = tuple(
            (boundaries[i + 1] - boundaries[i] - 1) / 20
            for i in range(len(sleeves))
        )
        portfolio_return = expected_return(weights, expected_returns)
        if portfolio_return + 1e-12 < objective_return:
            continue
        reserve = reserve_eligible_weight(weights, sleeves, eligible_sleeves)
        if reserve + 1e-12 < reserve_minimum:
            continue
        volatility = portfolio_volatility(weights, covariances)
        if best is None or volatility < best[2] - 1e-12:
            best = (weights, portfolio_return, volatility, reserve)
    return best


def estimate_from_prices(csv_file, last_36=False):
    """Annualized return, volatility and correlation from monthly prices.

    The CSV has a date column followed by 3-6 assets, oldest month first.
    `last_36` selects the last 36 monthly return observations.
    """
    if hasattr(csv_file, "seek"):
        csv_file.seek(0)
    raw = csv_file.read() if hasattr(csv_file, "read") else Path(csv_file).read_bytes()
    if isinstance(raw, bytes):
        raw = raw.decode("utf-8-sig")
    rows = list(csv.reader(raw.splitlines()))
    if not rows:
        raise ValueError("The price CSV is empty.")
    header = [cell.strip() for cell in rows[0]]
    if not 4 <= len(header) <= 7 or header[0].lower() != "date":
        raise ValueError("Use date first, followed by 3 to 6 asset columns.")
    sleeves = tuple(header[1:])
    if any(not sleeve for sleeve in sleeves) or len(set(sleeves)) != len(sleeves):
        raise ValueError("Asset column names must be nonempty and unique.")
    dates, prices = [], []
    for line_number, row in enumerate(rows[1:], start=2):
        if not row or all(not cell.strip() for cell in row):
            continue
        if len(row) != len(header):
            raise ValueError(f"Row {line_number} has the wrong number of columns.")
        try:
            date_text = row[0].strip()
            if not re.fullmatch(r"\d{4}-\d{2}(?:-\d{2})?", date_text):
                raise ValueError("invalid date")
            month = date.fromisoformat(date_text[:7] + "-01")
            values = tuple(float(cell) for cell in row[1:])
        except ValueError as error:
            raise ValueError(f"Row {line_number} has an invalid date or price.") from error
        if dates and month <= dates[-1]:
            raise ValueError("Dates must be unique and oldest month first.")
        if dates and (month.year - dates[-1].year) * 12 + month.month - dates[-1].month != 1:
            raise ValueError("Prices must have one row for each consecutive month.")
        if any(not 0 < value < float("inf") for value in values):
            raise ValueError(f"Row {line_number} needs positive, finite prices.")
        dates.append(month)
        prices.append(values)
    if len(prices) < (37 if last_36 else 3):
        raise ValueError("Need at least 37 prices for the last 36 returns, or 3 prices for all months.")

    monthly = [
        tuple(current / previous - 1 for previous, current in zip(prices[i - 1], prices[i]))
        for i in range(1, len(prices))
    ]
    if last_36:
        monthly = monthly[-36:]
    count = len(monthly)
    means = tuple(sum(row[i] for row in monthly) / count for i in range(len(sleeves)))
    covariance = tuple(
        tuple(
            sum((row[i] - means[i]) * (row[j] - means[j]) for row in monthly) / (count - 1)
            for j in range(len(sleeves))
        )
        for i in range(len(sleeves))
    )
    monthly_volatility = tuple(sqrt(covariance[i][i]) for i in range(len(sleeves)))
    if any(value == 0 for value in monthly_volatility):
        raise ValueError("Each asset needs varying monthly returns to estimate correlations.")
    correlations = tuple(
        tuple((1.0 if i == j else max(-1.0, min(1.0,
               covariance[i][j] / (monthly_volatility[i] * monthly_volatility[j]))))
              for j in range(len(sleeves)))
        for i in range(len(sleeves))
    )
    return (
        sleeves,
        tuple(mean * 12 for mean in means),
        tuple(value * sqrt(12) for value in monthly_volatility),
        correlations,
    )


def main():
    try:
        validate_inputs(SLEEVES, EXPECTED_RETURNS, VOLATILITIES, CORRELATIONS)
        covariances = covariance_matrix(VOLATILITIES, CORRELATIONS)
        portfolios = (
            ("Benchmark", benchmark_weights(SLEEVES)),
            ("Equal weight", equal_weights(SLEEVES)),
            ("Inverse volatility", inverse_volatility_weights(VOLATILITIES)),
        )
        print(f"Objective return: {OBJECTIVE_RETURN:.1%}")
        print("Weight order: " + " / ".join(SLEEVES))
        print("Portfolio | Weights (%) | Return (%) | Volatility (%) | Reserve-eligible (%) | Meets objective?")
        for name, weights in portfolios:
            portfolio_return = expected_return(weights, EXPECTED_RETURNS)
            volatility = portfolio_volatility(weights, covariances)
            reserve = reserve_eligible_weight(weights, SLEEVES, RESERVE_ELIGIBLE)
            weight_text = " / ".join(f"{weight * 100:.1f}" for weight in weights)
            verdict = "yes" if meets_objective(portfolio_return, OBJECTIVE_RETURN) else "no"
            print(
                f"{name} | {weight_text} | {portfolio_return * 100:.2f} | "
                f"{volatility * 100:.2f} | {reserve * 100:.1f} | {verdict}"
            )
    except ValueError as error:
        raise SystemExit(f"Input error: {error}") from error


if __name__ == "__main__":
    main()
