import sqlite3
import pandas as pd

conn = sqlite3.connect("nifty100.db")

companies = [
    "TCS",
    "INFY",
    "HDFCBANK",
    "ASIANPAINT",
    "HINDUNILVR"
]

for company in companies:

    print("=" * 60)
    print(company)

    calculated = pd.read_sql(
        """
        SELECT year,
               return_on_equity_pct
        FROM financial_ratios
        WHERE company_id=?
        ORDER BY year DESC
        LIMIT 1
        """,
        conn,
        params=[company]
    )

    source = pd.read_sql(
        """
        SELECT roe
        FROM analysis
        WHERE company_id=?
        """,
        conn,
        params=[company]
    )

    print("\nCalculated ROE")
    print(calculated)

    print("\nSource ROE")
    print(source)

conn.close()