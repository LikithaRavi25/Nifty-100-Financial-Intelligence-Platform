# row_counts.py

import sqlite3

conn = sqlite3.connect("nifty100.db")

cursor = conn.cursor()

tables = [
    "companies",
    "profitandloss",
    "balancesheet",
    "cashflow",
    "analysis",
    "documents",
    "prosandcons",
    "sectors",
    "stock_prices",
    "market_cap",
    "financial_ratios",
    "peer_groups"
]

print("\nTABLE ROW COUNTS\n")

for table in tables:

    try:

        cursor.execute(
            f"SELECT COUNT(*) FROM {table}"
        )

        count = cursor.fetchone()[0]

        print(
            f"{table:<20} {count}"
        )

    except Exception as e:

        print(
            f"{table:<20} ERROR"
        )

conn.close()