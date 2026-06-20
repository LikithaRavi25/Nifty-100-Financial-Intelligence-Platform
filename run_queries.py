import sqlite3
import pandas as pd

conn = sqlite3.connect("nifty100.db")

queries = {

    "Total Companies":
    """
    SELECT COUNT(*)
    FROM companies
    """,

    "Top Market Cap":
    """
    SELECT *
    FROM market_cap
    LIMIT 10
    """
}

for title, query in queries.items():

    print("\n")
    print("=" * 50)
    print(title)
    print("=" * 50)

    df = pd.read_sql(query, conn)

    print(df)

conn.close()