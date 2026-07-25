# Sprint 2 Retrospective

## Goals Achieved

- Built a complete financial ratio engine.
- Implemented profitability, leverage, efficiency and cash flow KPIs.
- Generated CAGR metrics.
- Created capital allocation classification.
- Populated the financial_ratios SQLite table.
- Added edge case logging for ROCE and ROE.
- Added high leverage suppression for financial companies.
- Implemented KPI unit tests.
- Successfully passed all unit tests.

## Key Formula Decisions

- ROE = Net Profit / (Equity Capital + Reserves)
- ROCE = EBIT / Capital Employed
- Debt to Equity = Borrowings / Equity
- Interest Coverage = EBIT / Interest
- Free Cash Flow = CFO + Investing Activity
- Asset Turnover = Sales / Total Assets

## Edge Cases Handled

- Zero sales
- Zero equity
- Zero interest
- Negative cash flow
- Financial sector leverage
- CAGR turnaround
- Zero base CAGR
- Missing values