"""Run with: python -m streamlit run app.py"""

import streamlit as st

from engine import ASSETS, CURRENT, run_case, stress_table

st.set_page_config(page_title="Meridian | Investment committee", layout="wide")
st.title("Meridian Foundation Reserve")
st.caption("Committee decision workspace | $100m reserve | educational analysis, not investment advice")
st.error("Recommendation: REJECT live allocation (0%). The model is a reviewable pilot, but issuer look-through, actual holdings, and the CIO loss rule are unresolved.")

with st.sidebar:
    st.header("Test the process")
    window = st.selectbox("Estimation window", ["All 60 monthly returns", "Last 36 monthly returns"])
    equity_delta = st.slider("SPY return estimate change (percentage points)", -5.0, 5.0, 0.0, 0.5) / 100
    fee = st.slider("Annual fund fee (basis points)", 0, 100, 10, 5)
    trade = st.slider("Cost per one-way traded dollar (basis points)", 0, 100, 10, 5)
    reserve_min = st.slider("Minimum reserve (%)", 3, 30, 3, 1) / 100
    turnover_limit = st.slider("Maximum annual turnover (%)", 5, 50, 25, 5) / 100
    st.caption("Actual starting holdings were not provided. Turnover uses the 60% SPY / 40% LQD benchmark as an explicit proxy.")

case = run_case(last_36=window.startswith("Last"), equity_delta=equity_delta,
                fee_bps=fee, trade_bps=trade, reserve_min=reserve_min,
                turnover_limit=turnover_limit)

st.subheader("Mandate")
st.write("**Objective:** CPI + 4% annually, net of costs, over rolling five years. The app uses 2.5% assumed CPI + 4% = **6.5% nominal** as a screening estimate, not a realized five-year test. **Benchmark:** 60% global equity / 40% U.S. investment-grade bonds. SPY is a U.S. equity proxy, so benchmark alignment is incomplete. **Risk measure:** annualized historical volatility; the CIO has not defined the requested calendar-year loss condition. **Hard limits:** long only; 3% payout reserve; 90% redeemable in five business days; issuer at most 8% unless exempt; annual turnover at most 25% without approval.")
st.caption("Universe: BIL Treasury bill ETF, IEF Treasury ETF, LQD investment-grade corporate bond ETF, SPY U.S. equity ETF. All four ETFs are assumed five-day liquid for the screen; this needs execution confirmation. No leverage, shorts, or derivatives are modeled.")


def pct(x):
    return f"{100*x:.2f}%"


def display_row(name, row):
    st.markdown(f"#### {name}")
    if row is None:
        st.warning("No mix on the 5% grid meets the net return screen and modeled hard limits.")
        return
    cols = st.columns(4)
    for col, label, value in zip(cols, ("Net estimate", "Volatility", "Reserve", "Turnover"),
                                  (row["net"], row["volatility"], row["reserve"], row["turnover"])):
        col.metric(label, pct(value))
    st.table({"Fund": ASSETS, "Weight": [pct(x) for x in row["weights"]]})
    st.write("**Modeled mandate verdict:** " + ("PASS" if not row["failures"] else "FAIL — " + "; ".join(row["failures"])))
    st.write("**6.5% net estimate screen:** " + ("PASS" if row["objective"] else "FAIL"))
    st.caption("Unverified for every option: " + "; ".join(row["unknowns"]))


tab1, tab2, tab3, tab4 = st.tabs(["Compare portfolios", "Stress and stop rule", "Point-in-time signal", "Evidence and method"])
with tab1:
    st.write("These are separate verdicts. A modeled PASS does not clear the unresolved policy items.")
    display_row("Equal weight baseline", case["equal"])
    display_row("Inverse-volatility baseline", case["inverse_vol"])
    display_row("Constrained lowest-volatility portfolio", case["portfolio"])
    with st.expander("Mandate benchmark (context)"):
        display_row("60/40 proxy", case["benchmark"])

with tab2:
    st.write("Each row reruns the same 5% grid search with a single changed input. Costs reduce the first-year net estimate. A blank portfolio means no feasible mix.")
    rows = []
    for item in stress_table():
        rows.append({"Scenario": item["scenario"],
                     "Feasible": "yes" if item["feasible"] else "no",
                     "BIL / IEF / LQD / SPY": " / ".join(f"{x:.0%}" for x in item["weights"]) if item["weights"] else "—",
                     "Net estimate": pct(item["net"]) if item["net"] is not None else "—",
                     "Volatility": pct(item["volatility"]) if item["volatility"] is not None else "—"})
    st.dataframe(rows, hide_index=True, width="stretch")
    st.error("**Stop condition:** Do not allocate if the search is infeasible, any checkable mandate rule fails, or issuer look-through, actual turnover, and the CIO loss rule are unverified. Reopen only with committee-approved definitions and current holdings; rerun all stress cases.")

with tab3:
    st.markdown("### BAA yield: point-in-time credit diagnostic")
    st.write("At the **2026-09-30** decision cutoff, the ALFRED vintage's latest nonmissing BAA observation was **August 2026: 6.32%**. The September observation **6.47%** was posted on **2026-10-01**, so it cannot be used for a September 30 decision. This is a monitored credit-yield level, not a spread or a return forecast. It does not change portfolio weights in this version.")
    st.info("Signal status: quarantined from optimization until every decision date has a stored ALFRED vintage and release check. Current snapshot data cannot reconstruct every historical vintage.")
    st.markdown("**Data card:** Moody's Seasoned Baa Corporate Bond Yield, monthly percent per annum, not seasonally adjusted, long-maturity corporate bonds; distributed by FRED/ALFRED. Observation month differs from publication date. Historical values may revise. Lab 17 checked the 2026-09-30 vintage on 2026-10-29 and found zero differences on common dates in that particular comparison. [FRED series](https://fred.stlouisfed.org/series/BAA) · [ALFRED vintages](https://alfred.stlouisfed.org/series?seid=BAA).")

with tab4:
    st.write("The bundled `prices.csv` has 61 consecutive month-end adjusted closes, July 2021–July 2026, from a pinned secondary snapshot downloaded 2026-10-22. Simple monthly returns are averaged ×12; sample standard deviations are annualized ×√12; pairwise correlations form the covariance matrix. The 5% grid searches long-only weights, screens net return and modeled limits, then picks the lowest estimated volatility. Historical sample means can be unstable and are not forecasts.")
    st.write("The source is [this pinned adjusted-close file](https://github.com/manisahni/marketdata/blob/65a079329e379e104495f459e12e76a8f995585a/daily_adjclose_wide.csv). Fund roles and provenance are detailed in the README. The fixed source snapshot was obtained after some observations, so this app is a current allocation screen, not a point-in-time backtest.")
    st.write("**Implementation risks:** SPY does not match a global equity benchmark; ETF issuer look-through and redemption terms need primary-source checks; actual Meridian positions were not supplied; the 6.5% screen assumes CPI; the CIO has not defined the annual loss test; only a 5% grid is searched.")

st.caption("AI assisted code and drafting; the analysis and decision are mine. Educational use only, not investment advice.")
