r"""Lab 15 portfolio stability app. Run: .\.venv\Scripts\python.exe -m streamlit run app.py"""

import hashlib
import streamlit as st

from portfolio import (
    CORRELATIONS, EXPECTED_RETURNS, OBJECTIVE_RETURN, RESERVE_ELIGIBLE,
    SLEEVES, VOLATILITIES, estimate_from_prices, lowest_risk_mix,
)


st.set_page_config(page_title="Portfolio Stability Decision", layout="wide")
st.title("Portfolio Stability Decision")
st.caption("Built with AI help, a learning demonstration, not investment advice.")

with st.sidebar:
    st.header("Mandate and data")
    objective = st.number_input("Objective return (%)", value=OBJECTIVE_RETURN * 100,
                                step=0.1, format="%.2f") / 100
    reserve_minimum = st.number_input("Reserve minimum (%)", min_value=0.0,
                                      max_value=100.0, value=3.0,
                                      step=1.0, format="%.2f") / 100
    upload = st.file_uploader("Upload prices.csv", type="csv")
    last_36 = st.toggle("Use last 36 monthly returns", disabled=upload is None)

source_id = "meridian" if upload is None else hashlib.sha256(upload.getvalue()).hexdigest()[:12]
return_id = source_id + ("_36" if last_36 else "_all")

try:
    if upload is None:
        sleeves, loaded_returns, volatilities, correlations = (
            SLEEVES, EXPECTED_RETURNS, VOLATILITIES, CORRELATIONS
        )
        source = "Meridian training inputs"
    else:
        # The comparison always uses estimates from all available months.
        sleeves, loaded_returns, volatilities, correlations = estimate_from_prices(
            upload, last_36=last_36
        )
        source = f"Uploaded CSV · {'last 36 monthly returns' if last_36 else 'all monthly returns'}"
except (ValueError, UnicodeError, OSError) as error:
    st.error(f"Could not read prices.csv: {error}")
    st.stop()

st.subheader(source)
if upload is None:
    st.caption("Meridian values are course training inputs.")
else:
    st.caption("Annualized returns are historical estimates from monthly adjusted close prices.")

st.write("Edit an expected return to test a one-point change. Choose the assets that satisfy the reserve rule.")
current_returns = []
eligible = []
for sleeve, loaded_return in zip(sleeves, loaded_returns):
    col_return, col_reserve = st.columns([2, 1])
    with col_return:
        value = st.number_input(f"{sleeve} expected return estimate (%)",
                                value=loaded_return * 100, step=0.1,
                                format="%.2f", key=f"return_{return_id}_{sleeve}")
        current_returns.append(value / 100)
    with col_reserve:
        if st.checkbox(f"{sleeve} reserve-eligible",
                       value=sleeve in RESERVE_ELIGIBLE if upload is None else False,
                       key=f"reserve_{source_id}_{sleeve}"):
            eligible.append(sleeve)

try:
    current = lowest_risk_mix(sleeves, current_returns, volatilities, correlations,
                              objective, eligible, reserve_minimum)
    if upload is None:
        baseline_returns, baseline_volatilities, baseline_correlations = (
            EXPECTED_RETURNS, VOLATILITIES, CORRELATIONS
        )
        baseline_eligible = RESERVE_ELIGIBLE
    else:
        _, baseline_returns, baseline_volatilities, baseline_correlations = (
            estimate_from_prices(upload)
        )
        baseline_eligible = eligible
    baseline = lowest_risk_mix(
        sleeves, baseline_returns, baseline_volatilities, baseline_correlations,
        objective, baseline_eligible, reserve_minimum
    )
except ValueError as error:
    st.error(str(error))
    st.stop()


def show_mix(mix, names):
    if mix is None:
        st.warning("No mix meets the objective")
        return
    weights, annual_return, volatility, reserve_weight = mix
    st.table({"Asset": list(names), "Weight (%)": [f"{weight * 100:.2f}" for weight in weights]})
    st.write(f"Return: **{annual_return * 100:.2f}%**")
    st.write(f"Volatility: **{volatility * 100:.2f}%**")
    st.write(f"Reserve-eligible weight: **{reserve_weight * 100:.2f}%**")


current_col, baseline_col = st.columns(2)
with current_col:
    st.subheader("Current inputs")
    show_mix(current, sleeves)
with baseline_col:
    st.subheader("As loaded · Meridian or all months")
    show_mix(baseline, sleeves)

if current is not None and baseline is not None:
    largest_change = max(abs(current[0][i] - baseline[0][i]) for i in range(len(sleeves)))
    st.metric("Largest weight change", f"{largest_change * 100:.0f} points")
else:
    st.info("Largest weight change is unavailable because at least one mix is infeasible.")
