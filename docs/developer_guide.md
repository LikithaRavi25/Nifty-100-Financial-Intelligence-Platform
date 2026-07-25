# NIFTY 100 Financial Intelligence Platform

# Developer Guide

Version 1.0

Author: Likitha R

Data Analyst INtern | Bluestock Fintech
# Table of Contents

1. Project Architecture
2. Folder Structure
3. ETL Pipeline
4. Database Schema
5. Analytics Engine
6. FastAPI Backend
7. Streamlit Dashboard
8. Testing Strategy
9. Deployment
10. Future Improvements


# 1. Project Architecture

The application follows a modular architecture consisting of four major layers.

- ETL Layer
- Analytics Layer
- API Layer
- Presentation Layer

```
Excel Files
      │
      ▼
 ETL Pipeline
      │
      ▼
 SQLite Database
      │
      ▼
 Analytics Engine
      │
      ▼
 FastAPI REST API
      │
      ▼
 Streamlit Dashboard
```


# 2. Folder Structure

```
src/
│
├── analytics/
├── api/
├── dashboard/
├── database/
├── etl/
├── reports/
└── validators/

tests/
docs/
output/
data/
screenshots/
```

# 3. ETL Pipeline

The ETL pipeline performs:

- Excel loading
- Data cleaning
- Column normalization
- Validation
- Duplicate detection
- Audit logging
- Database loading

Output files:

- load_audit.csv
- validation_failures.csv

# 4. Database Schema

Major tables:

- companies
- profitandloss
- balancesheet
- cashflow
- financial_ratios
- market_cap
- sectors
- peer_groups
- documents
- analysis

Indexes were created on frequently queried columns to improve performance.


# 5. Analytics Engine

Financial KPIs include:

- ROE
- ROCE
- ROA
- Net Profit Margin
- Operating Profit Margin
- Debt-to-Equity
- Interest Coverage
- Asset Turnover
- Free Cash Flow
- Revenue CAGR
- PAT CAGR
- EPS CAGR

Additional analytics include:

- Clustering
- Outlier Detection
- Peer Percentiles
- Capital Allocation Analysis


# 6. FastAPI Backend

Implemented APIs include:

- Health
- Companies
- Financial Statements
- Financial Ratios
- Stock Screener
- Sector Analysis
- Peer Groups
- Market Capitalization
- Annual Reports
- PDF Tearsheets

Swagger UI:

```
http://127.0.0.1:8000/docs
```


# 7. Streamlit Dashboard

Dashboard modules:

- Home
- Company Profile
- Stock Screener
- Peer Comparison
- Trend Analysis
- Sector Analysis
- Capital Allocation
- Annual Reports

The dashboard communicates with FastAPI using REST APIs.


# 8. Testing Strategy

Testing includes:

- Unit Testing
- API Testing
- Integration Testing
- Concurrent Load Testing
- Dashboard Performance Testing

Pytest HTML reports are generated after test execution.


# 9. Deployment

Run FastAPI

```bash
uvicorn src.api.main:app --reload
```

Run Streamlit

```bash
streamlit run src/dashboard/app.py
```

Run tests

```bash
pytest
```

# 10. Future Improvements

- PostgreSQL support
- Cloud deployment
- Authentication
- Portfolio Tracker
- AI-based Investment Advisor
- Live NSE/BSE integration


# Conclusion

The project follows a modular and scalable architecture. ETL, analytics, APIs, and dashboard components are loosely coupled, making the platform easy to maintain and extend.