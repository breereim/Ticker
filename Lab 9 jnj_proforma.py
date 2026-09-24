"""Johnson & Johnson five-year pro forma and FCFE valuation.

USD millions except per-share data.  Run: python jnj_drive_model.py
The balance-check assertion is deliberately live: do not remove it to make a
forecast appear to work.
"""

YEARS = [2026, 2027, 2028, 2029, 2030]

# FY2025 opening balance sheet (JNJ FY2025 Form 10-K, Consolidated Balance
# Sheets, p. 43).  Debt = loans and notes payable + long-term debt.
opening = {
    "cash": 19_709.0,
    "inventory": 14_191.0,
    "ppe": 23_169.0,
    "other_operating_assets": 142_141.0,
    "debt": 47_933.0,
    "other_liabilities": 69_733.0,
    "equity": 81_544.0,
    "revenue": 94_193.0,
}

# Assumptions: sourced history is in jnj_drive_submission.md; judgment items
# have reasons there.  JNJ has no floor-plan financing: the line is zero.
revenue_growth = [0.050, 0.040, 0.040, 0.035, 0.030]
gross_margin = 0.680
sga_to_gross_profit = 0.370
rd_to_revenue = 0.155
da_to_opening_ppe = 0.324  # total D&A / PP&E, 2025 historical relationship
ppe_depreciation_rate = 0.120  # portion of D&A charged against PP&E
inventory_days = 171.3
capex_to_revenue = 0.050
other_wc_to_incremental_revenue = 0.010
net_interest_rate = 0.020
tax_rate = 0.180
dividend_2026 = 12_750.0
dividend_growth = 0.030
minimum_cash = 10_000.0
cost_of_equity = 0.080
terminal_growth = 0.025
shares_outstanding = 2_407.939  # FY2025 issued less treasury shares


def rows(title, labels, forecasts):
    print(f"\n{title}")
    print(f"{'USD millions':<34}" + "".join(f"FY{y}E{'':>8}" for y in YEARS))
    for label, key in labels:
        print(f"{label:<34}" + "".join(f"{f[key]:>13,.1f}" for f in forecasts))


def project():
    prior = opening.copy()
    forecasts = []
    for i, year in enumerate(YEARS):
        revenue = prior["revenue"] * (1 + revenue_growth[i])
        gross_profit = revenue * gross_margin
        cogs = revenue - gross_profit
        sga = gross_profit * sga_to_gross_profit
        rd = revenue * rd_to_revenue

        # Total D&A is the historical D&A/PP&E relationship.  The PP&E and
        # intangible portions are separated so the balance-sheet roll-forward
        # and the cash-flow add-back describe the same economic expense.
        da = prior["ppe"] * da_to_opening_ppe
        ppe_depreciation = prior["ppe"] * ppe_depreciation_rate
        intangible_amortization = da - ppe_depreciation
        ebit = gross_profit - sga - rd - da
        interest = prior["debt"] * net_interest_rate
        pretax_income = ebit - interest
        tax = max(0.0, pretax_income) * tax_rate
        net_income = pretax_income - tax

        inventory = cogs * inventory_days / 365.0
        capex = revenue * capex_to_revenue
        ppe = prior["ppe"] + capex - ppe_depreciation
        other_wc_investment = other_wc_to_incremental_revenue * (revenue - prior["revenue"])
        other_operating_assets = (prior["other_operating_assets"] + other_wc_investment
                                  - intangible_amortization)
        debt = prior["debt"]  # no forecast debt repayment or draw
        other_liabilities = prior["other_liabilities"]
        dividend = dividend_2026 * (1 + dividend_growth) ** i
        equity = prior["equity"] + net_income - dividend

        # FCFE excludes the discretionary dividend: it is cash available to
        # shareholders before the payout decision.  There is no floor plan.
        change_inventory = inventory - prior["inventory"]
        fcfe = (net_income + da - capex - change_inventory
                - other_wc_investment)
        cash = prior["cash"] + fcfe - dividend
        floor_plan = 0.0
        revolver = 0.0
        balance_check = (inventory + ppe + other_operating_assets + cash
                         - debt - other_liabilities - equity)
        forecasts.append(locals().copy())
        prior = forecasts[-1]
    return forecasts


def assert_checks(forecasts):
    for f in forecasts:
        if abs(f["balance_check"]) > 0.05:
            raise AssertionError(f"FY{f['year']}E does not balance: {f['balance_check']:,.1f}")
        if f["cash"] < minimum_cash:
            raise AssertionError(f"FY{f['year']}E cash below floor: {f['cash']:,.1f}")


def value_equity(forecasts):
    pv_explicit = sum(f["fcfe"] / (1 + cost_of_equity) ** (i + 1)
                      for i, f in enumerate(forecasts))
    terminal_value = forecasts[-1]["fcfe"] * (1 + terminal_growth) / (cost_of_equity - terminal_growth)
    pv_terminal = terminal_value / (1 + cost_of_equity) ** len(forecasts)
    equity_value = pv_explicit + pv_terminal
    return equity_value, pv_terminal / equity_value, equity_value / shares_outstanding


if __name__ == "__main__":
    forecast = project()
    rows("Income Statement", [("Revenue", "revenue"), ("Gross profit", "gross_profit"),
         ("SG&A", "sga"), ("R&D", "rd"), ("D&A", "da"), ("EBIT", "ebit"),
         ("Net interest", "interest"), ("Pretax income", "pretax_income"),
         ("Tax", "tax"), ("Net income", "net_income")], forecast)
    rows("Balance Sheet", [("Inventory", "inventory"), ("PP&E", "ppe"),
         ("Other operating assets", "other_operating_assets"), ("Cash", "cash"),
         ("Floor plan (none)", "floor_plan"), ("Debt", "debt"),
         ("Other liabilities", "other_liabilities"), ("Shareholders' equity", "equity")], forecast)
    rows("Cash Flow / FCFE", [("Net income", "net_income"), ("D&A", "da"),
         ("Capital spending", "capex"), ("Change in inventory", "change_inventory"),
         ("Other working-capital investment", "other_wc_investment"),
         ("FCFE", "fcfe"), ("Dividend", "dividend")], forecast)
    print("\nChecks")
    for f in forecast:
        print(f"FY{f['year']}E  balance check: {f['balance_check']:,.1f}  "
              f"cash: {f['cash']:,.1f}  floor-plan/revolver draw: none")
    assert_checks(forecast)
    equity_value, terminal_share, value_per_share = value_equity(forecast)
    print(f"\nEquity value: ${equity_value:,.1f} million")
    print(f"Terminal-value share: {terminal_share:.1%}")
    print(f"Value per share: ${value_per_share:,.2f}")
