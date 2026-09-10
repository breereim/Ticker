"""A simple five-year FCFF discounted cash flow model (USD millions)."""

# Inputs — edit these values as needed.
STARTING_FCFF = 21325.1  # 24,530 operating cash flow + 1,977 interest paid × (1 - 17.7%) - 4,832 capex
GROWTH_RATES = [0.06, 0.05, 0.04, 0.03, 0.03]  # Years 1 through 5; forecast estimate
WACC = 0.0588  # Estimate: risk-free rate + beta × 5% equity premium, weighted with after-tax debt cost
TERMINAL_GROWTH = 0.03
NON_OPERATING_CASH = 19709.0  # USD millions
DEBT = 47933.0  # USD millions
DILUTED_SHARES = 2429.4  # Millions of shares

# Sensitivity-grid and reverse-DCF inputs.
SENSITIVITY_WACCS = [0.05, 0.0588, 0.07]
SENSITIVITY_TERMINAL_GROWTHS = [0.02, 0.03, 0.04]
TARGET_SHARE_PRICE = 267.08  # JNJ close, September 9, 2026, 4:00 PM EDT
REVERSE_DCF_LOWER_SHIFT = -0.05  # Percentage-point shift added to every growth rate
REVERSE_DCF_UPPER_SHIFT = 0.10


def calculate_valuation(wacc: float, terminal_growth: float, growth_rates: list[float]) -> dict[str, float | list[float]]:
    """Return all DCF outputs for the supplied assumptions (USD millions except per share)."""
    if terminal_growth >= wacc:
        raise ValueError("terminal growth must be less than WACC")

    fcff_by_year = []
    fcff = STARTING_FCFF
    for growth_rate in growth_rates:
        fcff *= 1.0 + growth_rate
        fcff_by_year.append(fcff)

    pv_explicit_fcff = sum(
        annual_fcff / (1.0 + wacc) ** year
        for year, annual_fcff in enumerate(fcff_by_year, start=1)
    )
    terminal_value_year_5 = (
        fcff_by_year[-1] * (1.0 + terminal_growth) / (wacc - terminal_growth)
    )
    pv_terminal_value = terminal_value_year_5 / (1.0 + wacc) ** 5
    enterprise_value = pv_explicit_fcff + pv_terminal_value
    equity_value = enterprise_value + NON_OPERATING_CASH - DEBT

    return {
        "fcff_by_year": fcff_by_year,
        "pv_explicit_fcff": pv_explicit_fcff,
        "terminal_value_year_5": terminal_value_year_5,
        "pv_terminal_value": pv_terminal_value,
        "enterprise_value": enterprise_value,
        "equity_value": equity_value,
        "value_per_diluted_share": equity_value / DILUTED_SHARES,
        "pv_terminal_as_share_of_ev": pv_terminal_value / enterprise_value,
    }


def value_per_share_with_shift(shift: float) -> float:
    """Value per share after adding one shift to each explicit growth rate."""
    shifted_growth_rates = [growth_rate + shift for growth_rate in GROWTH_RATES]
    return calculate_valuation(WACC, TERMINAL_GROWTH, shifted_growth_rates)[
        "value_per_diluted_share"
    ]


def solve_uniform_growth_shift() -> float | None:
    """Solve the reverse DCF by bisection, or return None when no valid bracket exists."""
    lower = REVERSE_DCF_LOWER_SHIFT
    upper = REVERSE_DCF_UPPER_SHIFT
    if lower >= upper:
        raise ValueError("reverse-DCF lower shift must be less than the upper shift")
    if any(growth_rate + lower <= -1.0 for growth_rate in GROWTH_RATES) or any(
        growth_rate + upper <= -1.0 for growth_rate in GROWTH_RATES
    ):
        raise ValueError("reverse-DCF bracket pushes an annual growth rate to -100% or below")

    lower_error = value_per_share_with_shift(lower) - TARGET_SHARE_PRICE
    upper_error = value_per_share_with_shift(upper) - TARGET_SHARE_PRICE
    if lower_error == 0:
        return lower
    if upper_error == 0:
        return upper
    if lower_error * upper_error > 0:
        return None

    for _ in range(100):
        midpoint = (lower + upper) / 2.0
        midpoint_error = value_per_share_with_shift(midpoint) - TARGET_SHARE_PRICE
        if abs(midpoint_error) < 1e-10:
            return midpoint
        if lower_error * midpoint_error < 0:
            upper = midpoint
            upper_error = midpoint_error
        else:
            lower = midpoint
            lower_error = midpoint_error
    return (lower + upper) / 2.0


def print_sensitivity_grid() -> None:
    print("\nSensitivity grid: value per diluted share")
    print("WACC \\ terminal growth", end="")
    for terminal_growth in SENSITIVITY_TERMINAL_GROWTHS:
        print(f" | {terminal_growth:.0%}", end="")
    print()
    for wacc in SENSITIVITY_WACCS:
        print(f"{wacc:.2%}", end="")
        for terminal_growth in SENSITIVITY_TERMINAL_GROWTHS:
            if terminal_growth >= wacc:
                cell = "invalid"
            else:
                cell = f"{calculate_valuation(wacc, terminal_growth, GROWTH_RATES)['value_per_diluted_share']:.2f}"
            print(f" | {cell}", end="")
        print()


def print_reverse_dcf() -> None:
    print("\nReverse DCF: uniform shift to all five explicit growth rates")
    try:
        solved_shift = solve_uniform_growth_shift()
    except ValueError as error:
        print(f"Reverse DCF: no solution — {error}.")
        return

    if solved_shift is None:
        print("Reverse DCF: no solution in the specified bracket.")
    else:
        print(f"Solved uniform growth shift: {solved_shift * 100:+.4f} percentage points")
    print(f"Target share price: {TARGET_SHARE_PRICE:.4f}")
    print(
        "Held fixed: "
        f"starting FCFF={STARTING_FCFF:.4f}; base growth rates={GROWTH_RATES}; "
        f"WACC={WACC:.2%}; terminal growth={TERMINAL_GROWTH:.2%}; "
        f"cash={NON_OPERATING_CASH:.4f}; debt={DEBT:.4f}; "
        f"diluted shares={DILUTED_SHARES:.4f}."
    )


def main() -> None:
    if TERMINAL_GROWTH >= WACC:
        raise SystemExit(
            "Error: terminal growth must be less than WACC for the Gordon-growth formula."
        )
    if len(GROWTH_RATES) != 5:
        raise SystemExit("Error: provide exactly five yearly growth rates.")
    if DILUTED_SHARES <= 0:
        raise SystemExit("Error: diluted shares must be greater than zero.")

    valuation = calculate_valuation(WACC, TERMINAL_GROWTH, GROWTH_RATES)
    fcff_by_year = valuation["fcff_by_year"]
    pv_explicit_fcff = valuation["pv_explicit_fcff"]
    terminal_value_year_5 = valuation["terminal_value_year_5"]
    pv_terminal_value = valuation["pv_terminal_value"]
    enterprise_value = valuation["enterprise_value"]
    equity_value = valuation["equity_value"]
    value_per_diluted_share = valuation["value_per_diluted_share"]
    pv_terminal_as_share_of_ev = valuation["pv_terminal_as_share_of_ev"]

    for year, annual_fcff in enumerate(fcff_by_year, start=1):
        print(f"FCFF Year {year}: {annual_fcff:.4f}")
    print(f"PV of explicit FCFF: {pv_explicit_fcff:.4f}")
    print(f"Terminal value at Year 5: {terminal_value_year_5:.4f}")
    print(f"PV of terminal value: {pv_terminal_value:.4f}")
    print(f"Enterprise value: {enterprise_value:.4f}")
    print(f"Equity value: {equity_value:.4f}")
    print(f"Value per diluted share: {value_per_diluted_share:.4f}")
    print(f"PV of terminal value as share of enterprise value: {pv_terminal_as_share_of_ev:.4f}")
    print_sensitivity_grid()
    print_reverse_dcf()


if __name__ == "__main__":
    main()
