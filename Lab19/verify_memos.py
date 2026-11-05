"""Audit all three saved memos for each live EDGAR panel run."""

from __future__ import annotations

import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / ".agents" / "skills" / "buffett-edgar" / "scripts"))
sys.path.insert(0, str(ROOT / "lab18"))
from edgar_buffett import build_report
from memo_audit import unprinted_numbers


def main() -> None:
    agent = os.getenv("SEC_USER_AGENT", "").strip()
    if "@" not in agent or len(agent.split()) < 2:
        raise SystemExit("Set SEC_USER_AGENT to your real name and email first.")
    for ticker in ("COST", "AAPL"):
        report = build_report(ticker, agent)
        for investor in ("buffett", "cathie_wood", "burry"):
            path = ROOT / "lab19" / "memos" / ticker / f"{investor}.md"
            memo = path.read_text(encoding="utf-8")
            unexpected = unprinted_numbers(memo, report)
            if unexpected:
                raise AssertionError(f"{path}: unprinted numbers: {unexpected}")
            print(f"{ticker} {investor}: numbers audited")


if __name__ == "__main__":
    main()
