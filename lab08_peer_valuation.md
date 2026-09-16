# Lab 08 — Johnson & Johnson Deal Evidence and Valuation Triangulation

**Target:** Johnson & Johnson (NYSE: JNJ)  
**Comparison / Week 3 valuation date:** September 10, 2026  
**Currency and valuation object:** USD per common share; GAAP diluted EPS and closing share prices.

## Define / discover

JNJ earns revenue by selling prescription medicines through Innovative Medicine and medical technologies through MedTech. Its 2025 Form 10-K describes the two segments and their product-based sales model in **Item 1, Business**. [JNJ FY2025 10-K, Item 1](https://www.sec.gov/Archives/edgar/data/200406/000020040626000016/jnj-20251228.htm). The target's FY2025 reported diluted EPS was **$11.03**, positive, and the January 21, 2026 results release was public well before the comparison date. The release separately identifies $10.79 adjusted EPS; I do **not** substitute it because the lab calculation uses reported annual EPS. [JNJ FY2025 results release, GAAP table](https://investor.jnj.com/investor-news/news-details/2026/Johnson--Johnson-reports-Q4-and-Full-Year-2025-results/default.aspx).

**Focused research question:** Which listed U.S.-dollar healthcare companies earn material revenue from both global medical products and pharmaceuticals/therapeutics, report positive FY2025 GAAP diluted EPS, and have product/regulatory economics comparable enough to be a qualified—not identical—P/E reference for JNJ?

## Initial peer policy — written before selection

I will look for listed operating companies with global healthcare-product economics: regulated product portfolios, recurring sales through hospitals/clinicians/distributors, material medical-device/diagnostic exposure **or** prescription-medicine exposure, and positive annual reported diluted EPS. I will qualify rather than treat as exact peers when one major JNJ segment is missing. I will exclude companies whose economics are primarily insurance, providers, distributors, contract research/manufacturing, consumer products, or pre-profit biotech. I will also keep reported and adjusted EPS separate, use only annual results already public by September 10, 2026, and use USD closing prices on that same date.

**Rejection evidence I would look for:** a candidate is primarily a payer/provider/distributor, has no substantial regulated product business, reports nonpositive annual GAAP diluted EPS, or requires a different currency/share basis. No policy revision was made after reviewing the two candidates.

## Candidate investigation and decisions

| Candidate | Decision | Source opened / locator | Business-fit judgment and important difference | FY2025 reported diluted EPS / public date |
|---|---|---|---|---|
| Abbott Laboratories (NYSE: ABT) | **Qualify / use** | [FY2025 10-K, Item 1 and Item 7](https://www.sec.gov/Archives/edgar/data/1800/000162828026010185/abt-20251231.htm): products are medical devices, diagnostics, nutritionals, and branded generic pharmaceuticals; Item 7 describes those revenue streams. | Its devices, diagnostics, pharmaceuticals, and global product sales make it a defensible diversified healthcare reference. It differs materially because its pharmaceutical business is branded generics and it has Nutritionals; it does not mirror JNJ's innovative-medicine portfolio. | **$3.72** GAAP diluted EPS, fiscal year ended Dec. 31, 2025; reported Jan. 22, 2026 in [Abbott FY2025 results release](https://abbott.mediaroom.com/2026-01-22-Abbott-Reports-Fourth-Quarter-and-Full-Year-2025-Results-Issues-2026-Financial-Outlook). |
| Merck & Co. (NYSE: MRK) | **Qualify / use** | [FY2025 10-K, Item 1 Business](https://www.sec.gov/Archives/edgar/data/310158/000031015826000063/mrk-20251231.htm) describes human-health pharmaceutical products and Animal Health. | It shares global, regulated prescription-drug and vaccine economics with JNJ Innovative Medicine. It lacks JNJ's MedTech segment and includes Animal Health, so its earnings mix and patent-concentration risk differ; it is qualified, not a close match. | **$7.28** GAAP EPS assuming dilution, fiscal year ended Dec. 31, 2025; announced Feb. 3, 2026 in [Merck FY2025 earnings announcement](https://www.merck.com/wp-content/uploads/sites/124/2026/02/4Q25-Merck-Earnings-Announcement.pdf). |

Both candidates meet the positive-EPS and USD-basis screen. I retain their differences instead of excluding them because the policy expressly permits a qualified company missing one major JNJ segment. A pure insurer, provider, distributor, CRO/CMO, consumer company, or loss-making biotech would be excluded under the same policy.

## Frozen inputs and calculation

The following are unadjusted closing prices on the exact same trading date, September 10, 2026. The price locators are historical-price tables: [JNJ](https://stockanalysis.com/stocks/jnj/history/), [ABT](https://chartexchange.com/symbol/nyse-abt/historical/), and [MRK](https://www.financecharts.com/stocks/MRK/summary/price). FY2025 results were all public before the valuation date. No quarterly or adjusted EPS is used.

| Company | Role | Price, Sep. 10, 2026 | Annual reported diluted EPS | Fiscal year-end | Earnings publication date | P/E |
|---|---|---:|---:|---|---|---:|
| JNJ | Target | $266.35 | $11.03 | Dec. 28, 2025 | Jan. 21, 2026 | — |
| ABT | Qualified peer | $103.36 | $3.72 | Dec. 31, 2025 | Jan. 22, 2026 | 27.784946x |
| MRK | Qualified peer | $144.71 | $7.28 | Dec. 31, 2025 | Feb. 3, 2026 | 19.877747x |

Run the saved calculation:

```powershell
python .\jnj_pe_valuation.py
```

The two-peer median is **23.831347x**. Applying the peer minimum, median, and maximum P/E to JNJ's $11.03 reported diluted EPS gives a **$219.25–$306.47** implied range, with **$262.86** at the median. This is a market-based reference range, not an instruction to average it with a DCF.

## Validation

Hand check for admitted peer MRK: **$144.71 / $7.28 = 19.877747x**. This matches the calculator (rounding only).

I predicted that removing ABT would lower the median-implied result because ABT has the higher P/E (27.784946x). The calculator confirms that removing ABT leaves MRK alone and changes the result to a **$219.25 reference estimate**, **-$43.61** from the full-peer median. Conversely, removing MRK leaves ABT and raises the reference estimate to **$306.47**, **+$43.61**. With just one peer remaining, that number is a reference, not a range.

## Evolve — DCF comparison and skeptical review

| Method | JNJ result and date | Main assumption or limitation |
|---|---|---|
| Week 3 DCF | **$320.59/share**, model date Sep. 10, 2026 | Forecast FCFF growth, 5.88% WACC, 3% terminal growth, and the cash/debt/share inputs. |
| Peer P/E | **$219.25–$306.47**, $262.86 median reference, Sep. 10, 2026 | Only two qualified (not exact) peers and annual reported EPS; JNJ reported EPS includes a material talc-reserve reversal. |

**Provisional call sent for challenge:** Watch-defer. The DCF exceeds the September 10 price ($266.35), while the peer-median reference is slightly below it and even the high peer reference remains below the DCF. The methods should not be averaged: they answer through different assumptions.

**What could most easily change my mind:** a source-supported normalization of the JNJ talc-reserve reversal, evidence that its future innovative-medicine and MedTech mix deserves a durable premium to ABT/MRK, or new results changing the STELARA replacement trajectory.

**Skeptical-colleague criticism:** *The weakest supported assumption is treating JNJ's FY2025 reported $11.03 EPS as recurring when the results materials say it includes the talc-reserve reversal; this can mechanically depress JNJ's implied P/E and inflate the price produced from peer multiples. Are you willing to defend a reported-EPS peer range when the target and peer earnings may carry very different one-time items?*

**Judgment: accept.** The criticism is supported by JNJ's FY2025 results materials, and it is a real comparability limitation. I retain the reported-EPS result because the stated lab basis requires it and I do not manufacture an adjusted peer range. It reduces confidence in the P/E range rather than invalidating the sourced arithmetic.

## Reflection and conditional conclusion

I chose ABT for its diversified medical-product portfolio and MRK for global prescription-drug/vaccine economics; each is explicitly only a qualified peer because neither duplicates JNJ's Innovative Medicine plus MedTech mix. The comparison adds a market view of how investors price two related earnings streams, while the DCF adds an explicit cash-flow forecast. They differ because of peer business mix and the target's reported EPS distortion from the talc-reserve reversal, as well as the DCF's forecast, WACC, and terminal-growth assumptions.

**Decision: watch-defer; do not initiate on this evidence alone.** I can defend the reported-EPS peer range of **$219.25–$306.47** and the Week 3 DCF value of **$320.59**, but not a single blended fair value. I would reconsider toward initiation if post-valuation-date evidence supports a recurring-earnings normalization, credible growth offsets STELARA erosion, and JNJ's price remains below a source-supported value range. I would defer longer if those offsets disappoint, litigation effects recur, or peer/target earnings prove less comparable. My answer to the skeptical question is yes: I can defend the range only as a transparent *reported-EPS* cross-check, not as a recurring-earnings valuation or stand-alone buy signal.
