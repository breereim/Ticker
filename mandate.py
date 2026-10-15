"""Check the Meridian Foundation Reserve's explicit, measurable mandate rules.

Run: python mandate.py
All dollar amounts are USD millions; portfolio weights are percentages.
"""

# Editable inputs
HOLDINGS = {
    "Cash": {
        "issuer": "none", "redeem_days": 0, "reserve_eligible": True,
        "issuer_exempt": True,
    },
    "Treasury bills": {
        "issuer": "U.S. Treasury", "redeem_days": 1, "reserve_eligible": True,
        "issuer_exempt": True,
    },
    "Treasury 10-year note": {
        "issuer": "U.S. Treasury", "redeem_days": 1, "reserve_eligible": True,
        "issuer_exempt": True,
    },
    "Global equity index fund": {
        "issuer": "diversified fund", "redeem_days": 2, "reserve_eligible": False,
        "issuer_exempt": True,
    },
    "Investment-grade bond fund": {
        "issuer": "diversified fund", "redeem_days": 3, "reserve_eligible": False,
        "issuer_exempt": True,
    },
    "Private real estate fund": {
        "issuer": "diversified fund", "redeem_days": 90, "reserve_eligible": False,
        "issuer_exempt": True,
    },
    "Acme Corp bonds": {
        "issuer": "Acme Corp", "redeem_days": 4, "reserve_eligible": False,
        "issuer_exempt": False,
    },
    "Acme Corp stock": {
        "issuer": "Acme Corp", "redeem_days": 1, "reserve_eligible": False,
        "issuer_exempt": False,
    },
}

CANDIDATES = {
    "A": {
        "Cash": 2, "Treasury bills": 2, "Treasury 10-year note": 10,
        "Global equity index fund": 60, "Investment-grade bond fund": 26,
        "Private real estate fund": 0, "Acme Corp bonds": 0, "Acme Corp stock": 0,
    },
    "B": {
        "Cash": 1, "Treasury bills": 0, "Treasury 10-year note": 0,
        "Global equity index fund": 55, "Investment-grade bond fund": 20,
        "Private real estate fund": 15, "Acme Corp bonds": 5, "Acme Corp stock": 4,
    },
    "C": {
        "Cash": 1, "Treasury bills": 1, "Treasury 10-year note": 0,
        "Global equity index fund": 70, "Investment-grade bond fund": 20,
        "Private real estate fund": 0, "Acme Corp bonds": 0, "Acme Corp stock": 8,
    },
    # Attack portfolio: passes the measurable rules, but may be unsuitable under S2/S10.
    "D": {
        "Cash": 3, "Treasury bills": 0, "Treasury 10-year note": 97,
        "Global equity index fund": 0, "Investment-grade bond fund": 0,
        "Private real estate fund": 0, "Acme Corp bonds": 0, "Acme Corp stock": 0,
    },
}

RESERVE_SIZE = 100
QUARTERLY_DISTRIBUTION = 0.75
QUARTERS_TO_COVER = 4
LIQUIDITY_WINDOW_DAYS = 5
MINIMUM_LIQUID_SHARE = 90
ISSUER_LIMIT = 8


def check_candidate(name, weights, reserve_minimum):
    """Print each checkable mandate rule and return its number of failures."""
    total_weight = sum(weights.values())
    lowest_weight = min(weights.values())
    reserve_weight = sum(
        weight for holding, weight in weights.items()
        if HOLDINGS[holding]["reserve_eligible"]
    )
    liquid_weight = sum(
        weight for holding, weight in weights.items()
        if HOLDINGS[holding]["redeem_days"] <= LIQUIDITY_WINDOW_DAYS
    )

    company_weights = {}
    for holding, weight in weights.items():
        details = HOLDINGS[holding]
        if not details["issuer_exempt"]:
            issuer = details["issuer"]
            company_weights[issuer] = company_weights.get(issuer, 0) + weight
    largest_company = max(company_weights.values(), default=0)

    checks = [
        ("Weights sum to 100", total_weight, total_weight == 100),
        ("Long-only (lowest weight)", lowest_weight, lowest_weight >= 0),
        (f"Reserve >= {reserve_minimum:.1f}%", reserve_weight,
         reserve_weight >= reserve_minimum),
        (f"Redeemable in {LIQUIDITY_WINDOW_DAYS} days >= {MINIMUM_LIQUID_SHARE:.1f}%",
         liquid_weight, liquid_weight >= MINIMUM_LIQUID_SHARE),
        (f"Largest single company <= {ISSUER_LIMIT:.1f}%", largest_company,
         largest_company <= ISSUER_LIMIT),
    ]

    print(f"\nCandidate {name}")
    failures = 0
    for label, value, passed in checks:
        result = "pass" if passed else "FAIL"
        print(f"{label}: {value:.1f} {result}")
        failures += not passed
    print("Calendar-year loss: requires CIO clarification")
    if failures:
        print(f"Verdict: fails {failures} rule(s)")
    else:
        print("Verdict: passes every checkable rule")
    return failures


def main():
    reserve_minimum = QUARTERS_TO_COVER * QUARTERLY_DISTRIBUTION / RESERVE_SIZE * 100
    print(f"Reserve minimum: {reserve_minimum:.1f}%")
    for name, weights in CANDIDATES.items():
        check_candidate(name, weights, reserve_minimum)


if __name__ == "__main__":
    main()
