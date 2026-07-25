import sqlite3
import pandas as pd

conn = sqlite3.connect("nifty100.db")   # Update path if needed

df = pd.read_sql(
    "PRAGMA foreign_key_check;",
    conn
)

conn.close()

print(df)

if df.empty:
    print("\n✅ AC-03 PASS")
else:
    print("\n❌ AC-03 FAIL")
    print(f"\nForeign key violations: {len(df)}")