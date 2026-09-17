"""Johnson & Johnson peer P/E valuation using frozen FY2025 GAAP EPS.

All prices are USD closing prices on September 10, 2026.  EPS is annual
reported diluted GAAP EPS for the fiscal year ended in 2025, disclosed before
the valuation date.  See JNJ-research/lab08_peer_valuation.md for sources.
"""

from statistics import median

TARGET = {
    "ticker": "JNJ",
    "name": "Johnson & Johnson",
    "price": 266.35,
    "diluted_eps": 11.03,
}

PEERS = [
    {"ticker": "ABT", "name": "Abbott Laboratories", "price": 103.36, "diluted_eps": 3.72},
    {"ticker": "MRK", "name": "Merck & Co.", "price": 144.71, "diluted_eps": 7.28},
]


def positive_number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and value > 0


def pe_multiple(company):
    """Return price / annual diluted EPS, or None when P/E is unusable."""
    if not positive_number(company.get("price")) or not positive_number(company.get("diluted_eps")):
        return None
    return company["price"] / company["diluted_eps"]


def implied_price(multiple, eps):
    return multiple * eps if positive_number(multiple) and positive_number(eps) else None


def main():
    target_eps = TARGET["diluted_eps"]
    print(f"Target: {TARGET['name']} ({TARGET['ticker']})")
    print("Basis: September 10, 2026 closing prices; FY2025 reported diluted GAAP EPS.")
    print("\nPeer P/E multiples")
    valid = []
    for peer in PEERS:
        multiple = pe_multiple(peer)
        if multiple is None:
            print(f"{peer['name']} ({peer['ticker']}): not meaningful")
        else:
            valid.append((peer, multiple))
            print(f"{peer['name']} ({peer['ticker']}): {multiple:.6f}x")

    if not valid or not positive_number(target_eps):
        print("\nNo usable peers or target EPS; no implied-price estimate.")
        return

    multiples = [multiple for _, multiple in valid]
    full_median = median(multiples)
    print(f"\nPeer median P/E: {full_median:.6f}x")
    for label, multiple in (("minimum", min(multiples)), ("median", full_median), ("maximum", max(multiples))):
        print(f"Target implied price at {label} P/E: ${implied_price(multiple, target_eps):,.2f} ({multiple:.6f}x)")

    print("\nLeave-one-peer-out analysis")
    for removed, _ in valid:
        remaining = [multiple for peer, multiple in valid if peer is not removed]
        if not remaining:
            print(f"Remove {removed['ticker']}: no estimate (no valid peers remain).")
            continue
        result = implied_price(median(remaining), target_eps)
        full = implied_price(full_median, target_eps)
        print(f"Remove {removed['ticker']}: reference estimate ${result:,.2f}; change from full-peer median ${result - full:,.2f}.")


if __name__ == "__main__":
    main()
