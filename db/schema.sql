-- Enable Foreign Keys
PRAGMA foreign_keys = ON;

-- Companies
CREATE TABLE IF NOT EXISTS companies (
    id INTEGER PRIMARY KEY,
    company_logo TEXT,
    company_name TEXT,
    chart_link TEXT,
    about_company TEXT,
    website TEXT,
    nse_profile TEXT,
    bse_profile TEXT,
    face_value REAL,
    book_value REAL,
    roce_percentage REAL,
    roe_percentage REAL
);

-- Profit & Loss
CREATE TABLE IF NOT EXISTS profitandloss (
    id INTEGER,
    company_id TEXT,
    year TEXT,
    sales REAL,
    expenses REAL,
    operating_profit REAL,
    opm_percentage REAL,
    other_income REAL,
    interest REAL,
    depreciation REAL,
    profit_before_tax REAL,
    tax_percentage REAL,
    net_profit REAL,
    eps REAL,
    dividend_payout REAL
);

-- Balance Sheet
CREATE TABLE IF NOT EXISTS balancesheet (
    id INTEGER,
    company_id TEXT,
    year TEXT,
    equity_capital REAL,
    reserves REAL,
    borrowings REAL,
    other_liabilities REAL,
    total_liabilities REAL,
    fixed_assets REAL,
    cwip REAL,
    investments REAL,
    other_asset REAL,
    total_assets REAL
);

-- Cash Flow
CREATE TABLE IF NOT EXISTS cashflow (
    id INTEGER,
    company_id TEXT,
    year TEXT,
    cash_from_operating_activity REAL,
    cash_from_investing_activity REAL,
    cash_from_financing_activity REAL,
    net_cash_flow REAL
);

-- Analysis
CREATE TABLE IF NOT EXISTS analysis (
    id INTEGER,
    company_id TEXT,
    analysis TEXT
);

-- Documents
CREATE TABLE IF NOT EXISTS documents (
    id INTEGER,
    company_id TEXT,
    document_name TEXT,
    document_link TEXT
);

-- Pros & Cons
CREATE TABLE IF NOT EXISTS prosandcons (
    id INTEGER,
    company_id TEXT,
    pros TEXT,
    cons TEXT
);

-- Sectors
CREATE TABLE IF NOT EXISTS sectors (
    id INTEGER,
    sector TEXT
);

-- Stock Prices
CREATE TABLE IF NOT EXISTS stock_prices (
    id INTEGER,
    company_id TEXT,
    date TEXT,
    open_price REAL,
    high_price REAL,
    low_price REAL,
    close_price REAL,
    volume REAL,
    adjusted_close REAL
);

-- Market Cap
CREATE TABLE IF NOT EXISTS market_cap (
    id INTEGER,
    company_id TEXT,
    year TEXT,
    market_cap REAL
);

-- Financial Ratios
CREATE TABLE IF NOT EXISTS financial_ratios (
    id INTEGER,
    company_id TEXT,
    year TEXT,
    ratio_name TEXT,
    ratio_value REAL
);

-- Peer Groups
CREATE TABLE IF NOT EXISTS peer_groups (
    id INTEGER,
    company_id TEXT,
    peer_company TEXT
);