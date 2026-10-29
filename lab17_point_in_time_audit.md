# Lab 17 — Point-in-Time Audit

Run the app from this folder:

```powershell
& .\.venv\Scripts\python.exe -m streamlit run asof_app.py
```

The **Compare selected series** chart overlays the selected IDs. Its sidebar controls switch between today's values and the chosen ALFRED vintage, and can index each line to 100 when series have different units. The individual charts below retain each series' current values.

Each line chart has a candlestick view beside it. These candles summarize the first, highest, lowest, and last *reported series values* within a period; they are not market trading OHLC prices. Daily and weekly series use monthly candles; monthly series use quarterly candles.

## Known-answer check, downloaded 2026-10-29

The app reads live FRED and ALFRED CSV files. For the 2026-10-05 vintage, it returned BAA September 2026 **6.47**, FEDFUNDS September 2026 **3.75**, DGS10 2026-10-02 **5.28**, and MORTGAGE30US 2026-10-01 **7.28**. For the 2025-01-15 PAYEMS vintage, December 2024 was **159,536** thousand persons; the current download says **158,316**, with **381** same-date values revised across the full common history.

## Data card — BAA (provisional choice)

- **Source:** [Moody's Seasoned Baa Corporate Bond Yield, FRED](https://fred.stlouisfed.org/series/BAA), a Moody's series distributed through the Federal Reserve Bank of St. Louis. [ALFRED](https://alfred.stlouisfed.org/series?seid=BAA) supplies historical vintages.
- **Measure and units:** Monthly average yield on seasoned Baa-rated corporate bonds, percent per annum, not seasonally adjusted. The FRED notes say the underlying bonds have maturities of 20 years and above. This is a yield level, not a credit spread.
- **Publication lag:** The September 2026 observation was posted 2026-10-01 according to the FRED page, one calendar day after the measured month ended. On 2026-09-30, ALFRED's last nonmissing observation was August 2026 at 6.32; the September 2026 value of 6.47 was unavailable. Actual release timing can vary by month, so a backtest must use the vintage for each decision date.
- **Revisions:** The 2026-09-30 vintage and today's download have zero differing values on their shared observation dates. This is evidence for this comparison, not a guarantee that BAA never changes.
- **Download date:** 2026-10-29.
- **Three values checked against the FRED page:** July 2026 **6.19**, August 2026 **6.32**, September 2026 **6.47** percent.

The observation date identifies the month measured; the ALFRED vintage date limits what was available for a decision. `download_as_known` requests that vintage and excludes observations after that date. The table compares matching observation dates to count revisions. Saying only “cleaned the data” omits the source, units, publication lag, revisions, and vintage rule needed to judge whether a backtest leaks future information.

**Provisional Project 2 call: quarantine BAA.** It is relevant to the investment-grade bond sleeve, but a fixed one-month lag or today's full history is not enough to prove every trading-day value was available. Admit it only when the backtest fetches the ALFRED vintage for each decision date and records the publication timing and any revisions; reject it if that rule cannot be implemented.


