import sqlite3

DB_PATH = "nifty100.db"   # Update if your database path is different

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

indexes = [

    # Financial Ratios
    """
    CREATE INDEX IF NOT EXISTS idx_financial_ratios_company_year
    ON financial_ratios(company_id, year)
    """,

    # Profit & Loss
    """
    CREATE INDEX IF NOT EXISTS idx_pl_company_year
    ON profitandloss(company_id, year)
    """,

    # Balance Sheet
    """
    CREATE INDEX IF NOT EXISTS idx_bs_company_year
    ON balancesheet(company_id, year)
    """,

    # Cash Flow
    """
    CREATE INDEX IF NOT EXISTS idx_cf_company_year
    ON cashflow(company_id, year)
    """,

    # Market Cap
    """
    CREATE INDEX IF NOT EXISTS idx_market_company_year
    ON market_cap(company_id, year)
    """,

    # Sectors
    """
    CREATE INDEX IF NOT EXISTS idx_sector_company
    ON sectors(company_id)
    """,

    # Companies
    """
    CREATE INDEX IF NOT EXISTS idx_company_id
    ON companies(id)
    """
]

for sql in indexes:
    cursor.execute(sql)

conn.commit()
conn.close()

print("All indexes created successfully.")