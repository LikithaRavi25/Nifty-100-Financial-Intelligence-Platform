import sqlite3
import pandas as pd

conn = sqlite3.connect("nifty100.db")

query = """
SELECT
    company_id,
    COUNT(*) AS ratio_records
FROM financial_ratios
GROUP BY company_id
ORDER BY ratio_records
"""

df = pd.read_sql(query, conn)

conn.close()

print(df)

print("\nMinimum records:", df["ratio_records"].min())
print("Maximum records:", df["ratio_records"].max())

print("\nCompanies with fewer than 10 ratio records:\n")
print(df[df["ratio_records"] < 10])