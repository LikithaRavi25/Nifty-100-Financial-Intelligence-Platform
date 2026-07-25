import sqlite3
import pandas as pd

conn = sqlite3.connect("nifty100.db")   # Update path if needed

query = """
SELECT COUNT(*) AS total
FROM financial_ratios
"""

result = pd.read_sql(query, conn)

conn.close()

count = result.loc[0, "total"]

print(result)

if count >= 1100:
    print(f"\n✅ AC-04 PASS ({count} records)")
else:
    print(f"\n❌ AC-04 FAIL ({count} records)")