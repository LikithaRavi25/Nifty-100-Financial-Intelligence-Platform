# NIFTY 100 Financial Intelligence Platform

# API Reference

Version 1.0


# Base URL

```
http://127.0.0.1:8000/api/v1
```

# Authentication

No authentication is required in the current version.


# Health API

## GET /health

Returns API status and database health.

### Response

```json
{
    "status":"ok",
    "version":"1.0.0"
}
```

# Companies API

## GET /companies

Returns all companies.

### Query Parameters

| Parameter | Description |
|------------|-------------|
| sector | Filter by sector |
| market_cap_category | Filter by market cap |
| search | Search by company |

## GET /companies/{ticker}

Returns complete company profile.

## GET /companies/{ticker}/pl

Returns Profit & Loss statements.

## GET /companies/{ticker}/bs

Returns Balance Sheet.

## GET /companies/{ticker}/cashflow

Returns Cash Flow statements.

## GET /companies/{ticker}/ratios

Returns Financial Ratios.

## GET /companies/{ticker}/tearsheet

Downloads the company PDF report.

# Screener API

## GET /screener

Supported Filters

- min_roe
- max_de
- max_pe
- sector
- min_sales_growth
- min_profit_growth

# Sector API

## GET /sectors

Returns sector summary.

## GET /sectors/{sector}/companies

Returns companies within the selected sector.

# Peer API

## GET /peers/{group}

Returns peer comparison.

# Market Cap API

## GET /market-cap/{ticker}

Returns valuation metrics.

# Error Codes

| Code | Meaning |
|------|----------|
|200|Success|
|400|Bad Request|
|404|Resource Not Found|
|422|Validation Error|
|500|Internal Server Error|