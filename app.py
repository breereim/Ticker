"""Streamlit view of the repo's Buffett EDGAR skill output."""

from __future__ import annotations

import os
from pathlib import Path
import sys

import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / ".agents" / "skills" / "buffett-edgar" / "scripts"
sys.path.insert(0, str(SCRIPT))
from edgar_buffett import TAGS, build_report, display_value
from memo_audit import unprinted_numbers


st.set_page_config(page_title="Buffet Business Lens", layout="wide")
st.title("Buffet Business Lens")
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
    for field in (*TAGS, "roe", "owner_earnings"):
        record[field.replace("_", " ").title()] = display_value(field, row[field]["value"])
        record[field.replace("_", " ").title() + " XBRL"] = row[field]["tag"]
    table.append(record)
st.dataframe(table, hide_index=True, width="stretch")
st.caption("Dollar values are USD millions. ROE uses net income / year-end equity; owner earnings use operating cash flow − capital spending.")

st.subheader("Buffett checks")
labels = {
    "roe_15_every_year": "ROE of 15% or more every year",
    "owner_earnings_positive_every_year": "Owner earnings positive every year",
    "owner_earnings_grew_first_to_last": "Owner earnings grew, first year to last",
}
st.dataframe([{"Check": labels[key], "Result": value} for key, value in report["checks"].items()], hide_index=True, width="stretch")

st.subheader("Buffett-style business memo")
memo_path = ROOT / "lab18" / "memos" / f"{ticker}.md"
stored_memo = memo_path.read_text(encoding="utf-8") if memo_path.exists() else ""
memo = st.text_area("Memo (editable for the number probe)", value=stored_memo, height=260, key=f"memo_{ticker}")
if st.button("Save memo"):
    memo_path.parent.mkdir(parents=True, exist_ok=True)
    memo_path.write_text(memo, encoding="utf-8")
    st.success(f"Saved {memo_path.relative_to(ROOT)}")
if memo:
    st.markdown(memo)
    unprinted = unprinted_numbers(memo, report)
    if unprinted:
        st.error("Numbers the script did not print: " + ", ".join(unprinted))
    else:
        st.success("Every number in this memo appears in the script report.")
else:
    st.info("Run the Buffett EDGAR skill for this ticker, then save its Markdown memo here.")
