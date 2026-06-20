# Nifty 100 Financial Intelligence Platform

## Project Overview

The Nifty 100 Financial Intelligence Platform is a data engineering and analytics solution developed to ingest, validate, transform, store, and analyze financial data of Nifty 100 companies. The project implements a complete ETL pipeline, data quality validation framework, SQLite-based data warehouse, and analytical querying system to support business intelligence and financial analysis.

## Objectives

* Build a scalable ETL pipeline for financial datasets.
* Standardize and normalize data from multiple Excel sources.
* Perform automated data quality validation.
* Create a centralized SQLite data warehouse.
* Generate audit and validation reports.
* Enable analytical querying and business intelligence reporting.

## Project Architecture

```text
Raw Excel Files
       │
       ▼
 ETL Pipeline
       │
       ▼
Data Normalization
       │
       ▼
Data Validation Engine
       │
       ▼
SQLite Data Warehouse
       │
       ▼
SQL Analytics & Reporting
```
## Tech Stack

### Programming Language

* Python

### Libraries

* Pandas
* NumPy
* OpenPyXL
* SQLite3
* SQLAlchemy
* Pytest

### Database

* SQLite

### Tools

* VS Code
* Git & GitHub

## Dataset Information

The project processes 12 datasets:

### Core Datasets

* Companies
* Profit and Loss
* Balance Sheet
* Cash Flow
* Analysis
* Documents
* Pros and Cons

### Supplementary Datasets

* Sectors
* Stock Prices
* Market Capitalization
* Financial Ratios
* Peer Groups

## Features Implemented

### ETL Pipeline

* Excel file ingestion
* Bulk file loading
* Data normalization
* Column standardization
* Company ID normalization
* Year format standardization

### Data Quality Validation

* Null value checks
* Duplicate detection
* Financial consistency checks
* Year format validation
* URL validation
* Validation report generation

### Database Layer

* SQLite database creation
* Multi-table schema design
* Data loading automation
* Foreign key validation
* Row count verification

### Analytics Layer

* Exploratory SQL queries
* Market cap analysis
* Sales analysis
* Profitability analysis
* Sector analysis

## Project Structure

```text
NIFTY100-FINANCIAL-INTELLIGENCE-PLATFORM
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── supplementary/
│
├── src/
│   ├── etl/
│   │   ├── loader.py
│   │   ├── normalizer.py
│   │   └── audit.py
│   │
│   ├── validators/
│   │   ├── rules.py
│   │   └── validator.py
│   │
│   └── database/
│       ├── db.py
│       ├── schema.py
│       └── loader.py
│
├── db/
│   └── schema.sql
│
├── tests/
│
├── notebooks/
│   └── exploratory_queries.sql
│
├── load_audit.csv
├── validation_failures.csv
├── nifty100.db
├── main.py
├── requirements.txt
└── README.md
```

## Generated Deliverables

* nifty100.db
* load_audit.csv
* validation_failures.csv
* schema.sql
* exploratory_queries.sql
* ETL modules
* Validation modules
* Database modules

## How to Run

### Clone Repository

```bash
git clone <repository-url>
cd nifty100-financial-intelligence-platform
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

Windows:

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Execute Pipeline

```bash
python main.py
```

## Output Files

### Audit Report

```text
load_audit.csv
```

Contains:

* Table Name
* Rows Loaded
* Runtime
* Timestamp

### Validation Report

```text
validation_failures.csv
```

Contains:

* Table
* Field
* Issue
* Severity

### Database

```text
nifty100.db
```

Contains all processed and validated datasets.

## Sprint 1 Achievements

* Environment Setup
* ETL Development
* Data Normalization
* Data Validation Framework
* SQLite Database Design
* Full Data Loading
* Foreign Key Validation
* Data Quality Review
* SQL Analytics Queries
* Sprint Review & Documentation

## Future Enhancements

* Streamlit Dashboard
* KPI Monitoring
* Financial Trend Analysis
* Automated Reporting
* REST API Integration
* Predictive Analytics
* Portfolio Insights


## Author

Likitha R

B.Tech Computer Science & Engineering

Data Analyst Intern
