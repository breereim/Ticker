"""Run with: python -m streamlit run app.py"""

import streamlit as st

from engine import ASSETS, run_case, stress_table


DEFAULT_INPUTS = {
    "window": "All 60 monthly returns",
    "equity_delta_pp": 0.0,
    "fee_bps": 10,
    "trade_bps": 10,
    "reserve_min_pct": 3,
    "turnover_limit_pct": 25,
}


def reset_inputs():
    for key, value in DEFAULT_INPUTS.items():
        st.session_state[key] = value

st.set_page_config(page_title="Meridian | Investment committee", layout="wide")
st.markdown(
    """<style>
    :root {
        --meridian-forest: #173C34;
        --meridian-cream: #F7F5EF;
        --meridian-gold: #B99B5F;
        --meridian-charcoal: #25302D;
        --meridian-line: #D7D4C9;
    }

    .stApp { background: var(--meridian-cream); }
    header[data-testid="stHeader"] { background: var(--meridian-cream); }
    section.main > div.block-container {
        max-width: 1500px;
        padding-top: 2.2rem;
        padding-bottom: 4rem;
    }

    section.main h1, section.main h2, section.main h3,
    section.main h4, section.main h5 {
        color: var(--meridian-forest);
        font-family: Georgia, 'Times New Roman', serif;
        font-weight: 600;
        letter-spacing: -0.025em;
    }
    section.main h1 {
        font-size: clamp(2.2rem, 3.2vw, 3.6rem);
        line-height: 1.12;
        padding-bottom: 0.45rem;
        border-bottom: 3px solid var(--meridian-gold);
        margin-bottom: 0.5rem;
    }
    section.main h2 {
        margin-top: 1.8rem;
        border-left: 4px solid var(--meridian-gold);
        padding-left: 0.8rem;
    }
    section.main p, section.main li { line-height: 1.65; }
    section.main a { color: var(--meridian-forest); text-decoration-thickness: 1px; }
    section.main a:hover { color: #0D2A23; text-decoration-thickness: 2px; }

    [data-testid="stSidebar"] {
        border-right: 3px solid var(--meridian-gold);
    }
    [data-testid="stSidebar"] > div:first-child { padding-top: 1.3rem; }
    [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: var(--meridian-cream);
        font-family: Georgia, 'Times New Roman', serif;
        border-bottom: 1px solid var(--meridian-gold);
        padding-bottom: 0.7rem;
    }
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
        color: var(--meridian-cream);
    }
    [data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
        opacity: 0.88;
        line-height: 1.55;
    }
    [data-testid="stSidebar"] [data-baseweb="select"] > div {
        background: #254C42;
        border: 1px solid #78958A;
        color: var(--meridian-cream);
        border-radius: 8px;
    }
    [data-testid="stSidebar"] button[kind="secondary"] {
        background: var(--meridian-gold);
        border: 1px solid var(--meridian-gold);
        border-radius: 8px;
        color: #172F28;
        font-weight: 700;
        letter-spacing: 0.015em;
        min-height: 2.8rem;
    }
    [data-testid="stSidebar"] button[kind="secondary"]:hover {
        background: #D1B677;
        border-color: #D1B677;
        color: #172F28;
    }

    div[data-testid="stAlert"] {
        border: 1px solid var(--meridian-line);
        border-left: 5px solid var(--meridian-gold);
        border-radius: 10px;
        box-shadow: 0 5px 20px rgba(23, 60, 52, 0.055);
    }
    div[data-testid="stAlert"] p { line-height: 1.55; }
    div[data-testid="stAlert"] strong { color: var(--meridian-forest); }

    [data-baseweb="tab-list"] {
        gap: 0.35rem;
        border-bottom: 1px solid var(--meridian-line);
        padding-bottom: 0.45rem;
    }
    [data-baseweb="tab"] {
        background: #ECE9DF;
        border: 1px solid var(--meridian-line);
        border-radius: 8px 8px 0 0;
        color: var(--meridian-charcoal);
        font-weight: 600;
        padding: 0.7rem 1rem;
    }
    [data-baseweb="tab"]:hover { background: #E3DED1; color: var(--meridian-forest); }
    [data-baseweb="tab"][aria-selected="true"] {
        background: var(--meridian-forest);
        border-color: var(--meridian-forest);
        color: var(--meridian-cream);
    }
    [data-baseweb="tab-highlight"] { background: var(--meridian-gold); }

    div[data-testid="stMetric"] {
        background: #FFFFFF;
        border: 1px solid var(--meridian-line);
        border-top: 3px solid var(--meridian-gold);
        border-radius: 10px;
        padding: 1rem 1.2rem;
        min-height: 112px;
        box-shadow: 0 5px 18px rgba(23, 60, 52, 0.05);
    }
    div[data-testid="stMetricLabel"] {
        color: #40564E;
        font-size: 0.85rem;
        font-weight: 700;
        letter-spacing: 0.045em;
        text-transform: uppercase;
    }
    div[data-testid="stMetricValue"] {
        color: var(--meridian-forest);
        font-family: Georgia, 'Times New Roman', serif;
        font-weight: 600;
    }

    div[data-testid="stDataFrame"], div[data-testid="stTable"],
    div[data-testid="stVegaLiteChart"] {
        background: #FFFFFF;
        border: 1px solid var(--meridian-line);
        border-radius: 10px;
        box-shadow: 0 5px 18px rgba(23, 60, 52, 0.045);
        overflow: hidden;
    }
    div[data-testid="stVegaLiteChart"] { padding: 0.7rem; }
    div[data-testid="stTable"] table { border-collapse: collapse; }
    div[data-testid="stTable"] th {
        background: #E9E5D9;
        color: var(--meridian-forest);
        font-weight: 700;
    }
    div[data-testid="stTable"] tr:nth-child(even) { background: #F5F3ED; }
    div[data-testid="stExpander"] {
        background: #FFFFFF;
        border: 1px solid var(--meridian-line);
        border-radius: 10px;
    }

    :is(button, [role="tab"], a, input):focus-visible {
        outline: 3px solid var(--meridian-gold) !important;
        outline-offset: 2px;
    }
    @media (max-width: 900px) {
        section.main > div.block-container { padding: 1.2rem 1rem 3rem; }
        [data-baseweb="tab"] { padding: 0.55rem 0.7rem; font-size: 0.88rem; }
    }
    </style>""",
    unsafe_allow_html=True,
)
for input_key, default_value in DEFAULT_INPUTS.items():
    if input_key not in st.session_state:
        st.session_state[input_key] = default_value
st.title("Meridian Foundation Reserve")
st.caption("Committee decision workspace | $100m reserve | educational analysis, not investment advice")
st.error("Recommendation: REJECT live allocation (0%). The model is a reviewable pilot, but issuer look-through, actual holdings, and the CIO loss rule are unresolved.")

with st.sidebar:
    st.header("Test the process")
    window = st.selectbox("Estimation window", ["All 60 monthly returns", "Last 36 monthly returns"], key="window")
    equity_delta = st.slider("SPY return estimate change (percentage points)", -5.0, 5.0, step=0.5, key="equity_delta_pp") / 100
    fee = st.slider("Annual fund fee (basis points)", 0, 100, step=5, key="fee_bps")
    trade = st.slider("Cost per one-way traded dollar (basis points)", 0, 100, step=5, key="trade_bps")
    reserve_min = st.slider("Minimum reserve (%)", 3, 30, step=1, key="reserve_min_pct") / 100
    turnover_limit = st.slider("Maximum annual turnover (%)", 5, 50, step=5, key="turnover_limit_pct") / 100
    st.button("Reset inputs", on_click=reset_inputs, width="stretch")
    st.caption("Actual starting holdings were not provided. Turnover uses the 60% SPY / 40% LQD benchmark as an explicit proxy.")

case = run_case(last_36=window.startswith("Last"), equity_delta=equity_delta,
                fee_bps=fee, trade_bps=trade, reserve_min=reserve_min,
                turnover_limit=turnover_limit)

if case["portfolio"] is None:
    st.warning("**Current input verdict: NO MODELED FEASIBLE PORTFOLIO.** No 5% grid mix passes the net return screen and checkable limits under these inputs. Live allocation remains 0%.")
else:
    selected = case["portfolio"]
    st.info(f"**Current input verdict: MODELED FEASIBLE.** The selected mix has {selected['net']:.2%} estimated first-year net return, {selected['volatility']:.2%} historical volatility, and {selected['turnover']:.0%} proxy turnover. Issuer exposure, actual turnover, and the CIO loss rule remain unverified; live allocation remains 0%.")

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


tab1, tab2, tab3, tab4, tab5 = st.tabs(["Compare portfolios", "Stress and stop rule", "Monitoring triggers", "Point-in-time signal", "Evidence and method"])
with tab1:
    st.write("These are separate verdicts. A modeled PASS does not clear the unresolved policy items.")
    comparison = [
        ("Equal weight", case["equal"]),
        ("Inverse volatility", case["inverse_vol"]),
        ("Constrained portfolio", case["portfolio"]),
    ]
    available = [(name, row) for name, row in comparison if row is not None]
    metric_data = [
        {"Portfolio": name, "Net estimate": 100 * row["net"], "Volatility": 100 * row["volatility"]}
        for name, row in available
    ]
    allocation_data = [
        {"Portfolio": name, **{asset: 100 * weight for asset, weight in zip(ASSETS, row["weights"])}}
        for name, row in available
    ]
    chart_left, chart_right = st.columns(2)
    with chart_left:
        st.markdown("#### Net estimate and volatility")
        st.bar_chart(metric_data, x="Portfolio", y=["Net estimate", "Volatility"], stack=False)
        st.caption("Annualized percent; net estimate is a first-year planning estimate, not a forecast.")
    with chart_right:
        st.markdown("#### Portfolio allocation")
        st.bar_chart(allocation_data, x="Portfolio", y=list(ASSETS), stack=True)
        st.caption("Percent of capital; each portfolio's sleeves total 100%.")
    if case["portfolio"] is None:
        st.caption("The constrained portfolio is omitted from both charts because the current inputs produce no feasible mix.")
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
    st.write("Use these thresholds at each input refresh and annual rebalance. A triggered review does not authorize a trade; the committee must approve any change to the 0% live allocation decision.")
    st.dataframe([
        {"Measure": "Modeled feasibility", "Reconsider when": "No 5% grid mix clears the 6.5% net screen and checkable limits", "Action": "Stop the process; review assumptions and constraints with the committee."},
        {"Measure": "Return estimate", "Reconsider when": "Selected mix falls below 6.5% first-year net after fees and trade cost", "Action": "Reject the modeled mix; do not relax a hard rule to restore feasibility."},
        {"Measure": "Turnover and reserve", "Reconsider when": "Actual turnover exceeds 25% without approval, or reserve falls below 3%", "Action": "Pause rebalancing; obtain current holdings and a compliant proposal."},
        {"Measure": "Liquidity and issuer exposure", "Reconsider when": "Less than 90% is redeemable within five business days, or any nonexempt issuer exceeds 8%", "Action": "Stop live allocation until fund evidence supports both checks."},
        {"Measure": "Portfolio stability", "Reconsider when": "Any sleeve weight moves by at least 10 percentage points on a routine input refresh", "Action": "Return the allocation to committee review before implementation."},
        {"Measure": "Missing decision evidence", "Reconsider when": "CIO loss rule, actual holdings, or ETF issuer look-through is still undocumented", "Action": "Maintain 0% live allocation; request the missing evidence."},
        {"Measure": "Point-in-time signal", "Reconsider when": "A decision-date BAA vintage or publication check is unavailable", "Action": "Keep BAA out of portfolio weights; verify the vintage before using it."},
    ], hide_index=True, width="stretch")
    st.caption("The 10 percentage-point sleeve threshold is a committee review trigger from the decision memo. The other percentages reflect the mandate or the app's stated planning screen.")

with tab4:
    st.markdown("### BAA yield: point-in-time credit diagnostic")
    st.write("At the **2026-09-30** decision cutoff, the ALFRED vintage's latest nonmissing BAA observation was **August 2026: 6.32%**. The September observation **6.47%** was posted on **2026-10-01**, so it cannot be used for a September 30 decision. This is a monitored credit-yield level, not a spread or a return forecast. It does not change portfolio weights in this version.")
    st.info("Signal status: quarantined from optimization until every decision date has a stored ALFRED vintage and release check. Current snapshot data cannot reconstruct every historical vintage.")
    st.markdown("**Data card:** Moody's Seasoned Baa Corporate Bond Yield, monthly percent per annum, not seasonally adjusted, long-maturity corporate bonds; distributed by FRED/ALFRED. Observation month differs from publication date. Historical values may revise. Lab 17 checked the 2026-09-30 vintage on 2026-10-29 and found zero differences on common dates in that particular comparison. [FRED series](https://fred.stlouisfed.org/series/BAA) · [ALFRED vintages](https://alfred.stlouisfed.org/series?seid=BAA).")

with tab5:
    st.markdown("### Why these design choices")
    st.dataframe([
        {"Choice": "BIL and IEF", "Reason": "Treasury bill and Treasury bond sleeves provide reserve-eligible assets and different interest-rate exposures.", "Limit": "Their market values can still move; reserve eligibility is a modeling rule."},
        {"Choice": "LQD and SPY", "Reason": "Investment-grade corporate bonds and equities represent the mandate's bond and growth exposures using liquid, familiar ETFs.", "Limit": "SPY is U.S., not global; ETF holdings require issuer look-through."},
        {"Choice": "Inverse-volatility baseline", "Reason": "A transparent comparison that gives less weight to assets with higher historical volatility, without optimizing expected return.", "Limit": "It ignores correlations, mandate feasibility, and return requirements when weights are set."},
        {"Choice": "2.5% CPI assumption", "Reason": "Carry forward Lab 15's explicit CPI estimate so its CPI + 4% mandate screen remains comparable: 2.5% + 4% = 6.5% nominal.", "Limit": "It is not an observed or forecast CPI series; update it before a live decision."},
        {"Choice": "Minimum volatility objective", "Reason": "Among mixes that pass the return screen and coded limits, select the one with the lowest estimated historical volatility.", "Limit": "Volatility is provisional and does not replace the CIO's undefined annual-loss rule."},
    ], hide_index=True, width="stretch")
    st.write("The bundled `prices.csv` has 61 consecutive month-end adjusted closes, July 2021–July 2026, from a pinned secondary snapshot downloaded 2026-10-22. Simple monthly returns are averaged ×12; sample standard deviations are annualized ×√12; pairwise correlations form the covariance matrix. The 5% grid searches long-only weights, screens net return and modeled limits, then picks the lowest estimated volatility. Historical sample means can be unstable and are not forecasts.")
    st.write("The source is [this pinned adjusted-close file](https://github.com/manisahni/marketdata/blob/65a079329e379e104495f459e12e76a8f995585a/daily_adjclose_wide.csv). Fund roles and provenance are detailed in the README. The fixed source snapshot was obtained after some observations, so this app is a current allocation screen, not a point-in-time backtest.")
    st.write("**Implementation risks:** SPY does not match a global equity benchmark; ETF issuer look-through and redemption terms need primary-source checks; actual Meridian positions were not supplied; the 6.5% screen assumes CPI; the CIO has not defined the annual loss test; only a 5% grid is searched.")

st.caption("AI assisted code and drafting; the analysis and decision are mine. Educational use only, not investment advice.")
