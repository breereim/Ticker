"""Five-year ABG pro forma and equity valuation (USD millions except per-share data)."""

YEARS = [2026, 2027, 2028, 2029, 2030]

# Opening FY2025 balance sheet
opening = {
    "revenue": 17999.0, "inventory": 2135.8, "ppe": 3070.4,
    "other_assets": 6371.6, "cash": 40.4, "floor_plan": 2027.0,
    "debt": 3572.0, "revolver": 0.0, "other_liabilities": 2127.5,
    "equity": 3891.7,
}

# Assumptions
growth = 0.018
gross_margin = 0.1705
sga_to_gross_profit = [0.665, 0.655, 0.645, 0.645, 0.645]
depreciation_to_opening_ppe = 82.4 / 3070.4
impairment = 120.0
capex = 250.0
tax_rate = 0.255
inventory_days = 2135.8 / (17999.0 - 3071.7) * 365
floor_plan_to_inventory = 2027.0 / 2135.8
other_working_capital_rate = 0.008
minimum_cash, revolver_limit, revolver_rate = 25.0, 850.0, 0.06
debt_repayment, share_buyback = 150.0, 150.0
floor_plan_rate, term_debt_rate = 0.0467, 0.0544
cost_of_equity, terminal_growth = 0.10, 0.025
shares_outstanding = 17.951349


def print_table(title, rows, results):
    print(f"\n{title}")
    print(f"{'USD millions':<30}" + "".join(f"FY{year}E{'':>8}" for year in YEARS))
    for label, key in rows:
        print(f"{label:<30}" + "".join(f"{result[key]:>13.1f}" for result in results))


def assert_balanced(results):
    for result in results:
        year = result["year"]
        gap = result["balance_check"]
        if abs(gap) > 0.05:
            raise AssertionError(f"FY{year}E does not balance: gap {gap:.1f}")
        if result["cash"] < minimum_cash - 0.05:
            raise AssertionError(f"FY{year}E cash below minimum: {result['cash']:.1f}")


def project():
    prior = opening.copy()
    results = []
    for index, year in enumerate(YEARS):
        revenue = prior["revenue"] * (1 + growth)
        gross_profit = revenue * gross_margin
        sga = gross_profit * sga_to_gross_profit[index]
        depreciation = prior["ppe"] * depreciation_to_opening_ppe
        operating_income = gross_profit - sga - depreciation - impairment
        interest = (prior["floor_plan"] * floor_plan_rate + prior["debt"] * term_debt_rate
                    + prior["revolver"] * revolver_rate)
        pretax_income = operating_income - interest
        tax = max(0.0, pretax_income) * tax_rate
        net_income = pretax_income - tax

        inventory = (revenue - gross_profit) * inventory_days / 365
        floor_plan = inventory * floor_plan_to_inventory
        ppe = prior["ppe"] + capex - depreciation
        change_revenue = revenue - prior["revenue"]
        other_working_capital = other_working_capital_rate * change_revenue
        other_assets = prior["other_assets"] + other_working_capital - impairment
        debt = prior["debt"] - debt_repayment
        other_liabilities = prior["other_liabilities"]
        equity = prior["equity"] + net_income - share_buyback

        fcfe = (net_income + depreciation + impairment - capex
                - (inventory - prior["inventory"]) - other_working_capital
                + (floor_plan - prior["floor_plan"]) - debt_repayment)
        cash_before_revolver = prior["cash"] + fcfe - share_buyback
        revolver = prior["revolver"]
        if cash_before_revolver < minimum_cash:
            draw = min(minimum_cash - cash_before_revolver, revolver_limit - revolver)
            revolver += draw
            cash = cash_before_revolver + draw
        else:
            repayment = min(cash_before_revolver - minimum_cash, revolver)
            revolver -= repayment
            cash = cash_before_revolver - repayment

        result = {
            "year": year, "revenue": revenue, "gross_profit": gross_profit, "sga": sga,
            "depreciation": depreciation, "impairment": impairment,
            "operating_income": operating_income, "interest": interest,
            "pretax_income": pretax_income, "tax": tax, "net_income": net_income,
            "inventory": inventory, "ppe": ppe, "other_assets": other_assets, "cash": cash,
            "floor_plan": floor_plan, "debt": debt, "revolver": revolver,
            "other_liabilities": other_liabilities, "equity": equity, "fcfe": fcfe,
            "capex": capex, "change_inventory": inventory - prior["inventory"],
            "change_other_working_capital": other_working_capital,
            "change_floor_plan": floor_plan - prior["floor_plan"],
            "debt_repayment": debt_repayment, "share_buyback": share_buyback,
        }
        result["balance_check"] = (inventory + ppe + other_assets + cash
                                   - floor_plan - debt - revolver - other_liabilities - equity)
        results.append(result)
        prior = {**result, "revenue": revenue}
    return results


def value_equity(results):
    pv_fcfe = sum(result["fcfe"] / (1 + cost_of_equity) ** (i + 1)
                  for i, result in enumerate(results))
    terminal_value = ((results[-1]["fcfe"] + debt_repayment) * (1 + terminal_growth)
                      / (cost_of_equity - terminal_growth))
    pv_terminal = terminal_value / (1 + cost_of_equity) ** 5
    equity_value = pv_fcfe + pv_terminal
    return equity_value, pv_terminal / equity_value, equity_value / shares_outstanding


if __name__ == "__main__":
    forecast = project()
    print_table("Income Statement", [("Revenue", "revenue"), ("Gross profit", "gross_profit"),
                ("SG&A", "sga"), ("Depreciation", "depreciation"), ("Impairment", "impairment"),
                ("Operating income", "operating_income"), ("Interest", "interest"),
                ("Pretax income", "pretax_income"), ("Tax", "tax"), ("Net income", "net_income")], forecast)
    print_table("Balance Sheet", [("Inventory", "inventory"), ("PP&E", "ppe"),
                ("Other assets", "other_assets"), ("Cash", "cash"), ("Floor plan", "floor_plan"),
                ("Term debt", "debt"), ("Revolver", "revolver"),
                ("Other liabilities", "other_liabilities"), ("Equity", "equity")], forecast)
    print_table("Cash Flow", [("Net income", "net_income"), ("Depreciation", "depreciation"),
                ("Impairment", "impairment"), ("Capital spending", "capex"),
                ("Change in inventory", "change_inventory"),
                ("Change in other working capital", "change_other_working_capital"),
                ("Change in floor plan", "change_floor_plan"),
                ("Debt repayment", "debt_repayment"), ("Free cash flow to equity", "fcfe"),
                ("Share buyback", "share_buyback")], forecast)
    print("\nChecks")
    for result in forecast:
        print(f"FY{result['year']}E  Assets - liabilities - equity: {result['balance_check']:.1f}"
              f"  Cash at or above minimum: {result['cash'] >= minimum_cash}")
    assert_balanced(forecast)
    equity_value, terminal_share, value_per_share = value_equity(forecast)
    print(f"\nEquity value: ${equity_value:,.2f} million")
    print(f"Share of value after 2030: {terminal_share:.1%}")
    print(f"Value per share: ${value_per_share:.2f}")
