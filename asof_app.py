"""Lab 17: compare live FRED values with an ALFRED historical vintage.

Run: python -m streamlit run asof_app.py
"""

from datetime import date
from io import StringIO
import re

import altair as alt
import pandas as pd
import requests
import streamlit as st


SERIES = {
    "BAA": "Moody's Baa corporate bond yield",
    "FEDFUNDS": "Federal funds rate",
    "DGS10": "10-year Treasury yield",
    "MORTGAGE30US": "30-year mortgage rate",
}
ID_PATTERN = re.compile(r"^[A-Z0-9_]+$")
LINE_COLORS = ["#1565C0", "#E65100", "#2E7D32", "#7B1FA2", "#C2185B"]


def parse_csv(body: str, series_id: str) -> pd.Series:
    """Read a single FRED/ALFRED download; a dot means no observation."""
    frame = pd.read_csv(StringIO(body), na_values=["."])
    if frame.shape[1] != 2 or frame.empty:
        raise ValueError("The download did not contain one date and one value column.")
    date_column, value_column = frame.columns
    if date_column not in ("observation_date", "DATE") or not value_column.startswith(series_id):
        raise ValueError("The download did not match the requested series.")
    dates = pd.to_datetime(frame[date_column], errors="raise")
    values = pd.to_numeric(frame[value_column], errors="raise")
    result = pd.Series(values.to_numpy(), index=dates, name=series_id).dropna()
    if result.index.has_duplicates:
        raise ValueError("The download contains duplicate observation dates.")
    return result.sort_index()


def download_csv(url: str, params: dict[str, str], series_id: str) -> pd.Series:
    response = requests.get(url, params=params, timeout=45)
    response.raise_for_status()
    return parse_csv(response.text, series_id)


@st.cache_data(ttl=3600, show_spinner=False)
def download_today(series_id: str) -> pd.Series:
    """One public FRED CSV request for the current series values."""
    return download_csv(
        "https://fred.stlouisfed.org/graph/fredgraph.csv",
        {"id": series_id},
        series_id,
    )


@st.cache_data(ttl=3600, show_spinner=False)
def download_as_known(series_id: str, vintage_date: date) -> pd.Series:
    """One public ALFRED CSV request for values available on vintage_date."""
    result = download_csv(
        "https://alfred.stlouisfed.org/graph/alfredgraph.csv",
        {"id": series_id, "vintage_date": vintage_date.isoformat()},
        series_id,
    )
    return result.loc[result.index <= pd.Timestamp(vintage_date)]


def summary(series_id: str, current: pd.Series, known: pd.Series) -> dict:
    known_date = known.index.max() if not known.empty else pd.NaT
    current_date = current.index.max() if not current.empty else pd.NaT
    shared_dates = known.index.intersection(current.index)
    revised = (known.loc[shared_dates] != current.loc[shared_dates]).sum()
    later = (current.index > known_date).sum() if pd.notna(known_date) else len(current)
    return {
        "Series": f"https://fred.stlouisfed.org/series/{series_id}",
        "Last measured date known then": known_date.date().isoformat() if pd.notna(known_date) else "—",
        "Value known then": float(known.iloc[-1]) if not known.empty else None,
        "Last measured date today": current_date.date().isoformat() if pd.notna(current_date) else "—",
        "Value today": float(current.iloc[-1]) if not current.empty else None,
        "Later values": int(later),
        "Revised same-date values": int(revised),
    }


def comparison_frame(
    series: dict[str, pd.Series], start: date, indexed: bool
) -> tuple[pd.DataFrame, list[str]]:
    """Align observed dates without filling unpublished or missing values."""
    columns = []
    skipped = []
    for series_id, values in series.items():
        visible = values.loc[values.index >= pd.Timestamp(start)]
        if visible.empty:
            skipped.append(series_id)
            continue
        if indexed:
            first = visible.iloc[0]
            if first == 0:
                skipped.append(series_id)
                continue
            visible = visible / first * 100
        columns.append(visible.rename(series_id))
    return (pd.concat(columns, axis=1, sort=True) if columns else pd.DataFrame()), skipped


def comparison_chart(frame: pd.DataFrame, y_label: str) -> alt.Chart:
    """Draw one clearly colored line per series, with an explicit legend."""
    long = (
        frame.rename_axis("Measured date")
        .reset_index()
        .melt(id_vars="Measured date", var_name="Series", value_name="Value")
        .dropna(subset=["Value"])
    )
    series_ids = list(frame.columns)
    return (
        alt.Chart(long)
        .mark_line(strokeWidth=2.6)
        .encode(
            x=alt.X("Measured date:T", title="Measured date"),
            y=alt.Y("Value:Q", title=y_label, scale=alt.Scale(zero=False)),
            color=alt.Color(
                "Series:N",
                scale=alt.Scale(
                    domain=series_ids,
                    range=[LINE_COLORS[i % len(LINE_COLORS)] for i in range(len(series_ids))],
                ),
                legend=alt.Legend(title="Series", orient="bottom", labelFontSize=13),
            ),
            tooltip=[
                alt.Tooltip("Measured date:T", format="%Y-%m-%d"),
                alt.Tooltip("Series:N"),
                alt.Tooltip("Value:Q", format=",.2f"),
            ],
        )
        .properties(height=430)
    )


def candle_data(values: pd.Series, start: date) -> tuple[pd.DataFrame, str]:
    """Summarize reported values into period first/high/low/last candles."""
    visible = values.loc[values.index >= pd.Timestamp(start)]
    if visible.empty:
        return pd.DataFrame(), ""
    gaps = visible.index.to_series().diff().dt.days.dropna()
    typical_gap = gaps.median() if not gaps.empty else 0
    if typical_gap >= 60:
        period_code, period_name = "Y", "yearly"
    elif typical_gap > 10:
        period_code, period_name = "Q", "quarterly"
    else:
        period_code, period_name = "M", "monthly"
    rows = []
    for period, group in visible.groupby(visible.index.to_period(period_code)):
        rows.append({
            "Period": period.start_time,
            "Open": float(group.iloc[0]),
            "High": float(group.max()),
            "Low": float(group.min()),
            "Close": float(group.iloc[-1]),
            "First observed": group.index[0],
            "Last observed": group.index[-1],
            "Observations": len(group),
            "Direction": "Rising" if group.iloc[-1] > group.iloc[0] else
                         "Falling" if group.iloc[-1] < group.iloc[0] else "Flat",
        })
    return pd.DataFrame(rows), period_name


def candlestick_chart(candles: pd.DataFrame, y_label: str) -> alt.LayerChart:
    """Render the period range and first-to-last body of each candle."""
    base = alt.Chart(candles).encode(
        x=alt.X("Period:T", title="Period start"),
        tooltip=[
            alt.Tooltip("Period:T", format="%Y-%m-%d"),
            alt.Tooltip("First observed:T", format="%Y-%m-%d"),
            alt.Tooltip("Last observed:T", format="%Y-%m-%d"),
            alt.Tooltip("Open:Q", format=",.2f"),
            alt.Tooltip("High:Q", format=",.2f"),
            alt.Tooltip("Low:Q", format=",.2f"),
            alt.Tooltip("Close:Q", format=",.2f"),
            alt.Tooltip("Observations:Q"),
        ],
    )
    wick = base.mark_rule(color="#475569", strokeWidth=1.5).encode(
        y=alt.Y("Low:Q", title=y_label, scale=alt.Scale(zero=False)),
        y2="High:Q",
    )
    body = base.mark_bar(size=9).encode(
        y=alt.Y("Open:Q", title=y_label, scale=alt.Scale(zero=False)),
        y2="Close:Q",
        color=alt.Color(
            "Direction:N",
            scale=alt.Scale(
                domain=["Rising", "Falling", "Flat"],
                range=["#C62828", "#2E7D32", "#64748B"],
            ),
            legend=alt.Legend(title="Rate move", orient="bottom"),
        ),
    )
    flat = base.transform_filter(alt.datum.Direction == "Flat").mark_tick(
        color="#64748B", size=12, thickness=2
    ).encode(y="Open:Q")
    return (wick + body + flat).properties(height=330)


def main() -> None:
    st.set_page_config(page_title="Point-in-Time Rates Audit", layout="wide")
    st.title("Point-in-Time Rates Audit")
    st.caption(
        "Data from FRED and ALFRED, Federal Reserve Bank of St. Louis, "
        f"downloaded {date.today().isoformat()}; built with AI help, a learning "
        "demonstration, not investment advice."
    )
    st.caption(
        "Candles summarize the first, highest, lowest, and last published series values "
        "within each month or quarter. They are not traded market OHLC prices."
    )

    with st.sidebar:
        selected = st.multiselect(
            "Rate series",
            options=list(SERIES),
            default=list(SERIES),
            format_func=lambda series_id: f"{series_id} — {SERIES[series_id]}",
        )
        extra = st.text_input("Add another FRED series ID (for example, PAYEMS)").strip().upper()
        start = st.date_input("Start date for charts", value=date(2020, 1, 1))
        vintage = st.date_input("As known on", value=date.today(), max_value=date.today())
        comparison_vintage = st.radio("Comparison chart data", ["Today", "As known on selected date"])
        indexed = st.checkbox(
            "Index comparison lines to 100",
            value=bool(extra),
            help="Useful when selected series have different units. Each line starts at 100 on its first visible observation.",
        )

    ids = list(dict.fromkeys(selected + ([extra] if extra else [])))
    if not ids:
        st.info("Select a rate series or enter a FRED series ID.")
        return
    if start > vintage:
        st.info("The chart start date is after the as-known date; the table still uses the full history.")

    loaded = {}
    errors = {}
    for series_id in ids:
        if not ID_PATTERN.fullmatch(series_id):
            errors[series_id] = "Use only letters, digits, and underscores in a FRED series ID."
            continue
        try:
            current = download_today(series_id)
            known = download_as_known(series_id, vintage)
        except (requests.RequestException, ValueError, pd.errors.ParserError) as error:
            errors[series_id] = f"Could not load this series: {error}"
            continue
        loaded[series_id] = (current, known)

    st.subheader("Compare selected series")
    source_index = 0 if comparison_vintage == "Today" else 1
    compare, skipped = comparison_frame(
        {series_id: pair[source_index] for series_id, pair in loaded.items()}, start, indexed
    )
    compare_left, compare_right = st.columns(2, gap="large")
    with compare_left:
        st.markdown("**Overlaid line chart**")
        if compare.empty:
            st.info("No observations to compare on or after the chart start date.")
        else:
            all_rates = all(series_id in SERIES for series_id in compare.columns)
            if not indexed and not all_rates:
                st.warning("These series may use different units. Index the lines to 100 for a comparable scale.")
            st.altair_chart(
                comparison_chart(
                    compare,
                    "Index (first visible value = 100)" if indexed else
                    "Rate (%)" if all_rates else "Series value (check units)",
                ),
                width="stretch",
            )
            st.caption("Recorded observations only; no dates are filled. Indexed lines use each series' first visible value.")
    with compare_right:
        st.markdown("**Candlestick view**")
        if loaded:
            candle_id = st.selectbox("Series to show as candles", list(loaded))
            candle_values = loaded[candle_id][source_index]
            candles, period_name = candle_data(candle_values, start)
            if candles.empty:
                st.info("No observations to summarize on or after the chart start date.")
            else:
                unit = "Rate (%)" if candle_id in SERIES else "Series value (check units)"
                st.altair_chart(candlestick_chart(candles, unit), width="stretch")
                st.caption(f"{period_name.capitalize()} candles for {candle_id}; first, high, low, and last reported value in each period.")
        else:
            st.info("No series loaded for candles.")
    if skipped:
        st.info(f"No comparison line for: {', '.join(skipped)} (no visible data or a zero index base).")

    rows = []
    for series_id in ids:
        st.subheader(f"{series_id} — {SERIES.get(series_id, 'FRED series')}")
        if series_id in errors:
            st.error(f"{series_id}: {errors[series_id]}")
            continue
        current, known = loaded[series_id]
        chart = current.loc[current.index >= pd.Timestamp(start)]
        left, right = st.columns(2, gap="large")
        with left:
            st.markdown("**Current values — line chart**")
            if chart.empty:
                st.info("No current observations on or after the chart start date.")
            else:
                st.line_chart(chart, x_label="Measured date", y_label="Rate (%)" if series_id in SERIES else "Value")
        with right:
            st.markdown("**Current values — candlestick view**")
            candles, period_name = candle_data(current, start)
            if candles.empty:
                st.info("No observations to summarize on or after the chart start date.")
            else:
                unit = "Rate (%)" if series_id in SERIES else "Series value (check units)"
                st.altair_chart(candlestick_chart(candles, unit), width="stretch")
                st.caption(f"{period_name.capitalize()} candles: first, high, low, and last reported value in each period.")
        if known.empty:
            st.write(f"Last date in data known on {vintage.isoformat()}: none")
        else:
            st.write(
                f"Last date in data known on {vintage.isoformat()}: "
                f"**{known.index[-1].date().isoformat()}**, value **{known.iloc[-1]:,.2f}**"
            )
        rows.append(summary(series_id, current, known))

    st.subheader("As-known comparison")
    if rows:
        st.dataframe(
            pd.DataFrame(rows),
            column_config={"Series": st.column_config.LinkColumn("Series", display_text=r"series/([A-Z0-9_]+)$")},
            hide_index=True,
            width="stretch",
        )
        st.caption(
            "Later values count today's nonmissing observations after the last measured date "
            "known then. Revised values compare nonmissing observations with the same "
            "measured date in both downloads. Counts use the full downloaded history."
        )
    else:
        st.warning("No series loaded. Check the IDs or the download connection.")


if __name__ == "__main__":
    main()
