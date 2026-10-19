# Lab 12 - Johnson & Johnson valuation reflection

> Historical reflection discussing an earlier FCFE model. It is retained as weekly-work evidence, not as the final valuation basis. See `docs/model-version-transition.md`.

**Company:** Johnson & Johnson (NYSE: JNJ)  
**Purpose:** Explain the company choice, valuation conclusion, key assumptions, competition, evidence base, model mechanics, and next research steps.

## Why I chose Johnson & Johnson

I chose Johnson & Johnson because it is a diversified healthcare company with both Innovative Medicine and MedTech businesses, substantial cash generation, and a clear valuation question. The central issue is whether growth from products such as DARZALEX, CARVYKTI, TREMFYA, and CAPLYTA, together with MedTech growth, can replace STELARA revenue lost to biosimilar competition.

## How JNJ earns money and the evidence base

JNJ earns revenue by selling regulated healthcare products worldwide. **Innovative Medicine** sells prescription medicines in areas including oncology, immunology, neuroscience, cardiovascular/metabolism, pulmonary hypertension, and infectious disease. **MedTech** sells medical devices and related technologies used by hospitals and clinicians, including surgery, orthopaedics, vision, cardiovascular, and other interventional-care products. Innovative Medicine generated **$60.4 billion** of FY2025 sales. Unless stated otherwise, financial figures are USD millions; per-share values are USD per common share. FY2025 ended December 28, 2025.

The main primary source is JNJ's [FY2025 Form 10-K, filed February 11, 2026](https://www.sec.gov/Archives/edgar/data/200406/000020040626000016/jnj-20251228.htm): Item 1 explains the businesses, Item 7/MD&A gives growth and product trends, and the financial statements provide historical inputs. I also used the [FY2025 results release, January 21, 2026](https://investor.jnj.com/investor-news/news-details/2026/Johnson--Johnson-reports-Q4-and-Full-Year-2025-results/default.aspx), the [Q2 2026 results release, July 15, 2026](https://www.jnj.com/media-center/press-releases/johnson-johnson-reports-q2-2026-results-raises-2026-outlook), and historical-price tables. The DCF used 2,429.4 million FY2025 diluted weighted-average shares and a saved market price of **$267.08 per share at the September 9, 2026 close**.

## How I moved from company choice to valuation conclusion

I began with JNJ's historical financial statements, product sales, cash flow, debt, and market price. FY2025 revenue was $94.2 billion and grew 6.0%, but I did not extend that headline rate mechanically. STELARA erosion was a material headwind, while acquisitions also contributed to reported growth. I therefore used a declining five-year revenue-growth forecast, modeled margins, reinvestment, taxes, debt, and cash flows, and valued the company with FCFE/DCF. I then cross-checked the result with qualified peer P/E references from Abbott and Merck.

The methods did not give one identical result. The earlier DCF was about $320.59 per share; the peer P/E reference range was $219.25-$306.47, with a $262.86 median; and the later conservative FCFE model produced $138.28 per share versus a cited market price near $269.17. Because the estimates differed and the outcome depends on uncertain revenue replacement, my conclusion was **watch/defer**, rather than a buy or sell recommendation. JNJ appears to be a high-quality business, but the evidence did not establish a sufficiently reliable margin of safety.

## Pro-forma mechanics and accounting check

The five-year pro forma began with FY2025 revenue of $94,193 million and FY2023-FY2025 historical margins, working-capital measures, capex, taxes, debt, and equity from the 10-K. I converted history into assumptions rather than assuming the past would repeat: revenue growth was 5.0%, 4.0%, 4.0%, 3.5%, and 3.0%; gross margin was 68.0%; SG&A was 37.0% of gross profit; R&D was 15.5% of revenue; capex was 5.0% of revenue; and the tax rate was 18.0%. The below-history growth path reflects the disclosed STELARA decline and acquisition contribution to FY2025 growth.

The model links the income statement, balance sheet, and cash flow statement: revenue drives gross profit, operating expenses, inventory, capex, and working capital; those flows determine FCFE and cash. Each forecast year passed the linked-statement accounting check **assets - liabilities - equity = 0.0** within display rounding. Cash also stayed above the $10.0 billion minimum-cash floor without a revolver draw.

## DCF valuation inputs and enterprise-to-equity bridge

The saved FCFF DCF is dated **September 10, 2026** and is an **enterprise-value** valuation before the cash/debt bridge. Starting FCFF was $21,325.1 million, calculated as operating cash flow of $24,530 million plus after-tax interest of $1,627.1 million less capex of $4,832 million. Explicit FCFF growth was 6%, 5%, 4%, 3%, and 3%; WACC was **5.88%**; and terminal growth was **3.0%**.

To calculate equity value, I added cash and cash equivalents of **$19,709 million** and subtracted total debt of **$47,933 million** from enterprise value. Dividing the resulting equity value by 2,429.4 million diluted shares produced the DCF result of **$320.59 per share**. This DCF is a conditional estimate, not proof that the stock was mispriced.

## Market price and reverse DCF

At the saved **$267.08 per-share** market close on September 9, 2026, the reverse DCF solved for a **-3.8032 percentage-point uniform shift** to the explicit FCFF-growth path. The market-price-consistent growth path is therefore approximately 2.20%, 1.20%, 0.20%, -0.80%, and -0.80% for Years 1-5.

The reverse DCF held starting FCFF, WACC, terminal growth, cash, debt, and diluted shares fixed. It is useful because it makes the growth expectation embedded in the price visible. Its limitation is that it is only one fixed-input combination consistent with the price; it does not prove that the market forecast is correct or that the stock is misvalued.

## Assumptions that drive the conclusion

The main operating assumption is **revenue growth**, especially the speed of STELARA erosion and the ability of JNJ's newer products and MedTech franchises to replace it. In the FCFE sensitivity analysis, lowering every annual revenue-growth rate by one percentage point reduced value to $133.62 per share; raising each rate by one point increased it to $143.06. This $9.44 per-share range was the largest tested driver, slightly greater than the $8.59 range from changing gross margin between 67% and 69%.

The sensitivity chain is: **revenue growth -> forecast revenue and gross profit/EBIT -> working capital, capex, and after-tax FCFE -> discounted equity value -> value per share.** Revenue growth ranked above gross margin only across the selected test ranges: five annual revenue changes compound, while the margin test was a one-point range. The ranking is not a probability forecast and does not establish that revenue growth is always the most important real-world risk.

The DCF is also sensitive to the required return/WACC and terminal growth because a large portion of value reflects cash flows beyond the explicit forecast period. These inputs are estimates, not facts.

## How other pharmaceutical companies relate to revenue growth

Other pharmaceutical companies matter because they compete for patients, physicians, payer budgets, and treatment categories. They can affect JNJ's market share, product prices, adoption rates, and the pace at which older products lose sales.

Moderna is a secondary competitive consideration for JNJ because its focus is vaccines and mRNA technology. More direct competitive influences on JNJ's forecast include:

- biosimilar manufacturers competing with STELARA;
- oncology and immunology competitors, including Merck, Pfizer, AbbVie, Bristol Myers Squibb, Eli Lilly, and Novartis;
- new clinical-trial results, regulatory approvals, or product launches that alter treatment choices; and
- insurer and government reimbursement decisions that increase price pressure.

Therefore, the revenue-growth forecast depends on JNJ's execution and competitors' ability to gain share or reduce pricing power. The most direct question is whether JNJ's replacement-product sales can grow faster than STELARA declines.

## Evidence that could change my mind

I would become more constructive if product-level results consistently show that new products and MedTech growth more than offset STELARA erosion, margins hold or improve, and a normalized earnings analysis supports recurring cash-flow strength. Clearer talc-litigation resolution and cash-payment timing, successful returns on acquisitions such as Intra-Cellular and Shockwave, or a supportable lower cost of equity could also improve the valuation case.

I would remain cautious if replacement products disappoint, biosimilar or competitor pressure increases, pricing deteriorates, litigation costs recur, or higher risk requires a higher discount rate. A lower market price relative to a source-supported valuation range would also be necessary before treating the analysis as an initiation case.

## How my view evolved and next research priority

I initially selected JNJ because its diversified businesses, oncology pipeline, and cash generation appeared attractive. After modeling the STELARA headwind, legal uncertainty, acquisition-funded debt, and different valuation results, my view became more cautious: JNJ remains a business worth following, but I cannot support an initiation solely from the current evidence. My next research priority is the **product-level revenue bridge replacing STELARA**: quarterly STELARA erosion versus growth in DARZALEX, CARVYKTI, TREMFYA, CAPLYTA, and MedTech.

## Partner-review record

**Question received and checked (Alyson Foster):** Alyson asked whether JNJ's reported FY2025 diluted EPS should be treated as recurring. I checked JNJ's FY2025 results materials and accepted that this is a genuine comparability limitation in the Abbott/Merck P/E cross-check. I retained the reported-EPS range because it was the required assignment basis, but labeled it a reported-EPS reference rather than a recurring-earnings valuation.

**Feedback I gave and follow-up:** My partner's McDonald's sensitivity analysis identified revenue growth as its leading driver. I asked whether a shift toward healthier food could weaken demand enough that the selected growth range did not capture the business risk. I checked that the partner stated the conclusion as conditional on the selected ranges. I will keep the principle that sensitivities need a business-risk explanation, revise my own work by making peer-EPS comparability explicit, and investigate JNJ's product-level STELARA replacement evidence next.
