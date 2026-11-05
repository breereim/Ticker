"""Live Lab 19 checkout for the Cathie Wood panel and missing-data probe."""

from __future__ import annotations

import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / ".agents" / "skills" / "buffett-edgar" / "scripts"))
sys.path.insert(0, str(ROOT / "lab18"))
from edgar_buffett import build_report, display_value
from memo_audit import unprinted_numbers


EXPECTED_COST = {
    "2022-08-28": (226954, 5844, 7392, 3891, 20642, "28.3%", 3501),
    "2023-09-03": (242290, 6292, 11068, 4323, 25058, "25.1%", 6745),
    "2024-09-01": (254453, 7367, 11339, 4710, 23622, "31.2%", 6629),
    "2025-08-31": (275235, 8099, 13335, 5498, 29164, "27.8%", 7837),
    "2026-08-30": (303154, 9226, 15817, 6435, 35803, "25.8%", 9382),
}
EXPECTED_RATIOS = {
    "2022-08-28": ("1.02", "2.11"),
    "2023-09-03": ("1.07", "1.75"),
    "2024-09-01": ("0.97", "1.96"),
    "2025-08-31": ("1.03", "1.64"),
    "2026-08-30": ("1.06", "1.49"),
}


def main() -> None:
    agent = os.getenv("SEC_USER_AGENT", "").strip()
    if "@" not in agent or len(agent.split()) < 2:
        raise SystemExit("Set SEC_USER_AGENT to your real name and email first.")
    cost = build_report("COST", agent)
    assert len(cost["rows"]) == 5
    for row in cost["rows"]:
        actual = tuple(
            display_value(field, row[field]["value"])
            for field in ("revenue", "net_income", "operating_cash_flow", "capital_spending", "equity", "roe", "owner_earnings")
        )
        expected = EXPECTED_COST[row["fy_end"]]
        assert actual == tuple(f"{value:,}" if isinstance(value, int) else value for value in expected), (row["fy_end"], actual, expected)
        ratios = tuple(display_value(field, row[field]["value"]) for field in ("current_ratio", "liabilities_to_equity"))
        assert ratios == EXPECTED_RATIOS[row["fy_end"]], (row["fy_end"], ratios)
    assert all(value == "pass" for value in cost["checks"].values())
    assert list(cost["panel"]["Cathie Wood"].values()) == ["pass", "not known", "not known"]
    assert list(cost["panel"]["Burry"].values()) == ["pass", "pass"]
    assert unprinted_numbers("The ROE is 40.0%.", cost) == ["40.0%"]
    print("COST Buffett, Cathie Wood, and Burry checks match; 40.0% flagged.")

    apple = build_report("AAPL", agent)
    assert display_value("research_and_development_intensity", apple["rows"][-1]["research_and_development_intensity"]["value"]) == "9.6%"
    assert list(apple["panel"]["Cathie Wood"].values()) == ["pass", "pass", "pass"]
    assert list(apple["panel"]["Burry"].values()) == ["fail", "fail"]
    print("AAPL Cathie Wood and Burry checks match the live facts.")

    jpm = build_report("JPM", agent)
    assert all(row["capital_spending"]["value"] is None for row in jpm["rows"])
    assert all(row["owner_earnings"]["value"] is None for row in jpm["rows"])
    assert jpm["checks"]["owner_earnings_positive_every_year"] == "not known"
    assert jpm["checks"]["owner_earnings_grew_first_to_last"] == "not known"
    print("JPM capital spending and owner earnings gaps stay unknown.")


if __name__ == "__main__":
    main()
