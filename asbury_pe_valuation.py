"""Asbury Automotive peer P/E valuation using the case's frozen FY2024 inputs.

Edit TARGET and PEERS below to use another target or peer set.  Inputs should
be year-end price per share and total GAAP diluted EPS for the same fiscal year.
"""

from statistics import median

# ---- Editable inputs -------------------------------------------------------
TARGET = {
    "ticker": "ABG",
    "name": "Asbury Automotive",
    "price": 243.03,
    "diluted_eps": 21.50,
}

PEERS = [
    {"ticker": "AN", "name": "AutoNation", "price": 169.84, "diluted_eps": 16.92},
    {"ticker": "GPI", "name": "Group 1 Automotive", "price": 421.48, "diluted_eps": 36.81},
]
# ---------------------------------------------------------------------------


def valid_positive_number(value):
    """Return True only for positive numeric price/EPS inputs."""
    return isinstance(value, (int, float)) and not isinstance(value, bool) and value > 0


def pe_multiple(company):
    """Return price / diluted EPS, or None when P/E is not meaningful."""
    price = company.get("price")
    eps = company.get("diluted_eps")
    if not valid_positive_number(price) or not valid_positive_number(eps):
        return None
    return price / eps


def print_estimate(label, multiple, target_eps):
    if multiple is None or not valid_positive_number(target_eps):
        print(f"{label}: not meaningful")
    else:
        print(f"{label}: ${multiple * target_eps:,.2f} ({multiple:.6f}x)")


def unique_eligible_peers(target, peers):
    """Deduplicate by ticker and exclude the target ticker."""
    target_ticker = str(target.get("ticker", "")).upper()
    seen = set()
    eligible = []
    for peer in peers:
        ticker = str(peer.get("ticker", "")).upper()
        key = ticker or peer.get("name", "").strip().upper()
        if ticker == target_ticker:
            print(f"Excluded {peer.get('name', ticker)}: it is the target.")
        elif not key or key in seen:
            print(f"Excluded {peer.get('name', ticker or 'unnamed peer')}: duplicate or missing identifier.")
        else:
            seen.add(key)
            eligible.append(peer)
    return eligible


def main():
    target_eps = TARGET.get("diluted_eps")
    print(f"Target: {TARGET['name']} ({TARGET['ticker']})")
    if not valid_positive_number(target_eps):
        print("Target diluted EPS is missing or nonpositive: implied prices are not meaningful.")

    eligible = unique_eligible_peers(TARGET, PEERS)
    valid = []
    print("\nPeer P/E multiples")
    for peer in eligible:
        multiple = pe_multiple(peer)
        if multiple is None:
            print(f"{peer['name']} ({peer['ticker']}): not meaningful (price and diluted EPS must be positive)")
        else:
            valid.append((peer, multiple))
            print(f"{peer['name']} ({peer['ticker']}): {multiple:.6f}x")

    if not valid:
        print("\nNo usable peers; no implied-price estimate.")
        return

    multiples = [multiple for _, multiple in valid]
    full_median = median(multiples)
    print(f"\nPeer median P/E: {full_median:.6f}x")
    if len(valid) == 1:
        print("One valid peer: reference estimate, no range.")
        print_estimate("Target reference estimate", full_median, target_eps)
    else:
        print_estimate("Target implied price at minimum P/E", min(multiples), target_eps)
        print_estimate("Target implied price at median P/E", full_median, target_eps)
        print_estimate("Target implied price at maximum P/E", max(multiples), target_eps)

    print("\nLeave-one-peer-out analysis")
    for removed_peer, _ in valid:
        remaining = [multiple for peer, multiple in valid if peer is not removed_peer]
        if not remaining or not valid_positive_number(target_eps):
            print(f"Remove {removed_peer['ticker']}: no estimate (no valid peers remain).")
            continue
        remaining_median = median(remaining)
        remaining_price = remaining_median * target_eps
        full_price = full_median * target_eps
        change = remaining_price - full_price
        descriptor = "reference estimate" if len(remaining) == 1 else "median-implied price"
        print(
            f"Remove {removed_peer['ticker']}: {descriptor} ${remaining_price:,.2f}; "
            f"change from full-peer estimate ${change:,.2f}."
        )


if __name__ == "__main__":
    main()
