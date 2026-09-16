# Lab 08 — Johnson & Johnson Peer P/E Calculator Run

Run the saved Johnson & Johnson calculator from the course folder:

```powershell
python .\jnj_pe_valuation.py
```

Verified output:

```text
Target: Johnson & Johnson (JNJ)
Basis: September 10, 2026 closing prices; FY2025 reported diluted GAAP EPS.

Peer P/E multiples
Abbott Laboratories (ABT): 27.784946x
Merck & Co. (MRK): 19.877747x

Peer median P/E: 23.831347x
Target implied price at minimum P/E: $219.25 (19.877747x)
Target implied price at median P/E: $262.86 (23.831347x)
Target implied price at maximum P/E: $306.47 (27.784946x)

Leave-one-peer-out analysis
Remove ABT: reference estimate $219.25; change from full-peer median $-43.61.
Remove MRK: reference estimate $306.47; change from full-peer median $43.61.
```

## Target, date, and peer policy

**Target:** Johnson & Johnson (NYSE: JNJ)  
**Comparison date:** September 10, 2026  
**Basis:** USD per common share, same-date closing prices, and FY2025 annual
reported diluted GAAP EPS.

JNJ earns revenue by selling prescription medicines through Innovative Medicine
and medical technologies through MedTech. Its FY2025 reported diluted EPS was
positive at $11.03. [JNJ FY2025 Form 10-K, Item 1 Business](https://www.sec.gov/Archives/edgar/data/200406/000020040626000016/jnj-20251228.htm)
and [FY2025 results release](https://investor.jnj.com/investor-news/news-details/2026/Johnson--Johnson-reports-Q4-and-Full-Year-2025-results/default.aspx).

**Research question:** Which global healthcare-product companies have
regulated medical-product or prescription-medicine economics, positive annual
reported EPS, and sufficiently comparable business models to be a qualified
P/E reference for JNJ?

**Policy written before selection:** I will consider listed operating companies
with regulated product portfolios and meaningful medical-device/diagnostic or
prescription-medicine revenue. A candidate is qualified, rather than identical,
when it lacks a major JNJ segment. I exclude insurance, providers,
distributors, CRO/CMOs, consumer companies, pre-profit biotech, nonpositive
annual EPS, and incompatible currency/share bases. Reported and adjusted EPS
remain separate.

## Candidate decisions and evidence

| Candidate | Decision | Business evidence and judgment | FY2025 reported diluted EPS |
|---|---|---|---:|
| Abbott Laboratories (ABT) | Qualify / use | [FY2025 10-K, Item 1 and Item 7](https://www.sec.gov/Archives/edgar/data/1800/000162828026010185/abt-20251231.htm) describes medical devices, diagnostics, nutritionals, and branded generic pharmaceuticals. Its global product portfolio makes it a qualified reference; branded generics and Nutritionals differ materially from JNJ's Innovative Medicine mix. | $3.72; fiscal year ended Dec. 31, 2025; published Jan. 22, 2026 in [FY2025 results](https://abbott.mediaroom.com/2026-01-22-Abbott-Reports-Fourth-Quarter-and-Full-Year-2025-Results-Issues-2026-Financial-Outlook). |
| Merck & Co. (MRK) | Qualify / use | [FY2025 10-K, Item 1 Business](https://www.sec.gov/Archives/edgar/data/310158/000031015826000063/mrk-20251231.htm) describes global human-health pharmaceutical products and Animal Health. It shares JNJ's prescription-drug and vaccine economics, but lacks MedTech and has Animal Health exposure. | $7.28; fiscal year ended Dec. 31, 2025; published Feb. 3, 2026 in [FY2025 earnings announcement](https://www.merck.com/wp-content/uploads/sites/124/2026/02/4Q25-Merck-Earnings-Announcement.pdf). |

I retained both as qualified peers because the policy permits a meaningful
segment difference but does not treat either company as an exact JNJ match.

## Inputs, result, and validation

Historical-price sources for the September 10, 2026 closes are
[JNJ](https://stockanalysis.com/stocks/jnj/history/),
[ABT](https://chartexchange.com/symbol/nyse-abt/historical/), and
[MRK](https://www.financecharts.com/stocks/MRK/summary/price). All FY2025
annual releases were public before the comparison date.

| Company | Role | Price | GAAP diluted EPS | Fiscal year-end | Publication date |
|---|---|---:|---:|---|---|
| JNJ | Target | $266.35 | $11.03 | Dec. 28, 2025 | Jan. 21, 2026 |
| ABT | Qualified peer | $103.36 | $3.72 | Dec. 31, 2025 | Jan. 22, 2026 |
| MRK | Qualified peer | $144.71 | $7.28 | Dec. 31, 2025 | Feb. 3, 2026 |

The peer P/E range is **19.877747x–27.784946x**, producing an implied JNJ
range of **$219.25–$306.47** and a **$262.86** median reference.

Manual check: MRK P/E = $144.71 / $7.28 = **19.877747x**, matching the
calculator. I predicted that removing ABT would lower the estimate because it
has the higher P/E. The output confirms that removing ABT leaves the $219.25
MRK reference, down $43.61 from the two-peer median. Removing MRK leaves the
$306.47 ABT reference, up $43.61. One peer is a reference, not a range.

## DCF comparison, challenge, and conclusion

| Method | JNJ result and date | Main assumption or limitation |
|---|---|---|
| Week 3 DCF | $320.59 per share, Sep. 10, 2026 | FCFF forecast, 5.88% WACC, 3% terminal growth, cash/debt/share assumptions |
| Peer P/E | $219.25–$306.47; $262.86 median reference, Sep. 10, 2026 | Two qualified rather than exact peers; reported EPS basis |

**Skeptical criticism:** The weakest assumption is treating JNJ's $11.03
reported FY2025 EPS as recurring, because the results materials identify a
material talc-reserve reversal. This can distort a P/E-based value. Would the
reported-EPS range remain defensible if target and peer one-time items differ?

**Judgment: accept.** The criticism is source-supported. I retain the reported
EPS calculation because it is the stated consistent basis, but do not present
it as a recurring-earnings valuation or create an unsupported adjusted range.

**Decision: watch-defer; do not initiate on this evidence alone.** The DCF is
higher than the $266.35 comparison-date price, while the peer median reference
is slightly below it. I will not average the methods: the DCF depends on cash
flow, discount rate, and terminal growth; the peer comparison depends on peer
economics and reported earnings. I would reconsider if evidence supports a
recurring-earnings normalization, credible growth offsets STELARA erosion, and
the market price remains below a source-supported valuation range. Evidence of
weaker replacement growth, recurring litigation effects, or poorer peer
comparability would support continued deferral.
