"""Lab 12 — Pro-Forma Sensitivity: Johnson & Johnson presentation answers.

Run from this folder:
    python "Lab 12 — Pro-Forma Sensitivity.py"

The accompanying Markdown file contains the complete presentation route,
sources, and live Nike partner-review blanks.
"""


def show(title, answer):
    print(f"{title}\n{answer}\n")


def main():
    print("LAB 12 — PRO-FORMA SENSITIVITY\nJohnson & Johnson (NYSE: JNJ) | Partner: Nike\n")
    show("CONCLUSION", "Watch/defer. JNJ is a high-quality healthcare company, but STELARA replacement, legal uncertainty, and divergent valuation outputs leave insufficiently reliable margin of safety.")
    show("TARGET SELECTION AND EVIDENCE", "JNJ combines Innovative Medicine and MedTech and has a clear question: can newer products and MedTech replace STELARA revenue lost to biosimilars? FY2025 revenue was $94,193m and Innovative Medicine sales were $60.4bn. The core primary source is the FY2025 Form 10-K.")
    show("PRO-FORMA", "Revenue growth: 5.0%, 4.0%, 4.0%, 3.5%, 3.0%. Gross margin: 68.0%; SG&A: 37.0% of gross profit; R&D: 15.5% of revenue; capex: 5.0% of revenue; tax: 18.0%. Forecast years passed assets - liabilities - equity = 0.0 within display rounding, and cash exceeded the $10bn floor.")
    show("VALUATION", "FCFF DCF, dated Sep. 10, 2026: starting FCFF $21,325.1m; WACC 5.88%; terminal growth 3.0%; cash $19,709m; debt $47,933m; shares 2,429.4m; value $320.59/share. Qualified-peer P/E reference: $219.25-$306.47/share, $262.86 median. The methods should not be averaged.")
    show("REVERSE DCF", "At the Sep. 9, 2026 saved price of $267.08/share, the price-consistent explicit FCFF growth path is about 2.20%, 1.20%, 0.20%, -0.80%, and -0.80%, holding starting FCFF, WACC, terminal growth, cash, debt, and shares fixed.")
    show("SENSITIVITY", "FCFE base value is $138.28/share. Revenue growth at -/+1 percentage point each year gives $133.62-$143.06, a $9.44 span; 67%-69% gross margin gives an $8.59 span. Chain: revenue growth -> revenue/gross profit/EBIT -> working capital and capex -> FCFE -> equity value/share. The ranking is conditional on the chosen ranges, not a probability forecast.")
    show("WHAT COULD CHANGE MY MIND", "I would investigate whether quarterly growth in DARZALEX, CARVYKTI, TREMFYA, CAPLYTA, and MedTech consistently offsets STELARA erosion. Better replacement growth, durable margins, normalized cash flow, and clearer litigation obligations would improve the case; weaker replacement growth, pricing pressure, litigation, or a higher required return would reinforce defer.")
    show("NIKE REVIEW", "Ask Nike to open a primary source supporting a key demand, revenue, or margin claim; trace one input through its statements and valuation; and explain whether the sensitivity-driver ranking depends on its selected range. Record only the evidence and feedback actually checked in the Markdown file.")


if __name__ == "__main__":
    main()
