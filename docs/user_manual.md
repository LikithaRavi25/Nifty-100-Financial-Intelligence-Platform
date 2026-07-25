# User Manual

## Getting Started

1. Start FastAPI

```bash
uvicorn src.api.main:app --reload
```

2. Start Streamlit

```bash
streamlit run src/dashboard/app.py
```

3. Open

```
http://localhost:8501
```

## Dashboard Navigation

- Home
- Company Profile
- Stock Screener
- Peer Comparison
- Trend Analysis
- Sector Analysis
- Capital Allocation
- Annual Reports

## Searching Companies

Use either:

- Company Name
- NSE Ticker


## Applying Screener Filters

Available filters include:

- ROE
- Debt-to-Equity
- PE Ratio
- Sales Growth
- Profit Growth

## Downloading PDF Reports

1. Open Company Profile
2. Click Generate Tearsheet
3. Save the generated PDF

## Viewing Annual Reports

Navigate to the Annual Reports page and select a company to open its available reports.

## Common Issues

- API not running
- Database missing
- Dashboard not loading
- PDF not generated

Refer to the Analyst Guide troubleshooting section for detailed solutions.