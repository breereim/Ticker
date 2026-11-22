"""Print the committee screen from the bundled data and model."""

from engine import ASSETS, run_case, stress_table


def percent(value):
    return f"{value:.2%}"


def weights(row):
    return " / ".join(f"{weight:.2%}" for weight in row["weights"])


def verdict(row):
    if row is None:
        return "INFEASIBLE"
    return "PASS" if not row["failures"] and row["objective"] else "FAIL"


def main():
    case = run_case()
    print("# Meridian Foundation Reserve - decision output")
    print()
    print("Data: 60 monthly returns through July 2026; 10 bp annual fee; "
          "10 bp one-way trade cost; benchmark starting-position proxy.")
    print("Screen: 6.5% first-year net estimate; 3% reserve minimum; "
          "25% turnover maximum; 5% weight grid.")
    print("Weights: " + " / ".join(ASSETS) + ".")
    print()
    print("| Portfolio | Weights | Net estimate | Volatility | Reserve | Turnover | Coded screen |")
    print("|---|---:|---:|---:|---:|---:|---|")
    for label, key in (("Equal weight", "equal"),
                       ("Inverse volatility", "inverse_vol"),
                       ("60/40 benchmark proxy", "benchmark"),
                       ("Constrained lowest volatility", "portfolio")):
        row = case[key]
        print(f"| {label} | {weights(row)} | {percent(row['net'])} | "
              f"{percent(row['volatility'])} | {percent(row['reserve'])} | "
              f"{percent(row['turnover'])} | {verdict(row)} |")
    print()
    print("## One-input stress runs")
    print()
    print("| Scenario | Weights | Net estimate | Volatility | Turnover | Feasible |")
    print("|---|---:|---:|---:|---:|---|")
    for row in stress_table():
        if not row["feasible"]:
            print(f"| {row['scenario']} | n/a | n/a | n/a | n/a | No |")
            continue
        print(f"| {row['scenario']} | {weights(row)} | {percent(row['net'])} | "
              f"{percent(row['volatility'])} | {percent(row['turnover'])} | Yes |")
    print()
    print("Committee decision: REJECT live allocation (0%); paper pilot only.")
    print("Issuer look-through, actual holdings/turnover, and the CIO annual-loss rule remain unverified.")
    print("A coded pass is a planning screen, not verified mandate compliance or a live allocation approval.")


if __name__ == "__main__":
    main()
