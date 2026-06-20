
from src.database.db import (
    get_connection
)

def create_companies_table():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS companies (

        company_id TEXT PRIMARY KEY,

        company_name TEXT,

        sector TEXT,

        industry TEXT,

        market_cap REAL

    )
    """)

    conn.commit()

    conn.close()

def create_profit_loss_table():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS profitandloss (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        company_id TEXT,

        year TEXT,

        sales REAL,

        operating_profit REAL,

        net_profit REAL,

        FOREIGN KEY(company_id)
        REFERENCES companies(company_id)

    )
    """)

    conn.commit()

    conn.close()

def create_balancesheet_table():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS balancesheet (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        company_id TEXT,

        year TEXT,

        total_assets REAL,

        total_liabilities REAL,

        FOREIGN KEY(company_id)
        REFERENCES companies(company_id)

    )
    """)

    conn.commit()

    conn.close()

def create_cashflow_table():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cashflow (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        company_id TEXT,

        year TEXT,

        operating_activity REAL,

        investing_activity REAL,

        financing_activity REAL,

        net_cash_flow REAL,

        FOREIGN KEY(company_id)
        REFERENCES companies(company_id)

    )
    """)

    conn.commit()

    conn.close()

def create_analysis_table():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS analysis (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        company_id TEXT,

        analysis TEXT,

        FOREIGN KEY(company_id)
        REFERENCES companies(company_id)

    )
    """)

    conn.commit()

    conn.close()

def create_documents_table():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS documents (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        company_id TEXT,

        analysis TEXT,

        FOREIGN KEY(company_id)
        REFERENCES companies(company_id)

    )
    """)

    conn.commit()

    conn.close()

def create_prosandcons_table():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS prosandcons (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        company_id TEXT,

        analysis TEXT,

        FOREIGN KEY(company_id)
        REFERENCES companies(company_id)

    )
    """)

    conn.commit()

    conn.close()

def create_sectors_table():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sectors (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        company_id TEXT,

        analysis TEXT,

        FOREIGN KEY(company_id)
        REFERENCES companies(company_id)

    )
    """)

    conn.commit()

    conn.close()

def create_stock_prices_table():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS stock_prices (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        company_id TEXT,

        analysis TEXT,

        FOREIGN KEY(company_id)
        REFERENCES companies(company_id)

    )
    """)

    conn.commit()

    conn.close()

def create_market_cap_table():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS market_cap (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        company_id TEXT,

        analysis TEXT,

        FOREIGN KEY(company_id)
        REFERENCES companies(company_id)

    )
    """)

    conn.commit()

    conn.close()

def create_financial_ratios_table():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS financial_ratios (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        company_id TEXT,

        analysis TEXT,

        FOREIGN KEY(company_id)
        REFERENCES companies(company_id)

    )
    """)

    conn.commit()

    conn.close()

def create_peer_groups_table():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS peer_groups (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        company_id TEXT,

        analysis TEXT,

        FOREIGN KEY(company_id)
        REFERENCES companies(company_id)

    )
    """)

    conn.commit()

    conn.close()

def create_all_tables():

    create_companies_table()

    create_profit_loss_table()

    create_balancesheet_table()

    create_cashflow_table()

    create_analysis_table()

    print(
        "Tables created successfully."
    )