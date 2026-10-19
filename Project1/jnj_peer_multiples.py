"""JNJ peer EV/EBIT and P/E cross-check; USD millions except per-share data.

All prices are September 10, 2026 closes.  FY2025 EBIT, cash, and debt are
from the named companies' FY2025 filings/results releases.  Weighted-average
diluted shares are used as a disclosed market-capitalization proxy; this is a
limitation, recorded in docs/peer-policy-and-multiples.md.
"""

from statistics import median

COMPANIES = [
    {"ticker": "JNJ", "price": 266.35, "shares": 2429.4, "cash": 19709,
     "debt": 47933, "ebit": 25287, "eps": 11.03},
    {"ticker": "ABT", "price": 103.36, "shares": 1749, "cash": 8900,
     "debt": 12900, "ebit": 8053, "eps": 3.72},
    {"ticker": "MRK", "price": 144.71, "shares": 2507, "cash": 14565,
     "debt": 49300, "ebit": 21067, "eps": 7.28},
]


def metrics(company):
    market_cap = company["price"] * company["shares"]
    enterprise_value = market_cap + company["debt"] - company["cash"]
    return market_cap, enterprise_value, enterprise_value / company["ebit"], company["price"] / company["eps"]


def main():
    values = {}
    print("Ticker | market cap | enterprise value | EV/EBIT | P/E")
    for company in COMPANIES:
        market_cap, ev, ev_ebit, pe = metrics(company)
        values[company["ticker"]] = (market_cap, ev, ev_ebit, pe)
        print(f"{company['ticker']:>5} | ${market_cap:10,.1f} | ${ev:16,.1f} | {ev_ebit:7.2f}x | {pe:6.2f}x")
    peer_ev_ebit = median([values["ABT"][2], values["MRK"][2]])
    target = COMPANIES[0]
    implied_ev = peer_ev_ebit * target["ebit"]
    implied_equity = implied_ev - target["debt"] + target["cash"]
    print(f"\nPeer median EV/EBIT: {peer_ev_ebit:.2f}x")
    print(f"JNJ implied value at peer median: ${implied_equity / target['shares']:.2f}/share")


if __name__ == "__main__":
    main()
