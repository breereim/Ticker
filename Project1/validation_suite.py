"""Reproducible technical validation for the JNJ Project 1 model.

Run from this folder with the supplied virtual-environment Python.
"""

from jnj_project1_fcff import (
    BASE_ASSUMPTIONS,
    MARKET_PRICE,
    dcf,
    evaluate_model,
    project,
)
from jnj_peer_multiples import COMPANIES, metrics


def approx(left: float, right: float, tolerance: float = 0.01) -> None:
    if abs(left - right) > tolerance:
        raise AssertionError(f"Expected {left} to equal {right} within {tolerance}.")


def main() -> None:
    base = evaluate_model()
    value = base["valuation"]["value_per_share"]
    checks = base["checks"]

    # Pro-forma articulation and base-year filing reconciliation.
    assert checks["all_forecast_balance_sheets_balance"]
    assert checks["cash_flow_ties_to_cash"]
    approx(checks["opening_balance_sheet_reconciliation"], 0.0)
    approx(checks["filing_input_benchmark_difference"], 0.0)
    for row in base["forecasts"]:
        approx(row["balance_check"], 0.0)
        approx(row["cash_flow_check"], 0.0)
        approx(row["net_change_in_cash"], row["fcfe"] - row["dividend"])

    # EV-to-equity bridge: EV + excess cash - debt = equity value.
    valuation = base["valuation"]
    approx(valuation["enterprise_value"] + valuation["excess_cash"] - valuation["debt"], valuation["equity_value"])
    approx(valuation["equity_value"] / base["metadata"]["shares_m"], value)

    # DCF boundaries and expected directions.
    forecasts = project(BASE_ASSUMPTIONS)
    lower_wacc = dcf(forecasts, {**BASE_ASSUMPTIONS, "wacc": 0.050})["value_per_share"]
    higher_wacc = dcf(forecasts, {**BASE_ASSUMPTIONS, "wacc": 0.070})["value_per_share"]
    lower_g = dcf(forecasts, {**BASE_ASSUMPTIONS, "terminal_growth": 0.020})["value_per_share"]
    higher_g = dcf(forecasts, {**BASE_ASSUMPTIONS, "terminal_growth": 0.035})["value_per_share"]
    assert lower_wacc > value > higher_wacc, "WACC monotonicity failed."
    assert lower_g < value < higher_g, "Terminal-growth monotonicity failed."

    # Highest-risk failure test, specified before execution in the locked-record template:
    # a one-point decline in every annual growth rate must reduce operating output and value.
    downside = evaluate_model({"revenue_growth": [0.040, 0.030, 0.030, 0.025, 0.020]})
    assert downside["forecasts"][-1]["fcff"] < base["forecasts"][-1]["fcff"]
    assert downside["valuation"]["enterprise_value"] < valuation["enterprise_value"]
    assert downside["valuation"]["value_per_share"] < value

    # Peer-policy / multiple-definition consistency: same formula and a hand-checkable MRK P/E.
    mrk = next(company for company in COMPANIES if company["ticker"] == "MRK")
    _, _, _, mrk_pe = metrics(mrk)
    approx(mrk_pe, 144.71 / 7.28, 0.000001)
    for company in COMPANIES:
        market_cap, enterprise_value, ev_ebit, pe = metrics(company)
        approx(enterprise_value, market_cap + company["debt"] - company["cash"])
        assert ev_ebit > 0 and pe > 0

    print("PASS: base-year reconciliation, articulation, bridge, DCF monotonicity, peer definitions, and high-risk downside test.")
    print(f"Base: ${value:.2f}/share; downside: ${downside['valuation']['value_per_share']:.2f}/share; market reference: ${MARKET_PRICE:.2f}/share.")


if __name__ == "__main__":
    main()
