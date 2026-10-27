"""Lab 16: point-in-time filter for the fictional card-spend index."""

from datetime import date


# Edit these inputs for a different decision date or training table.
DECISION_DATE = "2026-03-31"
ROWS = [
    (1, "AAA", "2026-01", "2026-02-10", 101.0),
    (2, "AAA", "2026-02", "2026-03-10", 104.0),
    (3, "AAA", "2026-03", "2026-04-10", 109.0),
    (4, "AAA", "2026-02", "2026-03-25", 103.0),
    (5, "BBB", "2026-01", "2026-02-10", 98.0),
    (6, "BBB", "2026-02", "2026-03-10", 97.0),
    (7, "BBB", "2026-02", "2026-03-10", 97.0),
    (8, "BBB", "2026-03", "2026-04-10", 92.0),
    (9, "CCC", "2026-01", "2026-02-10", 110.0),
    (10, "CCC", "2026-02", "2026-04-05", 112.0),
    (11, "", "2026-02", "2026-03-10", 99.0),
    (12, "CCC", "2026-02", "2026-03-10", 111.0),
]


def newest_publications(rows):
    """Select the latest publication for each ticker/month in the given rows."""
    latest = {}
    replaced = []
    for row in rows:
        number, ticker, month, published, value = row
        key = (ticker, month)
        previous = latest.get(key)
        if previous is None:
            latest[key] = row
        elif date.fromisoformat(published) > date.fromisoformat(previous[3]):
            replaced.append(previous[0])
            latest[key] = row
        elif published < previous[3]:
            replaced.append(number)
        else:
            raise ValueError(f"Conflicting values on the same publication date: rows {previous[0]}, {number}")
    return sorted(latest.values(), key=lambda row: (row[1], row[2])), sorted(replaced)


def signals(panel):
    """Return each ticker's change from the preceding month to its latest month."""
    by_ticker = {}
    for row in panel:
        by_ticker.setdefault(row[1], []).append(row)

    result = {}
    for ticker, series in by_ticker.items():
        series.sort(key=lambda row: row[2])
        if len(series) < 2:
            raise ValueError(f"{ticker} needs at least two monthly observations")
        earlier, latest = series[-2:]
        year, month = map(int, latest[2].split("-"))
        previous_month = f"{year - 1}-12" if month == 1 else f"{year}-{month - 1:02d}"
        if earlier[2] != previous_month:
            raise ValueError(f"{ticker} has no preceding month for {latest[2]}")
        if earlier[4] == 0:
            raise ValueError(f"{ticker} has a zero index in {earlier[2]}")
        result[ticker] = (latest[2], (latest[4] / earlier[4] - 1) * 100, latest[0])
    return result


def print_step(label, removed):
    numbers = ", ".join(map(str, sorted(removed))) or "none"
    print(f"{label}: {len(removed)} removed (rows {numbers})")


def main():
    cutoff = date.fromisoformat(DECISION_DATE)

    # Rule 1: quarantine missing tickers.
    quarantined = [row[0] for row in ROWS if not row[1].strip()]
    named = [row for row in ROWS if row[1].strip()]

    # Rule 2: remove exact duplicates, excluding the identifying row number.
    seen = set()
    unique = []
    duplicates = []
    for row in named:
        if row[1:] in seen:
            duplicates.append(row[0])
        else:
            seen.add(row[1:])
            unique.append(row)

    # Rule 3: exclude publications after the decision date.
    unpublished = [row[0] for row in unique if date.fromisoformat(row[3]) > cutoff]
    knowable = [row for row in unique if date.fromisoformat(row[3]) <= cutoff]

    # Rule 4: for each ticker/month, retain its latest knowable publication.
    panel, revisions = newest_publications(knowable)

    print(f"Decision date: {DECISION_DATE}")
    print("Row funnel")
    print_step("1. No ticker", quarantined)
    print_step("2. Exact duplicate", duplicates)
    print_step("3. Published after decision date", unpublished)
    print_step("4. Older vintage replaced", revisions)
    print("As-of panel")
    print("Row  Ticker  Month    Published   Index")
    for number, ticker, month, published, value in panel:
        print(f"{number:>3}  {ticker:<6}  {month}  {published}  {value:>5.1f}")

    # Naive view uses the same cleaned rows, but ignores the decision cutoff.
    naive_panel, _ = newest_publications(unique)
    asof = signals(panel)
    naive = signals(naive_panel)
    print("Signals")
    for ticker in sorted(asof):
        asof_month, asof_change, _ = asof[ticker]
        naive_month, naive_change, naive_row = naive[ticker]
        revised = ", revised" if any(
            row[1:3] == (ticker, naive_month) and row[0] != naive_row
            for row in unique
        ) else ""
        print(
            f"{ticker}: as-of {asof_change:+.2f}% ({asof_month}); "
            f"naive {naive_change:+.2f}% ({naive_month}{revised})"
        )


if __name__ == "__main__":
    main()
