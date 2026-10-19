"""Write a readable, static final-model handoff report without web dependencies."""
from pathlib import Path
from statistics import median

from jnj_project1_fcff import evaluate_model
from jnj_peer_multiples import COMPANIES, metrics
from jnj_pe_valuation import PEERS, TARGET, pe_multiple


def money(value):
    return f"${value:,.1f}"


def price(value):
    return f"${value:,.2f}"


def table(headers, rows):
    alignment = "|" + "|".join("---:" if index else "---" for index, _ in enumerate(headers)) + "|"
    return ["| " + " | ".join(headers) + " |", alignment, *[
        "| " + " | ".join(str(value) for value in row) + " |" for row in rows
    ]]


def statement_rows(rows, fields):
    def value(row, field):
        if field == "total_assets":
            return row["cash"] + row["inventory"] + row["ppe"] + row["other_operating_assets"]
        if field == "total_liabilities_and_equity":
            return row["debt"] + row["other_liabilities"] + row["equity"]
        return row[field]
    return [[label, *[money(value(row, field)) for row in rows]] for label, field in fields]


def peer_sections():
    peer_rows, values = [], {}
    for company in COMPANIES:
        market_cap, enterprise_value, ev_ebit, pe = metrics(company)
        values[company["ticker"]] = (market_cap, enterprise_value, ev_ebit, pe)
        peer_rows.append([
            company["ticker"], price(company["price"]), f"{company['shares']:,.1f}",
            money(market_cap), money(company["cash"]), money(company["debt"]),
            money(company["ebit"]), money(enterprise_value), f"{ev_ebit:.2f}x",
            f"{company['eps']:.2f}", f"{pe:.2f}x",
        ])
    peer_ev_ebit = median([values["ABT"][2], values["MRK"][2]])
    target = COMPANIES[0]
    implied_ev = peer_ev_ebit * target["ebit"]
    implied_equity = implied_ev - target["debt"] + target["cash"]
    pe_values = [pe_multiple(peer) for peer in PEERS]
    pe_min, pe_median, pe_max = min(pe_values), median(pe_values), max(pe_values)
    return [
        "", "## Comparable-company calculations", "",
        "FY2025 financial metrics and September 10, 2026 prices. Market capitalization uses diluted weighted-average shares as a disclosed proxy, not same-date shares outstanding.", "",
        *table(["Ticker", "Price", "Diluted-share proxy (m)", "Market cap", "Cash", "Debt", "FY25 EBIT", "EV", "EV/EBIT", "FY25 EPS", "P/E"], peer_rows), "",
        f"Peer-median EV/EBIT (ABT and MRK): **{peer_ev_ebit:.2f}x**. Applied to JNJ FY2025 EBIT of {money(target['ebit'])}, implied EV is {money(implied_ev)}, implied equity value is {money(implied_equity)}, and implied value is **{price(implied_equity / target['shares'])} per share**.", "",
        *table(["P/E reference", "Peer multiple", "JNJ FY25 reported EPS", "Implied JNJ value/share"], [
            ["Minimum", f"{pe_min:.2f}x", f"{TARGET['diluted_eps']:.2f}", price(pe_min * TARGET["diluted_eps"])],
            ["Median", f"{pe_median:.2f}x", f"{TARGET['diluted_eps']:.2f}", price(pe_median * TARGET["diluted_eps"])],
            ["Maximum", f"{pe_max:.2f}x", f"{TARGET['diluted_eps']:.2f}", price(pe_max * TARGET["diluted_eps"])],
        ]), "",
        "These are cross-checks, not values to average with the DCF. EV/EBIT remains sensitive to peer mix and EBIT definitions; reported-GAAP P/E has a talc-reserve comparability limitation.",
    ]


def main():
    model = evaluate_model()
    rows, valuation = model["forecasts"], model["valuation"]
    years = [f"FY{row['year']}E" for row in rows]
    lines = [
        "# JNJ final FCFF model static handoff report", "",
        "Generated from `jnj_project1_fcff.py`; USD millions except per-share values.", "",
        "## Committee action", "",
        "**Current action: watch/defer, not initiate.** The base DCF is an estimate, not an initiation signal: terminal value is 87.6% of enterprise value, the low case is below market, and the peer cross-checks are near to below market.", "",
        "Change to **initiate** only after a refreshed valuation retains a margin of safety and two consecutive quarters validate the revenue bridge, normalized FCFF, and bounded litigation/cash needs. Change to **do not initiate** if replacement medicines and MedTech miss the bridge for two consecutive quarters, STELARA erosion is at or worse than the bridge, recurring legal/restructuring cash costs emerge, and WACC reaches 7% or more.", "",
        "## Valuation", "",
        f"- Low / base / high: {price(model['cases']['low'])} / {price(model['cases']['base'])} / {price(model['cases']['high'])} per diluted share.",
        f"- Market reference: {price(model['metadata']['market_price'])}; terminal-value share: {valuation['terminal_value_share']:.1%}.",
        f"- Enterprise value: {money(valuation['enterprise_value'])}; equity value: {money(valuation['equity_value'])}.", "",
        "## Five-year income statements", "",
        *table(["USD millions", *years], statement_rows(rows, [
            ("Revenue", "revenue"), ("Cost of goods sold", "cogs"), ("Gross profit", "gross_profit"), ("SG&A", "sga"),
            ("R&D", "rd"), ("IPR&D impairment", "iprd_impairment"), ("Restructuring", "restructuring"),
            ("EBIT", "ebit"), ("Interest", "interest"), ("Pretax income", "pretax_income"), ("Tax", "tax"), ("Net income", "net_income"),
        ])), "",
        "## Five-year balance sheets", "",
        *table(["USD millions", *years], statement_rows(rows, [
            ("Cash", "cash"), ("Inventory", "inventory"), ("PP&E", "ppe"), ("Other operating assets", "other_operating_assets"),
            ("Total assets", "total_assets"), ("Debt", "debt"), ("Other liabilities", "other_liabilities"),
            ("Equity", "equity"), ("Total liabilities and equity", "total_liabilities_and_equity"), ("Balance check", "balance_check"),
        ])), "",
        "## Five-year cash-flow statements", "",
        *table(["USD millions", *years], statement_rows(rows, [
            ("Net income", "net_income"), ("D&A add-back", "da"), ("Less change in inventory", "change_inventory"),
            ("Less other working-capital investment", "other_wc_investment"), ("Less capex", "capex"), ("FCFF", "fcff"),
            ("Less dividends", "dividend"), ("FCFE / cash movement", "fcfe"), ("Net change in cash", "net_change_in_cash"), ("Cash-flow check", "cash_flow_check"),
        ])), "",
        "## Revenue-driver bridge", "",
        "All FY2026-30 entries are forecast judgments. The FY2026 STELARA drag is calibrated to a filing-sourced FY2025 observation; it is not filing-sourced FY2026 guidance. Base portfolio is a residual that balances to the selected growth path and does not independently substantiate it.", "",
        *table(["Year", "STELARA erosion", "Replacement medicines", "MedTech", "Base portfolio residual", "Total growth"], [
            [f"FY{row['year']}E", *(f"{row[key]:.1%}" for key in ("stelara_erosion", "replacement_medicines", "medtech", "base_portfolio", "total_growth"))]
            for row in model["revenue_driver_bridge"]
        ]), "",
        "## Enterprise-to-equity bridge", "",
        *table(["Item", "Amount"], [[label, money(valuation[key])] for label, key in [
            ("PV explicit FCFF", "pv_explicit_fcff"), ("PV terminal value", "pv_terminal_value"), ("Enterprise value", "enterprise_value"),
            ("Excess cash", "excess_cash"), ("Debt", "debt"), ("Equity value", "equity_value"),
        ]]), "",
        "## WACC and terminal-growth sensitivity", "",
        *table(["WACC / terminal growth", "2.0%", "2.5%", "3.0%"], [
            [f"{row['wacc']:.2%}", *("n.a." if value is None else price(value) for value in row["values"])]
            for row in model["sensitivity_grid"]
        ]), "",
        "## Checks", "", *[f"- {key}: {value}" for key, value in model["checks"].items()], "",
        "## One-at-a-time sensitivity", "",
        *table(["Driver", "FY30 EBIT low/base/high", "FY30 FCFF low/base/high", "Value/share low/base/high", "Value spread/share"], [
            [row["driver"], " / ".join(money(row[key]) for key in ("low_ebit", "base_ebit", "high_ebit")),
             " / ".join(money(row[key]) for key in ("low_fcff", "base_fcff", "high_fcff")),
             " / ".join(price(row[key]) for key in ("low", "base", "high")), price(row["spread"])]
            for row in model["one_at_a_time"]
        ]), "",
        "## Reverse DCF", "", f"Market price implies {model['reverse_dcf_fcff_multiplier']:.2f}x each projected FCFF, holding WACC, terminal growth, bridge, and shares fixed.",
    ]
    lines += peer_sections()
    lines += ["", "## Evidence and limitations", "", "See `docs/accounting-basis-and-normalization.md`, `docs/revenue-driver-bridge.md`, `docs/peer-policy-and-multiples.md`, and `docs/validation-status.md` for source evidence and limitations."]
    (Path(__file__).resolve().parent / "docs" / "final-model-report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
