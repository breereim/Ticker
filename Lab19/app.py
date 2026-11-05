"""Streamlit view of the three-investor EDGAR panel."""

from __future__ import annotations

import os
from pathlib import Path
import sys

import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / ".agents" / "skills" / "buffett-edgar" / "scripts"
sys.path.insert(0, str(SCRIPT))
sys.path.insert(0, str(ROOT / "lab18"))
from edgar_buffett import TAGS, build_report, display_value
from memo_audit import unprinted_numbers


st.set_page_config(page_title="Legend Investor Panel", layout="wide")
st.title("Legend Investor Panel")
st.caption("Data from SEC EDGAR; built with AI help, a learning demonstration, not investment advice.")
ticker = st.text_input("Ticker", value="COST").strip().upper()
if not ticker:
    st.stop()
user_agent = os.getenv("SEC_USER_AGENT", "").strip()
if "@" not in user_agent or len(user_agent.split()) < 2:
    st.error("Set SEC_USER_AGENT to your real name and email before requesting EDGAR data.")
    st.stop()


@st.cache_data(ttl=3600, show_spinner="Downloading SEC companyfacts...")
def load_report(symbol: str, agent: str) -> dict:
    return build_report(symbol, agent)


try:
    report = load_report(ticker, user_agent)
except Exception as error:
    st.error(f"EDGAR request failed: {error}")
    st.stop()

st.subheader(f"{report['company']} ({ticker})")
st.link_button("SEC companyfacts", report["source"])
rows = report["rows"]
if len(rows) != 5:
    st.warning(f"Only {len(rows)} annual 10-K periods were found; the five-year checks are not known.")

chart_rows = []
for row in rows:
    for field, label in (("owner_earnings", "Owner earnings"), ("net_income", "Net income")):
        value = row[field]["value"]
        if value is not None:
            chart_rows.append({"FY end": row["fy_end"], "Measure": label, "USD millions": value / 1_000_000})
st.subheader("Owner earnings and net income")
if chart_rows:
    st.line_chart(chart_rows, x="FY end", y="USD millions", color="Measure")
else:
    st.info("No chart values found.")

st.subheader("Five fiscal years")
table = []
for row in rows:
    record = {"FY end": row["fy_end"]}
    for field in (*TAGS, "roe", "owner_earnings", "current_ratio", "liabilities_to_equity", "research_and_development_intensity"):
        record[field.replace("_", " ").title()] = display_value(field, row[field]["value"])
        record[field.replace("_", " ").title() + " XBRL"] = row[field]["tag"]
    table.append(record)
st.dataframe(table, hide_index=True, width="stretch")
st.caption("Dollar values are USD millions. ROE uses net income / year-end equity; owner earnings use operating cash flow minus capital spending. Current ratio uses current assets / current liabilities.")

st.subheader("Panel checks")
labels = {
    "roe_15_every_year": "ROE of 15% or more every year",
    "owner_earnings_positive_every_year": "Owner earnings positive every year",
    "owner_earnings_grew_first_to_last": "Owner earnings grew, first year to last",
    "revenue_grew_first_to_last": "Revenue grew, first year to last",
    "research_and_development_grew_first_to_last": "R&D expense grew, first year to last",
    "research_and_development_intensity_latest": "R&D expense at least 5% of revenue, latest year",
    "operating_cash_flow_at_least_net_income_every_year": "Operating cash flow at least net income every year",
    "liabilities_no_more_than_twice_equity_latest": "Liabilities no more than twice equity, latest year",
}
panel = report["panel"]
st.dataframe([{"Investor": investor, "Check": labels[key], "Result": result}
              for investor, checks in panel.items() for key, result in checks.items()],
             hide_index=True, width="stretch")
st.subheader("Verdicts")
st.dataframe([{"Investor": investor, "Checks passed": f"{sum(value == 'pass' for value in checks.values())} of {len(checks)}",
               "Screen verdict": "passes all" if all(value == "pass" for value in checks.values()) else "has unknowns" if "not known" in checks.values() else "has failures"}
              for investor, checks in panel.items()], hide_index=True, width="stretch")

st.subheader("Investor memos")
memos = {}
for investor, column in zip(("Buffett", "Cathie Wood", "Burry"), st.columns(3)):
    with column:
        st.markdown(f"### {investor}")
        memo_path = ROOT / "lab19" / "memos" / ticker / f"{investor.lower().replace(' ', '_')}.md"
        if investor == "Buffett" and not memo_path.exists():
            memo_path = ROOT / "lab18" / "memos" / f"{ticker}.md"
        stored_memo = memo_path.read_text(encoding="utf-8") if memo_path.exists() else ""
        memo = st.text_area(f"{investor} memo", value=stored_memo, height=300, key=f"memo_{ticker}_{investor}")
        if st.button(f"Save {investor} memo", key=f"save_{ticker}_{investor}"):
            memo_path.parent.mkdir(parents=True, exist_ok=True)
            memo_path.write_text(memo, encoding="utf-8")
            st.success(f"Saved {memo_path.relative_to(ROOT)}")
        if memo:
            st.markdown(memo)
        else:
            st.info("Memo not written yet.")
        memos[investor] = memo
unprinted = {investor: unprinted_numbers(memo, report) for investor, memo in memos.items() if memo}
flagged = {investor: numbers for investor, numbers in unprinted.items() if numbers}
if flagged:
    st.error("Unprinted numbers: " + "; ".join(f"{investor}: {', '.join(numbers)}" for investor, numbers in flagged.items()))
elif len(unprinted) == 3:
    st.success("Every number across all three memos appears in the script report.")
else:
    st.info("The number audit will cover all three memos once each is written.")
