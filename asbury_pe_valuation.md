# Asbury Automotive: Comparable P/E Valuation

## Why use another company's price?

Comparable-company valuation uses how the market prices similar businesses as a
cross-check on an intrinsic valuation such as discounted cash flow (DCF). A
P/E comparison asks: **what would Asbury's share be worth at comparable
companies' P/E multiples?** It is a market benchmark, not proof of fair value.

## What P/E measures

\[
P/E = \frac{\text{price per share}}{\text{diluted earnings per share}}
\]

- **Price per share** is the market value of one common share.
- **Diluted EPS** is GAAP earnings attributable to common shareholders per
  diluted weighted-average share.
- A P/E of 10x means investors pay $10 of equity value for each $1 of annual
  earnings.

P/E makes different-sized companies comparable because it scales equity value
by earnings. It is equivalent in concept to market capitalization divided by
net income. DCF estimates value from the company's expected cash flows; P/E
shows how the market values similar companies' earnings. Using both provides a
useful cross-check.

## When P/E is useful and when it can mislead

P/E is most useful for profitable companies with comparable, recurring
earnings. The companies should have compatible fiscal periods, valuation dates,
GAAP/diluted-EPS definitions, business mix, geography, accounting, capital
structure, risk, and growth prospects.

P/E is not meaningful for zero or negative EPS. One-time gains can make EPS
temporarily high and P/E artificially low; unusual losses can do the reverse.
A lower P/E is therefore not automatically a better investment: it may reflect
slower expected growth, higher risk or leverage, weaker earnings quality, or a
less favorable business mix.

## Case peer policy

The relevant business is not merely "automotive." A vehicle manufacturer,
online used-vehicle seller, lender, or parts maker has a different economic
model. The appropriate comparison is a franchised vehicle retailer that also
earns from parts/service and F&I. Parts and service provide recurring
after-sales work and factory parts; vehicle retail is more sensitive to unit
sales, inventory, incentives, and vehicle margins.

| Company | Decision | Business rationale |
|---|---|---|
| AutoNation (AN) | Use | A close U.S. franchised-dealership comparison, with new/used vehicles, parts and service, and F&I—the same core streams as Asbury. Its smaller non-franchised operations should still be kept in mind. |
| Group 1 Automotive (GPI) | Qualify, but retain | It is also a franchised dealer and parts/service operator, so it is economically relevant. Its U.K. operations and different franchise-law/agency-model exposure make it less directly comparable to U.S.-focused Asbury. |

Asbury's 2024 Form 10-K describes 198 new-vehicle franchises, parts and
service, collision repair, and F&I. AutoNation's filing describes 325 new
vehicle franchises and the same broad dealership revenue streams. Group 1's
filing similarly describes dealership operations and parts/service, while also
identifying its U.K. exposure.

Sources: [Asbury 2024 Form 10-K](https://www.sec.gov/Archives/edgar/data/1144980/000114498025000077/abg-20241231.htm),
[AutoNation 2024 Form 10-K](https://www.sec.gov/Archives/edgar/data/350698/000035069825000029/an-20241231.htm), and
[Group 1 2024 Form 10-K](https://www.sec.gov/Archives/edgar/data/1031203/000103120325000021/a2024_10kxasxfiledx2x14x25.pdf).

## Frozen case calculation

| Company | Role | Price at Dec. 31, 2024 | FY2024 GAAP diluted EPS | P/E |
|---|---|---:|---:|---:|
| Asbury Automotive (ABG) | Target | $243.03 | $21.50 | — |
| AutoNation (AN) | Peer | $169.84 | $16.92 | 10.037825x |
| Group 1 Automotive (GPI) | Qualified peer | $421.48 | $36.81 | 11.450149x |

The peer median P/E is **10.743987x**.

| ABG implied price | Calculation | Result |
|---|---|---:|
| Minimum peer P/E | $21.50 x 10.037825 | $215.81 |
| Median peer P/E | $21.50 x 10.743987 | $231.00 |
| Maximum peer P/E | $21.50 x 11.450149 | $246.18 |

One manually reproducible estimate is: $21.50 x 10.037825 = **$215.81**.
This is the ABG price implied by AutoNation's P/E.

## Leave-one-peer-out interpretation

GPI has the higher P/E. Removing it should lower ABG's implied value because
only AN's lower 10.037825x multiple remains. The result is a reference estimate
of **$215.81**, a **-$15.18** change from the full-peer median estimate of
$231.00. One valid peer produces no range because there is no minimum-to-
maximum spread across multiple peers.

The result is conditional, not a conclusion that ABG is fairly valued. It
depends on whether the peer earnings, risks, business mix, and growth outlooks
are comparable. The calculation deliberately does not bridge P/E through cash
or debt: P/E is an equity-value multiple.

## Run the calculation

```powershell
python .\asbury_pe_valuation.py
```
