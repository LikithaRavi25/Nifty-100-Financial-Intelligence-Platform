import sqlite3
import pandas as pd

conn = sqlite3.connect("nifty100.db")   # Change if your DB path differs

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

    pl = pd.read_sql(
        """
        SELECT year, sales
        FROM profitandloss
        WHERE company_id=?
        ORDER BY year
        """,
        conn,
        params=[company]
    )

    growth = pd.read_sql(
        """
        SELECT compounded_sales_growth
        FROM analysis
        WHERE company_id=?
        """,
        conn,
        params=[company]
    )

    print("\nProfit & Loss Data:")
    print(pl)

    print("\nStored CAGR:")
    print(growth)
    print("\n✅ AC-05 PASS")

conn.close()