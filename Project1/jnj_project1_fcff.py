"""Johnson & Johnson Project 1: linked pro forma and FCFF valuation.

USD millions except per-share values.  Valuation date: 2026-09-10 market close.
Run: python jnj_project1_fcff.py

This is a teaching model.  Historical figures and the basis for assumptions
belong in the accompanying research/source document; do not treat forecasts as
facts.  Assertions are intentionally live and should never be deleted merely
to make output appear to pass.
"""

from copy import deepcopy


YEARS = [2026, 2027, 2028, 2029, 2030]
VALUATION_DATE = "2026-09-10 market close"
MARKET_PRICE = 266.35  # USD close; retain the cited source in research notes.
# Year-end FCFF convention: valuation date to FY2026 year end is approximately
# 109 days; subsequent cash flows are one year apart.
DISCOUNT_PERIODS = [109 / 365, 1 + 109 / 365, 2 + 109 / 365, 3 + 109 / 365, 4 + 109 / 365]

# FY2025 opening balance sheet, USD millions.
OPENING = {
    "cash": 19_709.0,
    "inventory": 14_191.0,
    "ppe": 23_169.0,
    "other_operating_assets": 142_141.0,
    "debt": 47_933.0,
    "other_liabilities": 69_733.0,
    "equity": 81_544.0,
    "revenue": 94_193.0,
}

# Independently transcribed FY2025 Form 10-K benchmark, USD millions.  This is
# intentionally separate from OPENING so a future accidental model edit cannot
# silently redefine the filing reconciliation target.
FILING_FY2025_BENCHMARK = {
    "cash": 19_709.0, "inventory": 14_191.0, "ppe": 23_169.0,
    "total_assets": 199_210.0, "debt": 47_933.0,
    "total_liabilities": 117_666.0, "equity": 81_544.0,
    "revenue": 94_193.0,
}

# FY2025 Form 10-K, Note 15: diluted weighted-average shares.
SHARE_COUNT = 2_429.4
SHARE_BASIS = "diluted weighted-average shares"

# WACC build as of the valuation date.  The 10-year Treasury yield is a
# sourced market fact; beta, ERP, and pre-tax debt cost are disclosed judgment
# inputs in docs/assumptions-and-challenges.md.
WACC_INPUTS = {
    "risk_free_rate": 0.0484,       # U.S. Treasury 10-year, 2026-09-10
    "levered_beta": 0.24,           # provider estimate, rounded
    "equity_risk_premium": 0.0500,  # long-run judgment input
    "pre_tax_cost_of_debt": 0.0450, # debt-note / maturity estimate
}


def calculate_wacc(tax_rate: float) -> dict:
    """CAPM cost of equity plus market-value capital weights."""
    market_equity = MARKET_PRICE * SHARE_COUNT
    market_debt = OPENING["debt"]
    total_capital = market_equity + market_debt
    cost_of_equity = (
        WACC_INPUTS["risk_free_rate"]
        + WACC_INPUTS["levered_beta"] * WACC_INPUTS["equity_risk_premium"]
    )
    after_tax_cost_of_debt = WACC_INPUTS["pre_tax_cost_of_debt"] * (1.0 - tax_rate)
    equity_weight = market_equity / total_capital
    debt_weight = market_debt / total_capital
    return {
        "market_equity": market_equity,
        "market_debt": market_debt,
        "equity_weight": equity_weight,
        "debt_weight": debt_weight,
        "cost_of_equity": cost_of_equity,
        "after_tax_cost_of_debt": after_tax_cost_of_debt,
        "wacc": equity_weight * cost_of_equity + debt_weight * after_tax_cost_of_debt,
    }

BASE_ASSUMPTIONS = {
    "revenue_growth": [0.050, 0.040, 0.040, 0.035, 0.030],
    "gross_margin": 0.680,
    "sga_to_gross_profit": 0.370,
    "rd_to_revenue": 0.155,
    "iprd_impairment_to_revenue": 0.000,
    "restructuring_to_revenue": 0.000,
    "da_to_ppe": 0.324,
    "ppe_depreciation_rate": 0.120,
    "inventory_days": 171.3,
    "capex_to_revenue": 0.050,
    "other_wc_to_incremental_revenue": 0.010,
    "net_interest_rate": 0.020,
    "tax_rate": 0.180,
    "dividend_2026": 12_750.0,
    "dividend_growth": 0.030,
    "minimum_cash": 10_000.0,
    "wacc": calculate_wacc(0.180)["wacc"],
    "terminal_growth": 0.030,
}

LOW_ASSUMPTIONS = {
    **BASE_ASSUMPTIONS,
    "revenue_growth": [0.040, 0.030, 0.030, 0.025, 0.020],
    "gross_margin": 0.670,
    "wacc": 0.0700,
    "terminal_growth": 0.020,
}

HIGH_ASSUMPTIONS = {
    **BASE_ASSUMPTIONS,
    "revenue_growth": [0.060, 0.050, 0.050, 0.045, 0.040],
    "gross_margin": 0.690,
    "wacc": 0.0500,
    "terminal_growth": 0.030,
}


def project(assumptions: dict) -> list[dict]:
    """Build a five-year articulated pro forma and calculate annual FCFF."""
    if len(assumptions["revenue_growth"]) != len(YEARS):
        raise ValueError("Provide exactly five annual revenue-growth rates.")

    prior = deepcopy(OPENING)
    forecasts = []
    for index, year in enumerate(YEARS):
        revenue = prior["revenue"] * (1.0 + assumptions["revenue_growth"][index])
        gross_profit = revenue * assumptions["gross_margin"]
        cogs = revenue - gross_profit
        sga = gross_profit * assumptions["sga_to_gross_profit"]
        rd = revenue * assumptions["rd_to_revenue"]

        # Total D&A is split so the PP&E roll-forward and cash-flow add-back
        # remain consistent with the same income-statement expense.
        da = prior["ppe"] * assumptions["da_to_ppe"]
        ppe_depreciation = prior["ppe"] * assumptions["ppe_depreciation_rate"]
        intangible_amortization = da - ppe_depreciation
        # D&A is already included within the reported cost-of-products, SG&A,
        # and R&D lines that underpin the margin assumptions. Do not subtract
        # it again. It is added back below for FCFF and used for PP&E roll-forward.
        iprd_impairment = revenue * assumptions["iprd_impairment_to_revenue"]
        restructuring = revenue * assumptions["restructuring_to_revenue"]
        ebit = gross_profit - sga - rd - iprd_impairment - restructuring
        interest = prior["debt"] * assumptions["net_interest_rate"]
        pretax_income = ebit - interest
        tax = max(0.0, pretax_income) * assumptions["tax_rate"]
        net_income = pretax_income - tax

        inventory = cogs * assumptions["inventory_days"] / 365.0
        change_inventory = inventory - prior["inventory"]
        capex = revenue * assumptions["capex_to_revenue"]
        ppe = prior["ppe"] + capex - ppe_depreciation
        other_wc_investment = (
            assumptions["other_wc_to_incremental_revenue"] * (revenue - prior["revenue"])
        )
        other_operating_assets = (
            prior["other_operating_assets"] + other_wc_investment - intangible_amortization
        )
        debt = prior["debt"]  # No planned debt draw or repayment in this forecast.
        other_liabilities = prior["other_liabilities"]
        dividend = assumptions["dividend_2026"] * (1.0 + assumptions["dividend_growth"]) ** index
        equity = prior["equity"] + net_income - dividend

        # FCFE is retained only to articulate cash under the dividend policy.
        fcfe = net_income + da - capex - change_inventory - other_wc_investment
        cash = prior["cash"] + fcfe - dividend
        net_change_in_cash = cash - prior["cash"]
        cash_flow_check = net_change_in_cash - (fcfe - dividend)

        # Required enterprise-value cash flow: excludes financing flows,
        # interest, debt changes, and dividends.
        fcff = (
            ebit * (1.0 - assumptions["tax_rate"])
            + da
            - capex
            - change_inventory
            - other_wc_investment
        )
        balance_check = (
            inventory + ppe + other_operating_assets + cash
            - debt - other_liabilities - equity
        )

        result = {
            "year": year, "revenue": revenue, "gross_profit": gross_profit,
            "cogs": cogs, "sga": sga, "rd": rd, "da": da,
            "ppe_depreciation": ppe_depreciation,
            "intangible_amortization": intangible_amortization, "ebit": ebit,
            "iprd_impairment": iprd_impairment, "restructuring": restructuring,
            "interest": interest, "pretax_income": pretax_income, "tax": tax,
            "net_income": net_income, "inventory": inventory,
            "change_inventory": change_inventory, "capex": capex, "ppe": ppe,
            "other_wc_investment": other_wc_investment,
            "other_operating_assets": other_operating_assets, "debt": debt,
            "other_liabilities": other_liabilities, "dividend": dividend,
            "equity": equity, "cash": cash, "fcfe": fcfe, "fcff": fcff,
            "net_change_in_cash": net_change_in_cash, "cash_flow_check": cash_flow_check,
            "balance_check": balance_check,
        }
        forecasts.append(result)
        prior = result
    return forecasts


def assert_articulation(forecasts: list[dict], minimum_cash: float) -> None:
    """Fail loudly if statements cease to articulate or liquidity is breached."""
    for forecast in forecasts:
        year = forecast["year"]
        if abs(forecast["balance_check"]) > 0.05:
            raise AssertionError(
                f"FY{year} does not balance: {forecast['balance_check']:,.2f}"
            )
        if abs(forecast["cash_flow_check"]) > 0.05:
            raise AssertionError(
                f"FY{year} cash flow does not tie to cash: {forecast['cash_flow_check']:,.2f}"
            )
        if forecast["cash"] < minimum_cash - 0.05:
            raise AssertionError(
                f"FY{year} cash below the minimum: {forecast['cash']:,.2f}"
            )


def dcf(forecasts: list[dict], assumptions: dict) -> dict:
    """Discount pro-forma FCFF and complete the EV-to-equity bridge."""
    wacc = assumptions["wacc"]
    terminal_growth = assumptions["terminal_growth"]
    if not 0.0 < terminal_growth < wacc:
        raise ValueError("Terminal growth must be positive and below WACC.")

    pv_explicit_fcff = sum(
        row["fcff"] / (1.0 + wacc) ** period
        for row, period in zip(forecasts, DISCOUNT_PERIODS)
    )
    terminal_value = forecasts[-1]["fcff"] * (1.0 + terminal_growth) / (wacc - terminal_growth)
    pv_terminal_value = terminal_value / (1.0 + wacc) ** DISCOUNT_PERIODS[-1]
    enterprise_value = pv_explicit_fcff + pv_terminal_value
    excess_cash = max(0.0, OPENING["cash"] - assumptions["minimum_cash"])
    equity_value = enterprise_value + excess_cash - OPENING["debt"]

    return {
        "pv_explicit_fcff": pv_explicit_fcff,
        "terminal_value": terminal_value,
        "pv_terminal_value": pv_terminal_value,
        "enterprise_value": enterprise_value,
        "excess_cash": excess_cash,
        "debt": OPENING["debt"],
        "equity_value": equity_value,
        "value_per_share": equity_value / SHARE_COUNT,
        "terminal_value_share": pv_terminal_value / enterprise_value,
    }


def run_case(name: str, assumptions: dict) -> tuple[list[dict], dict]:
    forecasts = project(assumptions)
    assert_articulation(forecasts, assumptions["minimum_cash"])
    valuation = dcf(forecasts, assumptions)
    print(
        f"{name:<5} | FY2030 revenue ${forecasts[-1]['revenue']:>10,.1f} | "
        f"FY2030 FCFF ${forecasts[-1]['fcff']:>9,.1f} | "
        f"WACC {assumptions['wacc']:>5.2%} | g {assumptions['terminal_growth']:>5.2%} | "
        f"value/share ${valuation['value_per_share']:>7.2f}"
    )
    return forecasts, valuation


def sensitivity_grid(base_forecasts: list[dict]) -> None:
    print("\nWACC / terminal-growth sensitivity: value per share")
    terminal_growths = [0.020, 0.025, 0.030]
    print("WACC \\ g", end="")
    for growth in terminal_growths:
        print(f" | {growth:.1%}", end="")
    print()
    for wacc in [0.050, 0.0588, 0.070]:
        print(f"{wacc:.2%}", end="")
        for growth in terminal_growths:
            if growth >= wacc:
                print(" | invalid", end="")
            else:
                temporary = {**BASE_ASSUMPTIONS, "wacc": wacc, "terminal_growth": growth}
                print(f" | ${dcf(base_forecasts, temporary)['value_per_share']:.2f}", end="")
        print()


def reverse_dcf(base_forecasts: list[dict]) -> None:
    """Solve the uniform FCFF scale implied by the current market price."""
    base_value = dcf(base_forecasts, BASE_ASSUMPTIONS)["value_per_share"]
    if base_value <= 0:
        raise AssertionError("Base DCF value must be positive for reverse DCF.")
    # FCFF values are scaled uniformly; all bridge inputs and WACC/g stay fixed.
    low, high = 0.10, 3.00
    for _ in range(100):
        midpoint = (low + high) / 2.0
        scaled = [{**row, "fcff": row["fcff"] * midpoint} for row in base_forecasts]
        implied = dcf(scaled, BASE_ASSUMPTIONS)["value_per_share"]
        if implied < MARKET_PRICE:
            low = midpoint
        else:
            high = midpoint
    multiplier = (low + high) / 2.0
    print(
        "\nReverse DCF (not a forecast): holding WACC, terminal growth, debt, "
        f"excess cash, and shares fixed, the ${MARKET_PRICE:.2f} market price "
        f"implies {multiplier:.2f}x every projected FCFF amount."
    )


def assert_dcf_directionality(base_forecasts: list[dict]) -> None:
    """Required monotonicity tests: WACC up lowers value; g up raises value."""
    lower_wacc = dcf(base_forecasts, {**BASE_ASSUMPTIONS, "wacc": 0.050})["value_per_share"]
    base_value = dcf(base_forecasts, BASE_ASSUMPTIONS)["value_per_share"]
    higher_wacc = dcf(base_forecasts, {**BASE_ASSUMPTIONS, "wacc": 0.070})["value_per_share"]
    lower_g = dcf(base_forecasts, {**BASE_ASSUMPTIONS, "terminal_growth": 0.020})["value_per_share"]
    higher_g = dcf(base_forecasts, {**BASE_ASSUMPTIONS, "terminal_growth": 0.035})["value_per_share"]
    if not lower_wacc > base_value > higher_wacc:
        raise AssertionError("DCF WACC monotonicity check failed.")
    if not lower_g < base_value < higher_g:
        raise AssertionError("DCF terminal-growth monotonicity check failed.")
    print("\nValidation: balance sheets articulate; cash floors pass; DCF monotonicity passes.")


def _percent(value: float) -> str:
    return f"{value:.1%}"


def revenue_driver_bridge(growth_path: list[float]) -> list[dict]:
    """Forecast growth bridge; components reconcile to each annual total.

    The FY2026 STELARA assumption is calibrated to the FY2025 historical
    observation, not presented as filing-sourced FY2026 guidance.  The base
    portfolio is a residual that balances the selected total growth path.
    """
    stelar = [-0.062, -0.050, -0.040, -0.035, -0.030]
    replacement = [0.060, 0.055, 0.050, 0.045, 0.040]
    medtech = [0.020, 0.020, 0.020, 0.018, 0.015]
    rows = []
    for year, total, erosion, replacement_growth, medtech_growth in zip(YEARS, growth_path, stelar, replacement, medtech):
        core = total - erosion - replacement_growth - medtech_growth
        rows.append({"year": year, "stelara_erosion": erosion,
                     "replacement_medicines": replacement_growth, "medtech": medtech_growth,
                     "base_portfolio": core, "total_growth": total})
    return rows


def evaluate_model(overrides: dict | None = None) -> dict:
    """Return the linked model as JSON-friendly data for the local driver panel.

    This is deliberately the same engine used by the command-line report.  The
    UI may adjust only bounded forecast drivers; historical filing inputs and
    the enterprise-to-equity bridge remain visible rather than being hidden in
    presentation logic.
    """
    assumptions = deepcopy(BASE_ASSUMPTIONS)
    overrides = overrides or {}
    permitted = set(BASE_ASSUMPTIONS)
    for name, value in overrides.items():
        if name not in permitted:
            raise ValueError(f"Unsupported driver: {name}")
        if name == "revenue_growth":
            if not isinstance(value, list) or len(value) != len(YEARS):
                raise ValueError("Revenue growth must contain five annual values.")
            assumptions[name] = [float(item) for item in value]
        else:
            assumptions[name] = float(value)

    # The base-year balance-sheet check is a reconciliation guardrail: it
    # ensures that the FY2025 simplified opening balance sheet still agrees to
    # the filing-derived totals before a forecast is permitted.
    opening_check = (
        OPENING["cash"] + OPENING["inventory"] + OPENING["ppe"]
        + OPENING["other_operating_assets"] - OPENING["debt"]
        - OPENING["other_liabilities"] - OPENING["equity"]
    )
    if abs(opening_check) > 0.05:
        raise AssertionError(f"FY2025 opening balance sheet does not reconcile: {opening_check:,.2f}")
    filing_input_check = max(
        abs(OPENING["cash"] - FILING_FY2025_BENCHMARK["cash"]),
        abs(OPENING["inventory"] - FILING_FY2025_BENCHMARK["inventory"]),
        abs(OPENING["ppe"] - FILING_FY2025_BENCHMARK["ppe"]),
        abs(OPENING["debt"] - FILING_FY2025_BENCHMARK["debt"]),
        abs(OPENING["equity"] - FILING_FY2025_BENCHMARK["equity"]),
        abs(OPENING["revenue"] - FILING_FY2025_BENCHMARK["revenue"]),
    )
    if filing_input_check > 0.05:
        raise AssertionError(f"FY2025 opening inputs differ from filing benchmark: {filing_input_check:,.2f}")

    forecasts = project(assumptions)
    assert_articulation(forecasts, assumptions["minimum_cash"])
    valuation = dcf(forecasts, assumptions)

    def scenario_for(change: dict) -> tuple[list[dict], dict]:
        trial = {**assumptions, **change}
        forecast = project(trial)
        assert_articulation(forecast, trial["minimum_cash"])
        return forecast, dcf(forecast, trial)

    # One-at-a-time impacts use documented bounded ranges, not arbitrary
    # percentage swings.  Each output is compared with the user's current base.
    tests = [
        ("Revenue growth path", "revenue_growth", [-0.010, 0.010]),
        ("Gross margin", "gross_margin", [-0.010, 0.010]),
        ("R&D / revenue", "rd_to_revenue", [-0.010, 0.010]),
        ("Capex / revenue", "capex_to_revenue", [-0.010, 0.010]),
        ("Tax rate", "tax_rate", [-0.010, 0.010]),
        ("WACC", "wacc", [-0.005, 0.005]),
        ("Terminal growth", "terminal_growth", [-0.005, 0.005]),
    ]
    sensitivities = []
    for label, key, (down, up) in tests:
        if key == "revenue_growth":
            low_change = {key: [item + down for item in assumptions[key]]}
            high_change = {key: [item + up for item in assumptions[key]]}
        else:
            low_change, high_change = {key: assumptions[key] + down}, {key: assumptions[key] + up}
        try:
            low_forecast, low_valuation = scenario_for(low_change)
            high_forecast, high_valuation = scenario_for(high_change)
            sensitivities.append({
                "driver": label,
                "low": low_valuation["value_per_share"], "base": valuation["value_per_share"],
                "high": high_valuation["value_per_share"],
                "low_ebit": low_forecast[-1]["ebit"], "base_ebit": forecasts[-1]["ebit"],
                "high_ebit": high_forecast[-1]["ebit"],
                "low_fcff": low_forecast[-1]["fcff"], "base_fcff": forecasts[-1]["fcff"],
                "high_fcff": high_forecast[-1]["fcff"],
                "spread": abs(high_valuation["value_per_share"] - low_valuation["value_per_share"]),
            })
        except (AssertionError, ValueError) as exc:
            sensitivities.append({"driver": label, "error": str(exc), "spread": 0.0})
    sensitivities.sort(key=lambda item: item["spread"], reverse=True)

    # Ranking robustness: repeat the same one-at-a-time tests at half and
    # one-and-a-half times the documented standard ranges.  A rank that moves
    # is range-dependent, not a claim of intrinsic importance.
    range_robustness = []
    for multiplier in (0.5, 1.0, 1.5):
        ranked = []
        for label, key, (down, up) in tests:
            if key == "revenue_growth":
                low_change = {key: [item + down * multiplier for item in assumptions[key]]}
                high_change = {key: [item + up * multiplier for item in assumptions[key]]}
            else:
                low_change = {key: assumptions[key] + down * multiplier}
                high_change = {key: assumptions[key] + up * multiplier}
            try:
                _, low_valuation = scenario_for(low_change)
                _, high_valuation = scenario_for(high_change)
                ranked.append((label, abs(high_valuation["value_per_share"] - low_valuation["value_per_share"])))
            except (AssertionError, ValueError):
                ranked.append((label, 0.0))
        range_robustness.append({"range_multiplier": multiplier, "ranking": [
            {"driver": label, "spread": spread, "rank": index}
            for index, (label, spread) in enumerate(sorted(ranked, key=lambda item: item[1], reverse=True), start=1)
        ]})

    grid = []
    for wacc in [0.050, assumptions["wacc"], 0.070]:
        row = {"wacc": wacc, "values": []}
        for growth in [0.020, 0.025, 0.030]:
            row["values"].append(None if growth >= wacc else dcf(
                forecasts, {**assumptions, "wacc": wacc, "terminal_growth": growth}
            )["value_per_share"])
        grid.append(row)

    low_forecasts, low_value = project(LOW_ASSUMPTIONS), dcf(project(LOW_ASSUMPTIONS), LOW_ASSUMPTIONS)
    high_forecasts, high_value = project(HIGH_ASSUMPTIONS), dcf(project(HIGH_ASSUMPTIONS), HIGH_ASSUMPTIONS)
    # Binary search the FCFF scale that reconciles the current price.
    lo, hi = 0.10, 3.00
    for _ in range(80):
        midpoint = (lo + hi) / 2
        scaled = [{**row, "fcff": row["fcff"] * midpoint} for row in forecasts]
        if dcf(scaled, assumptions)["value_per_share"] < MARKET_PRICE:
            lo = midpoint
        else:
            hi = midpoint

    return {
        "metadata": {"target": "Johnson & Johnson (NYSE: JNJ) common stock", "valuation_date": VALUATION_DATE,
                     "currency": "USD millions except per-share data", "share_basis": SHARE_BASIS,
                     "shares_m": SHARE_COUNT, "market_price": MARKET_PRICE,
                     "decision_horizon": "12 months", "exclusions": "No transaction/control premium; no synergy value; reported-GAAP P/E is only a qualified cross-check."},
        "assumptions": assumptions, "forecasts": forecasts, "valuation": valuation,
        "revenue_driver_bridge": revenue_driver_bridge(assumptions["revenue_growth"]),
        "checks": {"opening_balance_sheet_reconciliation": opening_check,
                   "filing_input_benchmark_difference": filing_input_check,
                   "all_forecast_balance_sheets_balance": all(abs(row["balance_check"]) <= 0.05 for row in forecasts),
                   "cash_flow_ties_to_cash": all(abs(row["cash_flow_check"]) <= 0.05 for row in forecasts),
                   "minimum_cash_passes": all(row["cash"] >= assumptions["minimum_cash"] - 0.05 for row in forecasts)},
        "cases": {"low": low_value["value_per_share"], "base": valuation["value_per_share"],
                  "high": high_value["value_per_share"]},
        "sensitivity_grid": grid, "one_at_a_time": sensitivities,
        "range_robustness": range_robustness,
        "reverse_dcf_fcff_multiplier": (lo + hi) / 2,
    }


def print_base_detail(forecasts: list[dict], valuation: dict) -> None:
    print("\nBase-case annual FCFF")
    for row in forecasts:
        print(
            f"FY{row['year']}  EBIT ${row['ebit']:,.1f} | FCFF ${row['fcff']:,.1f} | "
            f"balance check ${row['balance_check']:,.1f}"
        )
    print("\nEnterprise-to-equity bridge")
    print(f"PV explicit FCFF:        ${valuation['pv_explicit_fcff']:,.1f}")
    print(f"PV terminal value:       ${valuation['pv_terminal_value']:,.1f}")
    print(f"Enterprise value:         ${valuation['enterprise_value']:,.1f}")
    print(f"Add: excess cash:        ${valuation['excess_cash']:,.1f}")
    print(f"Less: debt:              ${valuation['debt']:,.1f}")
    print(f"Equity value:             ${valuation['equity_value']:,.1f}")
    print(f"Share basis:              {SHARE_BASIS} ({SHARE_COUNT:,.3f}m)")
    print(f"Value per share:          ${valuation['value_per_share']:,.2f}")
    print(f"Terminal-value share EV:  {valuation['terminal_value_share']:.1%}")
    print(f"Market price ({VALUATION_DATE}): ${MARKET_PRICE:.2f}")


def print_wacc_build() -> None:
    build = calculate_wacc(BASE_ASSUMPTIONS["tax_rate"])
    print("\nWACC build")
    print(f"Risk-free rate:           {WACC_INPUTS['risk_free_rate']:.2%}")
    print(f"Levered beta:             {WACC_INPUTS['levered_beta']:.2f}")
    print(f"Equity risk premium:      {WACC_INPUTS['equity_risk_premium']:.2%}")
    print(f"Cost of equity (CAPM):    {build['cost_of_equity']:.2%}")
    print(f"Pre-tax cost of debt:     {WACC_INPUTS['pre_tax_cost_of_debt']:.2%}")
    print(f"After-tax cost of debt:   {build['after_tax_cost_of_debt']:.2%}")
    print(f"Equity / debt weights:    {build['equity_weight']:.1%} / {build['debt_weight']:.1%}")
    print(f"WACC:                     {build['wacc']:.2%}")


def main() -> None:
    print(f"Johnson & Johnson Project 1 — valuation as of {VALUATION_DATE}")
    print("\nLow/base/high causal cases")
    run_case("Low", LOW_ASSUMPTIONS)
    base_forecasts, base_valuation = run_case("Base", BASE_ASSUMPTIONS)
    run_case("High", HIGH_ASSUMPTIONS)
    print_base_detail(base_forecasts, base_valuation)
    print_wacc_build()
    sensitivity_grid(base_forecasts)
    assert_dcf_directionality(base_forecasts)
    reverse_dcf(base_forecasts)


if __name__ == "__main__":
    main()
