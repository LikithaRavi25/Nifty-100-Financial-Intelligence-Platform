import sqlite3
import pandas as pd

conn = sqlite3.connect("nifty100.db")   # Update path if required

query = """
SELECT COUNT(*) AS total
FROM companies
"""

result = pd.read_sql(query, conn)

conn.close()

count = result.loc[0, "total"]

print(result)

if count == 92:
    print("\n✅ AC-01 PASS")
else:
    print(f"\n❌ AC-01 FAIL (Found {count} companies)")