# ABG Five-Year Pro Forma and Equity Valuation

The executable model is [`proforma.py`](proforma.py). It uses only the Python standard library and projects FY2026E through FY2030E in USD millions.

## Run

```powershell
python proforma.py
```

## Assumptions

| Assumption | Value |
| --- | ---: |
| Organic revenue growth | 1.8% |
| Gross margin | 17.05% |
| SG&A / gross profit (2026–2030) | 66.5%, 65.5%, 64.5%, 64.5%, 64.5% |
| Depreciation / opening PP&E | 82.4 / 3,070.4 |
| Non-cash impairment | 120.0 per year |
| Capital spending | 250.0 per year |
| Tax rate | 25.5% |
| Other working capital | 0.8% of revenue change |
| Debt repayment / buyback | 150.0 / 150.0 per year |
| Cost of equity / terminal growth | 10.0% / 2.5% |
| Shares outstanding | 17.951349 million |

## Verified outputs

| Line | FY2026E | FY2030E |
| --- | ---: | ---: |
| Revenue | 18,323.0 | 19,678.3 |
| Operating income | 844.2 | 971.4 |
| Net income | 413.6 | 527.5 |
| Free cash flow to equity | 211.4 | 342.3 |
| Cash, year end | 101.8 | 719.8 |
| Assets − liabilities − equity | 0.0 | 0.0 |

The model calculates an equity value of $5,237.34 million, a 79.8% post-2030 value share, and a value per share of **$291.75**.

## Integrity check

`assert_balanced` tests every forecast year before the valuation. Changing FY2026E cash from its calculated 101.8 to the opening 40.4 causes the model to refuse the forecast with:

```text
AssertionError: FY2026E does not balance: gap -61.4
```
