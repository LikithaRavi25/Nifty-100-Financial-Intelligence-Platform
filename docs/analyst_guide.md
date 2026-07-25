# NIFTY 100 Financial Intelligence Platform

# Analyst Guide

Version: 1.0

Author: Likitha R

Data Analyst Intern | Blustock Fintech


## Overview

The NIFTY 100 Financial Intelligence Platform is a financial analytics application that enables analysts, investors, and students to explore financial statements, evaluate company performance, compare sectors, perform stock screening, and generate professional PDF tearsheets.

The platform consists of:

- FastAPI REST API
- Streamlit Dashboard
- SQLite Database
- ETL Pipeline
- Financial KPI Engine

This guide explains how to use every feature of the platform.

# Table of Contents

1. Introduction

2. Dashboard Overview

3. Company Profile

4. Financial Screener

5. Sector Analysis

6. Peer Comparison

7. Market Capitalization

8. Portfolio Statistics

9. PDF Tearsheet Generation

10. REST API Usage

11. Troubleshooting

12. Frequently Asked Questions

# 1. Introduction

The platform provides an integrated environment for analyzing NIFTY 100 companies using historical financial statements and calculated financial ratios.

The dashboard allows users to:

- Search companies
- Analyze historical financial statements
- Compare companies
- Evaluate sectors
- Filter companies using financial KPIs
- Download professional PDF reports

All information is powered by a FastAPI backend connected to a SQLite database.

# 2. Dashboard Overview

The Streamlit dashboard is the primary user interface.

Major modules include:

- Company Explorer
- Financial Screener
- Sector Dashboard
- Peer Comparison
- Market Valuation
- Portfolio Statistics
- PDF Tearsheet

Navigation is available from the left sidebar.

Each page retrieves live data through FastAPI endpoints.


The dashboard is the main interface of the application.

![Dashboard Home](../screenshots/home.png)

# 3. Company Profile

The Company Profile page provides company information, financial ratios, and historical performance.

![Company Profile](../screenshots/profile.png)

#  4.  Stock Screener

Screen companies using financial filters and investment presets.

![Stock Screener](../screenshots/screener.png)

# 5.  Peer Comparison

Compare companies with peers using radar charts and KPIs.

![Peer Comparison](../screenshots/peers.png)

# 6. Trend Analysis

Analyze 10-year financial trends with interactive charts.

![Trend Analysis](../screenshots/trends.png)

# 7. Sector Analysis

Visualize sector performance using bubble charts and KPI summaries.

![Sector Analysis](../screenshots/sectors.png)

# 8. Capital Allocation Map

Interactive treemap of capital allocation strategies.

![Capital Allocation](../screenshots/capital.png)

# 9. Annual Reports

Access company annual reports directly from BSE.

![Annual Reports](../screenshots/reports.png)

# 10. REST API Usage

The NIFTY 100 Financial Intelligence Platform exposes a RESTful API built using FastAPI. All dashboard pages retrieve data from these APIs, making it easy to integrate the platform with external applications.

## API Base URL

```
http://127.0.0.1:8000/api/v1
```

## Interactive API Documentation

FastAPI automatically generates interactive documentation.

### Swagger UI

```
http://127.0.0.1:8000/docs
```

### OpenAPI Specification

```
http://127.0.0.1:8000/openapi.json
```


## Health Endpoint

Checks whether the API server and database are functioning correctly.

### Request

```bash
curl http://127.0.0.1:8000/api/v1/health
```

### Example Response

```json
{
    "status": "ok",
    "version": "1.0.0",
    "uptime_seconds": 245.63,
    "db_row_counts": {
        "companies": 92,
        "financial_ratios": 1068
    }
}
```


## Companies Endpoint

Returns the complete list of companies.

### Request

```bash
curl http://127.0.0.1:8000/api/v1/companies
```

Optional filters include:

- Sector
- Market Cap Category
- Search by Company Name
- Search by Ticker


## Company Profile

Returns detailed information for a specific company.

### Example

```bash
curl http://127.0.0.1:8000/api/v1/companies/TCS
```


## Financial Statements

Historical financial statements are available through dedicated endpoints.

### Profit & Loss

```
GET /api/v1/companies/{ticker}/pl
```

### Balance Sheet

```
GET /api/v1/companies/{ticker}/bs
```

### Cash Flow

```
GET /api/v1/companies/{ticker}/cashflow
```


## Financial Ratios

Returns all calculated KPIs.

```
GET /api/v1/companies/{ticker}/ratios
```

## Screener API

The screener endpoint supports multiple financial filters.

Example:

```bash
curl "http://127.0.0.1:8000/api/v1/screener?min_roe=20&max_pe=25"
```

Supported filters include:

- Minimum ROE
- Maximum Debt to Equity
- Maximum PE
- Sector
- Revenue CAGR
- Profit CAGR
- Free Cash Flow


## Sector APIs

Retrieve all sector summaries.

```
GET /api/v1/sectors
```

Retrieve companies within a sector.

```
GET /api/v1/sectors/Financials/companies
```


## Peer Group APIs

Retrieve peer comparison data.

```
GET /api/v1/peers/{group_name}
```


## Market Capitalization APIs

Retrieve historical valuation metrics.

```
GET /api/v1/market-cap/{ticker}
```


## Portfolio Statistics API

The platform also exposes portfolio-level statistical summaries through an API endpoint.

```
GET /api/v1/portfolio/stats
```

This endpoint provides percentile-based statistics across all supported companies and can be used for portfolio benchmarking and analytics.

# 11. PDF Tearsheet Generation

The platform can generate professional PDF reports for every company.

Each tearsheet includes:

- Company Information
- Sector Details
- Financial Ratios
- Profit & Loss Summary
- Balance Sheet Summary
- Cash Flow Summary
- Market Valuation Metrics
- Capital Allocation Overview

## Steps

1. Select a company.
2. Navigate to the Tearsheet section.
3. Click **Generate PDF**.
4. Download the generated report.

Generated PDF files are stored in the output reports directory.

Example location:

```
output/reports/
```

# 12. Troubleshooting

The following table lists common issues and recommended solutions.

| Problem | Possible Cause | Solution |
|----------|---------------|----------|
| API not starting | Port already in use | Stop existing process or change port |
| Database connection failed | Database path incorrect | Verify SQLite database location |
| Dashboard displays no data | API server not running | Start FastAPI before launching Streamlit |
| 404 Company Not Found | Invalid ticker | Use a valid NIFTY 100 ticker |
| Tearsheet missing | PDF not generated | Generate the report again |
| Swagger not loading | API not running | Start Uvicorn server |
| Slow responses | Missing indexes | Execute database optimization scripts |
| Empty Screener results | Very restrictive filters | Reset filter values |

# 13. Frequently Asked Questions

### Q1. Which companies are included?

The platform currently supports all companies listed in the NIFTY 100 index.


### Q2. Where does the financial data come from?

Financial statements are processed through the ETL pipeline and stored in a SQLite database before KPI calculations are performed.

### Q3. Can I download reports?

Yes.

Professional PDF tearsheets can be generated for every supported company.


### Q4. Can I use the API separately?

Yes.

Every dashboard feature is powered by the REST API and can also be accessed independently using HTTP requests.

### Q5. Does the platform calculate financial ratios automatically?

Yes.

ROE, ROCE, Debt-to-Equity, Interest Coverage Ratio, Asset Turnover, Free Cash Flow, and other KPIs are calculated automatically during data processing.


### Q6. Can I integrate this platform with another application?

Yes.

The REST API can be integrated with web applications, dashboards, notebooks, or external analytics tools.

### Q7. Which technologies are used?

- Python
- FastAPI
- Streamlit
- SQLite
- Pandas
- OpenPyXL
- Plotly
- Pytest


# 14. Conclusion

The NIFTY 100 Financial Intelligence Platform provides a complete financial analytics solution by integrating ETL pipelines, automated KPI computation, REST APIs, and an interactive Streamlit dashboard.

The platform enables users to:

- Explore historical financial statements
- Evaluate company performance
- Screen companies using financial metrics
- Analyze sectors and peer groups
- Review market valuation metrics
- Generate professional PDF tearsheets
- Access data through REST APIs

The modular architecture ensures scalability, maintainability, and ease of integration while providing a user-friendly interface for analysts, investors, students, and researchers.

By combining robust backend services with an interactive dashboard, the platform delivers a comprehensive environment for data-driven financial analysis and investment research.
