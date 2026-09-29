"""Lab 11 — JNJ one-at-a-time sensitivity analysis.

USD millions except per-share data. Run: python "Lab 11 jnj_sensitivity.py"
Uses the completed Lab 10 JNJ forecast engine but keeps a separate immutable
base input set and a fresh forecast for every lower/base/higher run.

Partner-exchange note: research spending reduces near-term profit and FCFE;
the argument for it is that successful research can later create products and
cash flows, subject to evidence about the size and timing of that payoff.
"""
from copy import deepcopy
import importlib.util
from pathlib import Path

MODEL_PATH = Path(__file__).with_name("Lab 10 jnj_proforma.py")
spec = importlib.util.spec_from_file_location("jnj_proforma", MODEL_PATH)
model = importlib.util.module_from_spec(spec)
spec.loader.exec_module(model)

BASE = {"revenue_growth": (0.050, 0.040, 0.040, 0.035, 0.030), "gross_margin": 0.680}
CASES = {
    "Revenue growth (FY2026E--FY2030E)": {
        "unit": "% of prior-year revenue",
        "inputs": {"Lower": (0.040, 0.030, 0.030, 0.025, 0.020), "Base": BASE["revenue_growth"], "Higher": (0.060, 0.050, 0.050, 0.045, 0.040)},
        "run": lambda value: model.project(revenue_growth_path=deepcopy(value), gross_margin_assumption=BASE["gross_margin"]),
        "format": lambda value: "/".join(f"{x:.1%}" for x in value),
    },
    "Gross margin (FY2026E--FY2030E)": {
        "unit": "% of revenue",
        "inputs": {"Lower": 0.670, "Base": BASE["gross_margin"], "Higher": 0.690},
        "run": lambda value: model.project(revenue_growth_path=BASE["revenue_growth"], gross_margin_assumption=value),
        "format": lambda value: f"{value:.1%}",
    },
}

def result(forecast):
    model.assert_checks(forecast)
    _, _, per_share = model.value_equity(forecast)
    final = forecast[-1]
    return {"ebit": final["ebit"], "fcfe": final["fcfe"], "per_share": per_share}

def main():
    before = result(model.project(revenue_growth_path=BASE["revenue_growth"], gross_margin_assumption=BASE["gross_margin"]))
    print("Lab 11 — JNJ one-at-a-time sensitivity | USD millions except $/share")
    print("Cash-flow metric: FCFE. All cases must pass annual balance and minimum-cash checks.")
    for driver, definition in CASES.items():
        runs = {label: result(definition["run"](deepcopy(value))) for label, value in definition["inputs"].items()}
        base = runs["Base"]
        print(f"\n{driver} | input unit: {definition['unit']}")
        print(f"{'Case':<8} {'Actual input':<35} {'FY2030 EBIT':>14} {'Change':>12} {'FY2030 FCFE':>14} {'Change':>12} {'Value/share':>13} {'Change':>12}")
        for label, value in definition["inputs"].items():
            item = runs[label]
            print(f"{label:<8} {definition['format'](value):<35} {item['ebit']:>14,.1f} {item['ebit']-base['ebit']:>+12,.1f} {item['fcfe']:>14,.1f} {item['fcfe']-base['fcfe']:>+12,.1f} ${item['per_share']:>11,.2f} {item['per_share']-base['per_share']:>+11,.2f}")
        print(f"Span: EBIT {max(x['ebit'] for x in runs.values())-min(x['ebit'] for x in runs.values()):,.1f}m; FCFE {max(x['fcfe'] for x in runs.values())-min(x['fcfe'] for x in runs.values()):,.1f}m; value/share ${max(x['per_share'] for x in runs.values())-min(x['per_share'] for x in runs.values()):,.2f}.")
    after = result(model.project(revenue_growth_path=BASE["revenue_growth"], gross_margin_assumption=BASE["gross_margin"]))
    passed = all(abs(before[key]-after[key]) <= 0.0001 for key in before)
    print(f"\nRestored-base check: {'PASS' if passed else 'FAIL'} | FY2030 EBIT {before['ebit']:,.1f}/{after['ebit']:,.1f}; FCFE {before['fcfe']:,.1f}/{after['fcfe']:,.1f}; value/share ${before['per_share']:,.2f}/${after['per_share']:,.2f}.")

if __name__ == "__main__":
    main()
