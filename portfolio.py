"""Price Meridian's three portfolio baselines using course training inputs.

Run: python portfolio.py
Returns, volatilities, correlations, and weights use decimal units internally.
"""

from math import sqrt


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
